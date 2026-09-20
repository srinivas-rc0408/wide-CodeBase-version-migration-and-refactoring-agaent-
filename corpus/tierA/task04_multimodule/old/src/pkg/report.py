"""Reporting. The module the batched migration is designed to leave behind."""

from datetime import datetime

from pkg.invoice import issue


def invoice_age_seconds(invoice: dict[str, object]) -> float:
    """Seconds since the invoice was issued.

    Reads its *own* clock and subtracts :func:`pkg.invoice.issue`'s stamp.
    ``invoice.py`` sits one batch earlier in dependency order, so there is a
    window in which it has moved to aware and this has not — and in that
    window the subtraction raises.
    """
    return (datetime.utcnow() - invoice["issued_at"]).total_seconds()


def summary(account: str, amount: int) -> dict[str, object]:
    """Issue an invoice and report how old it is."""
    invoice = issue(account, amount)
    return {"invoice": invoice, "age_s": invoice_age_seconds(invoice)}
