"""M2 — Post-Migration Test Pass Rate.

Transcribed verbatim from ``docs/05_DATA_EVALUATION_PROTOCOL.md`` §2.4. The
precondition is that the suite is green before migration (NB-10); without it
M2 is undefined, which is why the runner tests the tree before editing it.
"""

from __future__ import annotations


def m2(t_total: int, t_post_pass: int):
    return {"pass_rate": 100 * t_post_pass / max(t_total, 1),
            "regressions": t_total - t_post_pass}
