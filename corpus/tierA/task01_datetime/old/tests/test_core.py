"""Behaviour that must hold on BOTH the old and the migrated code.

No assertion here may depend on the migration having happened — the suite is
the oracle and must be green before the agent touches anything (NB-10).
"""

from datetime import datetime

from pkg.core import make_timestamp


def test_make_timestamp_returns_a_datetime() -> None:
    assert isinstance(make_timestamp(), datetime)


def test_make_timestamp_is_non_decreasing() -> None:
    first = make_timestamp()
    second = make_timestamp()
    assert second >= first
