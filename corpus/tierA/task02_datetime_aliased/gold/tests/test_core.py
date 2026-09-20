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


def test_make_timestamp_is_timezone_aware() -> None:
    """Gold-only: documents the semantic gain the migration must deliver.

    This assertion is false on the pre-migration tree, so it lives here and
    never in ``old/tests`` (see docs/05_DATA_EVALUATION_PROTOCOL.md §1.1).
    """
    assert make_timestamp().tzinfo is not None
