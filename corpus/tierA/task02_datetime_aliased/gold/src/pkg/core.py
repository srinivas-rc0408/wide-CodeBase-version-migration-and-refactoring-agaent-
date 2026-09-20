"""Timestamp helpers. Defines the contract that the migration changes."""

import datetime


def make_timestamp() -> datetime.datetime:
    """Return the current UTC time as a timezone-aware datetime."""
    return datetime.datetime.now(datetime.timezone.utc)
