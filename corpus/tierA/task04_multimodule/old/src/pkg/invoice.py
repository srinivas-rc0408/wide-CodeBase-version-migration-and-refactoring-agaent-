"""Invoicing. Stamps with its OWN clock reading, not the shared one.

That detail is the whole point of the fixture: because ``issued_at`` does not
come from :mod:`pkg.clock`, migrating the clock leaves this module consistent.
The break only appears once *this* module moves and :mod:`pkg.report`, which
subtracts from ``issued_at``, has not.
"""

from datetime import datetime

from pkg.ledger import post


def issue(account: str, amount: int) -> dict[str, object]:
    """Post the amount to the ledger and return the invoice record."""
    post(account, amount)
    return {"account": account, "amount": amount, "issued_at": datetime.utcnow()}
