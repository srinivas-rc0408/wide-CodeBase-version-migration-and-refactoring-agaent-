"""Static analysis: where the migration has to happen, and in what order it can."""

from mra.analysis.analyzer import analyze, flat_sites
from mra.analysis.call_sites import CallSite, find_in_repo, find_in_source
from mra.analysis.dep_graph import build, module_index, python_files, to_state_adjacency

__all__ = [
    "CallSite",
    "analyze",
    "build",
    "find_in_repo",
    "find_in_source",
    "flat_sites",
    "module_index",
    "python_files",
    "to_state_adjacency",
]
