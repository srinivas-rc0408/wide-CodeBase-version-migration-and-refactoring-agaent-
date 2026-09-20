"""Report building. Imports :mod:`pkg.core`, creating the cross-file dependency edge."""

import datetime as dt

from pkg.core import make_timestamp


def build_report(title: str) -> dict[str, object]:
    """Return a report record stamped with the current UTC time."""
    return {"title": title, "generated_at": make_timestamp()}


def stamp_age_seconds(generated_at: dt.datetime) -> float:
    """Return how many seconds ago ``generated_at`` was produced.

    Reads the clock through the aliased module import rather than through
    :func:`pkg.core.make_timestamp`, so a half-finished migration — core
    moved to aware, this site still naive — raises at runtime.
    """
    return (dt.datetime.now(dt.timezone.utc) - generated_at).total_seconds()
