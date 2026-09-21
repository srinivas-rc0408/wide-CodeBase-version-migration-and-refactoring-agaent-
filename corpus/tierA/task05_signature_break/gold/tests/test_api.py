"""The service edge: every module in the DAG on one call path."""

from pkg.api import serve


def test_serve_returns_the_whole_response() -> None:
    response = serve("frank", 60)
    assert response["result"]["entry"]["account"] == "frank"
    assert response["metrics"]["entries"] >= 1


def test_every_stamp_in_one_response_is_aware() -> None:
    """Syntactic success is not success: no module may be left on a naive clock."""
    response = serve("grace", 70)
    assert response["served_at"].tzinfo is not None
    assert response["result"]["received_at"].tzinfo is not None
    assert response["result"]["entry"]["posted_at"].tzinfo is not None
    assert response["metrics"]["taken_at"].tzinfo is not None
