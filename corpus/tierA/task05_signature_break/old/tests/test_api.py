"""The service edge: every module in the DAG on one call path."""

from pkg.api import serve


def test_serve_returns_the_whole_response() -> None:
    response = serve("frank", 60)
    assert response["result"]["entry"]["account"] == "frank"
    assert response["metrics"]["entries"] >= 1
