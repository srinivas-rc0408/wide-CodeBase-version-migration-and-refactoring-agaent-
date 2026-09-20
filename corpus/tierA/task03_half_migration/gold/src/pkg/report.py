"""Report building. The module the half-migration is designed to leave behind."""

from datetime import datetime, timezone

from pkg.core import make_timestamp


def build_report(title: str) -> dict[str, object]:
    """Return a report record stamped from the shared clock."""
    return {"title": title, "generated_at": make_timestamp()}


def stamp_age_seconds(generated_at: datetime) -> float:
    """Return how many seconds ago ``generated_at`` was produced.

    Reads its *own* clock and subtracts a value produced by
    :func:`pkg.core.make_timestamp`. Migrate core and not this file and the
    subtraction mixes an aware minuend with a naive subtrahend, which raises.
    """
    return (datetime.now(timezone.utc) - generated_at).total_seconds()
