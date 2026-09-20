"""The entry point, exercising the whole import DAG in one call."""

from datetime import datetime

from pkg.api import handle


def test_handle_serves_a_complete_response() -> None:
    response = handle("heidi", 75)
    assert isinstance(response["served_at"], datetime)
    assert response["currency"] == "INR"
    assert response["summary"]["invoice"]["account"] == "heidi"
    assert response["trail_size"] >= 1


def test_every_stamp_in_one_response_is_aware() -> None:
    """Syntactic success is not success: no module may be left on a naive clock."""
    response = handle("ivan", 5)
    assert response["served_at"].tzinfo is not None
    assert response["summary"]["invoice"]["issued_at"].tzinfo is not None
