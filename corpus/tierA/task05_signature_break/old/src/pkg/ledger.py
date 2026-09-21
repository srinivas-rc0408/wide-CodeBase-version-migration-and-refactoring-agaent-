"""Append-only ledger. Stamps entries with its own clock reading."""

from datetime import datetime

from pkg.timebase import elapsed_since

#: Every entry posted in this process.
ENTRIES: list[dict[str, object]] = []


def post(account: str, amount: int) -> dict[str, object]:
    """Record one amount against an account and return the entry."""
    entry = {"account": account, "amount": amount, "posted_at": datetime.utcnow()}
    ENTRIES.append(entry)
    return entry


def age_of(entry: dict[str, object]) -> float:
    """Seconds since ``entry`` was posted.

    Hands this module's own stamp back to the shared clock, so migrating it
    ahead of :mod:`pkg.timebase` raises here — at call time rather than at
    import time, the softer half of the same break.
    """
    return elapsed_since(entry["posted_at"])
