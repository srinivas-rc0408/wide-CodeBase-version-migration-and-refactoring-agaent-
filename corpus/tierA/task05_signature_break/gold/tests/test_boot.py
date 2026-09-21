"""Start-up constants. Importing this module is itself the assertion."""

from datetime import datetime

from pkg.boot import STARTED_AT, STARTUP_LAG_S, uptime_s


def test_started_at_is_a_datetime() -> None:
    assert isinstance(STARTED_AT, datetime)


def test_startup_lag_was_computed_at_import() -> None:
    assert STARTUP_LAG_S >= 0


def test_uptime_grows_from_the_import_stamp() -> None:
    assert uptime_s() >= STARTUP_LAG_S
