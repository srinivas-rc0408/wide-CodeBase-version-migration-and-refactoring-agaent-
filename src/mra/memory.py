"""Rolling memory: what the model is told about everything that is not in front of it.

NFR-12 says an edit call gets "only the target file + graph slice + rolling
summary". The reason is arithmetic, not taste: a prompt that names every
migrated file grows linearly with the repo, so the last batch of a 400-module
migration costs many times what the first did, and M3 degrades with exactly
the repo size the agent is supposed to scale to.

So every part of the context that *could* grow with repo size is capped here
instead:

* progress is carried as **counts and the last few events**, never as lists of
  files — :func:`progress_facts` is O(1) in repo size by construction;
* the dependency slice is truncated to the nearest few neighbours plus a count;
* the rolling summary is a bounded string, re-summarized by the cheap model.

What is left growing is the target file itself, which is the one thing the
model genuinely has to read.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mra.models import Router

#: Hard ceilings on the parts of a prompt that would otherwise track repo size.
SUMMARY_MAX_CHARS = 800
MAX_NEIGHBOURS = 5
TRACE_MAX_CHARS = 2000

SUMMARY_SYSTEM = (
    "You keep a running progress note for a code-migration agent. Rewrite the "
    "facts below as at most three short sentences of plain prose: what has been "
    "migrated so far, what has failed and how often, and what is outstanding. "
    "Never list file names. Never exceed 60 words. No preamble."
)


def progress_facts(state: dict[str, Any]) -> dict[str, Any]:
    """Everything worth remembering about a run, in constant size.

    Deliberately counts rather than names. A run over four files and a run
    over four thousand produce the same number of keys and the same order of
    magnitude of characters, which is what makes the prompt flat.
    """
    batches: list[list[str]] = state.get("edit_batches") or []
    status: dict[str, str] = state.get("file_status") or {}
    attempts: dict[str, int] = state.get("fix_attempts") or {}
    report: dict[str, Any] = state.get("last_test_report") or {}
    current = int(state.get("current_batch", 0))
    return {
        "batches_total": len(batches),
        "batches_done": min(current, len(batches)),
        "files_total": sum(len(batch) for batch in batches),
        "files_migrated": sum(1 for value in status.values()
                              if value in ("migrated", "verified")),
        "files_failed": sum(1 for value in status.values() if value == "failed"),
        "tests_total": report.get("total", 0),
        "tests_failed": report.get("failed", 0) + report.get("errors", 0),
        "corrections_attempted": sum(attempts.values()),
        "distinct_failures": len(attempts),
        "worst_signature_attempts": max(attempts.values(), default=0),
    }


def offline_summary(facts: dict[str, Any]) -> str:
    """The deterministic digest, used when no model is available.

    Also the input the cheap model rewrites, so the live and offline paths
    carry the same information and only differ in prose.
    """
    return (
        f"Batch {facts['batches_done']}/{facts['batches_total']}; "
        f"{facts['files_migrated']}/{facts['files_total']} files migrated, "
        f"{facts['files_failed']} failed. "
        f"Suite: {facts['tests_failed']} failing of {facts['tests_total']}. "
        f"Recovery: {facts['corrections_attempted']} attempt(s) across "
        f"{facts['distinct_failures']} distinct failure(s), "
        f"worst signature at {facts['worst_signature_attempts']}."
    )


def summarize(state: dict[str, Any], router: Router | None = None) -> str:
    """The rolling summary for the next prompt (V4-Flash), always length-capped.

    A model that ignores the word limit cannot blow the budget: the result is
    truncated either way.
    """
    facts = progress_facts(state)
    digest = offline_summary(facts)
    if router is None or not router.available:
        return digest[:SUMMARY_MAX_CHARS]
    previous = (state.get("summary") or "").strip()
    prompt = digest if not previous else f"previous note: {previous}\ncurrent facts: {digest}"
    try:
        text = router.complete("summary", SUMMARY_SYSTEM, prompt, max_tokens=200).strip()
    except Exception:
        # A summariser is a convenience. Losing it must not fail the migration.
        return digest[:SUMMARY_MAX_CHARS]
    return (text or digest)[:SUMMARY_MAX_CHARS]


def graph_slice(located: dict[str, Any]) -> str:
    """The dependency neighbourhood, truncated to a constant number of names."""

    def clip(names: list[str]) -> str:
        if not names:
            return "nothing"
        head = ", ".join(names[:MAX_NEIGHBOURS])
        extra = len(names) - MAX_NEIGHBOURS
        return f"{head} (+{extra} more)" if extra > 0 else head

    return (
        f"# {located['file']} is imported by: {clip(located['importers'])}\n"
        f"# {located['file']} imports: {clip(located['imports'])}"
    )


def edit_context(
    failure: dict[str, Any],
    located: dict[str, Any],
    contract: dict[str, Any],
    klass: str,
    summary: str = "",
) -> str:
    """The complete payload for one corrective-edit call (NFR-12).

    Everything except ``located["source"]`` is bounded by a constant, so the
    payload tracks the size of the file being fixed and not the size of the
    repo it lives in.
    """
    sites = [(site["line"], site["symbol"]) for site in located["sites"][:MAX_NEIGHBOURS]]
    return "\n".join([
        f"# migration contract: {contract.get('source_api')} -> {contract.get('target_api')}",
        f"# failure class: {klass}",
        f"# failing test: {failure.get('nodeid')}",
        f"# exception: {failure.get('exc_type')}: {failure.get('message')}",
        "",
        "# progress so far",
        f"# {summary[:SUMMARY_MAX_CHARS]}" if summary else "# (first correction of this run)",
        "",
        "# trace",
        str(failure.get("trace", ""))[:TRACE_MAX_CHARS],
        "",
        "# dependency-graph slice",
        graph_slice(located),
        f"# unmigrated call sites still in this file: {sites}",
        "",
        f"# file to rewrite: {located['file']}",
        "```python",
        located["source"],
        "```",
    ])
