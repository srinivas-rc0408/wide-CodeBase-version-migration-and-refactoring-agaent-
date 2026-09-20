"""Static settings. No clock, no in-repo imports — the graph's other root."""

CURRENCY = "INR"
RETENTION_DAYS = 30


def retention_seconds() -> int:
    """How long a record is kept, in seconds."""
    return RETENTION_DAYS * 24 * 60 * 60
