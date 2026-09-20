"""Timestamp helpers. Defines the contract that the migration changes."""

from datetime import datetime


def make_timestamp() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.utcnow()
