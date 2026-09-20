"""audit.py holds a call site but no cross-module subtraction.

Migrating it alone is safe, which is what makes it a useful third file: the
break has to come from report.py, not from sheer number of edits.
"""

from datetime import datetime

from pkg.audit import audit_record, audit_window


def test_audit_record_stamps_a_datetime() -> None:
    record = audit_record("login")
    assert record["label"] == "login"
    assert isinstance(record["at"], datetime)


def test_audit_window_is_ordered() -> None:
    start, end = audit_window(60)
    assert start < end
