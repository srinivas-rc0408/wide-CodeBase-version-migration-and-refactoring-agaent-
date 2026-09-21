"""Metrics snapshots."""

from pkg.ledger import post
from pkg.metrics import snapshot


def test_snapshot_counts_the_entries() -> None:
    before = snapshot()["entries"]
    post("carol", 30)
    assert snapshot()["entries"] == before + 1


def test_snapshot_reports_its_own_lag() -> None:
    assert snapshot()["lag_s"] >= 0
