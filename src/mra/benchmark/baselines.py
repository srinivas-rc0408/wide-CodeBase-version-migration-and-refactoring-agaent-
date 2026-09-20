"""The honesty check: what the existing static tools already do (docs/05, §2.2).

Before claiming an agent is needed, measure the tools that cost nothing. Two
are relevant to the `datetime.utcnow()` contract:

* **ruff** with the ``DTZ`` (flake8-datetimez) rules — ``DTZ003`` is exactly
  "``datetime.datetime.utcnow()`` used".
* **pyupgrade**, the standard mechanical modernizer.

Each is scored on the same three questions the agent is scored on: what did it
*detect* (M1's numerator, if detection were enough), what did it *fix*, and is
the suite green afterwards. Running them is the point — a claim that "linters
cannot do this" is worth nothing next to the number they actually score.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

from mra.analysis import call_sites as call_sites_module
from mra.codemods.datetime_utcnow import TARGET
from mra.sandbox import SandboxRunner

#: flake8-datetimez, as shipped by ruff. DTZ003 is the utcnow rule.
RUFF_SELECT = "DTZ"


def _tool(name: str) -> str:
    """The tool from this interpreter's environment, falling back to PATH."""
    beside = Path(sys.executable).with_name(name)
    return str(beside) if beside.exists() else name


def _ruff(argv: list[str]) -> subprocess.CompletedProcess[str]:
    # --isolated: the repo's own pyproject must not change what the baseline sees.
    return subprocess.run([_tool("ruff"), *argv], capture_output=True, text=True, check=False)


def _detect_with_ruff(tree: Path) -> list[dict[str, Any]]:
    """Every DTZ finding in ``tree``, as ``{file, line, code}``."""
    result = _ruff(["check", "--isolated", "--select", RUFF_SELECT,
                    "--output-format", "json", str(tree)])
    try:
        findings = json.loads(result.stdout or "[]")
    except json.JSONDecodeError:  # pragma: no cover - ruff failed to run at all
        return []
    return [{
        "file": Path(f["filename"]).resolve().relative_to(tree.resolve()).as_posix(),
        # ruff columns are 1-based and ours are 0-based, so only (file, line) is
        # compared; the column convention is not what this measurement is about.
        "line": f["location"]["row"],
        "code": f["code"],
    } for f in findings]


def _remaining_sites(tree: Path) -> int:
    """Call sites still on the old API after a tool has had its turn."""
    return sum(len(sites) for sites in call_sites_module.find_in_repo(tree, TARGET).values())


def _suite(tree: Path, task_id: str, runs_dir: Path) -> dict[str, Any]:
    runner = SandboxRunner(runs_dir=runs_dir)
    return runner.run(tree, task_id=task_id, phase="post",
                      run_id=f"baseline-{task_id}-{uuid.uuid4().hex[:6]}", lint=False)


def _score(tree: Path, task_id: str, truth: dict[str, Any], detected: list[dict[str, Any]],
           fixed_files: int, tool: str, runs_dir: Path) -> dict[str, Any]:
    expected = {(site["file"], site["line"]) for site in truth["call_sites"]}
    hits = {(f["file"], f["line"]) for f in detected}
    total = len(expected)
    remaining = _remaining_sites(tree)
    report = _suite(tree, task_id, runs_dir)
    return {
        "tool": tool,
        "detected": len(detected),
        "detect_recall": 100.0 * len(hits & expected) / max(total, 1),
        "detect_precision": 100.0 * len(hits & expected) / max(len(hits), 1),
        "fixed_files": fixed_files,
        # Nothing rewritten means nothing migrated, whatever was detected.
        "m1_recall_after_fix": 100.0 * (total - remaining) / max(total, 1),
        "sites_remaining": remaining,
        "suite_after_fix": f"{report['passed']}/{report['total']} passed",
        "suite_green": report["failed"] == 0 and report["errors"] == 0,
        "can_repair_cross_file_break": False,
    }


def ruff_baseline(task_dir: Path | str, runs_dir: Path | str = "runs/benchmark/runs") -> dict:
    """Detect with ruff, then let it fix what it can, and score the result."""
    task_dir, runs_dir = Path(task_dir), Path(runs_dir)
    truth = json.loads((task_dir / "ground_truth.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp) / "old"
        shutil.copytree(task_dir / "old", tree)
        detected = _detect_with_ruff(tree)
        before = {path: path.read_bytes() for path in tree.rglob("*.py")}
        _ruff(["check", "--isolated", "--select", RUFF_SELECT, "--fix",
               "--unsafe-fixes", str(tree)])
        fixed = sum(1 for path, blob in before.items() if path.read_bytes() != blob)
        return _score(tree, task_dir.name, truth, detected, fixed, "ruff (DTZ)", runs_dir)


def pyupgrade_baseline(task_dir: Path | str,
                       runs_dir: Path | str = "runs/benchmark/runs") -> dict:
    """Run pyupgrade over the task and score it the same way."""
    task_dir, runs_dir = Path(task_dir), Path(runs_dir)
    truth = json.loads((task_dir / "ground_truth.json").read_text())
    binary = Path(_tool("pyupgrade"))
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp) / "old"
        shutil.copytree(task_dir / "old", tree)
        files = sorted(tree.rglob("*.py"))
        before = {path: path.read_bytes() for path in files}
        if binary.exists() or binary.name == binary.as_posix():
            subprocess.run([str(binary), "--py312-plus", *map(str, files)],
                           capture_output=True, text=True, check=False)
        else:  # pragma: no cover - environment without the tool installed
            return {"tool": "pyupgrade", "detected": 0, "detect_recall": 0.0,
                    "detect_precision": 0.0, "fixed_files": 0, "m1_recall_after_fix": 0.0,
                    "sites_remaining": len(truth["call_sites"]),
                    "suite_after_fix": "not installed", "suite_green": False,
                    "can_repair_cross_file_break": False}
        fixed = sum(1 for path, blob in before.items() if path.read_bytes() != blob)
        # pyupgrade has no report mode: what it rewrote is its whole output, so
        # "detected" can only be counted as "files it chose to touch".
        return _score(tree, task_dir.name, truth, [], fixed, "pyupgrade", runs_dir)


def baseline_table(tasks, corpus: Path | str = "corpus/tierA",
                   runs_dir: Path | str = "runs/benchmark/runs") -> list[dict[str, Any]]:
    """Both tools over every task, in the shape ``results.json`` carries."""
    corpus = Path(corpus)
    table = []
    for task in tasks:
        task_dir = corpus / task
        truth = json.loads((task_dir / "ground_truth.json").read_text())
        table.append({
            "task_id": task,
            "ground_truth_sites": len(truth["call_sites"]),
            "tools": [ruff_baseline(task_dir, runs_dir), pyupgrade_baseline(task_dir, runs_dir)],
        })
    return table
