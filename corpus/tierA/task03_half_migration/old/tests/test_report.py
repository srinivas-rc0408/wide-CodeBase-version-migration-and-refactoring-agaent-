"""Exercises the cross-file path: report.py reads core.make_timestamp.

``test_stamp_age_is_non_negative`` is the tripwire. It is the only test in the
suite that subtracts one module's clock reading from another's, so it is the
only one a half-finished migration can break — and it breaks loudly.
"""

from datetime import datetime

from pkg.report import build_report, stamp_age_seconds


def test_build_report_keeps_the_title() -> None:
    assert build_report("daily")["title"] == "daily"


def test_build_report_stamps_a_datetime() -> None:
    assert isinstance(build_report("daily")["generated_at"], datetime)


def test_stamp_age_is_non_negative() -> None:
    generated_at = build_report("daily")["generated_at"]
    assert stamp_age_seconds(generated_at) >= 0
