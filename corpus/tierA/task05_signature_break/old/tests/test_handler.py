"""Request handling."""

from pkg.handler import handle


def test_handle_posts_the_entry() -> None:
    assert handle("dave", 40)["entry"]["amount"] == 40


def test_handle_reports_uptime() -> None:
    assert handle("erin", 50)["uptime_s"] >= 0
