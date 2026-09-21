"""The service edge: the deepest module in the import DAG."""

from datetime import datetime, timezone

from pkg.handler import handle
from pkg.metrics import snapshot


def serve(account: str, amount: int) -> dict[str, object]:
    """One request, its ledger entry and a metrics snapshot."""
    return {"served_at": datetime.now(timezone.utc), "result": handle(account, amount),
            "metrics": snapshot()}
