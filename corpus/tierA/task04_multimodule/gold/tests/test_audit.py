"""Audit trail, and the call that closes the import cycle with the ledger."""

from pkg.audit import note, reconcile, trail
from pkg.ledger import post


def test_note_appends_to_the_trail() -> None:
    before = len(trail())
    note("hello")
    assert len(trail()) == before + 1


def test_reconcile_reads_the_ledger_back() -> None:
    """Exercises audit -> ledger, the other direction of the cycle."""
    post("dave", 7)
    assert reconcile("dave")["balance"] == 7
