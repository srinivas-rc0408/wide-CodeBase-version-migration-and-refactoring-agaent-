"""P5 harness: run one agent configuration over the Tier-A corpus and score it.

The agent itself is unchanged here — this module only *drives* it. A
:class:`Config` names the four knobs the ablations in docs/05 §3 turn:

============  ===========================================================
``recovery``  the CORRECT loop on or off (ablation A, the flagship)
``order``     dependency-ordered batches or a deliberately worse order (B)
``model``     which model writes the corrective edit (C, needs a key)
``batch_size`` files per EDIT before the suite runs again (D)
============  ===========================================================

Two knobs are set through the environment rather than an argument, because
that is where the agent already reads them (``MRA_EDIT_BATCH_SIZE`` in
``plan_node``, ``MRA_MAX_FIX_ATTEMPTS`` in ``route_after_test``). Turning
recovery *off* therefore needs no flag in the agent at all: a cap of zero
means no failure ever has an attempt left, so the router takes ``give_up``
on the first red suite. That is exactly the "no self-correction" condition
the ablation wants, and it keeps the production path free of a dead branch.

Every configuration runs ``repeats`` times (docs/05 §3: the LLM path is
non-deterministic) and the table reports mean and spread. The deterministic
configurations will report a spread of zero on everything but wall clock —
that is the point of having them: they are reproducible without a key.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import statistics
import time
import uuid
from collections.abc import Iterator, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mra.analysis import dep_graph as dep_graph_module
from mra.codemods.datetime_utcnow import TARGET
from mra.graph import run_migration
from mra.nodes.correct_node import classify_offline, locate
from mra.nodes.edit_node import apply_codemod
from mra.nodes.plan_node import DEFAULT_EDIT_BATCH_SIZE, plan_batches, plan_node

#: The Tier-A corpus, in the order the table reports it.
TASKS = ("task01_datetime", "task02_datetime_aliased",
         "task03_half_migration", "task04_multimodule")

DEFAULT_REPEATS = 3
DEFAULT_CORPUS = Path("corpus/tierA")
DEFAULT_OUT = Path("runs/benchmark")


# -- configuration ---------------------------------------------------------


@dataclass(frozen=True)
class Config:
    """One point in the ablation matrix (docs/05 §3: one variable at a time)."""

    name: str
    recovery: bool = True
    order: str = "dependency"          # dependency | alphabetical | fr3_violating
    batch_size: int = DEFAULT_EDIT_BATCH_SIZE
    model: str = "deterministic"       # deterministic | v4-pro | v4-flash
    ablation: str = ""
    note: str = ""

    @property
    def requires_key(self) -> bool:
        """True when this row cannot be produced without ``DEEPSEEK_API_KEY``."""
        return self.model != "deterministic"


#: The published matrix. ``baseline`` is the reference row every ablation is
#: read against; each other config changes exactly one thing about it.
CONFIGS: tuple[Config, ...] = (
    Config("baseline", ablation="reference",
           note="recovery on, dependency order, batch 3, deterministic corrector"),
    Config("no-recovery", recovery=False, ablation="A",
           note="CORRECT loop disabled (MRA_MAX_FIX_ATTEMPTS=0)"),
    Config("order-alphabetical", order="alphabetical", ablation="B",
           note="batches by file name instead of the dependency graph"),
    Config("order-fr3-violating", order="fr3_violating", ablation="B",
           note="plain topological order — dependents before dependencies, "
                "the docs/04 §3.4 pseudocode defect"),
    # At batch 3 a Tier-A task is 1-2 batches wide, so batch size and edit order
    # are confounded: an order that happens to group a producer with its consumer
    # never exposes an intermediate state at all. These two arms re-run the
    # ordering comparison at one file per batch, where the only thing left that
    # can differ is the sequence.
    Config("order-alphabetical-b1", order="alphabetical", batch_size=1, ablation="B",
           note="file-name order, one file per EDIT"),
    Config("order-fr3-violating-b1", order="fr3_violating", batch_size=1, ablation="B",
           note="dependents-first order, one file per EDIT"),
    Config("batch-1", batch_size=1, ablation="D", note="one file per EDIT"),
    Config("batch-5", batch_size=5, ablation="D", note="five files per EDIT"),
    Config("edit-v4-pro", model="v4-pro", ablation="C",
           note="live corrective edits from the strong model"),
    Config("edit-v4-flash", model="v4-flash", ablation="C",
           note="live corrective edits from the cheap model"),
)


@contextlib.contextmanager
def _env(**values: str) -> Iterator[None]:
    """Set env vars for the duration of one run, then put them back."""
    previous = {key: os.environ.get(key) for key in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for key, was in previous.items():
            if was is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = was


# -- the deterministic corrector -------------------------------------------


def codemod_corrector(repo: Path, failure: dict[str, Any], context: dict[str, Any]) -> list[str]:
    """The CORRECT node with the model taken out and the codemod put in.

    It localizes through the same :func:`locate` the LLM corrector uses — same
    trace parsing, same dependency slice, same NB-4 test-file filter — and then
    applies the deterministic transform instead of asking V4-Pro for a file.
    The loop mechanics under test are therefore identical; only the patch
    generator is reproducible. This is what lets ablation A be demonstrated
    without an API key.
    """
    located = locate(repo, failure, TARGET, dep_graph=context.get("graph"))
    if located is None:
        return []
    return apply_codemod(repo, {located["file"]: located["sites"]})


# -- the planners the ordering ablation compares ---------------------------


def _chunk(items: list[str], size: int) -> list[list[str]]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def make_planner(order: str) -> Any:
    """Return the PLAN node for an ordering arm.

    * ``dependency`` — the agent's own :func:`plan_node` (FR-3 holds).
    * ``alphabetical`` — the arbitrary order of docs/05 §3, file name order,
      ignoring the graph entirely.
    * ``fr3_violating`` — :func:`plan_batches` fed the *reversed* graph, which
      makes it emit dependents before their dependencies: the exact inversion
      the docs/04 §3.4 pseudocode produces if its missing ``.reverse()`` is
      taken at face value. Cycles stay atomic, so the only variable that moves
      is the order itself.
    """
    if order == "dependency":
        return plan_node

    def planner(state: dict[str, Any]) -> dict[str, Any]:
        graph = state.get("graph") or dep_graph_module.build(state["repo_path"])
        call_sites = state.get("call_sites") or {}
        size = int(os.getenv("MRA_EDIT_BATCH_SIZE", str(DEFAULT_EDIT_BATCH_SIZE)))
        if order == "alphabetical":
            batches = _chunk(sorted(f for f, sites in call_sites.items() if sites), size)
        elif order == "fr3_violating":
            batches = plan_batches(graph.reverse(copy=True), call_sites, batch_size=size)
        else:  # pragma: no cover - guarded by Config validation at call sites
            raise ValueError(f"unknown batch order: {order}")
        from mra.nodes.plan_node import violations

        return {
            "edit_batches": batches,
            "current_batch": 0,
            "note": {
                "action": f"planned {len(batches)} batch(es) over "
                          f"{sum(len(b) for b in batches)} file(s) [{order}]",
                "detail": {"batches": batches, "order": order, "batch_size": size,
                           "cycles_collapsed": [],
                           "fr3_violations": violations(batches, graph)},
            },
        }

    return planner


# -- one (task, config) run ------------------------------------------------


def _f1(recall: float, precision: float) -> float:
    return 0.0 if (recall + precision) == 0 else 2 * recall * precision / (recall + precision)


def _failures(report: dict[str, Any]) -> list[dict[str, Any]]:
    """The surviving failures, tagged with their docs/04 §2.5 class."""
    return [{
        "nodeid": failure.get("nodeid", ""),
        "signature": failure.get("signature", ""),
        "exc_type": failure.get("exc_type", ""),
        "message": (failure.get("message") or "")[:200],
        "file": failure.get("file", ""),
        "failure_class": classify_offline(failure),
    } for failure in report.get("failures", [])]


def run_one(
    task_dir: Path | str,
    config: Config,
    *,
    repeat: int = 0,
    runs_dir: Path | str = DEFAULT_OUT / "runs",
    target: str = TARGET,
) -> dict[str, Any]:
    """Run one configuration on one task and return the benchmark row."""
    task_dir = Path(task_dir)
    run_id = f"{config.name}-{task_dir.name}-r{repeat}-{uuid.uuid4().hex[:6]}"

    corrector: Any = codemod_corrector if config.recovery else None
    router = None
    state = None
    if config.recovery and config.requires_key:
        from mra.models import Router
        from mra.nodes.correct_node import LLMCorrector
        from mra.state import new_state

        truth = json.loads((task_dir / "ground_truth.json").read_text())
        state = new_state(run_id, "", {"task_id": task_dir.name,
                                       "source_api": truth["source_api"],
                                       "target_api": truth["target_api"]})
        router = Router(state["tokens"])
        corrector = LLMCorrector(router, target, state["contract"])

    # A cap of zero is how recovery is switched off; see the module docstring.
    environment = {"MRA_EDIT_BATCH_SIZE": str(config.batch_size)}
    if not config.recovery:
        environment["MRA_MAX_FIX_ATTEMPTS"] = "0"
    if config.model == "v4-flash":
        environment["MRA_EDIT_MODEL"] = os.getenv("MRA_UTILITY_MODEL", "deepseek-v4-flash")

    started = time.perf_counter()
    with _env(**environment):
        result = run_migration(
            task_dir, run_id=run_id, runs_dir=runs_dir, target=target,
            corrector=corrector, router=router, state=state,
            planner=make_planner(config.order),
        )
    wall_clock = time.perf_counter() - started

    metrics = result["metrics"]
    tokens = dict(result["state"].get("tokens") or {})
    finish = next((e for e in reversed(result["trajectory"]) if e["node"] == "FINISH"), None)
    return {
        "config": config.name,
        "ablation": config.ablation,
        "task_id": result["task_id"],
        "repeat": repeat,
        "run_id": run_id,
        "outcome": metrics["outcome"],
        "m1_recall": metrics["m1_recall"],
        "m1_precision": metrics["m1_precision"],
        "m1_f1": _f1(metrics["m1_recall"], metrics["m1_precision"]),
        "m2_pass_rate": metrics["m2_pass_rate"],
        "m2_regressions": metrics["m2_regressions"],
        "m3_tokens": metrics["m3_tokens"],
        "pro_in": tokens.get("pro_in", 0), "pro_out": tokens.get("pro_out", 0),
        "flash_in": tokens.get("flash_in", 0), "flash_out": tokens.get("flash_out", 0),
        "m3_steps": metrics["m3_steps"],
        "cost_usd": metrics["m3_cost_usd"],
        "recovery_used": metrics["recovery_used"],
        # What the loop had to spend: one CORRECT visit per attempt. The
        # ordering ablation lives here — a worse order is paid for in
        # corrective edits long before it is paid for in a failed run.
        "corrections": sum((result["state"].get("fix_attempts") or {}).values()),
        "wall_clock_s": round(wall_clock, 2),
        "batches": result["batches"],
        "changed_files": result["changed_files"],
        "fix_attempts": dict(result["state"].get("fix_attempts") or {}),
        "failures": _failures(result["test_report"]),
        "stopped_at_batch": (finish or {}).get("action", ""),
    }


# -- the matrix ------------------------------------------------------------

MEAN_FIELDS = ("m1_recall", "m1_precision", "m1_f1", "m2_pass_rate", "m2_regressions",
               "corrections", "m3_tokens", "m3_steps", "cost_usd", "wall_clock_s")


def _aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Mean and spread (max - min) per (config, task), as docs/05 §3 requires."""
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault((row["config"], row["task_id"]), []).append(row)

    summary = []
    for (config, task), group in groups.items():
        entry: dict[str, Any] = {
            "config": config, "task_id": task, "ablation": group[0]["ablation"],
            "n": len(group),
            "outcomes": {o: sum(1 for r in group if r["outcome"] == o)
                         for o in sorted({r["outcome"] for r in group})},
            "recovery_used": any(r["recovery_used"] for r in group),
        }
        for field_name in MEAN_FIELDS:
            values = [r[field_name] for r in group]
            entry[f"{field_name}_mean"] = statistics.fmean(values)
            entry[f"{field_name}_spread"] = max(values) - min(values)
        summary.append(entry)
    return summary


def run_matrix(
    tasks: Sequence[str] = TASKS,
    configs: Sequence[Config] = CONFIGS,
    *,
    repeats: int = DEFAULT_REPEATS,
    corpus: Path | str = DEFAULT_CORPUS,
    out_dir: Path | str = DEFAULT_OUT,
    baselines: bool = True,
) -> dict[str, Any]:
    """Run every (task, config, repeat) and write results.json / .md / failure-analysis.md."""
    from mra.benchmark.baselines import baseline_table

    corpus, out_dir = Path(corpus), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    have_key = bool(os.getenv("DEEPSEEK_API_KEY"))

    rows: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for config in configs:
        if config.requires_key and not have_key:
            skipped.extend({"config": config.name, "task_id": task,
                            "reason": "requires DEEPSEEK_API_KEY"} for task in tasks)
            continue
        for task in tasks:
            for repeat in range(repeats):
                rows.append(run_one(corpus / task, config, repeat=repeat,
                                    runs_dir=out_dir / "runs"))

    results = {
        "schema": "mra:benchmark_results/1",
        "generated_at": datetime.now(UTC).isoformat(),
        "out_dir": str(out_dir),
        "repeats": repeats,
        "tasks": list(tasks),
        "configs": [asdict(c) for c in configs],
        "live_llm_available": have_key,
        "rows": rows,
        "skipped": skipped,
        "aggregates": _aggregate(rows),
        "baselines": baseline_table(tasks, corpus=corpus) if baselines else [],
    }
    (out_dir / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    (out_dir / "results.md").write_text(render_markdown(results))
    (out_dir / "failure-analysis.md").write_text(failure_analysis(results))
    return results


# -- rendering -------------------------------------------------------------


def _cell(entry: dict[str, Any], field_name: str, digits: int = 1) -> str:
    """``mean`` alone when every repeat agreed, ``mean ±spread`` when they did not."""
    mean, spread = entry[f"{field_name}_mean"], entry[f"{field_name}_spread"]
    text = f"{mean:.{digits}f}"
    return text if spread == 0 else f"{text} ±{spread:.{digits}f}"


def _verdict(entry: dict[str, Any]) -> str:
    return ", ".join(f"{count}× {outcome}" for outcome, count in entry["outcomes"].items())


def _table(entries: list[dict[str, Any]], key: str = "config") -> list[str]:
    header = (f"| {key} | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr "
              "| steps | tokens | cost $ | wall s |")
    lines = [header, "|" + "---|" * 12]
    for entry in entries:
        lines.append(
            f"| `{entry[key]}` | {_verdict(entry)} | {_cell(entry, 'm1_recall')} "
            f"| {_cell(entry, 'm1_precision')} | {_cell(entry, 'm1_f1')} "
            f"| {_cell(entry, 'm2_pass_rate')} | {_cell(entry, 'm2_regressions', 0)} "
            f"| {_cell(entry, 'corrections', 0)} "
            f"| {_cell(entry, 'm3_steps', 0)} | {_cell(entry, 'm3_tokens', 0)} "
            f"| {entry['cost_usd_mean']:.4f} | {_cell(entry, 'wall_clock_s', 2)} |"
        )
    return lines


def _pick(aggregates: list[dict[str, Any]], configs: Sequence[str],
          task: str) -> list[dict[str, Any]]:
    order = {name: index for index, name in enumerate(configs)}
    found = [a for a in aggregates if a["task_id"] == task and a["config"] in order]
    return sorted(found, key=lambda a: order[a["config"]])


def render_markdown(results: dict[str, Any]) -> str:
    """The results table the paper reports (docs/05 §3)."""
    aggregates = results["aggregates"]
    notes = {c["name"]: c["note"] for c in results["configs"]}
    lines = [
        "# Benchmark results — Tier A",
        "",
        f"Generated {results['generated_at']} · {results['repeats']} repeat(s) per "
        f"(task, config) · mean ±spread across repeats.",
        "",
        "Every row is one agent configuration on one task. `baseline` is the reference "
        "(recovery on, dependency-ordered batches of 3, deterministic corrector); every "
        "other configuration changes exactly one thing about it (docs/05 §3).",
        "",
        "## 1. Per task, per configuration",
        "",
    ]
    for task in results["tasks"]:
        entries = [a for a in aggregates if a["task_id"] == task]
        if not entries:
            continue
        lines += [f"### {task}", ""] + _table(entries) + [""]

    lines += ["## 2. Ablations", ""]
    lines += _ablation_a(results) + _ablation_b(results)
    lines += _ablation_d(results) + _ablation_c(results)
    lines += _baseline_section(results)

    lines += ["## 4. Configuration key", "", "| config | what it changes |", "|---|---|"]
    lines += [f"| `{name}` | {note} |" for name, note in notes.items()]
    lines += ["", "*Generated by `python -m mra.benchmark`.*", ""]
    return "\n".join(lines)


def _ablation_a(results: dict[str, Any]) -> list[str]:
    lines = ["### A. Recovery loop ON vs OFF — the headline", "",
             "The only variable is whether the CORRECT loop may run. Both arms use the "
             "deterministic corrector, so this contrast is reproducible without an API "
             "key: the loop's *mechanics* are what is being measured, not the model's.",
             ""]
    for task in results["tasks"]:
        entries = _pick(results["aggregates"], ("baseline", "no-recovery"), task)
        if len(entries) == 2:
            lines += [f"**{task}**", ""] + _table(entries) + [""]
    return lines


def _ablation_b(results: dict[str, Any]) -> list[str]:
    lines = ["### B. Dependency-ordered batching vs arbitrary order", "",
             "`baseline`/`batch-1` use the FR-3 order; the `order-alphabetical` arms "
             "ignore the graph; the `order-fr3-violating` arms are `plan_batches` on the "
             "*reversed* graph — dependents before their dependencies, the inversion "
             "docs/04 §3.4's pseudocode produces if its missing `.reverse()` is taken "
             "literally. Recovery is on in every arm, so an order is charged for in "
             "corrective edits (`corr`) and steps before it is charged for in a failed "
             "run.", "",
             "Read the two groups separately. At batch 3 a Tier-A task is only one or "
             "two batches wide, so edit order and batch size are confounded — an order "
             "that happens to put a producer and its consumer in the same batch never "
             "exposes the intermediate state at all. The `-b1` group edits one file per "
             "batch, where sequence is the only variable left.", ""]
    groups = (
        ("batch size 3", ("baseline", "order-alphabetical", "order-fr3-violating")),
        ("batch size 1", ("batch-1", "order-alphabetical-b1", "order-fr3-violating-b1")),
    )
    for label, arms in groups:
        lines += [f"#### {label}", ""]
        for task in results["tasks"]:
            entries = _pick(results["aggregates"], arms, task)
            if len(entries) > 1:
                lines += [f"**{task}**", ""] + _table(entries) + [""]

    lines += ["#### What the data says", "",
              "Corrective edits per task, one file per batch (lower is better):", ""]
    dependency, alphabetical, violating = groups[1][1]
    for task in results["tasks"]:
        found = {e["config"]: e for e in _pick(results["aggregates"], groups[1][1], task)}
        if len(found) < 3:
            continue
        lines.append(
            f"- **{task}** — dependency order {found[dependency]['corrections_mean']:.0f}, "
            f"file-name order {found[alphabetical]['corrections_mean']:.0f}, "
            f"dependents-first {found[violating]['corrections_mean']:.0f}"
        )
    lines += [
        "",
        "Two findings, one of them not the expected one.",
        "",
        "1. **The dependents-first order is never cheaper and is sometimes the most "
        "expensive arm run** — on `task04_multimodule` it spends the full NFR-1 retry "
        "ceiling of 3 attempts where the dependency order spends 2, i.e. it finishes one "
        "attempt away from failing the task. That is what violating FR-3 costs here: not "
        "a wrong answer, a thinner margin.",
        "",
        "2. **File-name order is not a worse order on this corpus.** At batch 3 a "
        "Tier-A task is one or two batches wide, so alphabetical order degenerates into "
        "a near big-bang migration that never exposes an intermediate state and needs no "
        "recovery at all. That is a property of a six-file corpus, not evidence that the "
        "graph is unnecessary — but it is the honest reading of these numbers, and the "
        "textbook result (an arbitrary order causing a regression the dependency order "
        "avoids) is **not reproduced here**. Getting it would need a task whose break is "
        "a *signature* change rather than a semantic one, where editing a caller before "
        "its callee raises on import instead of producing a wrong value. Tier A has no "
        "such task yet; that is the gap to close before this ablation can carry the "
        "claim docs/05 §3 assigns it.",
        "",
    ]
    return lines


def _ablation_c(results: dict[str, Any]) -> list[str]:
    lines = ["### C. Edit model — V4-Pro vs V4-Flash", ""]
    entries = [a for a in results["aggregates"] if a["ablation"] == "C"]
    if not entries:
        skipped = {s["config"] for s in results["skipped"]}
        lines += [
            "**Requires a key — not run.** " + (", ".join(f"`{s}`" for s in sorted(skipped))
                                                or "No live configuration") +
            " needs `DEEPSEEK_API_KEY`; the offline matrix above is complete without it.",
            "",
            "Caveat for when it does run: `Router.TIER` bills an *edit* to the pro tier "
            "whatever `MRA_EDIT_MODEL` names, so the cost column for the V4-Flash arm "
            "is an upper bound, not a quote.", "",
        ]
        return lines
    for task in results["tasks"]:
        found = _pick(results["aggregates"], ("edit-v4-pro", "edit-v4-flash"), task)
        if found:
            lines += [f"**{task}**", ""] + _table(found) + [""]
    return lines


def _ablation_d(results: dict[str, Any]) -> list[str]:
    arms = ("batch-1", "baseline", "batch-5")
    lines = ["### D. Batch size 1 vs 3 vs 5", "",
             "Batch size caps how many files one EDIT touches before the suite runs "
             "again (NFR-5): smaller batches localize a failure more precisely and cost "
             "more TEST steps.", ""]
    for task in results["tasks"]:
        entries = _pick(results["aggregates"], arms, task)
        if len(entries) > 1:
            lines += [f"**{task}**", ""] + _table(entries) + [""]
    return lines


def _baseline_section(results: dict[str, Any]) -> list[str]:
    baselines = results.get("baselines") or []
    lines = ["## 3. Deterministic baselines — ruff (DTZ) and pyupgrade", "",
             "The honesty check (docs/05, RESOURCE_PACK §2.2): what do the existing "
             "static tools already do on these tasks?", "",
             "| task | tool | detected | \\|A\\| | detect recall | fixed | M1 recall "
             "after fix | suite after fix |", "|" + "---|" * 8]
    for entry in baselines:
        for tool in entry["tools"]:
            lines.append(
                f"| {entry['task_id']} | `{tool['tool']}` | {tool['detected']} "
                f"| {entry['ground_truth_sites']} | {tool['detect_recall']:.0f}% "
                f"| {tool['fixed_files']} | {tool['m1_recall_after_fix']:.0f}% "
                f"| {tool['suite_after_fix']} |"
            )
    lines += ["", "`detected` counts sites the tool reported; `fixed` counts files it "
              "rewrote. A tool that reports a site but cannot rewrite it scores 0 on M1 "
              "however good its detection is — and none of them can repair the cross-file "
              "break that task03/task04 are built around, because they never edit "
              "anything.", ""]
    return lines


# -- failure analysis ------------------------------------------------------


def _why(row: dict[str, Any], configs: dict[str, dict[str, Any]]) -> str:
    config = configs.get(row["config"], {})
    if not config.get("recovery", True):
        return ("recovery disabled (ablation A): the run gives up on the first red suite, "
                "so the remaining batches are never edited")
    cap = max(row["fix_attempts"].values(), default=0)
    if row["fix_attempts"]:
        return (f"the CORRECT loop spent its per-signature retry ceiling (NFR-1): "
                f"{cap} attempt(s) on this signature without reaching green")
    return "the suite was red and no failure had an attempt left to spend"


def failure_analysis(results: dict[str, Any]) -> str:
    """One entry per failing (config, task): class, signature, and why it stood."""
    configs = {c["name"]: c for c in results["configs"]}
    failing = [r for r in results["rows"]
               if r["outcome"] != "success" or r["m2_pass_rate"] < 100]
    lines = [
        "# Failure analysis", "",
        f"Generated {results['generated_at']}. Every run that gave up or finished with "
        f"M2 < 100 is listed with its failure class (docs/04 §2.5), its normalized "
        f"signature, and why the loop did not recover it.", "",
        f"{len(failing)} of {len(results['rows'])} runs failed.", "",
    ]
    if not failing:
        return "\n".join(lines + ["No run failed.", ""])

    seen: set[tuple[str, str, str]] = set()
    for row in failing:
        signatures = tuple(f["signature"] for f in row["failures"])
        key = (row["config"], row["task_id"], "|".join(signatures))
        if key in seen:  # repeats of the same deterministic outcome
            continue
        seen.add(key)
        repeats = sum(1 for r in failing if r["config"] == row["config"]
                      and r["task_id"] == row["task_id"])
        lines += [
            f"## `{row['config']}` on {row['task_id']}", "",
            f"- **outcome:** {row['outcome']} ({repeats}/{results['repeats']} repeats) — "
            f"{row['stopped_at_batch']}",
            f"- **M1 recall:** {row['m1_recall']:.0f}%   **M2:** "
            f"{row['m2_pass_rate']:.1f}% with {row['m2_regressions']} regression(s)",
            f"- **planned batches:** {row['batches']}",
            f"- **files actually migrated:** {row['changed_files'] or 'none'}",
            "- **surviving failures:**",
        ]
        for failure in row["failures"]:
            lines.append(
                f"  - `{failure['nodeid']}` — **{failure['failure_class']}** break, "
                f"`{failure['exc_type']}`\n"
                f"    - signature: `{failure['signature']}`\n"
                f"    - message: {failure['message']}"
            )
        lines += [f"- **why it was not recovered:** {_why(row, configs)}", ""]
    return "\n".join(lines)


# -- CLI -------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the P5 benchmark matrix.")
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    parser.add_argument("--repeats", type=int, default=DEFAULT_REPEATS)
    parser.add_argument("--tasks", nargs="*", default=list(TASKS))
    parser.add_argument("--configs", nargs="*", default=None,
                        help="config names to run (default: all)")
    args = parser.parse_args(argv)

    chosen = CONFIGS if args.configs is None else tuple(
        c for c in CONFIGS if c.name in set(args.configs))
    results = run_matrix(args.tasks, chosen, repeats=args.repeats,
                         corpus=args.corpus, out_dir=args.out_dir)
    failed = sum(1 for r in results["rows"] if r["outcome"] != "success")
    print(f"{len(results['rows'])} run(s), {failed} not green "
          f"({len(results['skipped'])} skipped without a key)")
    print(f"  -> {Path(args.out_dir) / 'results.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
