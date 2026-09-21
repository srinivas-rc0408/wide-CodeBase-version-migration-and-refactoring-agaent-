# Graph Report - File1  (2026-09-21)

## Corpus Check
- 161 files · ~79,212 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1280 nodes · 2126 edges · 98 communities (76 shown, 22 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 159 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7c4eeebe`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- sandbox/runner.py
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
- call_sites.py
- test_p2_end_to_end.py
- Literature Review & State of the Art
- test_sandbox.py
- task05_signature_break — Tier-A edit-order fixture
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
- test_p4_graph.py
- graph.py
- run.py
- correct_node.py
- Any
- test_benchmark.py
- make_timestamp
- benchmark/runner.py
- make_timestamp
- sandbox/__init__.py
- Router
- loop.py
- issue
- 1b. Per task, per configuration
- post
- task04_multimodule/gold/src/pkg/audit.py
- task04_multimodule/old/src/pkg/audit.py
- issue
- Product Requirements Document (PRD)
- Codebase-Wide Version Migration & Refactoring Agent (MRA)
- make_timestamp
- old/src/pkg/api.py
- post
- make_timestamp
- baselines.py
- _ImportCollector
- datetime_utcnow.py
- handle
- old/src/pkg/ledger.py
- gold/src/pkg/api.py
- apply_codemod
- summarize
- Failure analysis
- test_issue_stamps_and_posts
- task03_half_migration/gold/src/pkg/__init__.py
- task03_half_migration/old/src/pkg/__init__.py
- task04_multimodule/gold/src/pkg/__init__.py
- task04_multimodule/old/src/pkg/__init__.py
- pkg
- pkg
- pkg
- pkg
- test_recovery.py
- Path
- snapshot
- ImportBindings
- post
- elapsed_since
- post
- elapsed_since
- serve
- uptime_s
- gold/tests/test_timebase.py
- uptime_s
- 2. Ablations
- handle
- snapshot
- handle
- old/tests/test_timebase.py
- parametrize
- LLMCorrector
- What the Tier-A benchmark shows
- bad_corrector
- task05_signature_break/gold/src/pkg/__init__.py
- task05_signature_break/old/src/pkg/__init__.py
- pkg
- pkg

## God Nodes (most connected - your core abstractions)
1. `Router` - 28 edges
2. `migrate_task()` - 28 edges
3. `SandboxRunner` - 28 edges
4. `run_migration()` - 25 edges
5. `run_one()` - 18 edges
6. `analyze()` - 17 edges
7. `locate()` - 16 edges
8. `apply_codemod()` - 16 edges
9. `Migration Agent — Master Resource Pack` - 16 edges
10. `recover()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `analyses()` --calls--> `analyze()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/analyzer.py
- `test_fr3_property_holds_for_every_task_in_the_corpus()` --calls--> `analyze()`  [INFERRED]
  tests/test_p4_graph.py → src/mra/analysis/analyzer.py
- `test_task04_batches_are_dependency_ordered_and_collapse_the_cycle()` --calls--> `analyze()`  [INFERRED]
  tests/test_p4_graph.py → src/mra/analysis/analyzer.py
- `test_every_import_spelling_resolves_to_one_symbol()` --calls--> `find_in_source()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/call_sites.py
- `test_finder_does_not_match_lookalikes()` --calls--> `find_in_source()`  [INFERRED]
  tests/test_analyzer.py → src/mra/analysis/call_sites.py

## Import Cycles
- None detected.

## Communities (98 total, 22 thin omitted)

### Community 0 - "sandbox/runner.py"
Cohesion: 0.11
Nodes (23): Phase, _exc_type_from(), _failure_from_collector(), _failure_from_test(), failure_signature(), _lint_counts(), normalize_message(), Any (+15 more)

### Community 1 - "analysis/__init__.py"
Cohesion: 0.13
Nodes (24): analyze(), Any, Path, MAP-node analysis: locate the work, map the dependencies. Nothing else.…, Scan ``repo`` for ``target`` and map its imports. Args: repo: repository root…, build(), from_state_adjacency(), module_index() (+16 more)

### Community 2 - "test_analyzer.py"
Cohesion: 0.25
Nodes (16): flat_sites(), Flatten the per-file map into one list, the form ground truth uses., m1(), analyses(), _ground_truth(), _key(), Any, fixture (+8 more)

### Community 3 - "Project Synopsis & Charter"
Cohesion: 0.17
Nodes (12): 10. Open items for first guide meeting, 1. Problem statement, 2. Proposed solution, 3. Scope and finalized migration targets, 4. Deliverables, 5. Success criteria (metrics), 6. Technology stack (summary), 7. Timeline (indicative, aligned to the build phases) (+4 more)

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

### Community 12 - "call_sites.py"
Cohesion: 0.13
Nodes (17): Name, CallSite, _CallSiteVisitor, dotted_path(), find_in_repo(), find_in_source(), Any, BaseExpression (+9 more)

### Community 13 - "test_p2_end_to_end.py"
Cohesion: 0.14
Nodes (27): _added_import_lines(), corpus_digests(), Any, fixture, needs_docker, parametrize, Path, TempPathFactory (+19 more)

### Community 14 - "Literature Review & State of the Art"
Cohesion: 0.15
Nodes (12): 1. Problem framing: version migration vs. issue resolution, 2. Deterministic refactoring tools — the baselines, 3.1 SWE-agent — the Agent-Computer Interface (ACI), 3.2 OpenHands (formerly OpenDevin) — CodeAct and the event stream, 3.3 Agentless — the pipeline counter-argument, 3.4 Summary comparison, 3. LLM-based software-engineering systems — the SOTA, 4. Evaluation methodology in the field (+4 more)

### Community 15 - "test_sandbox.py"
Cohesion: 0.11
Nodes (28): _break_copy(), green_report(), fixture, needs_docker, Path, TempPathFactory, P0 acceptance: the sandbox verifies a real corpus task and reports it as data.…, The source tree is mounted :ro and copied inside; a run must not touch it. The… (+20 more)

### Community 16 - "task05_signature_break — Tier-A edit-order fixture"
Cohesion: 0.06
Nodes (27): task01_datetime — Tier-A controlled task, Test-oracle rule, The `pkg` name-collision gotcha, The two states live in one commit, Import changes: deliberately empty, Running the two states, task02_datetime_aliased — Tier-A controlled task, The cross-file break (+19 more)

### Community 17 - "CLAUDE.md"
Cohesion: 0.18
Nodes (9): Coding conventions, Commit conventions, Current phase / context, Golden rules (do not violate), How to run and test, Tech stack (fixed — verified Aug 2026), What this project is, When unsure (+1 more)

### Community 18 - "Configuration & Secrets"
Cohesion: 0.22
Nodes (8): 1. First-time setup, 2. Required keys, 3. Optional keys, 4. Configuration variables (non-secret), 5. Loading config in code, 6. Security rules, 7. CI / grading environments, Configuration & Secrets

### Community 28 - "test_p4_graph.py"
Cohesion: 0.10
Nodes (40): bad_corrector(), capped03(), corpus_digests(), graph03(), graph04(), _nodes(), payload_sizes(), Any (+32 more)

### Community 29 - "graph.py"
Cohesion: 0.11
Nodes (33): all_batches_done(), build_graph(), _cap(), changed_files(), finish_node(), is_green(), _key(), outcome_of() (+25 more)

### Community 31 - "run.py"
Cohesion: 0.12
Nodes (17): Collection, Metric computation (M1/M2/M3), following docs/05_DATA_EVALUATION_PROTOCOL.md., M1 — Migration Completeness. Transcribed verbatim from…, m2(), M2 — Post-Migration Test Pass Rate. Transcribed verbatim from…, TEST node: verify the tree in the sandbox and write the report into state…, _key(), main() (+9 more)

### Community 32 - "correct_node.py"
Cohesion: 0.16
Nodes (21): apply_source(), classify(), classify_offline(), corrective_patch(), extract_source(), _hinted_files(), is_test_path(), locate() (+13 more)

### Community 33 - "Any"
Cohesion: 0.15
Nodes (19): _nodes(), Any, needs_docker, The headline: a broken half-migration is finished automatically., Recovery from the wrong failure would prove nothing about this fixture., FR-7's audit trail: the sequence, not just the outcome (SRS §4.1)., M1 and M2 both at 100: the loop finished the migration, it did not mask it., FR-10: the deliverable covers the corrected file too, not just the batch. (+11 more)

### Community 34 - "test_benchmark.py"
Cohesion: 0.08
Nodes (44): ablation_a(), ablation_b(), ablation_b_task05(), corpus_digests(), matrix(), Any, fixture, parametrize (+36 more)

### Community 35 - "make_timestamp"
Cohesion: 0.08
Nodes (28): audit_record(), audit_window(), datetime, Audit trail. Imports the clock contract and also reads the clock directly., Return the ``seconds``-long window ending now. Both ends come from the same…, Stamp an audit record from the shared clock., make_timestamp(), datetime (+20 more)

### Community 36 - "benchmark/runner.py"
Cohesion: 0.07
Nodes (59): MonkeyPatch, P5 benchmarking: run the agent across the corpus under controlled conditions., ``python -m mra.benchmark`` — run the matrix and write the report., _ablation_a(), _ablation_b(), _ablation_c(), _ablation_d(), _aggregate() (+51 more)

### Community 37 - "make_timestamp"
Cohesion: 0.08
Nodes (26): audit_record(), audit_window(), datetime, Audit trail. Imports the clock contract and also reads the clock directly., Return the ``seconds``-long window ending now. Both ends come from the same…, Stamp an audit record from the shared clock., make_timestamp(), datetime (+18 more)

### Community 38 - "sandbox/__init__.py"
Cohesion: 0.25
Nodes (13): changed_paths(), diff(), Path, Git snapshot / rollback / diff, exposed as agent tools. These operate on the…, Open ``path`` as a git repo, initializing it if it is not one yet., Commit the whole working tree and return the new commit SHA. Allows an empty…, Hard-reset the tree to ``sha`` and drop untracked files; return the SHA., Repo-relative paths differing from ``against``, untracked files included. The… (+5 more)

### Community 39 - "Router"
Cohesion: 0.10
Nodes (26): LLM routing and token accounting. The only place a model name is chosen., cost_usd(), model_id(), Any, Model router: which DeepSeek model answers which question, and what it cost.…, True when a live call can be made. False means: skip, do not fail., One chat completion for ``task``; bills its tokens and returns the text., The configured model name for a task class. (+18 more)

### Community 41 - "loop.py"
Cohesion: 0.21
Nodes (14): Protocol, Self-correction: the loop that turns a failing migration into a passing one., Corrector, is_green(), _next_failure(), Any, Path, The recovery loop: EDIT -> TEST -> CORRECT -> TEST -> ... -> green or give up.… (+6 more)

### Community 42 - "issue"
Cohesion: 0.15
Nodes (13): issue(), Invoicing. Stamps with its OWN clock reading, not the shared one. That detail…, Post the amount to the ledger and return the invoice record., invoice_age_seconds(), Reporting. The module the batched migration is designed to leave behind., Issue an invoice and report how old it is., Seconds since the invoice was issued. Reads its *own* clock and subtracts…, summary() (+5 more)

### Community 43 - "1b. Per task, per configuration"
Cohesion: 0.20
Nodes (10): 1. The whole offline matrix, 1b. Per task, per configuration, 3. Deterministic baselines — ruff (DTZ) and pyupgrade, 4. Configuration key, Benchmark results — Tier A, task01_datetime, task02_datetime_aliased, task03_half_migration (+2 more)

### Community 44 - "post"
Cohesion: 0.17
Nodes (13): balance(), post(), datetime, Double-entry ledger. Half of the import cycle with :mod:`pkg.audit`. ``import…, Record an entry, stamped from the shared clock, and note it in the audit trail., Sum of every amount posted to ``account``., The ``seconds``-long window ending now. Both ends come from one reading, so…, snapshot_window() (+5 more)

### Community 45 - "task04_multimodule/gold/src/pkg/audit.py"
Cohesion: 0.20
Nodes (10): note(), Audit trail. The other half of the import cycle with :mod:`pkg.ledger`., Append a message to the trail, stamped from the shared clock., Read the ledger back — the call that closes the cycle. ``checked_at`` is never…, reconcile(), trail(), Audit trail, and the call that closes the import cycle with the ledger., Exercises audit -> ledger, the other direction of the cycle. (+2 more)

### Community 46 - "task04_multimodule/old/src/pkg/audit.py"
Cohesion: 0.20
Nodes (10): note(), Audit trail. The other half of the import cycle with :mod:`pkg.ledger`., Append a message to the trail, stamped from the shared clock., Read the ledger back — the call that closes the cycle. ``checked_at`` is never…, reconcile(), trail(), Audit trail, and the call that closes the import cycle with the ledger., Exercises audit -> ledger, the other direction of the cycle. (+2 more)

### Community 47 - "issue"
Cohesion: 0.23
Nodes (10): issue(), Post the amount to the ledger and return the invoice record., invoice_age_seconds(), Reporting. The module the batched migration is designed to leave behind., Issue an invoice and report how old it is., Seconds since the invoice was issued. Reads its *own* clock and subtracts…, summary(), The tripwire. ``invoice_age_seconds`` is the only place in the package where… (+2 more)

### Community 48 - "Product Requirements Document (PRD)"
Cohesion: 0.17
Nodes (12): 10. Risks, 1. Problem, 2. Goal, 3. Non-goals, 4. Users / personas, 5. User stories, 6. Scope (in / out), 7. Success metrics (+4 more)

### Community 49 - "Codebase-Wide Version Migration & Refactoring Agent (MRA)"
Cohesion: 0.17
Nodes (12): Acknowledgements, Architecture at a glance, Codebase-Wide Version Migration & Refactoring Agent (MRA), Documentation index, Evaluation, License, Quickstart, Repository structure (+4 more)

### Community 50 - "make_timestamp"
Cohesion: 0.24
Nodes (9): make_timestamp(), datetime, The shared clock. Nothing in the package imports anything to provide it. Most-…, Return the current UTC time as a naive datetime., The shared clock. No assertion here may depend on the migration (NB-10)., The semantic check. Fails against ``old/`` — that is the point., test_make_timestamp_is_non_decreasing(), test_make_timestamp_is_timezone_aware() (+1 more)

### Community 51 - "old/src/pkg/api.py"
Cohesion: 0.18
Nodes (8): handle(), The entry point. Depends on report, audit and config — the graph's deepest…, Serve one request. ``served_at`` is this module's own, self-contained reading., Static settings. No clock, no in-repo imports — the graph's other root., How long a record is kept, in seconds., retention_seconds(), The entry point, exercising the whole import DAG in one call., test_handle_serves_a_complete_response()

### Community 52 - "post"
Cohesion: 0.22
Nodes (8): Invoicing. Stamps with its OWN clock reading, not the shared one. That detail…, balance(), post(), Record an entry, stamped from the shared clock, and note it in the audit trail., Sum of every amount posted to ``account``., Ledger, including its self-contained clock reading., test_balance_sums_only_that_account(), test_post_returns_a_stamped_entry()

### Community 53 - "make_timestamp"
Cohesion: 0.28
Nodes (7): make_timestamp(), datetime, The shared clock. Nothing in the package imports anything to provide it. Most-…, Return the current UTC time as a naive datetime., The shared clock. No assertion here may depend on the migration (NB-10)., test_make_timestamp_is_non_decreasing(), test_make_timestamp_returns_a_datetime()

### Community 54 - "baselines.py"
Cohesion: 0.16
Nodes (23): CompletedProcess, baseline_table(), _detect_with_ruff(), Any, Path, pyupgrade_baseline(), The honesty check: what the existing static tools already do (docs/05, §2.2).…, Run pyupgrade over the task and score it the same way. (+15 more)

### Community 55 - "_ImportCollector"
Cohesion: 0.25
Nodes (6): _ImportCollector, _module_name(), BaseExpression, Import, ImportFrom, Collects the dotted module names a file imports, including submodules.

### Community 56 - "datetime_utcnow.py"
Cohesion: 0.12
Nodes (13): ConvertUtcnowCommand, BaseExpression, Call, T1 codemod: ``datetime.utcnow()`` -> ``datetime.now(timezone.utc)``.…, Rewrite every resolved ``datetime.utcnow()`` call, whatever its spelling., Deterministic libcst codemods, one per migration task (golden rule 5)., _codemod(), FakeDeepSeek (+5 more)

### Community 57 - "handle"
Cohesion: 0.33
Nodes (6): handle(), Serve one request. ``served_at`` is this module's own, self-contained reading., The entry point, exercising the whole import DAG in one call., Syntactic success is not success: no module may be left on a naive clock., test_every_stamp_in_one_response_is_aware(), test_handle_serves_a_complete_response()

### Community 58 - "old/src/pkg/ledger.py"
Cohesion: 0.33
Nodes (6): datetime, Double-entry ledger. Half of the import cycle with :mod:`pkg.audit`. ``import…, The ``seconds``-long window ending now. Both ends come from one reading, so…, snapshot_window(), Both ends come from one reading — safe whichever side of the migration., test_snapshot_window_is_ordered()

### Community 60 - "gold/src/pkg/api.py"
Cohesion: 0.33
Nodes (4): The entry point. Depends on report, audit and config — the graph's deepest…, Static settings. No clock, no in-repo imports — the graph's other root., How long a record is kept, in seconds., retention_seconds()

### Community 61 - "apply_codemod"
Cohesion: 0.24
Nodes (8): apply_codemod(), make_edit_node(), Any, Path, EDIT node: apply the migration codemod to the files the analyzer flagged. It…, Run the codemod over every file in ``call_sites``; return the ones that…, Bind nothing and return the node LangGraph calls. The node edits…, State-machine nodes. Plain functions for now; LangGraph wiring lands in P4.

### Community 62 - "summarize"
Cohesion: 0.18
Nodes (16): edit_context(), graph_slice(), offline_summary(), progress_facts(), Any, Rolling memory: what the model is told about everything that is not in front of…, The dependency neighbourhood, truncated to a constant number of names., The complete payload for one corrective-edit call (NFR-12). Everything except… (+8 more)

### Community 63 - "Failure analysis"
Cohesion: 0.13
Nodes (15): Failure analysis, `no-recovery` on task02_datetime_aliased, `no-recovery` on task03_half_migration, `no-recovery` on task04_multimodule, `order-alphabetical-b1-norecovery` on task02_datetime_aliased, `order-alphabetical-b1-norecovery` on task03_half_migration, `order-alphabetical-b1-norecovery` on task04_multimodule, `order-alphabetical-b1-norecovery` on task05_signature_break (+7 more)

### Community 73 - "test_recovery.py"
Cohesion: 0.16
Nodes (16): corpus_digest(), gave_up(), fixture, TempPathFactory, P3 acceptance: the recovery loop, proved without a paid API key. The loop and…, Taken before any run, compared after: the corpus must be read-only in practice., NB-4 on the happy path, plus: edits land on the copy, never on corpus/., docs/04 §2.5: a bare TypeError with no signature change is behavioural. (+8 more)

### Community 74 - "Path"
Cohesion: 0.13
Nodes (16): oracle_tampering_corrector(), needs_key, Path, No sandbox needed: the fixture's shape is a static property., Golden rule 1. A patch that edits tests is reverted, not just logged., The trace names report.py; the slice reports who imports it., Nothing left to migrate means this node cannot be the fix. Say so., NB-4 at the localization step, before a model is ever asked for a patch. (+8 more)

### Community 75 - "snapshot"
Cohesion: 0.16
Nodes (10): The service edge: the deepest module in the import DAG., One request, its ledger entry and a metrics snapshot., serve(), Point-in-time metrics over the ledger., Entry count plus how long this reading took to assemble., snapshot(), The service edge: every module in the DAG on one call path., test_serve_returns_the_whole_response() (+2 more)

### Community 76 - "ImportBindings"
Cohesion: 0.15
Nodes (10): bindings_of(), ImportBindings, _module_name(), Import, ImportFrom, Module, Collect a whole module's import bindings up front., Dotted text of an import's module expression (``a.b.c``). (+2 more)

### Community 77 - "post"
Cohesion: 0.24
Nodes (8): age_of(), post(), Append-only ledger. Stamps entries with its own clock reading., Record one amount against an account and return the entry., Seconds since ``entry`` was posted. Hands this module's own stamp back to the…, The ledger and the call-time half of the break., test_age_of_an_entry_is_non_negative(), test_post_records_the_amount()

### Community 78 - "elapsed_since"
Cohesion: 0.33
Nodes (9): aligned(), elapsed_since(), datetime, The package clock, and the one place its contract is enforced. Every module…, The current UTC time, in whatever shape the package contract is in., Read ``stamp`` in the shape ``reference`` is in. Upgrades only, never…, Seconds between ``stamp`` and now, for a stamp this package produced. The…, utc_now() (+1 more)

### Community 79 - "post"
Cohesion: 0.24
Nodes (8): age_of(), post(), Append-only ledger. Stamps entries with its own clock reading., Record one amount against an account and return the entry., Seconds since ``entry`` was posted. Hands this module's own stamp back to the…, The ledger and the call-time half of the break., test_age_of_an_entry_is_non_negative(), test_post_records_the_amount()

### Community 80 - "elapsed_since"
Cohesion: 0.33
Nodes (9): aligned(), elapsed_since(), datetime, The package clock, and the one place its contract is enforced. Every module…, The current UTC time, in whatever shape the package contract is in., Read ``stamp`` in the shape ``reference`` is in. Upgrades only, never…, Seconds between ``stamp`` and now, for a stamp this package produced. The…, utc_now() (+1 more)

### Community 81 - "serve"
Cohesion: 0.25
Nodes (7): The service edge: the deepest module in the import DAG., One request, its ledger entry and a metrics snapshot., serve(), The service edge: every module in the DAG on one call path., Syntactic success is not success: no module may be left on a naive clock., test_every_stamp_in_one_response_is_aware(), test_serve_returns_the_whole_response()

### Community 82 - "uptime_s"
Cohesion: 0.22
Nodes (5): Start-up bookkeeping. Both of its constants are computed at *import* time. That…, Seconds since :data:`STARTED_AT`., uptime_s(), Start-up constants. Importing this module is itself the assertion., test_uptime_grows_from_the_import_stamp()

### Community 83 - "gold/tests/test_timebase.py"
Cohesion: 0.22
Nodes (8): The clock contract. No assertion here may depend on the migration (NB-10).…, The safe window: a caller that has not moved yet is upgraded for free., The refusal: an aware stamp meeting a naive clock is passed through, not…, The semantic check. Fails against ``old/`` — that is the point., test_aligned_never_strips_a_tzinfo(), test_aligned_reads_a_naive_stamp_as_utc_when_the_clock_is_aware(), test_utc_now_is_timezone_aware(), test_utc_now_returns_a_datetime()

### Community 84 - "uptime_s"
Cohesion: 0.22
Nodes (5): Start-up bookkeeping. Both of its constants are computed at *import* time. That…, Seconds since :data:`STARTED_AT`., uptime_s(), Start-up constants. Importing this module is itself the assertion., test_uptime_grows_from_the_import_stamp()

### Community 85 - "2. Ablations"
Cohesion: 0.22
Nodes (9): 2. Ablations, A. Recovery loop ON vs OFF — the headline, B. Dependency-ordered batching vs arbitrary order, batch size 1, recovery OFF, batch size 1, recovery on, batch size 3, recovery on, C. Edit model — V4-Pro vs V4-Flash, D. Batch size 1 vs 3 vs 5 (+1 more)

### Community 86 - "handle"
Cohesion: 0.33
Nodes (5): handle(), Request handling. Its own stamp never leaves the module, so it is self-…, Post one amount and return the handled record., test_handle_posts_the_entry(), test_handle_reports_uptime()

### Community 87 - "snapshot"
Cohesion: 0.33
Nodes (5): Point-in-time metrics over the ledger., Entry count plus how long this reading took to assemble., snapshot(), test_snapshot_counts_the_entries(), test_snapshot_reports_its_own_lag()

### Community 88 - "handle"
Cohesion: 0.33
Nodes (5): handle(), Request handling. Its own stamp never leaves the module, so it is self-…, Post one amount and return the handled record., test_handle_posts_the_entry(), test_handle_reports_uptime()

### Community 89 - "old/tests/test_timebase.py"
Cohesion: 0.29
Nodes (6): The clock contract. No assertion here may depend on the migration (NB-10).…, The safe window: a caller that has not moved yet is upgraded for free., The refusal: an aware stamp meeting a naive clock is passed through, not…, test_aligned_never_strips_a_tzinfo(), test_aligned_reads_a_naive_stamp_as_utc_when_the_clock_is_aware(), test_utc_now_returns_a_datetime()

### Community 90 - "parametrize"
Cohesion: 0.29
Nodes (7): parametrize, SRS §4.1 defines dep_graph as file -> files that import it (predecessors)., False positives cost M1 precision and cause wrong edits, not missed ones., test_dep_graph_has_the_cross_file_edge_and_nothing_spurious(), test_every_import_spelling_resolves_to_one_symbol(), test_finder_does_not_match_lookalikes(), test_state_adjacency_is_importers_per_file()

### Community 91 - "LLMCorrector"
Cohesion: 0.33
Nodes (5): LLMCorrector, The CORRECT node as a corrector callable, for :func:`mra.recovery.recover`. One…, needs_key, The real model, through the real graph, on the biggest fixture., test_live_llm_drives_the_graph_on_the_multimodule_task()

### Community 92 - "What the Tier-A benchmark shows"
Cohesion: 0.40
Nodes (5): (a) The recovery loop is what finishes a cross-file migration, (b) The existing static tools detect the work and do none of it, (c) Dependency-ordered batching: what the data actually supports, Scope and honesty notes, What the Tier-A benchmark shows

### Community 93 - "bad_corrector"
Cohesion: 0.50
Nodes (4): bad_corrector(), The ceiling is configurable (MRA_MAX_FIX_ATTEMPTS), not hard-coded at 3., Claims a fix, changes nothing. The failure — and its signature — survive., test_custom_cap_is_honoured()

## Knowledge Gaps
- **188 isolated node(s):** `pkg`, `pkg`, `pkg`, `pkg`, `pkg` (+183 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SandboxRunner` connect `run.py` to `sandbox/runner.py`, `sandbox/__init__.py`, `loop.py`, `test_p2_end_to_end.py`, `test_sandbox.py`, `baselines.py`, `graph.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `Router` connect `Router` to `correct_node.py`, `benchmark/runner.py`, `test_recovery.py`, `Path`, `datetime_utcnow.py`, `LLMCorrector`, `test_p4_graph.py`, `graph.py`, `summarize`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `migrate_task()` connect `run.py` to `analysis/__init__.py`, `test_analyzer.py`, `sandbox/__init__.py`, `Router`, `loop.py`, `test_recovery.py`, `Path`, `test_p2_end_to_end.py`, `bad_corrector`, `test_p4_graph.py`, `apply_codemod`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Router` (e.g. with `Tokens` and `payload_sizes()`) actually correct?**
  _`Router` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SandboxRunner` (e.g. with `test_migrated_tree_satisfies_the_gold_semantic_check()` and `test_trajectory_is_reconstructed_from_the_checkpoint_file_on_disk()`) actually correct?**
  _`SandboxRunner` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `pkg`, `pkg`, `pkg` to the rest of the system?**
  _188 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `sandbox/runner.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11083743842364532 - nodes in this community are weakly interconnected._