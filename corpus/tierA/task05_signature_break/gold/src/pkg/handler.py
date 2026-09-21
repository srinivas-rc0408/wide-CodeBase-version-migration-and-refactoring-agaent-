"""Request handling. Its own stamp never leaves the module, so it is self-contained."""

from datetime import datetime, timezone

from pkg.boot import uptime_s
from pkg.ledger import post


def handle(account: str, amount: int) -> dict[str, object]:
    """Post one amount and return the handled record."""
    received_at = datetime.now(timezone.utc)
    return {"received_at": received_at, "entry": post(account, amount),
            "uptime_s": uptime_s()}
