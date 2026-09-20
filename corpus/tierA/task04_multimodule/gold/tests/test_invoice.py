"""Invoicing. Its stamp is its own reading, not the shared clock's."""

from datetime import datetime

from pkg.invoice import issue
from pkg.ledger import balance


def test_issue_stamps_and_posts() -> None:
    invoice = issue("erin", 500)
    assert isinstance(invoice["issued_at"], datetime)
    assert balance("erin") == 500
