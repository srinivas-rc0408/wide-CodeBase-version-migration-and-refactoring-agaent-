"""The shared clock. Nothing in the package imports anything to provide it.

Most-depended-upon module in the repo, so dependency-ordered batching edits it
first — which is exactly what makes the later cross-file break possible.
"""

from datetime import datetime, timezone


def make_timestamp() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.now(timezone.utc)
