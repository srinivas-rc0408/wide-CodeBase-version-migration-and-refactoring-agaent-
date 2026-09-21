"""The ledger and the call-time half of the break."""

from pkg.ledger import age_of, post


def test_post_records_the_amount() -> None:
    assert post("alice", 10)["amount"] == 10


def test_age_of_an_entry_is_non_negative() -> None:
    assert age_of(post("bob", 20)) >= 0
