"""The tripwire.

``invoice_age_seconds`` is the only place in the package where one module's
clock reading is subtracted from another's. It is therefore the only test a
dependency-ordered migration can break, and it breaks in the window between
``invoice.py`` moving and ``report.py`` following.
"""

from pkg.report import invoice_age_seconds, summary


def test_invoice_age_is_non_negative() -> None:
    from pkg.invoice import issue

    assert invoice_age_seconds(issue("frank", 10)) >= 0


def test_summary_reports_the_invoice_and_its_age() -> None:
    result = summary("grace", 20)
    assert result["invoice"]["amount"] == 20
    assert result["age_s"] >= 0
