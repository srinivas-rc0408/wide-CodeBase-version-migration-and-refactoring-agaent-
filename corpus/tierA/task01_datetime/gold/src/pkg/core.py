"""Timestamp helpers. Defines the contract that the migration changes."""

from datetime import datetime, timezone


def make_timestamp() -> datetime:
    """Return the current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)
