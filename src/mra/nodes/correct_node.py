"""CORRECT node: turn one test failure back into a green tree (FR-7).

The node reads a single entry from the ``mra:test_report`` the sandbox
produced (SRS §4.3) and runs the four steps of docs/04 §2.5:

    classify (V4-Flash)  ->  locate (analyzer + dep graph)
                         ->  patch (V4-Pro)  ->  apply

Two rules shape the whole module. **NB-4**: a corrective patch may never touch
a test file — the suite is the oracle, and repairing the oracle is how an agent
fakes a green run — so test paths are filtered out at localization and refused
again at apply. **NFR-12**: the patch prompt gets the failing file, the trace,
the contract and the graph slice around that file, and nothing else. Sending
the repo is how a long-horizon run runs out of context and out of budget.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import libcst as cst

from mra.analysis import call_sites as call_sites_module
from mra.analysis import dep_graph as dep_graph_module
from mra.memory import edit_context
from mra.models import Router

#: docs/04 §2.5 taxonomy. "non_fixable" is the class that ends the loop.
FAILURE_CLASSES = ("import", "signature", "behaviour", "assertion", "non_fixable")

#: How an exception maps onto the taxonomy, checked in order. A bare
#: ``TypeError`` is deliberately NOT a signature break: the half-migration's
#: "can't subtract offset-naive and offset-aware" raises TypeError but no
#: signature moved, and its fix is the semantic transform — a behaviour break
#: in docs/04 §2.5 terms. Only argument-shaped TypeErrors are signature breaks.
_CLASS_HINTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("import", ("ImportError", "ModuleNotFoundError")),
    ("signature", ("unexpected keyword argument", "positional argument",
                   "missing 1 required", "takes no arguments")),
    ("assertion", ("AssertionError",)),
)

_PY_PATH = re.compile(r"([\w./-]+\.py)")
_CODE_FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S)

CLASSIFY_SYSTEM = (
    "You triage Python test failures during a library migration. "
    "Answer with exactly one word from this list and nothing else: "
    + ", ".join(FAILURE_CLASSES) + "."
)

PATCH_SYSTEM = (
    "You finish partially applied Python migrations. You are given ONE source "
    "file that still uses the old API, the failure it caused, and the migration "
    "contract. Rewrite that one file so the contract holds everywhere in it.\n"
    "Rules:\n"
    "- Change only what the contract requires. Keep all other code, comments, "
    "docstrings, formatting and public behaviour byte-identical.\n"
    "- Add any import the new API needs.\n"
    "- Never modify, add or delete tests.\n"
    "- Reply with the complete corrected file inside one ```python fence, and "
    "no prose before or after it."
)


def is_test_path(path: str) -> bool:
    """True for anything that is part of the test oracle (NB-4)."""
    parts = Path(path).parts
    name = Path(path).name
    return (
        any(part in ("tests", "test") for part in parts)
        or name.startswith("test_")
        or name.endswith("_test.py")
        or name == "conftest.py"
    )


# -- (a) classify ----------------------------------------------------------


def classify_offline(failure: dict[str, Any]) -> str:
    """Taxonomy class from the exception alone — the fallback when no LLM is available.

    Deliberately crude. It exists so the loop still classifies when the key is
    absent, and so the LLM has a defined answer to be compared against.
    """
    blob = f"{failure.get('exc_type', '')}: {failure.get('message', '')}"
    for label, needles in _CLASS_HINTS:
        if any(needle in blob for needle in needles):
            return label
    return "behaviour"


def classify(failure: dict[str, Any], router: Router | None = None) -> str:
    """Classify one failure into the docs/04 §2.5 taxonomy (V4-Flash)."""
    if router is None or not router.available:
        return classify_offline(failure)
    prompt = (
        f"exception: {failure.get('exc_type', '')}\n"
        f"message: {failure.get('message', '')}\n"
        f"test: {failure.get('nodeid', '')}\n"
        f"trace:\n{str(failure.get('trace', ''))[:1500]}"
    )
    answer = router.complete("classify", CLASSIFY_SYSTEM, prompt).strip().lower()
    for label in FAILURE_CLASSES:
        if label in answer:
            return label
    return classify_offline(failure)


# -- (b) locate ------------------------------------------------------------


def _hinted_files(failure: dict[str, Any]) -> set[str]:
    """Repo-relative .py paths the failure points at: its crash site and its trace."""
    blob = f"{failure.get('file', '')}\n{failure.get('trace', '')}"
    return {match for match in _PY_PATH.findall(blob) if not is_test_path(match)}


def locate(
    repo: Path | str,
    failure: dict[str, Any],
    target: str,
    dep_graph: Any = None,
) -> dict[str, Any] | None:
    """Map a failure onto the source file that still holds an unmigrated call site.

    Re-runs the analyzer over the *current* tree, so "what is left to migrate"
    is measured rather than remembered — the half-migrated files have already
    dropped out of the result. The failure's own crash path and trace pick
    which of the remaining files to repair first; the dependency graph supplies
    the slice of neighbours that goes into the patch prompt (NFR-12).

    Returns ``None`` when nothing is left to migrate, which means the failure
    is not a half-migration and this node cannot fix it.
    """
    repo = Path(repo)
    remaining = call_sites_module.find_in_repo(repo, target)
    candidates = {path: sites for path, sites in remaining.items() if not is_test_path(path)}
    if not candidates:
        return None

    hinted = _hinted_files(failure) & candidates.keys()
    chosen = sorted(hinted)[0] if hinted else sorted(candidates)[0]

    graph = dep_graph if dep_graph is not None else dep_graph_module.build(repo)
    return {
        "file": chosen,
        "source": (repo / chosen).read_text(),
        "sites": candidates[chosen],
        # Who breaks if this file's contract moves, and what it depends on.
        "importers": sorted(graph.predecessors(chosen)) if graph.has_node(chosen) else [],
        "imports": sorted(graph.successors(chosen)) if graph.has_node(chosen) else [],
        "hinted_by_trace": bool(hinted),
        "remaining_files": sorted(candidates),
    }


# -- (c) generate ----------------------------------------------------------


def patch_prompt(
    failure: dict[str, Any],
    located: dict[str, Any],
    contract: dict[str, Any],
    klass: str,
    summary: str = "",
) -> str:
    """The whole context a corrective edit gets. Nothing else is sent (NFR-12).

    Assembled by :mod:`mra.memory`, which caps every component that would
    otherwise grow with the repo — the neighbour list, the trace and the
    rolling summary — so the payload tracks the file being fixed, not the
    number of files around it.
    """
    return edit_context(failure, located, contract, klass, summary)


def extract_source(reply: str) -> str:
    """Pull the corrected file out of the model's reply and prove it parses.

    A patch that does not parse is worse than no patch: it turns a semantic
    failure into a collection error and hides the original break.
    """
    match = _CODE_FENCE.search(reply)
    source = (match.group(1) if match else reply).strip() + "\n"
    cst.parse_module(source)  # raises ParserSyntaxError on garbage
    return source


def corrective_patch(
    router: Router,
    failure: dict[str, Any],
    located: dict[str, Any],
    contract: dict[str, Any],
    klass: str,
    summary: str = "",
) -> str:
    """Ask V4-Pro for the corrected file (whole-file, libcst-validated)."""
    reply = router.complete(
        "edit", PATCH_SYSTEM, patch_prompt(failure, located, contract, klass, summary)
    )
    return extract_source(reply)


# -- (d) apply -------------------------------------------------------------


def apply_source(repo: Path | str, relative: str, source: str) -> list[str]:
    """Write a corrected file, refusing test paths and no-op writes."""
    if is_test_path(relative):
        raise PermissionError(f"NB-4: CORRECT may not edit the test oracle ({relative})")
    path = Path(repo) / relative
    if path.read_text() == source:
        return []
    path.write_text(source)
    return [relative]


class LLMCorrector:
    """The CORRECT node as a corrector callable, for :func:`mra.recovery.recover`.

    One call = one repaired file. The loop re-tests after every call, so a
    migration left half-done across several files converges one file per round
    instead of being guessed at in one shot.
    """

    def __init__(self, router: Router, target: str, contract: dict[str, Any]) -> None:
        self.router = router
        self.target = target
        self.contract = contract
        #: What each round decided, for the trajectory.
        self.log: list[dict[str, Any]] = []
        #: Size of every prompt sent, so the context budget is measurable
        #: rather than asserted (NFR-12, M3).
        self.payload_chars: list[int] = []

    def __call__(
        self, repo: Path, failure: dict[str, Any], context: dict[str, Any]
    ) -> list[str]:
        klass = classify(failure, self.router)
        located = locate(repo, failure, self.target, dep_graph=context.get("graph"))
        if located is None or klass == "non_fixable":
            self.log.append({"class": klass, "file": None, "reason": "nothing left to migrate"})
            return []
        summary = context.get("summary", "")
        self.payload_chars.append(
            len(patch_prompt(failure, located, self.contract, klass, summary))
        )
        source = corrective_patch(
            self.router, failure, located, self.contract, klass, summary
        )
        changed = apply_source(repo, located["file"], source)
        self.log.append({
            "class": klass,
            "file": located["file"],
            "hinted_by_trace": located["hinted_by_trace"],
            "changed": changed,
        })
        return changed


def make_correct_node(corrector: Any, router: Router | None = None):
    """Bind a corrector and return the node LangGraph calls.

    One visit repairs one failure. The node owns the two invariants the loop
    cannot delegate: the per-signature attempt counter (NFR-1), and the NB-4
    guard that reverts a patch which touched the test oracle before it can be
    tested against it.
    """
    from mra.memory import summarize
    from mra.sandbox import changed_paths, rollback, snapshot

    def correct_node(state: dict[str, Any]) -> dict[str, Any]:
        report = state["last_test_report"]
        attempts = dict(state.get("fix_attempts") or {})
        cap = _cap()
        failure = next(
            (f for f in report["failures"] if attempts.get(f["signature"], 0) < cap), None
        )
        if failure is None:  # pragma: no cover - the router routes to give_up first
            return {"note": {"action": "no failure left with attempts to spend", "detail": {}}}

        signature = failure["signature"]
        attempts[signature] = attempts.get(signature, 0) + 1
        repo = Path(state["repo_path"])
        summary = summarize(state, router)

        base_sha = snapshot(repo, f"pre-correction ({signature})")
        changed = corrector(repo, failure, {
            "call_sites": state.get("call_sites") or {},
            "dep_graph": state.get("dep_graph") or {},
            "contract": state.get("contract") or {},
            "summary": summary,
        })

        tampered = [p for p in changed_paths(repo, base_sha) if is_test_path(p)]
        if tampered:
            # Golden rule 1: revert first, report second.
            rollback(repo, base_sha)
            return {
                "fix_attempts": attempts, "summary": summary,
                "note": {
                    "action": "rejected a patch that edited the test oracle (NB-4)",
                    "detail": {"signature": signature, "attempt": attempts[signature],
                               "rejected": tampered, "changed": []},
                },
            }

        sha = snapshot(repo, f"correction {attempts[signature]} for {signature}")
        status = dict(state.get("file_status") or {})
        for file in changed:
            status[file] = "migrated"
        return {
            "fix_attempts": attempts,
            "file_status": status,
            "summary": summary,
            "note": {
                "action": f"attempt {attempts[signature]}/{cap} on {failure['nodeid']}",
                "detail": {"signature": signature, "attempt": attempts[signature],
                           "exc_type": failure.get("exc_type"), "changed": changed, "sha": sha},
            },
        }

    return correct_node


def _cap() -> int:
    from mra.recovery.loop import DEFAULT_MAX_FIX_ATTEMPTS

    return int(os.environ.get("MRA_MAX_FIX_ATTEMPTS", str(DEFAULT_MAX_FIX_ATTEMPTS)))
