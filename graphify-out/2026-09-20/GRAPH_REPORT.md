# Graph Report - File1  (2026-09-20)

## Corpus Check
- 63 files · ~22,642 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 437 nodes · 574 edges · 41 communities (32 shown, 9 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4e730240`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_sandbox.py
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
- _CallSiteVisitor
- sandbox/__init__.py
- Literature Review & State of the Art
- Product Requirements Document (PRD)
- task02_datetime_aliased — Tier-A controlled task
- Codebase-Wide Version Migration & Refactoring Agent (MRA)
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
1. `Migration Agent — Master Resource Pack` - 16 edges
2. `SandboxRunner` - 15 edges
3. `Project Synopsis & Charter` - 12 edges
4. `Product Requirements Document (PRD)` - 12 edges
5. `build()` - 11 edges
6. `Codebase-Wide Version Migration & Refactoring Agent (MRA)` - 11 edges
7. `analyze()` - 10 edges
8. `Software Requirements Specification (SRS)` - 10 edges
9. `make_timestamp()` - 9 edges
10. `python_files()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `analyses()` --calls--> `analyze()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/analyzer.py
- `test_every_import_spelling_resolves_to_one_symbol()` --calls--> `find_in_source()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/call_sites.py
- `test_finder_does_not_match_lookalikes()` --calls--> `find_in_source()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/call_sites.py
- `test_dep_graph_has_the_cross_file_edge_and_nothing_spurious()` --calls--> `build()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/dep_graph.py
- `test_state_adjacency_is_importers_per_file()` --calls--> `build()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/dep_graph.py

## Import Cycles
- None detected.

## Communities (41 total, 9 thin omitted)

### Community 0 - "test_sandbox.py"
Cohesion: 0.06
Nodes (51): needs_docker, Phase, _exc_type_from(), _failure_from_collector(), _failure_from_test(), failure_signature(), _lint_counts(), normalize_message() (+43 more)

### Community 1 - "analysis/__init__.py"
Cohesion: 0.09
Nodes (33): DiGraph, analyze(), Path, MAP-node analysis: locate the work, map the dependencies. Nothing else.…, Scan ``repo`` for ``target`` and map its imports. Args: repo: repository root…, CallSite, find_in_repo(), find_in_source() (+25 more)

### Community 2 - "test_analyzer.py"
Cohesion: 0.13
Nodes (26): parametrize, flat_sites(), Any, Flatten the per-file map into one list, the form ground truth uses., Metric computation (M1/M2/M3), following docs/05_DATA_EVALUATION_PROTOCOL.md., m1(), M1 — Migration Completeness. Transcribed verbatim from…, analyses() (+18 more)

### Community 3 - "Project Synopsis & Charter"
Cohesion: 0.07
Nodes (21): Coding conventions, Commit conventions, Current phase / context, Golden rules (do not violate), How to run and test, Tech stack (fixed — verified Aug 2026), What this project is, When unsure (+13 more)

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
Cohesion: 0.11
Nodes (17): 1.1 Purpose, 1.2 Definitions, 1.3 Actors, 1. Introduction, 2. Overall description, 3. Functional requirements, 4.1 `MigrationState` (the agent's working memory), 4.2 `ground_truth.json` (Tier-A scoring key) (+9 more)

### Community 12 - "_CallSiteVisitor"
Cohesion: 0.15
Nodes (12): Call, Name, _CallSiteVisitor, _dotted(), _module_name(), BaseExpression, Import, ImportFrom (+4 more)

### Community 13 - "sandbox/__init__.py"
Cohesion: 0.24
Nodes (13): diff(), Path, Git snapshot / rollback / diff, exposed as agent tools. These operate on the…, Open ``path`` as a git repo, initializing it if it is not one yet., Commit the whole working tree and return the new commit SHA. Allows an empty…, Hard-reset the tree to ``sha`` and drop untracked files; return the SHA., Return a unified diff of the working tree against ``against``. Includes…, _repo() (+5 more)

### Community 14 - "Literature Review & State of the Art"
Cohesion: 0.15
Nodes (12): 1. Problem framing: version migration vs. issue resolution, 2. Deterministic refactoring tools — the baselines, 3.1 SWE-agent — the Agent-Computer Interface (ACI), 3.2 OpenHands (formerly OpenDevin) — CodeAct and the event stream, 3.3 Agentless — the pipeline counter-argument, 3.4 Summary comparison, 3. LLM-based software-engineering systems — the SOTA, 4. Evaluation methodology in the field (+4 more)

### Community 15 - "Product Requirements Document (PRD)"
Cohesion: 0.17
Nodes (12): 10. Risks, 1. Problem, 2. Goal, 3. Non-goals, 4. Users / personas, 5. User stories, 6. Scope (in / out), 7. Success metrics (+4 more)

### Community 16 - "task02_datetime_aliased — Tier-A controlled task"
Cohesion: 0.18
Nodes (9): task01_datetime — Tier-A controlled task, Test-oracle rule, The `pkg` name-collision gotcha, The two states live in one commit, Import changes: deliberately empty, Running the two states, task02_datetime_aliased — Tier-A controlled task, The cross-file break (+1 more)

### Community 17 - "Codebase-Wide Version Migration & Refactoring Agent (MRA)"
Cohesion: 0.18
Nodes (11): Acknowledgements, Architecture at a glance, Codebase-Wide Version Migration & Refactoring Agent (MRA), Documentation index, Evaluation, License, Quickstart, Repository structure (+3 more)

### Community 18 - "Configuration & Secrets"
Cohesion: 0.22
Nodes (8): 1. First-time setup, 2. Required keys, 3. Optional keys, 4. Configuration variables (non-secret), 5. Loading config in code, 6. Security rules, 7. CI / grading environments, Configuration & Secrets

## Knowledge Gaps
- **133 isolated node(s):** `pkg`, `pkg`, `pkg`, `pkg`, `mra` (+128 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Migration Agent — Master Resource Pack` connect `Migration Agent — Master Resource Pack` to `Project Synopsis & Charter`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `build()` (e.g. with `test_dep_graph_has_the_cross_file_edge_and_nothing_spurious()` and `test_state_adjacency_is_importers_per_file()`) actually correct?**
  _`build()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `pkg`, `pkg`, `pkg` to the rest of the system?**
  _133 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_sandbox.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06291591046581972 - nodes in this community are weakly interconnected._
- **Should `analysis/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08658536585365853 - nodes in this community are weakly interconnected._
- **Should `test_analyzer.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12807881773399016 - nodes in this community are weakly interconnected._
- **Should `Project Synopsis & Charter` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._