---
title: "Dependency-Ordered, Self-Correcting Codebase Migration: An Agent and a Controlled Benchmark"
author: "TODO — author list"
date: "TODO"
---

<!--
  P5 paper draft.

  PROVENANCE RULE: every number in this document must carry an HTML comment
  naming the file and the cell it came from. Nothing is typed from memory.
  A SOURCE comment covers every line above it, back to the previous SOURCE
  comment or the nearest heading — so a claim sentence and the table it
  introduces share one pointer. That rule is what makes the coverage check
  mechanical: no numeric line in §7 may sit in a span that ends without one.
  The two sources are:
    - runs/benchmark/results.md          (generated 2026-09-21T05:49:48Z)
    - runs/benchmark/RESULTS_SUMMARY.md  (same source results.json)
  Regenerate with `python -m mra.benchmark` and re-check §7 if either moves.

  STATUS: §3-§9 are written. Abstract, §1, §2, §10 are deliberate stubs —
  bullet outlines only, to be written by hand. Do not auto-fill them.
  §2 carries [CITE: ...] placeholders; fill from docs/02_LITERATURE_REVIEW.md
  only, and only after verifying each reference exists.
-->

# Abstract

> **STUB — outline only. Do not ghost-write.**

- One-sentence framing: codebase-wide API migration is a cross-file contract
  problem, not a find-and-replace problem.
- What we built: a 5-node LangGraph agent (MAP/PLAN/EDIT/TEST/CORRECT) that
  orders its edits by the import dependency graph and repairs its own
  regressions from test traces.
- What we evaluated: 5 controlled Tier-A tasks, 11 offline configurations,
  3 repeats, 165 deterministic runs.
- The three results, in one clause each: recovery loop is load-bearing;
  static tools detect everything and fix nothing; dependency ordering is a
  cost reduction in general and a correctness condition in one designed case.
- The honest limit: one migration family, one fixed codemod, no real-world
  repo yet.

---

# 1. Introduction

> **STUB — outline only. Do not ghost-write.**

- **The problem.** A version migration changes a *contract*, and every caller
  of that contract is a potential break. The unit of work is the dependency
  graph, not the file.
- **Why the obvious tools stop short.** Linters detect the pattern; they do
  not own the consequences of changing it. (Forward-reference the ruff row in
  §7.2 — it is the cleanest motivating number in the paper.)
- **Why an LLM alone stops short.** No verification loop, no ordering
  discipline, no bound on retries; the failure mode is a confident wrong
  patch with a red suite.
- **The gap we target.** An agent whose *loop* and *edit order* are explicit,
  inspectable artefacts rather than emergent behaviour.
- **Contributions**, as a numbered list:
  1. A 5-node state machine whose checkpoint history *is* its audit log.
  2. Dependency-ordered batching with atomic cycle collapse (FR-3).
  3. A signature-based retry cap that makes "gave up" a defined outcome.
  4. A 5-task controlled corpus with gold states and complete ground truth,
     including a fixture built specifically to make edit order decisive.
  5. A fully offline, deterministic ablation matrix — reproducible without
     an API key.
- **Roadmap paragraph** — one sentence per section.

---

# 2. Related Work

> **STUB — outline only. Do not ghost-write. Every citation below is a
> placeholder; fill only from `docs/02_LITERATURE_REVIEW.md` after verifying
> the reference exists. Do not invent.**

- **Automated program repair / test-driven repair.** Position our CORRECT
  node against classical APR: we repair *our own* regression against a known
  contract, not an arbitrary bug. [CITE: APR survey]
- **Agentic software engineering benchmarks.** SWE-bench and successors
  measure issue-resolution on real repos; we measure *migration completeness*
  on controlled repos where ground truth is total rather than proxied by a
  PR diff. Explain why that trade (external validity down, attributability
  up) is the right one for an ablation study. [CITE: SWE-bench]
  [CITE: SWE-agent or comparable agent scaffold]
- **LLM agent scaffolds and state machines.** Why an explicit graph rather
  than a free-running tool-use loop. [CITE: LangGraph / state-machine agent
  reference] [CITE: ReAct or equivalent tool-use loop]
- **Deterministic codemods and refactoring tools.** libcst, ruff, pyupgrade,
  2to3-lineage tooling: exact, cheap, and unable to cross a file boundary or
  repair a consequence. This is the row we beat in §7.2.
  [CITE: libcst] [CITE: ruff] [CITE: pyupgrade]
- **Dependency-aware change impact analysis.** Prior work on ordering edits
  by module dependency; what is new here is coupling the order to a
  *verification* loop and measuring the coupling. [CITE: change impact
  analysis]
- **Positioning paragraph.** One paragraph naming the gap the above leaves:
  no existing line of work reports an ablation that separates "the loop" from
  "the ordering" on a corpus where both are exercised.

---

# 3. System

The agent is a LangGraph 1.x `StateGraph` over a single typed `MigrationState`
object. Five nodes, one conditional router, and a SQLite checkpointer that is
not a debugging aid but the deliverable audit log.

<!-- SOURCE: docs/04_ARCHITECTURE_HLD_LLD.md §2 (LLD). No benchmark numbers in this section. -->

## 3.1 The state machine

```
[*] → MAP → PLAN → EDIT → TEST ─┬─ green ∧ batches remain ──→ EDIT (k+1)
                                 ├─ green ∧ all done ────────→ SUCCESS
                                 ├─ red ∧ attempts[sig] < N ─→ CORRECT → TEST
                                 └─ red ∧ attempts[sig] ≥ N ─→ GIVE_UP
```

The canonical rendering is the `stateDiagram-v2` figure in
`docs/04_ARCHITECTURE_HLD_LLD.md` §2.1; the HLD component diagram is §1.1 of
the same document. Both should be reproduced as figures in the typeset
version (Figure 1: components; Figure 2: state machine).

Each node is a pure `state → partial state update` function; side effects
(file writes, sandbox invocations) are explicit rather than incidental.

| Node | Reads | Writes | Side effects |
|---|---|---|---|
| **MAP** | `repo_path`, `contract` | `call_sites`, `dep_graph`, `file_status` | none — read-only analysis |
| **PLAN** | `dep_graph`, `call_sites` | `edit_batches`, `current_batch = 0` | none |
| **EDIT** | `edit_batches[k]`, contract, graph slice, rolling summary | edited files, `file_status`, `tokens` | file writes, `git` snapshot |
| **TEST** | `repo_path` | `last_test_report` | `pytest` + `ruff` in the sandbox |
| **CORRECT** | `last_test_report.failures[0]` | corrective edit, `fix_attempts[sig] += 1`, `tokens` | file writes |

<!-- SOURCE: docs/04 §2.2 node contract table, reproduced. -->

Two implementation defects in the design pseudocode were found during P4 and
are worth reporting rather than silently fixing, because both are the kind of
error the architecture invites:

1. The router in `docs/04` §2.3 increments `current_batch` inside
   `route_after_test`. A LangGraph router receives a read-only view of the
   state and returns only an edge name, so the write is discarded and the run
   re-edits batch 0 indefinitely. The counter is advanced by `edit_node` after
   it consumes its batch; the routing *decision* is unchanged.
2. The batching pseudocode in `docs/04` §3.4 topologically sorts the
   dependency graph directly. Edges run `importer → imported`, so the plain
   order yields importers first — the exact inverse of the intended rule.
   The sort must be taken over the reversed graph. This inversion is not
   merely corrected: it is preserved as an experimental arm
   (`order-fr3-violating`, §6) so its cost can be measured.

<!-- SOURCE: docs/04 §2.3 implementation note (P4). -->

## 3.2 Dependency-ordered batching

A migration changes a symbol's contract; every module that uses that symbol
may break. Editing in arbitrary order produces circular regressions — fixing
A breaks B, fixing B breaks A — and makes each intermediate TEST
uninterpretable. The planner therefore derives edit order from the import
graph.

The graph is built by parsing every module with `libcst`, resolving `Import`
and `ImportFrom` nodes to in-repo module paths (third-party imports are
ignored), and adding a directed edge `importer → imported` to a
`networkx.DiGraph` whose nodes are module files. Call sites of the migrated
symbol are recorded separately, scope- and alias-resolved; that set is what
M1 scores against and what EDIT targets.

Batching then follows three rules:

- **Condensation, then topological order.** `networkx.condensation` reduces
  the graph to a DAG over strongly connected components;
  `networkx.topological_sort` over the *reversed* graph orders those
  components leaf-most first, so no batch is edited on top of an unmigrated
  dependency. This is requirement **FR-3**.
- **Atomic cycles.** An import cycle is a strongly connected component with
  more than one member. No safe internal order exists, so the whole component
  is emitted as one batch and tested once. `task04` exists to exercise this.
- **Only files with call sites.** A module in the order that contains no site
  of the migrated symbol is dropped from the plan rather than edited as a
  no-op.

<!-- SOURCE: docs/04 §3.2-§3.4. -->

## 3.3 Codemod first, model second

Deterministic edits are implemented as `libcst` codemods, not model calls.
The T1 codemod rewrites `datetime.utcnow()` to `datetime.now(timezone.utc)`
under every binding form it can resolve — `from datetime import datetime`,
`import datetime`, and `import datetime as dt` — and adds
`from datetime import timezone` **only** for the from-import form, because
under a module import the timezone is already reachable through the existing
binding. Adding the import there would be an unnecessary edit, which is
precisely the precision failure `task02` was built to catch (§4).

This split is a correctness and a cost decision. A codemod is exact,
reproducible, and costs zero tokens against M3; the model is reserved for
genuinely ambiguous edits and for failure recovery. It is also the constraint
that shapes the corpus: because the agent runs one fixed codemod, a migration
that changes a *first-party* function's arity is not expressible in this
system, and the corpus reflects that (§4.3, §9).

<!-- SOURCE: src/mra/codemods/datetime_utcnow.py module docstring; CLAUDE.md golden rule 5. -->

## 3.4 The verifier and the sandbox

All execution happens inside a Docker `python:3.12-slim` sandbox with a
writable copy of the repository and no network at agent runtime. `pytest` is
run under `pytest-json-report` and `ruff` alongside it; their output is
normalized into a single `test_report` JSON contract rather than scraped from
free text. `git` inside the sandbox provides snapshot, rollback, and the final
unified `migration.patch`. A bad edit therefore cannot reach the host, and a
run is reproducible from its checkpoint database.

<!-- SOURCE: docs/04 §1.2 component table; docs/05 §4; CLAUDE.md golden rule 3. -->

## 3.5 Recovery and the signature-based retry cap

When TEST is red, CORRECT takes the first surviving failure and runs three
steps: **classify** the failure into the taxonomy
(`import` / `signature` / `behaviour` / `assertion`), **locate** the broken
contract by mapping the traceback's `file:line` back to a call site or a
dependency edge, and **patch** that one file. The located file is filtered so
a test file is never edited (boundary **NB-4**) — the suite is the oracle and
editing it is a hard failure.

The retry cap is keyed on a *normalized failure signature*, not on a global
counter. `fix_attempts[sig]` increments per signature, and the run gives up
when any signature reaches `MAX_FIX_ATTEMPTS = 3`. Keying on the signature is
what makes "gave up" a defined outcome rather than a timeout: the agent stops
when it has demonstrably failed to move the *same* failure three times, while
a run that keeps uncovering new failures keeps working. Setting the cap to
zero disables recovery entirely, which is how ablation A is run without adding
a dead branch to the production path (§6).

<!-- SOURCE: docs/04 §2.3 route_after_test, §2.5 recovery internals; src/mra/benchmark/runner.py module docstring. -->

---

# 4. Corpus & Ground Truth

## 4.1 Construction

Tier A is five controlled Python packages authored for this study. Each task
is a directory holding `old/` (a tree whose suite **passes** on the old API),
`gold/` (a hand-verified migrated tree whose suite passes on the new API),
`ground_truth.json`, and `task.yaml`. The agent always operates on a fresh
copy of `old/`; `gold/` is the scoring reference and is pinned by commit
hash in `ground_truth.json` so the state is reproducible.

Four authoring rules are non-negotiable:

1. `old/` must be green, or M2 is undefined.
2. `ground_truth.json` lists **every** site that must change — it is M1's
   denominator, not a sample.
3. Every task must contain cross-file breakage: a contract change in one file
   that breaks a caller in another. Without it the dependency graph is never
   exercised.
4. Tasks vary **one factor at a time**, so a difference in results is
   attributable to that factor.

`gold/` additionally carries assertions the shared suite does not, so a
migration that leaves any single module behind fails the gold check even when
the shared suite is green. These are the `semantic_checks` in
`ground_truth.json`.

<!-- SOURCE: docs/05_DATA_EVALUATION_PROTOCOL.md §1.1 authoring rules; corpus/tierA/*/ground_truth.json. -->

## 4.2 The five tasks

All five migrate the same contract, **T1**: `datetime.utcnow()` →
`datetime.now(timezone.utc)`. Holding the contract fixed is what makes the
factor that varies attributable.

| Task | \|A\| | Files | Tests | Difficulty | The one factor it varies |
|---|---|---|---|---|---|
| `task01_datetime` | 1 | 1 | 5 | easy | Baseline. From-import style, single site. The control. |
| `task02_datetime_aliased` | 2 | 2 | 5 | easy | **Alias resolution.** `import datetime` and `import datetime as dt`. Its `expected_import_changes` name both files with an empty `add` list — adding `from datetime import timezone` here is an unnecessary edit, so the task scores *precision*, not just recall. |
| `task03_half_migration` | 3 | 3 | 7 | medium | **Recovery.** The tree starts partially migrated; one module subtracts its own clock reading from another module's, so the mixed state is already broken. Asks whether the agent can finish from the failure alone. |
| `task04_multimodule` | 6 | 6 | 11 | hard | **Scale and cycles.** Seven modules with a genuine import cycle that must be migrated atomically, and a break that only surfaces after an earlier batch lands. Exercises condensation and batch planning. |
| `task05_signature_break` | 6 | 6 | 14 | hard | **Edit order.** An asymmetric break: migrating the contract owner first is always safe, migrating any caller first raises at import time. The only task on which order changes the verdict. |

<!-- SOURCE: |A| and file counts from corpus/tierA/*/ground_truth.json (call_sites length, distinct file count).
     Test counts from runs/benchmark/results.md §3 "suite after fix" column: 5/5, 5/5, 7/7, 11/11, 14/14.
     Difficulty from each ground_truth.json "difficulty" field.
     Factor descriptions from each corpus/tierA/*/README.md. -->

`task02`'s empty-`add` `expected_import_changes` deserve emphasis because they
are the corpus's only precision trap. A matcher tuned to `task01` looks for
`Attribute(value=Name("datetime"), attr=Name("utcnow"))`; in `task02` the
receiver is itself an `Attribute`, so that matcher — and a
`datetime\.utcnow\(` regex — finds **zero** of the two sites. Correct
enumeration requires reading the import statements first and resolving `dt`
back to the `datetime` module.

<!-- SOURCE: corpus/tierA/task02_datetime_aliased/README.md. -->

## 4.3 `task05` and one honest limitation

`task01`–`task04` cannot separate the batching orders. Their breaks are
symmetric: every order opens some window, and the recovery loop closes all of
them, so ablation B had nothing to measure. `task05` was authored to close
that gap.

Its contract owner, `pkg.timebase`, normalizes every stamp it is handed
through a deliberately one-way shim. A *naive* stamp from a module that has
not migrated yet is read as UTC, because the old contract promised it was
UTC. An *aware* stamp handed to a still-naive clock is **not** downgraded,
because stripping a `tzinfo` silently reinterprets the value;
`elapsed_since` checks the mismatch before doing any arithmetic and raises a
named `TypeError` describing the ordering violation. `pkg.boot` performs that
handback at **module scope**, so a caller migrated ahead of the contract owner
raises during *import* and pytest reports collection errors rather than test
failures.

**The limitation, stated plainly.** The task name promises a signature break,
and what it delivers is a *contract* break. The signature that moves is the
tz-awareness of `timebase.utc_now()`'s return value, enforced at the package
boundary — not a first-party arity change with a parameter threaded through
call sites. An arity change is **not expressible in this system**: the agent
runs one fixed codemod (§3.3) that only rewrites `datetime.utcnow()` calls,
so a gold state requiring new arguments at call sites would be unreachable by
construction. The property the fixture was built for — a caller edited before
its callee fails hard, at import/collection time — is fully realized; the
mechanism is a guard rather than an arity mismatch. Consequently the offline
classifier files the resulting failure as `behaviour`, not `signature`, since
it reserves `signature` for argument-shaped messages (§8).

<!-- SOURCE: corpus/tierA/task05_signature_break/README.md; runs/benchmark/RESULTS_SUMMARY.md "Scope and honesty notes". -->

---

# 5. Metrics

Three metrics, defined in `docs/05_DATA_EVALUATION_PROTOCOL.md` §2. For a
task, let $A$ be the set of affected call sites listed in
`ground_truth.json`, $X$ the set of sites the agent actually modified,
$\mathrm{TP}$ the sites in $A$ that the agent modified *and* matched gold
semantics, $T$ the total number of tests, and $T_{\text{post}}$ the number
passing after migration.

## 5.1 M1 — Migration Completeness

$$
M_1^{\text{recall}} = \frac{\mathrm{TP}}{|A|}\times 100
\qquad
M_1^{\text{precision}} = \frac{\mathrm{TP}}{|X|}\times 100
\qquad
M_1^{F_1} = \frac{2\,M_1^{\text{recall}}M_1^{\text{precision}}}{M_1^{\text{recall}} + M_1^{\text{precision}}}
$$

**Why both halves are reported.** Recall alone is trivially gamed by editing
everything; precision alone is trivially gamed by editing one site correctly
and stopping. The corpus contains a live instance of the precision half:
`task02`'s `expected_import_changes` require no import to be added, so an agent that helpfully
adds `from datetime import timezone` under a module-import binding is
*correct-looking and wrong*, and only precision records it.

The clearest argument for reporting M1 at all is the baseline row in §7.2:
`ruff` detects 100 % of the ground-truth sites on all five tasks and rewrites
none of them, so its M1 recall after `--fix` is 0 % while M2 remains 100 %.
A migration that never happened is indistinguishable from a successful one if
M2 is the only metric on the page.

<!-- SOURCE: docs/05 §2.1 formulas; §7.2 of this paper for the ruff figures. -->

## 5.2 M2 — Post-Migration Test Pass Rate

$$
M_2 = \frac{T_{\text{post}}}{T}\times 100
\qquad
R = T_{\text{pre}} - T_{\text{post}}
$$

with the precondition $T_{\text{pre}} = T$ (the suite is green before
migration — authoring rule 1). $M_2 = 100\,\%$ with $R = 0$ is a fully
successful migration. $R$ is reported separately because on suites of 5–14
tests a raw regression count is more informative than a percentage — and
because a collection error, which takes out whole test modules at once,
shows up in $R$ far more legibly than in $M_2$.

<!-- SOURCE: docs/05 §2.2. -->

## 5.3 M3 — Token / Step Overhead

$$
\text{Tokens} = \sum_m (t^{\text{in}}_m + t^{\text{out}}_m)
\qquad
\text{Steps} = (\text{LLM calls}) + (\text{tool calls})
\qquad
\text{Cost} = \sum_m (t^{\text{in}}_m p^{\text{in}}_m + t^{\text{out}}_m p^{\text{out}}_m)
$$

normalized per call site as $\text{Tokens}/|A|$ and $\text{Steps}/|A|$ for
cross-task comparison. In the offline matrix that carries this paper's
results, the corrector is a codemod rather than a model, so tokens and cost
are identically zero and **Steps is the meaningful M3 column** (§7.1).

<!-- SOURCE: docs/05 §2.3 formulas. Zero-token claim: runs/benchmark/results.md §1, "tokens" and "cost $" columns are 0 / 0.0000 in all 55 rows. -->

We additionally report **corrective edits** (`corr`) — one CORRECT visit per
retry attempt — because it is where the cost of a bad edit order is paid long
before it is paid in a failed run.

---

# 6. Experimental Setup

**Configurations.** Each row of the matrix is one `Config` that changes
exactly one thing about a named `baseline` (recovery on, dependency-ordered
batches of 3, deterministic corrector). Eleven configurations run offline;
two more (ablation C) require an API key.

| Ablation | Arms | Question |
|---|---|---|
| **A** | `baseline`, `no-recovery` | How much does self-correction contribute? |
| **B** | `order-alphabetical`, `order-fr3-violating` (batch 3); the same two plus `batch-1` at batch size 1; and all three again with the loop off (`*-b1-norecovery`) | Does principled edit order prevent regressions? |
| **C** | `edit-v4-pro`, `edit-v4-flash` | Capability vs. cost on the live model path. **Not run** — requires `DEEPSEEK_API_KEY`. |
| **D** | `batch-1`, `baseline`, `batch-5` | Effect of batch size on localization and overhead. |

<!-- SOURCE: src/mra/benchmark/runner.py CONFIGS tuple; runs/benchmark/results.md §4 "Configuration key". -->

**Why ablation B has three groups.** At batch size 3 a Tier-A task is only
one or two batches wide, so edit order and batch size are confounded: an
order that happens to put a producer and its consumer in the same batch never
exposes an intermediate state at all. The `-b1` group edits one file per
batch, where sequence is the only remaining variable. The `-norecovery` group
then removes the loop, which is the only condition under which an order's
cost can appear as an *outcome* rather than as corrective edits.

**How recovery is switched off.** `MRA_MAX_FIX_ATTEMPTS=0` means no failure
ever has an attempt left, so the router takes `give_up` on the first red
suite. No flag is added to the agent and no dead branch enters the production
path. `MAX_FIX_ATTEMPTS = 3` in every other arm.

**The offline corrector.** The CORRECT node is run with the model replaced by
the codemod. It localizes through the same `locate` the LLM corrector uses —
same trace parsing, same dependency slice, same NB-4 test-file filter — and
then applies the deterministic transform instead of requesting a file from
V4-Pro. The loop *mechanics* under test are therefore identical; only the
patch generator is reproducible. This is what makes ablation A demonstrable
without an API key.

**Repeats and determinism.** Every (task, configuration) pair is run
`repeats = 3` times and the tables report mean ± spread (max − min). Because
the offline path contains no model call, **the spread is zero on every metric
except wall clock**, which is the point of having a deterministic arm: it is
reproducible byte-for-byte. The live arms (ablation C) are the ones the repeat
count exists for; they are marked *requires key* and are absent from
`results.json.rows` rather than estimated.

**Isolation.** Each run executes in the Docker sandbox against a fresh
writable copy of `old/`, with no network. Test files are never editable
(NB-4), and the suite asserts that the corpus tree digest is unchanged after
the entire benchmark — including the deliberately bad orders.

**Totals.** 5 tasks × 11 offline configurations × 3 repeats = **165 runs**,
with 10 (task, config) pairs skipped for want of a key.

<!-- SOURCE: runs/benchmark/results.md header line ("3 repeat(s) per (task, config)");
     runs/benchmark/RESULTS_SUMMARY.md opening paragraph ("5 tasks × 11 offline configurations × 3 repeats = 165 runs");
     results.json "skipped" = 10 entries across edit-v4-pro / edit-v4-flash;
     src/mra/benchmark/runner.py module docstring for the MRA_MAX_FIX_ATTEMPTS=0 mechanism. -->

---

# 7. Results

All figures in this section are drawn from `runs/benchmark/results.md` and
`runs/benchmark/RESULTS_SUMMARY.md`, both generated from `results.json` at
**2026-09-21T05:49:48Z**. Each claim carries an HTML comment naming its
source table.

<!-- SOURCE: runs/benchmark/results.md line 3, "Generated 2026-09-21T05:49:48.150512+00:00 · 3 repeat(s) per (task, config)". -->

Three columns are constant across all 55 offline rows and are stated once
rather than repeated: **M1 precision = 100.0**, **tokens = 0**, **cost =
$0.0000**. Nothing was over-edited in any configuration, and the offline path
makes no model call.

<!-- SOURCE: runs/benchmark/results.md §1 — the "M1 prec", "tokens" and "cost $" columns read 100.0 / 0 / 0.0000 in every one of the 55 rows. -->

## 7.1 The consolidated matrix

Every (task, configuration) pair, mean ± spread over 3 repeats. Reproduced
verbatim from `runs/benchmark/results.md` §1.

<!-- SOURCE: runs/benchmark/results.md §1 "The whole offline matrix", all 55 rows, transcribed without modification. -->

| task / config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `task01_datetime / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.14 |
| `task01_datetime / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.05 |
| `task01_datetime / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.74 ±0.05 |
| `task01_datetime / no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.74 ±0.09 |
| `task01_datetime / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.06 |
| `task01_datetime / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.05 |
| `task01_datetime / order-alphabetical-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.03 |
| `task01_datetime / order-dependency-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.05 |
| `task01_datetime / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.06 |
| `task01_datetime / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.11 |
| `task01_datetime / order-fr3-violating-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.76 ±0.02 |
| `task02_datetime_aliased / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.53 ±0.09 |
| `task02_datetime_aliased / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.09 |
| `task02_datetime_aliased / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.38 ±0.10 |
| `task02_datetime_aliased / no-recovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.09 |
| `task02_datetime_aliased / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.03 |
| `task02_datetime_aliased / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.46 ±0.25 |
| `task02_datetime_aliased / order-alphabetical-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.71 ±0.08 |
| `task02_datetime_aliased / order-dependency-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.69 ±0.02 |
| `task02_datetime_aliased / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.12 |
| `task02_datetime_aliased / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.48 ±0.25 |
| `task02_datetime_aliased / order-fr3-violating-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.69 ±0.02 |
| `task03_half_migration / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.70 ±0.13 |
| `task03_half_migration / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.54 ±0.12 |
| `task03_half_migration / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.72 ±0.33 |
| `task03_half_migration / no-recovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 1.81 ±0.01 |
| `task03_half_migration / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.04 |
| `task03_half_migration / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.49 ±0.07 |
| `task03_half_migration / order-alphabetical-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 85.7 | 1 | 0 | 7 | 0 | 0.0000 | 2.71 ±0.09 |
| `task03_half_migration / order-dependency-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 1.85 ±0.07 |
| `task03_half_migration / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.63 ±0.25 |
| `task03_half_migration / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.44 ±0.08 |
| `task03_half_migration / order-fr3-violating-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 85.7 | 1 | 0 | 7 | 0 | 0.0000 | 2.66 ±0.04 |
| `task04_multimodule / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.06 ±0.08 |
| `task04_multimodule / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 7.92 ±0.09 |
| `task04_multimodule / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.42 ±0.27 |
| `task04_multimodule / no-recovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 3.97 ±0.17 |
| `task04_multimodule / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 7 | 0 | 0.0000 | 3.21 ±0.08 |
| `task04_multimodule / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 7.74 ±0.22 |
| `task04_multimodule / order-alphabetical-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 11 | 0 | 0.0000 | 4.73 ±0.24 |
| `task04_multimodule / order-dependency-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 3.92 ±0.08 |
| `task04_multimodule / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 9.16 ±0.18 |
| `task04_multimodule / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 9.14 ±0.04 |
| `task04_multimodule / order-fr3-violating-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 72.7 | 3 | 0 | 7 | 0 | 0.0000 | 2.97 ±0.10 |
| `task05_signature_break / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.81 ±0.24 |
| `task05_signature_break / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.26 ±0.09 |
| `task05_signature_break / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.93 ±0.27 |
| `task05_signature_break / no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.72 ±0.08 |
| `task05_signature_break / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 4.53 ±0.15 |
| `task05_signature_break / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 19 | 0 | 0.0000 | 9.07 ±0.04 |
| `task05_signature_break / order-alphabetical-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 0.0 | 14 | 0 | 7 | 0 | 0.0000 | 3.12 ±0.06 |
| `task05_signature_break / order-dependency-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.25 ±0.02 |
| `task05_signature_break / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 13 | 0 | 0.0000 | 5.91 ±0.06 |
| `task05_signature_break / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 7.43 ±0.07 |
| `task05_signature_break / order-fr3-violating-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 78.6 | 3 | 0 | 9 | 0 | 0.0000 | 3.72 ±0.03 |

Spread is `0` on every metric except wall clock in all 55 rows, as expected of
a path with no model call.

<!-- SOURCE: runs/benchmark/results.md §1 — the only cells carrying a "±" are in the "wall s" column. -->

## 7.2 Claim (a) — the recovery loop is what finishes a cross-file migration

**With the CORRECT loop disabled, 3 of the 5 tasks end in `gave_up` with a
regression the agent cannot repair; with it enabled all 5 finish at M1 100 % /
M2 100 % / 0 regressions — and the two tasks that do not move are the two
where nothing ever breaks, which is what makes them controls rather than
counter-evidence.**

| task | loop on (`baseline`) | loop off (`no-recovery`) |
|---|---|---|
| `task01_datetime` *(control: single file)* | success, M1 100, 0 regr | success, M1 100, 0 regr |
| `task02_datetime_aliased` | success, M1 100, M2 100, 1 corr | **gave_up, M1 50, M2 80.0, 1 regr** |
| `task03_half_migration` | success, M1 100, M2 100, 1 corr | **gave_up, M1 33, M2 85.7, 1 regr** |
| `task04_multimodule` | success, M1 100, M2 100, 2 corr | **gave_up, M1 67, M2 72.7, 3 regr** |
| `task05_signature_break` *(control: dependency order opens no window)* | success, M1 100, 0 corr | success, M1 100, 0 regr |

<!-- SOURCE: runs/benchmark/results.md §2A "Recovery loop ON vs OFF"; equivalently §1 rows
     `<task> / baseline` and `<task> / no-recovery`. Cross-checked against
     runs/benchmark/RESULTS_SUMMARY.md claim (a) table. -->

The `task05` row is the control the corpus previously lacked. It is a *hard*
task that the loop does not rescue, because in dependency order there is
nothing to rescue — so ablation A's effect tracks "is there a break?", not
"is the task big?". Without it, the correlation between task difficulty and
loop dependence would be uncontrolled.

## 7.3 Claim (b) — the existing static tools detect the work and do none of it

**`ruff` (DTZ) reports 100 % of the ground-truth call sites on all five tasks
and rewrites zero of them, so its M1 recall after running with `--fix` is 0 %
on every task — and because it changes nothing, the suite stays green, which
is exactly why M2 alone cannot tell you a migration did not happen.**

| task | \|A\| | ruff detected | ruff fixed | M1 after fix | suite after fix | pyupgrade detected |
|---|---|---|---|---|---|---|
| `task01_datetime` | 1 | 1 (100 %) | 0 | 0 % | 5/5 passed | 0 (0 %) |
| `task02_datetime_aliased` | 2 | 2 (100 %) | 0 | 0 % | 5/5 passed | 0 (0 %) |
| `task03_half_migration` | 3 | 3 (100 %) | 0 | 0 % | 7/7 passed | 0 (0 %) |
| `task04_multimodule` | 6 | 6 (100 %) | 0 | 0 % | 11/11 passed | 0 (0 %) |
| `task05_signature_break` | 6 | 7 (100 % recall, 86 % precision) | 0 | 0 % | 14/14 passed | 0 (0 %) |

<!-- SOURCE: runs/benchmark/results.md §3 "Deterministic baselines — ruff (DTZ) and pyupgrade",
     columns: detected / |A| / detect recall / fixed / M1 recall after fix / suite after fix.
     Cross-checked against runs/benchmark/RESULTS_SUMMARY.md claim (b) table. -->

Two details are reported rather than smoothed over. `ruff`'s seventh hit on
`task05` is a genuine `DTZ001` on the naive datetime constant in
`tests/test_timebase.py` — a false positive against $A$, and the only place
in the corpus where detection precision falls below 100 %. `pyupgrade`
detects nothing at all: this migration is not in its rule set, so its row is
a floor, not a failure.

<!-- SOURCE: results.json baselines[task05_signature_break].tools["ruff (DTZ)"]:
     detected 7 against ground_truth_sites 6, detect_recall 100.0, detect_precision 85.714… (→ 86 %).
     The seventh hit is DTZ001 at corpus/tierA/task05_signature_break/old/tests/test_timebase.py:12,
     `NAIVE = datetime(2024, 1, 1, 12, 0, 0)` — reproduce with
     `ruff check --select DTZ corpus/tierA/task05_signature_break/old`.
     Every other task's detect_precision is 100.0 in the same structure.
     pyupgrade: detected 0 / detect_recall 0.0 on all five tasks. -->

Neither tool can repair a cross-file break, because neither edits across
files at all: on `task03`, `task04` and `task05` the regression the agent
recovers from does not exist for them, since they never create it. That is
the asymmetry the comparison is meant to expose — a tool that does no work
cannot regress, and a metric that only measures regressions will reward it.

## 7.4 Claim (c) — dependency ordering: a cost reduction, and in one case a correctness condition

The ordering result splits in two, and both halves are reported.

**(c-i) Regression avoidance — with the loop off, and only on `task05`.**
With the CORRECT loop disabled and one file per batch, dependency order
completes `task05_signature_break` green while both arbitrary orders give up
with a red suite; on the other four tasks all three orders break, so this
half of the claim rests on `task05` alone.

| task | dependency | file-name | dependents-first |
|---|---|---|---|
| `task01_datetime` | 3× success, 0 regr | 3× success, 0 regr | 3× success, 0 regr |
| `task02_datetime_aliased` | 3× gave_up, M1 50 | 3× gave_up, M1 50 | 3× gave_up, M1 50 |
| `task03_half_migration` | 3× gave_up, M1 33 | 3× gave_up, M1 67 | 3× gave_up, M1 67 |
| `task04_multimodule` | 3× gave_up, M1 67 | 3× gave_up, M1 67 | 3× gave_up, M1 33 |
| **`task05_signature_break`** | **3× success, M1 100, M2 100, 0 regr** | **3× gave_up, M1 33, M2 0.0, 14 regr** | **3× gave_up, M1 50, M2 78.6, 3 regr** |

<!-- SOURCE: runs/benchmark/results.md §2B, group "batch size 1, recovery OFF" — arms
     order-dependency-b1-norecovery / order-alphabetical-b1-norecovery / order-fr3-violating-b1-norecovery.
     Equivalently §1 rows with those config names. Cross-checked against
     runs/benchmark/RESULTS_SUMMARY.md claim (c) claim-1 table. -->

The two arbitrary orders on `task05` break *differently*, and that difference
is the finding, and the planned batch lists explain it exactly.

File-name order plans
`[api] [boot] [handler] [ledger] [metrics] [timebase]` and so reaches
`src/pkg/boot.py` at batch 2 — four batches ahead of the contract owner
`src/pkg/timebase.py` at batch 6. `boot.py` performs its clock handback at
**module scope**, so the `TypeError` is raised during *import*: the run gives
up after batch 2, three test modules never load, and the failing node IDs are
whole files with no `::test_` component — M2 0.0 % with 14 regressions, the
entire suite.

Dependents-first order plans
`[api] [handler] [metrics] [boot] [ledger] [timebase]` and never reaches
`boot.py` at all: it gives up after batch 3 of 6, with `api`, `handler` and
`metrics` migrated ahead of `timebase`. The same guard therefore trips at
*call* time rather than import time, inside three tests in
`tests/test_api.py` and `tests/test_metrics.py` — M2 78.6 % with 3
regressions. Dependency order reaches neither window: 3× success, 0
regressions, 0 corrective edits.

The two arbitrary orders are thus not two degrees of the same break but two
different ones, and only the earlier of the two takes out the suite wholesale.

<!-- SOURCE: runs/benchmark/failure-analysis.md, entries
     "`order-alphabetical-b1-norecovery` on task05_signature_break" — planned batches
     [[api],[boot],[handler],[ledger],[metrics],[timebase]], "gave_up after batch 2/6", M2 0.0%, 14 regressions,
     3 surviving failures whose nodeids are tests/test_api.py, tests/test_boot.py, tests/test_handler.py (no "::")
     — and "`order-fr3-violating-b1-norecovery` on task05_signature_break" — planned batches
     [[api],[handler],[metrics],[boot],[ledger],[timebase]], "gave_up after batch 3/6",
     files actually migrated [api, handler, metrics], M2 78.6%, 3 regressions whose nodeids are
     tests/test_api.py::test_serve_returns_the_whole_response and two in tests/test_metrics.py (all carry "::"). -->

**(c-ii) Corrective-edit cost — with the loop on, and not uniform.**
Dependency order is never the most expensive arm and dependents-first order is
never the cheapest, but the ranking does not hold task-by-task, so this is a
weaker claim than (c-i).

Mean corrective edits, one file per batch, recovery on (lower is better):

| task | dependency (`batch-1`) | file-name (`-b1`) | dependents-first (`-b1`) |
|---|---|---|---|
| `task01_datetime` | 0 | 0 | 0 |
| `task02_datetime_aliased` | 1 | 1 | 1 |
| `task03_half_migration` | 1 | 1 | 1 |
| `task04_multimodule` | 2 | **1** | **3** |
| `task05_signature_break` | **0** | **2** | 1 |

<!-- SOURCE: runs/benchmark/results.md §2B, group "batch size 1, recovery on" — the "corr" column of arms
     batch-1 / order-alphabetical-b1 / order-fr3-violating-b1; also summarized in that section's
     "What the data says" bullet list. Cross-checked against runs/benchmark/RESULTS_SUMMARY.md claim (c) claim-2 table. -->

The `task04` row is reported as found: file-name order costs one edit *fewer*
than dependency order there. That is luck about which files that particular
alphabet happens to group, not evidence against FR-3 — and the same order
costs 2 where dependency order costs 0 on `task05`. Both dependents-first arms
on `task04` — batch 3 and batch 1 — spend the full retry ceiling of 3 attempts
on a *single* failure signature, i.e. they finish one attempt away from failing
the task outright; dependency order spends 2 on the same task.

<!-- SOURCE: runs/benchmark/results.md §2B "What the data says", finding 2, for the ranking.
     The "single signature" detail from results.json rows order-fr3-violating / task04_multimodule
     and order-fr3-violating-b1 / task04_multimodule: fix_attempts == {"2773f89c64a8ae65": 3} in all
     3 repeats of each, against {"…": 2} for baseline / task04_multimodule. -->

**(c-iii) What is *not* shown.** With the loop on, every order completes every
Tier-A task at M1 100 / M2 100, `task05` included. On this corpus, edit order
is a cost and a risk — never a verdict — once recovery is available. Any
quotation of (c-i) must carry this alongside it.

<!-- SOURCE: runs/benchmark/results.md §1 — every row whose config does not end in "-norecovery"
     reads "3× success" at M1 100.0 / M2 100.0 / 0 regr. Cross-checked against
     runs/benchmark/RESULTS_SUMMARY.md claim (c) claim-3. -->

## 7.5 Ablation D — batch size

Batch size caps how many files one EDIT touches before the suite runs again:
smaller batches localize a failure more precisely and cost more TEST steps.
On this corpus the effect on *outcome* is nil and the effect on *cost* is
small and confined to two tasks.

| task | steps @ batch 1 | steps @ batch 3 | steps @ batch 5 | corrective edits (all three) |
|---|---|---|---|---|
| `task01_datetime` | 5 | 5 | 5 | 0 |
| `task02_datetime_aliased` | 9 | 9 | 9 | 1 |
| `task03_half_migration` | **11** | 9 | 9 | 1 |
| `task04_multimodule` | 17 | 17 | 17 | 2 |
| `task05_signature_break` | **15** | 11 | 11 | 0 |

<!-- SOURCE: runs/benchmark/results.md §2D "Batch size 1 vs 3 vs 5", the "steps" and "corr" columns
     of arms batch-1 / baseline / batch-5 for each task. Identical values appear in §1 rows
     `<task> / batch-1`, `<task> / baseline`, `<task> / batch-5`. -->

All fifteen (task, batch size) cells reach M1 100 / M2 100 with 0 regressions
and the same corrective-edit count, so batch size never changes the verdict
here. Steps are identical at batch 3 and batch 5 on every task, because at
those sizes a Tier-A task is already only one or two batches wide — the cap
stops binding. Batch 1 costs extra steps only where it actually splits work
the larger batches fused: `task03` (11 vs 9) and `task05` (15 vs 11).
`task04` is flat at 17 across all three, because its import cycle is collapsed
into one atomic batch regardless of the cap (§3.2), so the batch count does
not move with the size.

The ablation's stated question — does a smaller batch localize failures
better? — is therefore not answered by this corpus: with the recovery loop
enabled no failure survives to be localized, and the arms differ only in step
count. A corpus with more files per contract unit would be needed to separate
them.

<!-- SOURCE: runs/benchmark/results.md §2D — every row across all five tasks reads
     "3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0" for outcome / M1 recall / prec / F1 / M2 / regr. -->

## 7.6 Ablation C — live models

Not run. `edit-v4-pro` and `edit-v4-flash` require `DEEPSEEK_API_KEY`; both
read *requires key* in `results.md` §2C and are absent from
`results.json.rows` rather than estimated. 10 (task, config) pairs are
recorded as skipped. The offline matrix is complete without them.

One caveat is recorded for when they do run: the router bills an *edit* to the
pro tier whatever `MRA_EDIT_MODEL` names, so the cost column for the V4-Flash
arm will be an upper bound, not a quote.

<!-- SOURCE: runs/benchmark/results.md §2C "Edit model — V4-Pro vs V4-Flash" (the "Requires a key — not run"
     block and its billing caveat); results.json "skipped" list = 10 entries. -->

---

# 8. Failure Analysis

Of 165 runs, **42 did not reach green**, collapsing to **14 distinct
(configuration, task) pairs** once the three identical repeats of each
deterministic outcome are folded together.

<!-- SOURCE: runs/benchmark/failure-analysis.md header, "42 of 165 runs failed";
     the file lists 14 "## `<config>` on <task>" entries. -->

**Every failing pair has the recovery loop disabled.** All 14 come from four
configuration families — `no-recovery` and the three `*-b1-norecovery` arms —
and no configuration with the loop enabled appears anywhere in the failure
analysis. That is the same result as claim (a), read from the other end.

<!-- SOURCE: runs/benchmark/failure-analysis.md — the 14 entry headings name only the configs
     no-recovery, order-dependency-b1-norecovery, order-alphabetical-b1-norecovery,
     order-fr3-violating-b1-norecovery. -->

**By failure class, the distribution is degenerate: all 26 surviving failures
across the 14 pairs classify as `behaviour`, and all 26 carry `TypeError`.**
This is a property of the corpus rather than of the classifier. Every task
migrates the same contract, and a half-migrated tz-awareness contract always
surfaces as a `TypeError` — either from a datetime operation or, in `task05`,
from the explicit contract guard. The taxonomy's other three classes
(`import`, `signature`, `assertion`) are unexercised, and a corpus that
exercises them is future work (§9).

<!-- SOURCE: runs/benchmark/failure-analysis.md — every "surviving failures" bullet across all 14
     entries reads "**behaviour** break, `TypeError`". Count of 26 obtained by summing the
     surviving-failure bullets over the 14 entries (1+1+3+1+1+3+1+1+3+3+1+1+3+3). -->

**By why recovery did not happen**, all 14 pairs carry the same reason:
*"recovery disabled: the run gives up on the first red suite, so the remaining
batches are never edited."* **No run anywhere in the matrix gave up by
exhausting the retry cap.** The highest `fix_attempts` counter observed is
exactly `MAX_FIX_ATTEMPTS = 3`, reached on one signature
(`2773f89c64a8ae65`) by both dependents-first arms on `task04_multimodule` —
and both finish **green**, because the third corrective edit turns the suite
green before the router is asked to take `give_up` (§7.4). Every failure in
this section is a *disabled* loop, never an exhausted one, so this matrix says
nothing about whether 3 is the right ceiling.

<!-- SOURCE: runs/benchmark/failure-analysis.md — the "why it was not recovered" line of all 14 entries
     reads "recovery disabled (ablation A|B)". Cap figures from results.json: max over all 165 rows of
     max(fix_attempts.values()) == 3, attained only by order-fr3-violating / task04_multimodule and
     order-fr3-violating-b1 / task04_multimodule (outcome "success" in all 6 rows); no row with
     outcome "gave_up" has any fix_attempts entry >= 3. -->

**The two shapes of break.** The 14 pairs divide into two failure geometries
that the node IDs distinguish without ambiguity:

- **Call-time failures (13 pairs).** The failing node IDs carry a
  `::test_name` component: the module imported, the test ran, the contract
  broke inside it. M2 degrades proportionally — 80.0 %, 85.7 %, 72.7 %,
  78.6 % depending on how much of the suite touches the half-migrated path.
- **Import-time failures (1 pair).** `order-alphabetical-b1-norecovery` on
  `task05_signature_break`: all three failing node IDs are whole test modules
  with no `::`, because `pkg.boot` raises while being imported. M2 collapses
  to 0.0 % with 14 regressions — the entire suite, not a subset.

<!-- SOURCE: runs/benchmark/failure-analysis.md — nodeid fields of every entry; the single entry whose
     nodeids lack "::" is "`order-alphabetical-b1-norecovery` on task05_signature_break" (M2 0.0%, 14 regr).
     M2 values from the "M1 recall / M2" line of each entry. -->

That single import-time pair is the whole of claim (c-i), and its rarity is
the honest measure of how much the corpus supports the ordering argument: one
designed fixture, one arm, one geometry of break.

**M1 recall under failure is not monotone in order.** The `no-recovery` arms
stop at the first red suite, so M1 recall records how many batches landed
before the break — which depends on where the break sits in that particular
order, not on the order's quality. On `task03` the dependency order records
the *lowest* recall of the three (33 % vs 67 %), because it breaks earlier;
on `task04` the dependents-first order records the lowest (33 % vs 67 %).
Recall under a disabled loop is therefore a diagnostic of break position, and
only the outcome column carries the ordering verdict.

<!-- SOURCE: runs/benchmark/results.md §1, rows task03_half_migration / order-dependency-b1-norecovery
     (M1 33.3) vs / order-alphabetical-b1-norecovery and / order-fr3-violating-b1-norecovery (M1 66.7);
     task04_multimodule / order-fr3-violating-b1-norecovery (M1 33.3) vs the other two (M1 66.7). -->

---

# 9. Limitations

Five limitations bound what these results support. They are stated here in
full rather than distributed through the paper.

1. **One migration family.** All five tasks migrate the same contract,
   `datetime.utcnow()` → `datetime.now(timezone.utc)`. Holding it fixed is
   what makes each task's varied factor attributable, but it means the
   failure taxonomy is exercised in one class only (§8: 26/26 `behaviour`),
   and that conclusions about batching and recovery generalize no further
   than one migration contract on a corpus of this size.
   <!-- SOURCE: runs/benchmark/failure-analysis.md — all 26 surviving-failure bullets across the
        14 entries read "**behaviour** break, `TypeError`". Contract from corpus/tierA/*/task.yaml
        (source_api: datetime.utcnow, target_api: datetime.now(timezone.utc)) in all five tasks. -->

2. **One fixed codemod, so arity changes are not expressible.** The agent's
   edit path is a deterministic `libcst` codemod (§3.3). A migration that
   adds or renames a parameter on a *first-party* function — threading a new
   argument through every call site — cannot be represented, because the gold
   state would be unreachable by the only transform the agent can apply.
   `task05` therefore realizes the ordering property through a contract guard
   rather than an arity mismatch (§4.3). The property under test is intact;
   the mechanism is a substitute, and the offline classifier records the
   consequence by filing the failure as `behaviour` rather than `signature`.

3. **Tier A only — no real repository yet.** The corpus is authored, not
   sampled. That buys total ground truth (`ground_truth.json` is the complete
   set $A$, not a proxy) and clean attribution, at the cost of external
   validity. The Tier-B protocol — take a real migration pull request, use its
   parent commit as the "before" state and the merged diff as the gold patch —
   is specified in `docs/05` §1.3 but not yet executed. Until it is, nothing
   here is evidence about repositories the authors did not write.

4. **The live-model arms have not been run.** Ablation C requires an API key
   and is reported as *requires key*, not estimated (§7.6). Every number in
   this paper comes from the deterministic corrector, which shares the loop's
   mechanics with the LLM corrector but not its patch generator. The claim
   this supports is about the *loop*, not about a model's ability to write a
   patch; the two are not interchangeable and no result here should be read
   as the latter.

5. **The ordering claim rests on one designed fixture.** `task05` was built
   *after* `task01`–`task04` failed to separate the orders, specifically to
   exercise ablation B. It is a constructed instance, not a sample: it shows
   that dependency order *can* be the difference between a green migration and
   a failed one, not how often that situation arises in practice. The
   complementary negative result is equally part of the finding — with the
   recovery loop enabled, no order changed the verdict on any task (§7.4
   c-iii), and on `task04` an arbitrary order was measurably *cheaper* than
   the dependency order.

A sixth, smaller caveat: suites of 5–14 tests make M2 coarse. A single
collection error takes out an entire module, which is why regressions are
reported as a count alongside the percentage (§5.2).

---

# 10. Conclusion

> **STUB — outline only. Do not ghost-write.**

- Restate what was built and what was measured, in two sentences, without
  new claims.
- The one-line version of each result: loop load-bearing; static tools detect
  but do not fix; ordering is cost in general and correctness in the
  constructed case.
- The methodological point worth generalizing: an ablation is only as good as
  the fixture that can separate its arms — `task01`–`task04` could not
  separate the orders, and building `task05` was a *result*, not a detour.
- Future work, one clause each: Tier-B external validity; a second migration
  family to exercise the rest of the failure taxonomy; the live-model arms;
  an editor expressive enough to represent arity changes.
- Closing sentence — no new claims.

---

# References

> **STUB.** To be filled from `docs/02_LITERATURE_REVIEW.md` once each entry
> is verified. Every `[CITE: ...]` placeholder in §2 must resolve to an entry
> here. Do not add a reference that has not been checked against the source.
