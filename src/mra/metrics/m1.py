"""M1 — Migration Completeness.

Transcribed verbatim from ``docs/05_DATA_EVALUATION_PROTOCOL.md`` §2.4, which is
the scoring contract. Do not re-derive the formula here; if it changes, it
changes in the protocol first and this follows (golden rule 4).

Recall answers "did it find every required site?", precision answers "of what it
touched, how much was correct and necessary?". Completeness alone can be gamed
by editing everything, which is why both are reported.
"""

from __future__ import annotations


def m1(agent_sites: set, correct_sites: set, ground_truth_sites: set):
    tp = len(correct_sites & ground_truth_sites)
    recall = 100 * tp / max(len(ground_truth_sites), 1)
    precision = 100 * tp / max(len(agent_sites), 1)
    f1 = 0 if (recall + precision) == 0 else 2 * recall * precision / (recall + precision)
    return {"recall": recall, "precision": precision, "f1": f1}
