"""The service edge: the deepest module in the import DAG."""

from datetime import datetime

from pkg.handler import handle
from pkg.metrics import snapshot


def serve(account: str, amount: int) -> dict[str, object]:
    """One request, its ledger entry and a metrics snapshot."""
    return {"served_at": datetime.utcnow(), "result": handle(account, amount),
            "metrics": snapshot()}
