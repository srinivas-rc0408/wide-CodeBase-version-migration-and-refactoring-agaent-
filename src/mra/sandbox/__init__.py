"""Isolated execution: container-backed verification and git snapshot/rollback."""

from mra.sandbox.git_tools import diff, rollback, snapshot
from mra.sandbox.runner import SandboxRunner, failure_signature, normalize_message

__all__ = [
    "SandboxRunner",
    "diff",
    "failure_signature",
    "normalize_message",
    "rollback",
    "snapshot",
]
