"""The clock contract. Every other module in this package reads from it."""

from datetime import datetime, timezone


def make_timestamp() -> datetime:
    """Return the current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)
