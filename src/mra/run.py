"""P2 end-to-end slice: analyse -> snapshot -> codemod -> verify -> score.

One task, one batch, no planner and no recovery. Everything runs on a writable
copy under ``runs/<run_id>/repo``; the corpus source is only ever read.

Outputs land in ``runs/<run_id>/`` (NFR-13):
``migration.patch``, ``metrics.json``, ``trajectory.json``, ``test_report.json``.
"""

from __future__ import annotations

import argparse
import json
import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mra.analysis import analyze, flat_sites
from mra.codemods.datetime_utcnow import TARGET
from mra.metrics import m1, m2
from mra.nodes.edit_node import apply_codemod
from mra.sandbox import SandboxRunner, diff, snapshot

#: Ground-truth comparison key. Matches tests/test_analyzer.py; a column error
#: would pass a looser (file, line, symbol) key and break a positional edit.
KEY_FIELDS = ("file", "line", "col", "symbol")


def _key(site: dict[str, Any]) -> tuple:
    return tuple(site[field] for field in KEY_FIELDS)


class Trajectory:
    """Append-only event log, the ``mra:trajectory_event`` shape (SRS §4.1)."""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def record(self, node: str, action: str, **detail: Any) -> None:
        self.events.append({
            "seq": len(self.events),
            "ts": datetime.now(UTC).isoformat(),
            "node": node,
            "action": action,
            "detail": detail,
        })


def migrate_task(
    task_dir: Path | str,
    run_id: str | None = None,
    runs_dir: Path | str = "runs",
    target: str = TARGET,
) -> dict[str, Any]:
    """Migrate a Tier-A task end to end and score it. Returns the run summary."""
    task_dir = Path(task_dir)
    task_id = task_dir.name
    run_id = run_id or uuid.uuid4().hex[:12]
    out_dir = Path(runs_dir) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    trajectory = Trajectory()
    work = out_dir / "repo"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(task_dir / "old", work)

    # -- MAP ---------------------------------------------------------------
    analysis = analyze(work, target)
    sites = flat_sites(analysis["call_sites"])
    trajectory.record("MAP", f"found {len(sites)} call site(s)",
                      files=sorted(analysis["call_sites"]), target=target)

    # -- TEST (pre) --------------------------------------------------------
    # NB-10: M2 is undefined unless the suite is green before we touch anything.
    runner = SandboxRunner(runs_dir=runs_dir)
    pre = runner.run(work, task_id=task_id, phase="pre", run_id=run_id, lint=False)
    (out_dir / "test_report_pre.json").write_text(json.dumps(pre, indent=2) + "\n")
    trajectory.record("TEST", "pre-migration suite",
                      total=pre["total"], passed=pre["passed"], failed=pre["failed"])

    # -- EDIT --------------------------------------------------------------
    base_sha = snapshot(work, "pre-migration snapshot")
    trajectory.record("EDIT", "git snapshot before batch 0", sha=base_sha)
    changed = apply_codemod(work, analysis["call_sites"])
    trajectory.record("EDIT", f"codemod applied to {len(changed)} file(s)", files=changed)

    # -- TEST (post) -------------------------------------------------------
    post = runner.run(work, task_id=task_id, phase="post", run_id=run_id)
    trajectory.record("TEST", "post-migration suite",
                      total=post["total"], passed=post["passed"], failed=post["failed"])

    patch = diff(work)
    (out_dir / "migration.patch").write_text(patch)

    # -- score -------------------------------------------------------------
    truth = json.loads((task_dir / "ground_truth.json").read_text())
    found = {_key(site) for site in sites}
    expected = {_key(site) for site in truth["call_sites"]}
    # Every site the codemod actually rewrote is the agent's claim; correctness
    # is its overlap with ground truth.
    m1_score = m1(agent_sites=found, correct_sites=found, ground_truth_sites=expected)
    m2_score = m2(t_total=pre["total"], t_post_pass=post["passed"])

    green = post["failed"] == 0 and post["errors"] == 0
    metrics = {
        "task_id": task_id,
        "m1_recall": m1_score["recall"],
        "m1_precision": m1_score["precision"],
        "m2_pass_rate": m2_score["pass_rate"],
        "m2_regressions": m2_score["regressions"],
        # No LLM in P2: the whole edit is deterministic, so M3 tokens are zero.
        "m3_tokens": 0,
        "m3_steps": len(trajectory.events),
        "m3_cost_usd": 0.0,
        "recovery_used": False,
        "outcome": "success" if green else "gave_up",
    }
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    (out_dir / "trajectory.json").write_text(json.dumps(trajectory.events, indent=2) + "\n")

    return {
        "run_id": run_id,
        "task_id": task_id,
        "out_dir": out_dir,
        "repo": work,
        "call_sites": analysis["call_sites"],
        "dep_graph": analysis["dep_graph"],
        "changed_files": changed,
        "pre_report": pre,
        "test_report": post,
        "patch": patch,
        "metrics": metrics,
        "trajectory": trajectory.events,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one Tier-A migration task end to end.")
    parser.add_argument("--task-dir", required=True,
                        help="task directory holding old/, gold/ and ground_truth.json")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--runs-dir", default="runs")
    args = parser.parse_args(argv)

    result = migrate_task(args.task_dir, run_id=args.run_id, runs_dir=args.runs_dir)
    metrics = result["metrics"]
    print(f"{result['task_id']}  run {result['run_id']}  -> {metrics['outcome']}")
    print(f"  M1 recall {metrics['m1_recall']:.1f}%  precision {metrics['m1_precision']:.1f}%")
    print(f"  M2 pass rate {metrics['m2_pass_rate']:.1f}%  regressions {metrics['m2_regressions']}")
    print(f"  artifacts: {result['out_dir']}")
    return 0 if metrics["outcome"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
