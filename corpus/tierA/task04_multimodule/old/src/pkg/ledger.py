"""Double-entry ledger. Half of the import cycle with :mod:`pkg.audit`.

``import pkg.audit`` at module scope with the attribute read deferred to call
time is what makes the cycle importable at all; the dependency graph still
sees the edge, so the two modules must be migrated together.
"""

from datetime import datetime, timedelta

import pkg.audit
from pkg.clock import make_timestamp

_ENTRIES: list[dict[str, object]] = []


def post(account: str, amount: int) -> dict[str, object]:
    """Record an entry, stamped from the shared clock, and note it in the audit trail."""
    entry: dict[str, object] = {"account": account, "amount": amount, "at": make_timestamp()}
    _ENTRIES.append(entry)
    pkg.audit.note(f"posted {amount} to {account}")
    return entry


def balance(account: str) -> int:
    """Sum of every amount posted to ``account``."""
    return sum(int(e["amount"]) for e in _ENTRIES if e["account"] == account)


def snapshot_window(seconds: int) -> tuple[datetime, datetime]:
    """The ``seconds``-long window ending now.

    Both ends come from one reading, so migrating this module on its own
    cannot mix naive and aware values.
    """
    end = datetime.utcnow()
    return end - timedelta(seconds=seconds), end
