"""Ledger, including its self-contained clock reading."""

from pkg.ledger import balance, post, snapshot_window


def test_post_returns_a_stamped_entry() -> None:
    entry = post("alice", 100)
    assert entry["account"] == "alice"
    assert entry["at"] is not None


def test_balance_sums_only_that_account() -> None:
    post("bob", 40)
    post("bob", 2)
    post("carol", 999)
    assert balance("bob") == 42


def test_snapshot_window_is_ordered() -> None:
    """Both ends come from one reading — safe whichever side of the migration."""
    start, end = snapshot_window(60)
    assert start < end
