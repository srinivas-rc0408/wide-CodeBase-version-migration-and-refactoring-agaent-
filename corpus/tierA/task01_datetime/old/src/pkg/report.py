"""Report building. Imports :mod:`pkg.core`, creating the cross-file dependency edge."""

from datetime import datetime

from pkg.core import make_timestamp


def build_report(title: str) -> dict[str, object]:
    """Return a report record stamped with the current UTC time."""
    return {"title": title, "generated_at": make_timestamp()}


def stamp_age_seconds(generated_at: datetime) -> float:
    """Return how many seconds ago ``generated_at`` was produced."""
    return (make_timestamp() - generated_at).total_seconds()
