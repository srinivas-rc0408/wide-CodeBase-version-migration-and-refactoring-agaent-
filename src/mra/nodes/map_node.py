"""MAP node: locate the work and map the dependencies. Read-only (FR-1, FR-2)."""

from __future__ import annotations

from typing import Any

from mra.analysis import analyze, flat_sites


def make_map_node(target: str):
    """Bind the target symbol and return the node LangGraph calls."""

    def map_node(state: dict[str, Any]) -> dict[str, Any]:
        analysis = analyze(state["repo_path"], target)
        sites = flat_sites(analysis["call_sites"])
        return {
            "call_sites": analysis["call_sites"],
            "dep_graph": analysis["dep_graph"],
            # Every file with a site starts pending; PLAN decides the order.
            "file_status": dict.fromkeys(analysis["call_sites"], "pending"),
            "note": {
                "action": f"found {len(sites)} call site(s) in "
                          f"{len(analysis['call_sites'])} file(s)",
                "detail": {"files": sorted(analysis["call_sites"]), "target": target},
            },
        }

    return map_node
