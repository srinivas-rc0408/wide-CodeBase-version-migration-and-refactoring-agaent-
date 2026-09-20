"""Timestamp helpers. Defines the contract that the migration changes."""

import datetime


def make_timestamp() -> datetime.datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.datetime.utcnow()
