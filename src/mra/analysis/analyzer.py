"""MAP-node analysis: locate the work, map the dependencies. Nothing else.

Produces exactly the two fields the MAP node writes into ``MigrationState``
(SRS §4.1) — ``call_sites`` and ``dep_graph`` — and touches nothing. Read-only
by construction: no edits, no ordering, no LLM.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mra.analysis import call_sites as call_sites_module
from mra.analysis import dep_graph as dep_graph_module


def analyze(repo: Path | str, target: str) -> dict[str, Any]:
    """Scan ``repo`` for ``target`` and map its imports.

    Args:
        repo: repository root to analyse (read-only).
        target: fully-qualified symbol to find, e.g. ``datetime.datetime.utcnow``.

    Returns:
        ``{"call_sites": {file: [call_site, ...]}, "dep_graph": {file: [importers]}}``
        — the MAP node's partial state update.
    """
    repo = Path(repo)
    files = dep_graph_module.python_files(repo)
    return {
        "call_sites": call_sites_module.find_in_repo(repo, target, files=files),
        "dep_graph": dep_graph_module.to_state_adjacency(dep_graph_module.build(repo)),
    }


def flat_sites(call_sites: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Flatten the per-file map into one list, the form ground truth uses."""
    return [site for sites in call_sites.values() for site in sites]
