"""The clock contract. Every other module in this package reads from it."""

from datetime import datetime


def make_timestamp() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.utcnow()
