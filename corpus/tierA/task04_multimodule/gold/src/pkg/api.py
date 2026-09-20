"""The entry point. Depends on report, audit and config — the graph's deepest module."""

from datetime import datetime, timezone

from pkg import audit, config
from pkg.report import summary


def handle(account: str, amount: int) -> dict[str, object]:
    """Serve one request. ``served_at`` is this module's own, self-contained reading."""
    return {
        "served_at": datetime.now(timezone.utc),
        "currency": config.CURRENCY,
        "summary": summary(account, amount),
        "trail_size": len(audit.trail()),
    }
