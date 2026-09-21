"""Point-in-time metrics over the ledger."""

from datetime import datetime

from pkg.ledger import ENTRIES
from pkg.timebase import elapsed_since


def snapshot() -> dict[str, object]:
    """Entry count plus how long this reading took to assemble."""
    taken_at = datetime.utcnow()
    return {"taken_at": taken_at, "entries": len(ENTRIES), "lag_s": elapsed_since(taken_at)}
