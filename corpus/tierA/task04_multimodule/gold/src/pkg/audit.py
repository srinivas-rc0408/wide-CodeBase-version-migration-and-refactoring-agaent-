"""Audit trail. The other half of the import cycle with :mod:`pkg.ledger`."""

from datetime import datetime, timezone

import pkg.ledger
from pkg.clock import make_timestamp

_LOG: list[dict[str, object]] = []


def note(message: str) -> dict[str, object]:
    """Append a message to the trail, stamped from the shared clock."""
    record: dict[str, object] = {"message": message, "at": make_timestamp()}
    _LOG.append(record)
    return record


def trail() -> list[dict[str, object]]:
    return list(_LOG)


def reconcile(account: str) -> dict[str, object]:
    """Read the ledger back — the call that closes the cycle.

    ``checked_at`` is never compared against anything, so this module's own
    clock reading is safe to migrate in isolation.
    """
    return {
        "account": account,
        "balance": pkg.ledger.balance(account),
        "checked_at": datetime.now(timezone.utc),
    }
