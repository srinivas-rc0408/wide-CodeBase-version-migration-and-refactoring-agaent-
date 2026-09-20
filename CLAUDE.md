# CLAUDE.md

Instructions for AI coding assistants (Claude Code, Cursor, etc.) working in this repository. Read this before making changes. Human contributors should read it too — it encodes the project's conventions and hard rules.

## What this project is

The **Migration & Refactoring Agent (MRA)**: an autonomous agent that performs a specified library/language version migration across a multi-module **Python** codebase and verifies the result with the repo's own test suite. It is an **academic research project**, not a product. Correctness, reproducibility, and inspectability matter more than speed or features.

The agent is a **LangGraph 1.x state machine**: `MAP → PLAN → EDIT → TEST → CORRECT`. The self-correction loop and the dependency-ordered editing are the point of the project — never shortcut them.

## Golden rules (do not violate)

1. **Never weaken or edit the test suite to make it pass.** The tests are the oracle. Changing test files to force a green run is a hard failure. If a test seems wrong, flag it — do not touch it.
2. **Never put secrets in code, docs, or commits.** API keys come from environment variables (`os.environ["DEEPSEEK_API_KEY"]`) loaded from `.env` (gitignored). See `CONFIGURATION.md`. If you see a hard-coded key, stop and remove it.
3. **All code execution happens inside the Docker sandbox**, never on the host. Do not add code that shells out on the host filesystem.
4. **Data shapes are contracts.** `MigrationState`, `ground_truth.json`, the test report, and the metrics record follow the JSON Schemas in `docs/03_SRS.md §4`. Do not change a shape without updating the schema and the doc in the same change.
5. **Deterministic edits are codemods, not LLM calls.** If an edit is a mechanical, rule-based transform, implement it as a `libcst` codemod under `src/mra/codemods/`. Reserve the LLM for genuinely ambiguous edits and for failure recovery. This is a correctness and cost (M3) requirement.
6. **Respect the functional boundaries** in `docs/03_SRS.md §5` (NB-1…NB-10). In particular: Python source only; no infra/CI changes; no business-logic rewrites unrelated to the migration; no network at agent runtime; stop at `MAX_FIX_ATTEMPTS`.
7. **Pin dependencies.** Never add an unpinned dependency. Add it to `pyproject.toml` with a version and explain why.

## Tech stack (fixed — verified Aug 2026)

- **Python 3.12**
- **LangGraph 1.x** (build v1 patterns; the 0.x API is maintenance-only)
- **libcst** — analysis + codemods (preserves formatting/comments)
- **networkx** — dependency/call graph
- **pytest** + **pytest-json-report** + **ruff** — verification
- **GitPython** — snapshot / rollback / patch
- **Docker** `python:3.12-slim` (or rootless Podman) — sandbox
- **DeepSeek V4-Pro** (edits, trace reasoning) and **V4-Flash** (summaries, classification) via the OpenAI-compatible endpoint `https://api.deepseek.com`

Do not swap frameworks or add new heavy dependencies without updating `docs/` and getting sign-off.

## Where things live

| Area | Path |
|---|---|
| State object | `src/mra/state.py` |
| Graph wiring (nodes + edges) | `src/mra/graph.py` |
| Node logic | `src/mra/nodes/*.py` |
| Static analysis (libcst visitors, graph builder) | `src/mra/analysis/` |
| Deterministic codemods (per migration task) | `src/mra/codemods/` |
| Sandbox wrappers (docker run, git) | `src/mra/sandbox/` |
| Model router + token accounting | `src/mra/models/` |
| Metric computation (M1/M2/M3) | `src/mra/metrics/` |
| Corpus | `corpus/tierA/`, `corpus/tierB/` |
| Run outputs | `runs/<run_id>/` (gitignored) |

## Coding conventions

- **Type hints everywhere.** Public functions are fully annotated. Run `mypy` if configured.
- **Small, single-purpose functions.** Nodes are `state -> partial state update`; keep side effects explicit (file writes, sandbox runs).
- **Structured I/O only.** Parse `pytest`/tool output into the JSON contracts; never scrape free text with regex where a structured report exists (`pytest-json-report`).
- **Determinism.** LLM temperature 0.0–0.2 for edits; log the model ID and token counts for every call (feeds M3).
- **No `print` for logging.** Use the logger; every LLM/tool call is recorded to the trajectory.
- **Docstrings** state the node/function contract (inputs read, outputs written, side effects).

## How to run and test

```bash
# unit tests for the agent itself
pytest tests/ -q

# lint + format
ruff check . && ruff format .

# build the sandbox image
docker build -f Dockerfile.sandbox -t mra-sandbox:py312 .

# run a migration on a controlled task
python -m mra.run --task-dir corpus/tierA/task01_datetime
```

Before proposing a change as done: `pytest tests/` passes, `ruff check .` is clean, and no schema in `docs/03_SRS.md §4` was changed without updating the doc.

## Commit conventions

Use Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`. One logical change per commit. Reference the build phase where relevant (e.g. `feat(analysis): call-site visitor for datetime.utcnow [P1]`).

## Current phase / context

Fill this in as you progress so the assistant has current context:

- **Current phase:** P2 (deterministic edit + verify; P0 sandbox and P1 analyzer done)
- **Active migration task:** T1 — `datetime.utcnow()` → `datetime.now(timezone.utc)`
- **Next milestone:** end-to-end migrate task01 and task02 to green + generate patch

## When unsure

If a change would touch a data contract, a functional boundary, the test oracle, or a dependency version — stop and ask the human. Prefer the smallest correct change. Correctness and reproducibility beat cleverness.
