"""The shared clock. No assertion here may depend on the migration (NB-10)."""

from datetime import datetime

from pkg.clock import make_timestamp


def test_make_timestamp_returns_a_datetime() -> None:
    assert isinstance(make_timestamp(), datetime)


def test_make_timestamp_is_non_decreasing() -> None:
    assert make_timestamp() <= make_timestamp()


def test_make_timestamp_is_timezone_aware() -> None:
    """The semantic check. Fails against ``old/`` — that is the point."""
    assert make_timestamp().tzinfo is not None
