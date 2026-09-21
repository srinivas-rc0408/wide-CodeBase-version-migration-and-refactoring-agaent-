# Graph Report - File1  (2026-09-20)

## Corpus Check
- 66 files · ~24,612 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 503 nodes · 710 edges · 37 communities (28 shown, 9 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4e730240`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- runner.py
- analysis/__init__.py
- test_analyzer.py
- Project Synopsis & Charter
- make_timestamp
- make_timestamp
- Migration Agent — Master Resource Pack
- make_timestamp
- make_timestamp
- 2. Low-Level Design (LLD) — the LangGraph state machine
- Data & Evaluation Protocol
- Software Requirements Specification (SRS)
- ConvertUtcnowCommand
- run.py
- Literature Review & State of the Art
- SandboxRunner
- task02_datetime_aliased — Tier-A controlled task
- CLAUDE.md
- Configuration & Secrets
- task01_datetime/gold/src/pkg/__init__.py
- task01_datetime/old/src/pkg/__init__.py
- task02_datetime_aliased/gold/src/pkg/__init__.py
- task02_datetime_aliased/old/src/pkg/__init__.py
- pkg
- pkg
- pkg
- pkg
- mra

## God Nodes (most connected - your core abstractions)
1. `SandboxRunner` - 18 edges
2. `migrate_task()` - 16 edges
3. `Migration Agent — Master Resource Pack` - 16 edges
4. `analyze()` - 12 edges
5. `Project Synopsis & Charter` - 12 edges
6. `Product Requirements Document (PRD)` - 12 edges
7. `build()` - 11 edges
8. `Codebase-Wide Version Migration & Refactoring Agent (MRA)` - 11 edges
9. `flat_sites()` - 10 edges
10. `Software Requirements Specification (SRS)` - 10 edges

## Surprising Connections (you probably didn't know these)
- `analyses()` --calls--> `analyze()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/analyzer.py
- `test_every_import_spelling_resolves_to_one_symbol()` --calls--> `find_in_source()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/call_sites.py
- `test_finder_does_not_match_lookalikes()` --calls--> `find_in_source()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/call_sites.py
- `test_dep_graph_has_the_cross_file_edge_and_nothing_spurious()` --calls--> `build()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/dep_graph.py
- `test_normalization_strips_volatile_text()` --calls--> `normalize_message()`  [INFERRED]
  tests/test_sandbox.py → src/mra/sandbox/runner.py

## Import Cycles
- None detected.

## Communities (37 total, 9 thin omitted)

### Community 0 - "runner.py"
Cohesion: 0.11
Nodes (23): Phase, _exc_type_from(), _failure_from_collector(), _failure_from_test(), failure_signature(), _lint_counts(), normalize_message(), Any (+15 more)

### Community 1 - "analysis/__init__.py"
Cohesion: 0.08
Nodes (35): DiGraph, analyze(), Path, MAP-node analysis: locate the work, map the dependencies. Nothing else.…, Scan ``repo`` for ``target`` and map its imports. Args: repo: repository root…, CallSite, find_in_repo(), find_in_source() (+27 more)

### Community 2 - "test_analyzer.py"
Cohesion: 0.17
Nodes (22): flat_sites(), Any, Flatten the per-file map into one list, the form ground truth uses., m1(), analyses(), _ground_truth(), _key(), Any (+14 more)

### Community 3 - "Project Synopsis & Charter"
Cohesion: 0.05
Nodes (35): 10. Open items for first guide meeting, 1. Problem statement, 2. Proposed solution, 3. Scope and finalized migration targets, 4. Deliverables, 5. Success criteria (metrics), 6. Technology stack (summary), 7. Timeline (indicative, aligned to the build phases) (+27 more)

### Community 4 - "make_timestamp"
Cohesion: 0.12
Nodes (19): make_timestamp(), datetime, Timestamp helpers. Defines the contract that the migration changes., Return the current UTC time as a timezone-aware datetime., build_report(), datetime, Report building. Imports :mod:`pkg.core`, creating the cross-file dependency…, Return how many seconds ago ``generated_at`` was produced. (+11 more)

### Community 5 - "make_timestamp"
Cohesion: 0.12
Nodes (19): make_timestamp(), datetime, Timestamp helpers. Defines the contract that the migration changes., Return the current UTC time as a timezone-aware datetime., build_report(), datetime, Report building. Imports :mod:`pkg.core`, creating the cross-file dependency…, Return how many seconds ago ``generated_at`` was produced. Reads the clock… (+11 more)

### Community 6 - "Migration Agent — Master Resource Pack"
Cohesion: 0.09
Nodes (23): 0. Read this first — the one thing that will sink you, 10. Trap checklist (expanded with the version facts I found), 11. Questions for Dr Nimrita Koul (first meeting) — refined, 12. The paper plan (start the skeleton in week 1, not week 9), 13. Your one-sentence story (memorize it — this is the interview weapon), 1. Verified stack (checked 24 Aug 2026), 2.1 `datetime.utcnow()` → timezone-aware (EASY — build this first), 2.2 Python 3.8 → 3.12 modernization (EASY–MEDIUM, has a baseline) (+15 more)

### Community 7 - "make_timestamp"
Cohesion: 0.13
Nodes (17): make_timestamp(), datetime, Timestamp helpers. Defines the contract that the migration changes., Return the current UTC time as a naive datetime., build_report(), datetime, Report building. Imports :mod:`pkg.core`, creating the cross-file dependency…, Return how many seconds ago ``generated_at`` was produced. (+9 more)

### Community 8 - "make_timestamp"
Cohesion: 0.13
Nodes (17): make_timestamp(), datetime, Timestamp helpers. Defines the contract that the migration changes., Return the current UTC time as a naive datetime., build_report(), datetime, Report building. Imports :mod:`pkg.core`, creating the cross-file dependency…, Return how many seconds ago ``generated_at`` was produced. Reads the clock… (+9 more)

### Community 9 - "2. Low-Level Design (LLD) — the LangGraph state machine"
Cohesion: 0.10
Nodes (19): 1.1 Component diagram, 1.2 Component responsibilities, 1.3 Data flow (one task, happy path then recovery), 1.4 Key architectural decisions (ADR summary), 1. High-Level Design (HLD), 2.1 State machine diagram, 2.2 Nodes (contracts), 2.3 Conditional routing after TEST (the graded logic) (+11 more)

### Community 10 - "Data & Evaluation Protocol"
Cohesion: 0.11
Nodes (18): 1.1 Tier A — controlled repos you author (gold standard), 1.2 Tier A git-tagging strategy, 1.3 Tier B — real OSS repos (external validity), 1. Corpus specification, 2.1 M1 — Migration Completeness, 2.2 M2 — Post-Migration Test Pass Rate, 2.3 M3 — Token / Step Overhead, 2.4 Reference computation (already stubbed in the resource pack) (+10 more)

### Community 11 - "Software Requirements Specification (SRS)"
Cohesion: 0.12
Nodes (17): 1.1 Purpose, 1.2 Definitions, 1.3 Actors, 1. Introduction, 2. Overall description, 3. Functional requirements, 4.1 `MigrationState` (the agent's working memory), 4.2 `ground_truth.json` (Tier-A scoring key) (+9 more)

### Community 12 - "ConvertUtcnowCommand"
Cohesion: 0.06
Nodes (31): Name, bindings_of(), _CallSiteVisitor, dotted_path(), ImportBindings, _module_name(), BaseExpression, Call (+23 more)

### Community 13 - "run.py"
Cohesion: 0.06
Nodes (53): Metric computation (M1/M2/M3), following docs/05_DATA_EVALUATION_PROTOCOL.md., M1 — Migration Completeness. Transcribed verbatim from…, m2(), M2 — Post-Migration Test Pass Rate. Transcribed verbatim from…, _key(), main(), migrate_task(), Any (+45 more)

### Community 14 - "Literature Review & State of the Art"
Cohesion: 0.15
Nodes (12): 1. Problem framing: version migration vs. issue resolution, 2. Deterministic refactoring tools — the baselines, 3.1 SWE-agent — the Agent-Computer Interface (ACI), 3.2 OpenHands (formerly OpenDevin) — CodeAct and the event stream, 3.3 Agentless — the pipeline counter-argument, 3.4 Summary comparison, 3. LLM-based software-engineering systems — the SOTA, 4. Evaluation methodology in the field (+4 more)

### Community 15 - "SandboxRunner"
Cohesion: 0.13
Nodes (28): Runs a repo's suite in one throwaway container and returns a test_report. The…, SandboxRunner, _break_copy(), green_report(), fixture, needs_docker, Path, TempPathFactory (+20 more)

### Community 16 - "task02_datetime_aliased — Tier-A controlled task"
Cohesion: 0.18
Nodes (9): task01_datetime — Tier-A controlled task, Test-oracle rule, The `pkg` name-collision gotcha, The two states live in one commit, Import changes: deliberately empty, Running the two states, task02_datetime_aliased — Tier-A controlled task, The cross-file break (+1 more)

### Community 17 - "CLAUDE.md"
Cohesion: 0.20
Nodes (9): Coding conventions, Commit conventions, Current phase / context, Golden rules (do not violate), How to run and test, Tech stack (fixed — verified Aug 2026), What this project is, When unsure (+1 more)

### Community 18 - "Configuration & Secrets"
Cohesion: 0.22
Nodes (8): 1. First-time setup, 2. Required keys, 3. Optional keys, 4. Configuration variables (non-secret), 5. Loading config in code, 6. Security rules, 7. CI / grading environments, Configuration & Secrets

## Knowledge Gaps
- **133 isolated node(s):** `pkg`, `pkg`, `pkg`, `pkg`, `mra` (+128 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SandboxRunner` connect `SandboxRunner` to `runner.py`, `run.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `migrate_task()` connect `run.py` to `analysis/__init__.py`, `test_analyzer.py`, `ConvertUtcnowCommand`, `SandboxRunner`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Migration Agent — Master Resource Pack` connect `Migration Agent — Master Resource Pack` to `Project Synopsis & Charter`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **What connects `pkg`, `pkg`, `pkg` to the rest of the system?**
  _133 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `runner.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11083743842364532 - nodes in this community are weakly interconnected._
- **Should `analysis/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08194905869324474 - nodes in this community are weakly interconnected._
- **Should `Project Synopsis & Charter` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._