"""The clock contract. No assertion here may depend on the migration (NB-10).

:func:`aligned` is tested with explicit constants rather than clock readings,
so both of its branches are exercised identically before and after the
migration — including the refusal that the whole fixture turns on.
"""

from datetime import datetime, timezone

from pkg.timebase import aligned, elapsed_since, utc_now

NAIVE = datetime(2024, 1, 1, 12, 0, 0)
AWARE = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def test_utc_now_returns_a_datetime() -> None:
    assert isinstance(utc_now(), datetime)


def test_elapsed_since_its_own_reading_is_non_negative() -> None:
    assert elapsed_since(utc_now()) >= 0


def test_aligned_reads_a_naive_stamp_as_utc_when_the_clock_is_aware() -> None:
    """The safe window: a caller that has not moved yet is upgraded for free."""
    assert aligned(NAIVE, AWARE).tzinfo is timezone.utc


def test_aligned_never_strips_a_tzinfo() -> None:
    """The refusal: an aware stamp meeting a naive clock is passed through, not downgraded."""
    assert aligned(AWARE, NAIVE) is AWARE
