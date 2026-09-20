"""Audit trail. Imports the clock contract and also reads the clock directly."""

from datetime import datetime, timedelta, timezone

from pkg.core import make_timestamp


def audit_record(label: str) -> dict[str, object]:
    """Stamp an audit record from the shared clock."""
    return {"label": label, "at": make_timestamp()}


def audit_window(seconds: int) -> tuple[datetime, datetime]:
    """Return the ``seconds``-long window ending now.

    Both ends come from the same reading, so migrating this file on its own
    cannot mix naive and aware values — unlike :mod:`pkg.report`.
    """
    end = datetime.now(timezone.utc)
    return end - timedelta(seconds=seconds), end
