"""Isolated execution: container-backed verification and git snapshot/rollback."""

from mra.sandbox.git_tools import changed_paths, diff, rollback, snapshot
from mra.sandbox.runner import SandboxRunner, failure_signature, normalize_message

__all__ = [
    "SandboxRunner",
    "changed_paths",
    "diff",
    "failure_signature",
    "normalize_message",
    "rollback",
    "snapshot",
]
