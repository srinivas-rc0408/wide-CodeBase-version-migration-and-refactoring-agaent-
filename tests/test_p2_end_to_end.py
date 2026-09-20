"""P2 acceptance: analyse -> codemod -> verify, end to end, on both real tasks.

The two tasks check opposite things. task01 is the recall case: the migration
is wrong unless an import is added. task02 is the precision case: the migration
is wrong if one is. A codemod that always calls AddImportsVisitor passes the
first and fails the second, which is why both exist.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

from mra.run import migrate_task
from mra.sandbox import SandboxRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS = REPO_ROOT / "corpus" / "tierA"
TASKS = ("task01_datetime", "task02_datetime_aliased")
ADDED_IMPORT = "from datetime import timezone"

needs_docker = pytest.mark.skipif(
    shutil.which("docker") is None
    or subprocess.run(["docker", "info"], capture_output=True).returncode != 0,
    reason="needs a working Docker daemon",
)


def _tree_digest(root: Path) -> str:
    sha = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        sha.update(str(path.relative_to(root)).encode())
        sha.update(path.read_bytes())
    return sha.hexdigest()


@pytest.fixture(scope="session")
def corpus_digests() -> dict[str, str]:
    """Taken before any run, compared after: the corpus must be read-only in practice."""
    return {task: _tree_digest(CORPUS / task) for task in TASKS}


@pytest.fixture(scope="session")
def runs(
    tmp_path_factory: pytest.TempPathFactory, corpus_digests: dict[str, str]
) -> dict[str, Any]:
    runs_dir = tmp_path_factory.mktemp("runs")
    return {task: migrate_task(CORPUS / task, run_id=task, runs_dir=runs_dir) for task in TASKS}


def _added_import_lines(patch: str) -> list[str]:
    """Added lines that introduce `from datetime import timezone`."""
    return [
        line for line in patch.splitlines()
        if line.startswith("+") and not line.startswith("+++") and ADDED_IMPORT in line
    ]


# -- scoring ---------------------------------------------------------------


@needs_docker
@pytest.mark.parametrize("task", TASKS)
def test_migration_is_green_and_perfectly_scored(task: str, runs: dict[str, Any]) -> None:
    metrics = runs[task]["metrics"]
    assert metrics["outcome"] == "success"
    assert metrics["m1_recall"] == 100.0
    assert metrics["m1_precision"] == 100.0
    assert metrics["m2_pass_rate"] == 100.0
    assert metrics["m2_regressions"] == 0


@needs_docker
@pytest.mark.parametrize("task", TASKS)
def test_suite_was_green_before_migration(task: str, runs: dict[str, Any]) -> None:
    """NB-10: without this precondition M2 means nothing."""
    pre = runs[task]["pre_report"]
    assert pre["total"] == pre["passed"]
    assert pre["failed"] == 0


# -- the import trap -------------------------------------------------------


@needs_docker
def test_task01_patch_adds_the_timezone_import(runs: dict[str, Any]) -> None:
    """From-import form: `timezone` is not in scope, so the migration must add it."""
    patch = runs["task01_datetime"]["patch"]
    assert _added_import_lines(patch), "task01 needs `from datetime import timezone`"
    assert "+    return datetime.now(timezone.utc)" in patch
    assert runs["task01_datetime"]["changed_files"] == ["src/pkg/core.py"]


@needs_docker
def test_task02_patch_adds_no_import(runs: dict[str, Any]) -> None:
    """Module/aliased forms: timezone already rides the import. Adding one is over-editing."""
    patch = runs["task02_datetime_aliased"]["patch"]
    assert _added_import_lines(patch) == []
    assert "+    return datetime.datetime.now(datetime.timezone.utc)" in patch
    assert "+    return (dt.datetime.now(dt.timezone.utc) - generated_at).total_seconds()" in patch
    assert runs["task02_datetime_aliased"]["changed_files"] == [
        "src/pkg/core.py", "src/pkg/report.py",
    ]


# -- semantics -------------------------------------------------------------


@needs_docker
@pytest.mark.parametrize("task", TASKS)
def test_migrated_tree_satisfies_the_gold_semantic_check(
    task: str, runs: dict[str, Any], tmp_path: Path
) -> None:
    """Syntactic success is not success: gold's tz-aware test must pass on our output.

    Runs in the sandbox like every other execution (golden rule 3), against the
    migrated sources paired with gold's suite.
    """
    graft = tmp_path / f"{task}_graft"
    shutil.copytree(runs[task]["repo"], graft, ignore=shutil.ignore_patterns(".git", "tests"))
    shutil.copytree(CORPUS / task / "gold" / "tests", graft / "tests")

    report = SandboxRunner(runs_dir=tmp_path / "runs").run(
        graft, task_id=task, phase="post", lint=False
    )
    assert report["failed"] == 0 and report["errors"] == 0
    # 6 = the 5 shared tests plus gold's timezone-aware assertion.
    assert report["total"] == 6


# -- isolation and portability ---------------------------------------------


@needs_docker
@pytest.mark.parametrize("task", TASKS)
def test_corpus_source_is_untouched(
    task: str, runs: dict[str, Any], corpus_digests: dict[str, str]
) -> None:
    """Edits happen on the copy under runs/<run_id>/repo, never on the corpus."""
    assert _tree_digest(CORPUS / task) == corpus_digests[task]


@needs_docker
@pytest.mark.parametrize("task", TASKS)
def test_patch_applies_to_a_fresh_checkout(task: str, runs: dict[str, Any], tmp_path: Path) -> None:
    """FR-10: the deliverable patch must apply to a clean old/ tree."""
    fresh = tmp_path / f"{task}_fresh"
    shutil.copytree(CORPUS / task / "old", fresh)
    subprocess.run(["git", "init", "-q"], cwd=fresh, check=True)

    patch_file = runs[task]["out_dir"] / "migration.patch"
    result = subprocess.run(
        ["git", "apply", "--check", str(patch_file)],
        cwd=fresh, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


@needs_docker
@pytest.mark.parametrize("task", TASKS)
def test_run_writes_every_artifact(task: str, runs: dict[str, Any]) -> None:
    out_dir = runs[task]["out_dir"]
    for name in ("migration.patch", "metrics.json", "trajectory.json", "test_report.json"):
        assert (out_dir / name).is_file(), name
    # The trajectory is the audit deliverable; it must cover the whole slice.
    nodes = [event["node"] for event in runs[task]["trajectory"]]
    assert nodes == ["MAP", "TEST", "EDIT", "EDIT", "TEST"]
