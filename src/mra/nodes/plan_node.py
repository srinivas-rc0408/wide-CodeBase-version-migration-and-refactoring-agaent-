"""PLAN node: turn the dependency graph into an ordered list of edit batches (FR-3).

docs/04 §3.3 gives three rules and this module implements all three:

1. **Cycles are atomic.** An import cycle has no safe internal order — edit
   half of it and the half that moved is calling the half that did not — so
   every strongly connected component with more than one member becomes one
   batch and is tested once. ``networkx.condensation`` collapses exactly those
   components, which is the same set ``nx.simple_cycles`` enumerates, without
   the exponential enumeration.

2. **Dependencies before dependents.** Batches are ordered so that a file is
   never edited while something it imports is still unmigrated and scheduled
   for later. This is the FR-3 property the tests assert programmatically.

   Note the direction. The graph's edges run ``importer -> imported``, so a
   plain ``topological_sort`` yields importers *first* — the opposite of what
   "process leaf-most contracts first" (§3.3) requires. The order therefore
   comes from the **reversed** graph. The pseudocode in docs/04 §3.4 omits
   that flip; following it literally inverts every batch plan and fails the
   FR-3 assertion.

3. **Bounded batch size.** ``MRA_EDIT_BATCH_SIZE`` (NFR-5) caps how many files
   one EDIT touches before the suite runs again, which is what keeps the blast
   radius of a bad edit small. Independence beats size: files are chunked only
   within a topological generation, where they cannot depend on each other,
   and an atomic cycle is never split to satisfy the cap.
"""

from __future__ import annotations

import os
from typing import Any

import networkx as nx

DEFAULT_EDIT_BATCH_SIZE = 3


def _chunk(items: list[str], size: int) -> list[list[str]]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def cycles(graph: nx.DiGraph) -> list[list[str]]:
    """Every import cycle, as the set of files that must be edited together."""
    return [sorted(component) for component in nx.strongly_connected_components(graph)
            if len(component) > 1]


def plan_batches(
    graph: nx.DiGraph,
    call_sites: dict[str, list[dict[str, Any]]],
    batch_size: int | None = None,
) -> list[list[str]]:
    """Order the files that need editing into dependency-safe, size-capped batches.

    Args:
        graph: the repo import graph, ``importer -> imported``.
        call_sites: the MAP node's map; only files with a site are scheduled.
        batch_size: cap per batch; defaults to ``MRA_EDIT_BATCH_SIZE``.

    Returns:
        Ordered batches of repo-relative paths. Every file with a call site
        appears exactly once, including files the graph never saw (a module
        nothing imports still has to be migrated).
    """
    size = batch_size or int(os.getenv("MRA_EDIT_BATCH_SIZE", str(DEFAULT_EDIT_BATCH_SIZE)))
    needs_edit = {file for file, sites in call_sites.items() if sites}
    if not needs_edit:
        return []

    work = graph.copy()
    work.add_nodes_from(needs_edit)  # an unimported module is still a node

    condensed = nx.condensation(work)
    members: dict[int, list[str]] = {
        component: sorted(set(condensed.nodes[component]["members"]) & needs_edit)
        for component in condensed.nodes
    }

    batches: list[list[str]] = []
    # Reversed: generation 0 is what nothing in the repo depends on being
    # migrated first — the leaf-most contracts.
    for generation in nx.topological_generations(condensed.reverse()):
        atomic = [members[c] for c in generation if len(members[c]) > 1]
        singles = sorted(file for c in generation for file in members[c]
                         if len(members[c]) == 1)
        # A cycle keeps its own batch whatever the cap says; splitting it is
        # the one thing rule 1 forbids.
        batches.extend(sorted(atomic))
        batches.extend(_chunk(singles, size))
    return batches


def violations(batches: list[list[str]], graph: nx.DiGraph) -> list[tuple[str, str]]:
    """FR-3 check: ``(importer, imported)`` pairs scheduled in the wrong order.

    A violation is an edited file whose in-repo dependency is edited in a
    *later* batch — the case where a caller is migrated on top of something
    that has not moved yet. An empty list is the property holding.
    """
    index = {file: number for number, batch in enumerate(batches) for file in batch}
    return sorted(
        (importer, imported)
        for importer, imported in graph.edges
        if importer in index and imported in index and index[imported] > index[importer]
    )


def plan_node(state: dict[str, Any]) -> dict[str, Any]:
    """``MigrationState`` -> ``edit_batches`` (+ the audit note for this step)."""
    from mra.analysis import dep_graph as dep_graph_module

    graph = state.get("graph") or dep_graph_module.build(state["repo_path"])
    batches = plan_batches(graph, state.get("call_sites", {}))
    collapsed = [c for c in cycles(graph) if any(f in set().union(*batches) for f in c)] \
        if batches else []
    return {
        "edit_batches": batches,
        "current_batch": 0,
        "note": {
            "action": f"planned {len(batches)} batch(es) over "
                      f"{sum(len(b) for b in batches)} file(s)",
            "detail": {
                "batches": batches,
                "cycles_collapsed": collapsed,
                "batch_size": int(os.getenv("MRA_EDIT_BATCH_SIZE",
                                            str(DEFAULT_EDIT_BATCH_SIZE))),
                "fr3_violations": violations(batches, graph),
            },
        },
    }
