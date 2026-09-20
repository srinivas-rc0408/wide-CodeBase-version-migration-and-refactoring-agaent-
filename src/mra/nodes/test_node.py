"""TEST node: verify the tree in the sandbox and write the report into state (FR-6).

Never executes repo code on the host — that is :class:`mra.sandbox.SandboxRunner`'s
job and golden rule 3. This node only decides which phase label the run carries
and hands the normalized ``mra:test_report`` (SRS §4.3) to the router.
"""

from __future__ import annotations

from typing import Any

from mra.sandbox.runner import SandboxRunner


def make_test_node(runner: SandboxRunner, task_id: str, run_id: str | None = None):
    """Bind the sandbox and return the node LangGraph calls."""

    def test_node(state: dict[str, Any]) -> dict[str, Any]:
        # "recovery" once a correction has been attempted, "post" otherwise:
        # the phase is what tells a reader whether a report is the first
        # verdict on a batch or the result of a repair.
        phase = "recovery" if state.get("fix_attempts") else "post"
        report = runner.run(
            state["repo_path"], task_id=task_id, phase=phase, run_id=run_id, lint=False
        )
        return {
            "last_test_report": report,
            "note": {
                "action": f"suite after batch {state.get('current_batch', 0)}: "
                          f"{report['passed']}/{report['total']} passed",
                "detail": {
                    "phase": phase,
                    "total": report["total"], "passed": report["passed"],
                    "failed": report["failed"], "errors": report["errors"],
                    "failures": [f["nodeid"] for f in report["failures"]],
                },
            },
        }

    return test_node
