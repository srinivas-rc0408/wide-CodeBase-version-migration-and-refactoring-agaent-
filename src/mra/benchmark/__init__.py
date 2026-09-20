"""P5 benchmarking: run the agent across the corpus under controlled conditions."""

from mra.benchmark.baselines import baseline_table, ruff_baseline
from mra.benchmark.runner import (
    CONFIGS,
    Config,
    codemod_corrector,
    failure_analysis,
    make_planner,
    render_markdown,
    run_matrix,
    run_one,
)

__all__ = [
    "CONFIGS", "Config", "baseline_table", "codemod_corrector", "failure_analysis",
    "make_planner", "render_markdown", "ruff_baseline", "run_matrix", "run_one",
]
