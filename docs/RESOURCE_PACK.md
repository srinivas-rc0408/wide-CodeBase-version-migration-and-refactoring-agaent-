# Migration Agent — Master Resource Pack
### Everything verified, everything you need to execute. Companion to your locked brief.
**Compiled:** 24 Aug 2026. **Owner:** Srinivas RC. **Guide:** Dr Nimrita Koul.

> How to use this file: your brief tells you *what* to build and *in what order*. This file gives you the *verified current stack*, the *actual migration data your agent must handle*, the *corpus*, the *eval harness*, and *reference code for the hard parts*. Drop this into your repo as `docs/RESOURCE_PACK.md`. Everything version-sensitive here was checked on the web on 24 Aug 2026 — re-pin at install time.

---

## 0. Read this first — the one thing that will sink you

Do not spend two weeks "gathering resources." You have them now. The graded parts of this project are the **recovery loop** and the **dependency graph**, and the thing that makes it *publishable* is a **rigorous corpus with ground truth**. Everything else is plumbing. Build the corpus and the loop; treat the rest as done.

Your stated weak point is communicating technical work. This project is a technical monster, which means the *paper*, the *viva*, and your *one-sentence interview story* are where you win or lose — not the code. Budget real time for them from week 1, not week 9.

---

## 1. Verified stack (checked 24 Aug 2026)

Pin the latest patch of each at install time. The **major-version facts below are verified** — those are the ones that break tutorials.

| Layer | Package | Verified fact (Aug 2026) | Install |
|---|---|---|---|
| Agent framework | `langgraph` | **1.x is current.** 0.x in maintenance until Dec 2026. Build v1 patterns. | `pip install -U langgraph` |
| Checkpointer | `langgraph-checkpoint-sqlite` | SQLite saver is fine for your scale (single run, not concurrent load). Matches your existing FastAPI+SQLite muscle memory. | `pip install -U langgraph-checkpoint-sqlite` |
| Refactor engine | `libcst` | Codemod API stable (`VisitorBasedCodemodCommand`, `AddImportsVisitor`, `parallel_exec_transform_with_prettyprint`). Preserves formatting/comments — this is why you use it over `ast`. | `pip install -U libcst` |
| Analysis (alt) | `tree-sitter`, `tree-sitter-python` | Use for language-agnostic parsing if you ever go beyond Python. For a Python-only project, `libcst` alone is enough. | `pip install -U tree-sitter tree-sitter-python` |
| Dep graph | `networkx` | Build + topologically sort the import/call graph. | `pip install -U networkx` |
| Test runner | `pytest` | Your verifier. Capture JSON via `--json-report` (`pytest-json-report`) so the agent parses results as data, not scraped text. | `pip install -U pytest pytest-json-report` |
| Linter | `ruff` | Fast, single binary. Its `UP` rules also double as a **baseline** to compare your agent against for the py3.x modernization task. | `pip install -U ruff` |
| Git | `GitPython` | Snapshots, rollback, and generating the unified `.patch` deliverable. Raw `git` via subprocess also fine. | `pip install -U GitPython` |
| Sandbox | Docker + `docker` SDK | One container per run. Non-negotiable — see §8. | `pip install -U docker` |
| LLM (edits) | DeepSeek **V4-Pro** | ~81% SWE-bench Verified, OpenAI-compatible, 1M ctx, auto prompt caching, 5M free tokens on signup. | OpenAI SDK, `base_url=https://api.deepseek.com` |
| LLM (cheap) | DeepSeek **V4-Flash** | ~$0.14–0.22 /M input, ~$0.28–0.66 /M output (peak/off-peak). Use for summaries + failure classification to control token overhead. | same endpoint, model `deepseek-v4-flash` |

**Model routing rule (reuse your White Cat multi-model router):** strong model for *edits and stack-trace reasoning*, cheap model for *classification and rolling summaries*. Log tokens per call — token overhead is a graded metric.

**Pricing note (verify before you budget):** DeepSeek moved to peak/off-peak billing (peak = 01:00–04:00 and 06:00–10:00 UTC, ~2× off-peak). Off-peak V4-Flash ≈ $0.22/M in, $0.66/M out; V4-Pro ≈ $0.66/M in, $1.98/M out. Cache hits are ~1/10 to 1/100 of input — your repo context and system prompt are a stable prefix, so cache them. Confirm current numbers at `api-docs.deepseek.com`.

**Framework decision — LangGraph, not Claude Agent SDK. Here's why, and defend it in your viva:**
The Claude Agent SDK ("Claude Code as a library") *hides the tool loop* — Claude runs edit→test→correct for you. That is exactly wrong for this project, because **the loop is what's being graded.** LangGraph makes the state machine *explicit*: your file-status tracker literally *is* the graph state, its checkpointer *is* your trajectory/audit log, and you get deterministic control over ordering, retries, and stop conditions. You want to *own* the loop and *show* it. Use LangGraph. (You can still call any LLM inside a node — the two are not exclusive.)

---

## 2. The migration targets — the actual data your agent must handle

Pick 3–5 in rising difficulty (confirm the final list with Dr Koul). For each, the **official migration guide IS your migration spec** — feed it to the planner as context. Below is the concrete breaking-change data so you can (a) build controlled repos and (b) score completeness.

### 2.1 `datetime.utcnow()` → timezone-aware (EASY — build this first)
- **Why:** `datetime.utcnow()` and `datetime.utcfromtimestamp()` are deprecated since **Python 3.12** (they return naive datetimes, a bug magnet).
- **The transform:**
  - `datetime.utcnow()` → `datetime.now(timezone.utc)`
  - `datetime.utcfromtimestamp(t)` → `datetime.fromtimestamp(t, timezone.utc)`
  - add `from datetime import timezone` (or use `datetime.UTC`, Python 3.11+)
- **The trap that teaches the whole project:** `datetime.utcnow()` (from `from datetime import datetime`) vs `datetime.datetime.utcnow()` (from `import datetime`) vs an aliased import. A dumb find-replace breaks on all three. Your **static analyzer must resolve scope/imports** to find real call sites. This one task justifies the entire dependency-graph component.

### 2.2 Python 3.8 → 3.12 modernization (EASY–MEDIUM, has a baseline)
- **Transforms:** `typing.List`→`list`, `typing.Dict`→`dict`, `typing.Optional[X]`→`X | None`, `typing.Union[A,B]`→`A | B`, old `%`/`.format()`→f-strings, `open(...).read()` context managers, etc.
- **Baseline to beat:** `pyupgrade --py312-plus` and `ruff check --select UP`. Report your agent's completeness *against* these tools. Beating or matching a deterministic tool on a fuzzy superset is a clean paper result.

### 2.3 `requests` → `httpx` (MEDIUM)
- Mostly drop-in, with sharp edges that make good test cases:
  - `requests.Session()` → `httpx.Client()` (context-manager preferred)
  - **`allow_redirects=True` → `follow_redirects=True`, and httpx defaults redirects to `False`** — silent behavior change, great for testing your verifier catches semantic (not just syntactic) breakage.
  - `timeout` is required-ish in httpx (has a default but semantics differ); naive migration changes behavior.
  - `resp.json()`, `params=`, `json=`, `data=` mostly identical.
  - async path: `httpx.AsyncClient` — optional stretch.

### 2.4 Pydantic v1 → v2 (HARD, well-documented — strong choice)
Official guide: `docs.pydantic.dev/latest/migration/`. Core breaking changes (this is your completeness checklist):
- Method renames on models: `.dict()`→`.model_dump()`, `.json()`→`.model_dump_json()`, `.parse_obj()`→`.model_validate()`, `.parse_raw()`→`.model_validate_json()`, `.copy()`→`.model_copy()`, `.schema()`→`.model_json_schema()`, `.construct()`→`.model_construct()`, `__fields__`→`model_fields`.
- Validators: `@validator`→`@field_validator` (now needs `@classmethod`), `@root_validator`→`@model_validator`.
- Config: `class Config:` → `model_config = ConfigDict(...)`. `orm_mode=True`→`from_attributes=True`. `allow_population_by_field_name`→`populate_by_name`. `allow_mutation=False`→`frozen=True`.
- Field args: `min_items/max_items`→`min_length/max_length`, `regex`→`pattern`, `const` removed.
- **Semantic trap:** in v2, `Optional[x]` **no longer implies a default of `None`** — you must write `x: Optional[int] = None`. Miss this and models that "worked" now raise on construction. Perfect verifier bait.
- `BaseSettings` moved to the separate `pydantic-settings` package.
- `GenericModel` removed (`BaseModel` is generic now).

### 2.5 SQLAlchemy 1.4 → 2.0 (HARDEST — the spec's own example)
Official guides: "SQLAlchemy 2.0 - Major Migration Guide" and "What's New in 2.0" (`docs.sqlalchemy.org/en/20/changelog/migration_20.html`). Note **2.1 now exists** but 1.4→2.0 remains the canonical, best-documented jump. Core changes:
- **`session.query(...)` (Query API) is legacy** → `select()` + `session.execute(...)`, then `.scalars().all()` / `.scalar_one()`.
- **`engine.execute(...)` removed** → open a connection explicitly; wrap raw SQL in `text()`; `conn.execute(...)`.
- **Autocommit removed** → explicit `with engine.begin() as conn:` / `session.commit()`.
- Declarative modernization: `declarative_base()` → subclass `DeclarativeBase`; typed columns `Mapped[int] = mapped_column(...)`.
- Strategy the guide itself recommends (and you should mirror in your agent's plan): get code running on 1.4 with `SQLALCHEMY_WARN_20=1`, fix every deprecation warning, *then* flip to 2.0. That warning stream is a free, structured to-do list your agent can consume.

---

## 3. Your corpus — how to get data with ground truth

You need codebases with **real breaking changes AND passing test suites**. Two tiers. Build A first; it's your scientific control.

### 3.1 Tier A — controlled repos you author (your gold standard)
Author 3–5 small multi-module Python packages. Each one, this exact shape:

```
task01_datetime/
├── old/                      # runs & passes pytest on the OLD API
│   ├── src/pkg/
│   │   ├── __init__.py
│   │   ├── core.py           # contains datetime.utcnow() call sites
│   │   ├── models.py         # imports core -> creates a dependency edge
│   │   └── utils.py          # another caller (cross-file breakage)
│   └── tests/
│       ├── test_core.py
│       └── test_models.py
├── gold/                     # the CORRECT migrated version (hand-written)
│   └── ... (same tree, migrated)
├── ground_truth.json         # every affected call site: file, line, symbol
└── task.yaml                 # {id, description, source_api, target_api, difficulty}
```

Rules that give you a real benchmark (steal the discipline from your QASPER work):
- The test suite **must pass on `old/`** before migration, or Test-Pass-Rate is meaningless.
- `ground_truth.json` lists **every** affected call site → this is what Migration-Completeness scores against.
- `gold/` is hand-verified correct → diff the agent's output against it.
- Vary **one thing at a time** across tasks: number of files, number of call sites, whether the change is purely syntactic or semantic.
- Deliberately include **cross-file breakage** (function signature change in file A breaks callers in B and C). Without this, the dependency graph is untested and the project is a toy.

### 3.2 Tier B — real OSS repos (external validity)
The pro move most students miss: **the migration PR in a real repo's git history is your ground truth.**
1. Find a real project that actually did one of your migrations (search its history/changelog for "SQLAlchemy 2.0", "pydantic v2", "migrate to httpx").
2. Take the **parent commit** of that PR as your "old" state (checkout by SHA/tag).
3. The **merged PR diff** is the human "gold patch."
4. Run your agent on the old commit; score its patch against the human patch and against the repo's own test suite.

This is exactly how **SWE-bench** is built (real GitHub issue + real fixing PR + real test suite) — cite that parallel in your paper. Good hunting grounds: repos already in SWE-bench's 12 source projects (django, flask, requests, sympy, scikit-learn, etc.), plus any well-tested mid-size library. Always verify the repo's *current* state before committing — check out a fixed old tag so your corpus is reproducible.

---

## 4. Evaluation harness — define it before you build (like a scientist)

Three metrics, straight from the spec. Precise definitions + how to compute them.

**M1 — Migration Completeness (%)** = (call sites correctly updated) / (total affected call sites).
Needs `ground_truth.json`. "Correctly updated" = the site matches `gold/` semantics, not just "changed."

**M2 — Post-Migration Test Pass Rate (%)** = (tests passing after migration) / (total tests).
Suite must pass on `old/` first. Run inside the sandbox; parse the JSON report.

**M3 — Token / Step Overhead** = total tokens (in+out, per model) and total tool calls per completed task. Log every LLM call and every tool call. Report cost too (tokens × current price).

Reference computation:

```python
import json, subprocess

def migration_completeness(agent_sites: set, ground_truth_path: str) -> float:
    gt = json.load(open(ground_truth_path))
    gt_sites = {(s["file"], s["line"], s["symbol"]) for s in gt["call_sites"]}
    correct = agent_sites & gt_sites
    return 100.0 * len(correct) / max(len(gt_sites), 1)

def test_pass_rate(repo_dir: str) -> float:
    # run in the sandbox; requires pytest-json-report
    subprocess.run(
        ["pytest", "--json-report", "--json-report-file=/tmp/rep.json", repo_dir],
        capture_output=True,
    )
    rep = json.load(open("/tmp/rep.json"))
    s = rep["summary"]
    total = s.get("total", 0)
    passed = s.get("passed", 0)
    return 100.0 * passed / max(total, 1)
```

Generate the `.patch` deliverable (unified git diff across the whole repo):

```python
from git import Repo
def make_patch(repo_dir: str, out="migration.patch") -> str:
    repo = Repo(repo_dir)
    diff = repo.git.diff()          # working tree vs HEAD, after edits
    open(out, "w").write(diff)
    return out
```

**Run the ablations that make the paper:** with vs without the recovery loop; strong vs cheap edit model; batch size 1 vs N; with vs without dependency-graph ordering. Report failures honestly — the failure analysis is what makes it publishable and what a viva panel will grill you on.

---

## 5. The state schema (your "graph-based memory")

This is the heart of the memory component. Keep it small enough to stay under the token budget — you never feed the whole thing to the LLM; you feed a *summary* of it.

```python
from typing import TypedDict, Literal, Annotated
from operator import add

FileStatus = Literal["pending", "in_progress", "migrated", "partial", "verified", "failed"]

class MigrationState(TypedDict):
    repo_path: str
    task: str                          # human-readable migration spec
    target_pattern: str                # e.g. "datetime.utcnow"
    call_sites: dict                   # file -> [ {line, symbol, context} ]  (from MAP)
    dep_graph: dict                    # file -> [files importing it]         (from MAP)
    edit_batches: list                 # ordered list of file batches         (from PLAN)
    file_status: dict                  # file -> FileStatus
    current_batch: int
    last_test_report: dict             # {passed, failed, failures:[{test, trace}]}
    fix_attempts: dict                 # failure_signature -> count  (for N-retry stop)
    trajectory: Annotated[list, add]   # append-only audit log (this IS your deliverable log)
    done: bool
```

**Context-budget rule:** the LLM edit node receives only (a) the file being edited, (b) the target pattern, (c) the relevant slice of the dep graph, and (d) a one-line rolling summary of what's done/pending. Never the full state. Summaries are produced by the *cheap* model. Build this from Phase 4, not as an afterthought — long horizons blow context, and token overhead is graded.

---

## 6. The agent loop (LangGraph v1 skeleton)

Correct-shaped reference. Fill the node bodies as you build phases.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

MAX_FIX_ATTEMPTS = 3

def map_node(state):        ...   # static analysis -> call_sites + dep_graph
def plan_node(state):       ...   # topological sort -> edit_batches
def edit_node(state):       ...   # apply next batch (libcst codemod or LLM edit)
def test_node(state):       ...   # run pytest+ruff in sandbox -> last_test_report
def correct_node(state):    ...   # parse trace -> locate broken contract -> patch

def route_after_test(state) -> str:
    report = state["last_test_report"]
    if report["failed"] == 0:
        # batch is green
        if state["current_batch"] + 1 >= len(state["edit_batches"]):
            return "done"
        return "next_batch"
    sig = report["failures"][0]["signature"]
    if state["fix_attempts"].get(sig, 0) >= MAX_FIX_ATTEMPTS:
        return "give_up"          # log + flag for human
    return "correct"

g = StateGraph(MigrationState)
g.add_node("map", map_node)
g.add_node("plan", plan_node)
g.add_node("edit", edit_node)
g.add_node("test", test_node)
g.add_node("correct", correct_node)

g.add_edge(START, "map")
g.add_edge("map", "plan")
g.add_edge("plan", "edit")
g.add_edge("edit", "test")
g.add_conditional_edges("test", route_after_test, {
    "correct": "correct",
    "next_batch": "edit",
    "done": END,
    "give_up": END,
})
g.add_edge("correct", "test")     # re-test after every corrective patch

with SqliteSaver.from_conn_string("state.db") as saver:
    app = g.compile(checkpointer=saver)   # checkpointer = your trajectory log
```

Stop conditions (from your brief, encoded above): all batches done AND suite green → success; same failure N times → give up, log, flag. The checkpointer persists every node transition — that's your **execution trajectory / state audit log** deliverable, for free.

---

## 7. A real, working libcst codemod (the datetime starter)

Deterministic edits should be codemods, not LLM calls (cheaper, exact, no token overhead). This one is runnable. Note the caveat — it's why you need the analyzer.

```python
import libcst as cst
import libcst.matchers as m
from libcst.codemod import VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor

class ConvertUtcnowCommand(VisitorBasedCodemodCommand):
    DESCRIPTION = "Replace datetime.utcnow() with datetime.now(timezone.utc)."

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call):
        # matches `datetime.utcnow()` i.e. from `from datetime import datetime`
        if m.matches(
            updated_node,
            m.Call(
                func=m.Attribute(value=m.Name("datetime"), attr=m.Name("utcnow")),
                args=[],
            ),
        ):
            AddImportsVisitor.add_needed_import(self.context, "datetime", "timezone")
            return updated_node.with_changes(
                func=cst.Attribute(value=cst.Name("datetime"), attr=cst.Name("now")),
                args=[cst.Arg(value=cst.Attribute(
                    value=cst.Name("timezone"), attr=cst.Name("utc")))],
            )
        return updated_node
```

Run it: `python -m libcst.tool codemod convert_utcnow.ConvertUtcnowCommand ./src`

**Caveat = the whole point:** this only catches `datetime.utcnow()`. It misses `datetime.datetime.utcnow()` (from `import datetime`) and aliased imports (`import datetime as dt`). A robust migration must resolve imports/scope *before* editing — which is your static analyzer + dependency graph. State this limitation explicitly in your paper; it demonstrates you understand why the hard 80% exists.

---

## 8. The sandbox (Docker from day one)

Never let the agent edit and run code on your bare machine. Minimal image:

```dockerfile
# Dockerfile.sandbox
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pytest pytest-json-report ruff
WORKDIR /work
# repo is bind-mounted at run time, not baked in
```

Run pattern: one container per agent run; bind-mount the repo copy; `git` snapshot at start so any batch is reversible; capture pytest JSON to a mounted path. On CachyOS/Arch you already have Docker in muscle memory from health-risk-mlops — reuse it. This also makes your runs reproducible for the paper.

---

## 9. Key docs & papers to collect (with what to get from each)

**Official migration guides (these ARE your migration specs — read the one you pick):**
- SQLAlchemy 2.0 Major Migration Guide — `docs.sqlalchemy.org/en/20/changelog/migration_20.html`
- Pydantic v2 Migration Guide — `docs.pydantic.dev/latest/migration/`
- httpx "Compatibility with requests" — httpx docs, the requests-comparison page
- Python 3.12 "What's New" (datetime deprecations) — `docs.python.org/3/whatsnew/3.12.html`

**Tooling docs:**
- LibCST Codemods tutorial + Codemods reference — `libcst.readthedocs.io/en/latest/codemods.html`
- LangGraph docs (StateGraph, conditional edges, checkpointers) — build v1 patterns
- networkx (topological_sort, DiGraph)
- pyupgrade / ruff `UP` rules — your baselines

**Papers for the related-work section (get 2–4):**
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** (Jimenez et al.) — the founding benchmark; your eval design mirrors it (repo + issue → git diff patch → test suite passes in Docker). Cite it as your methodological template.
- **SWE-bench Verified** (OpenAI, 2024) — the human-filtered 500-task subset; explains why curation matters. Note OpenAI's 2026 post arguing Verified is saturating — use it to justify *your* controlled corpus.
- One agent-scaffold paper (OpenHands/CodeAct, Agentless, or SWE-agent) — for how others structure the plan→edit→test loop.
- Optional: a "why code agents fail at issue resolution" empirical paper — feeds your failure analysis framing.

**Baselines to name in the paper:** `pyupgrade`, `2to3`, `ruff --fix`. Your agent's pitch is: it handles the *fuzzy, cross-file, semantic* cases these deterministic tools can't, and it *verifies itself*.

---

## 10. Trap checklist (expanded with the version facts I found)

- **Skipping the recovery loop** → fancy find-replace. It's ~80% of the grade.
- **No dependency graph** → circular regressions, agent chasing its tail.
- **Ignoring token budget** → build summarization in Phase 4, log tokens from Phase 0.
- **Toy files only** → the spec wants *multi-file*. Prove it on a real multi-module repo (Tier B).
- **No sandbox** → Docker from day one.
- **Building big before end-to-end** → ship tiny and working by Phase 2.
- **NEW — scaffolding on LangGraph 0.x** → use v1; 0.x is maintenance-only.
- **NEW — assuming Pydantic v3** → it isn't out; v1→v2 is still the right target.
- **NEW — dumb find-replace on `utcnow`** → misses `datetime.datetime.utcnow()` and aliases; forces the analyzer.
- **NEW — treating syntactic pass as success** → the httpx `follow_redirects` default flip and Pydantic `Optional` change are *semantic* breaks; only the test suite catches them. Good news: that's your M2 metric earning its keep.

---

## 11. Questions for Dr Nimrita Koul (first meeting) — refined

1. **"510 tasks" — confirm it's 5–10, not five hundred.** Changes corpus size entirely.
2. Which migration target(s) — pick from the menu (datetime → py3.12 → httpx → Pydantic v2 → SQLAlchemy 2.0), or hers?
3. Is the **research paper** a hard deliverable? Which venue and deadline?
4. Team size — solo or group? Module ownership?
5. Compute limits — is your machine + free-tier DeepSeek (5M tokens) + Colab enough, or is there a budget?
6. Success threshold for Migration Completeness — what % counts as "done"?
7. Does she want **Tier B (real OSS repo)** results, or are controlled repos sufficient for the grade?

---

## 12. The paper plan (start the skeleton in week 1, not week 9)

**Why now:** writing the eval section first *forces* you to define metrics precisely, which improves the build. This is also the deliverable that trains your weak point.

**Structure (standard systems/ML-for-SE paper):**
1. Abstract + Intro — the problem (cross-file, long-horizon, self-verifying migration) and your contribution.
2. Related work — SWE-bench + agent scaffolds + deterministic tools (pyupgrade/2to3).
3. System — your six components + the state machine diagram (draw it from memory; if you can't, you can't defend it).
4. Corpus — controlled + real, with ground-truth methodology.
5. Metrics — M1/M2/M3, defined exactly.
6. Results + **ablations** (with/without recovery loop is the headline).
7. Failure analysis — the honest part that makes it real.
8. Limitations + future work.

**Realistic venues for an Indian UG major project** (confirm with your guide): an IEEE/ACM student or regional conference, a workshop track, or arXiv preprint + a journal like a Scopus-indexed SE/AI venue. The ablation table + failure analysis is what gets it accepted anywhere.

---

## 13. Your one-sentence story (memorize it — this is the interview weapon)

> "I built an autonomous agent that migrates an entire codebase across a breaking library upgrade — it maps every affected call site with a dependency graph, plans a safe edit order, and runs a test-driven self-correction loop until the suite passes, benchmarked on completeness, test-pass-rate, and token cost."

That sentence maps directly onto what Cursor, Cognition (Devin), and every dev-tools company hires for. Practise saying it in 15 seconds, then in 90 seconds with the architecture, then in 5 minutes with a failure you fixed. That progression *is* interview prep for your weak point.

---

*All version-sensitive facts verified on the web 24 Aug 2026. Re-pin package versions at install. Confirm every project specific with Dr Koul before committing the corpus.*
