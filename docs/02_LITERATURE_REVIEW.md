# Literature Review & State of the Art
### Codebase-Wide Version Migration & Refactoring Agent (MRA)

| Field | Value |
|---|---|
| **Document** | Literature Review / SOTA (Deliverable D2) |
| **Author** | Srinivas RC | **Guide** | Dr Nimrita Koul |
| **Version** | 0.1 (Draft) | **Date** | 24 August 2026 |
| **Status** | For guide review |

**Revision history**

| Ver | Date | Change |
|---|---|---|
| 0.1 | 24 Aug 2026 | Initial draft; SOTA descriptions verified against primary sources (Aug 2026) |

> Scope of this review: it establishes the academic value of the project by showing (a) what deterministic refactoring tools can and cannot do, (b) how modern LLM-based software-engineering agents are structured and where they fall short for *version migration specifically*, and (c) how the field evaluates such systems. It closes by positioning the MRA in that landscape.

---

## 1. Problem framing: version migration vs. issue resolution

Most published LLM software-engineering systems target **issue resolution** — given a natural-language bug report and a repository, produce a patch that makes a hidden test pass. Version migration is a related but distinct problem:

- The change is **specified by an upgrade contract** (the library's migration guide), not by a bug report. This is an advantage: the "what" is knowable in advance.
- The change is **cross-cutting** — the same deprecated pattern recurs across many files, and one contract change breaks many callers.
- Correctness is partly **semantic** — some breaks never raise on import and surface only as failing behaviour, so a verification loop is mandatory, not optional.

This framing matters because it lets the MRA borrow the strongest ideas from issue-resolution research (dependency-aware localization, diff-format patches, test-based validation) while adding what those systems lack: an explicit dependency graph driving safe **edit ordering** across files, and a migration contract as the planning input.

## 2. Deterministic refactoring tools — the baselines

These tools are fast, exact, and free of hallucination, but they apply only rules a human pre-programmed. They are the MRA's baselines, not its competitors.

| Tool | What it does | Limitation for migration |
|---|---|---|
| **`2to3`** | Fixed library of Python 2→3 fixers over the AST. | Single hard-coded migration; not extensible to arbitrary library upgrades; no verification. |
| **`pyupgrade`** | Rewrites older Python idioms to newer syntax (typing, f-strings, etc.) by version flag. | Pattern-bounded; cannot handle library API migrations or cross-file contract breaks; no test loop. |
| **`ruff` (`UP` rules)** | Extremely fast linter/fixer; the `UP` rule set overlaps `pyupgrade`. | Same class limitation; rule-bounded, single-file, no semantic verification. |
| **`libcst` codemods** | Concrete-syntax-tree transforms that **preserve formatting/comments**; can express complex, custom rewrites. | Each codemod is hand-written per migration; the transform itself does no cross-file reasoning and no self-correction. |

**Key insight the MRA exploits:** `libcst` is not a competitor — it is a *tool the agent uses*. Deterministic edits (e.g. a mechanical method rename) should be codemods (exact, zero-token); the LLM is reserved for the ambiguous, context-dependent edits and for repairing failures. This hybrid is cheaper and more reliable than an all-LLM approach.

## 3. LLM-based software-engineering systems — the SOTA

The field split into two camps: **autonomous agents** that decide their own actions in a loop, and **pipeline ("agentless")** methods that fix the control flow and only use the LLM for bounded sub-tasks.

### 3.1 SWE-agent — the Agent-Computer Interface (ACI)
*Yang, Jimenez, Wettig, Lieret, Yao, Narasimhan, Press. "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering." NeurIPS 2024. arXiv:2405.15793 (Princeton PLI).*

SWE-agent's contribution is the **ACI**: a purpose-built command interface (view file, search, edit a chunk, run) designed for an LLM rather than a human, plus informative feedback after each command. The agent runs a **ReAct-style loop** — think, act, observe — and the paper shows that interface design (concise commands, clear error messages, guard rails) materially changes agent success. Its early result (~12.5% on the full SWE-bench, vs ~3.8% for retrieval-augmented baselines at the time) established that a well-designed interaction layer, not just a bigger model, drives agent performance.

**Relevance to MRA:** the ACI lesson — that the agent's tools and their feedback format determine success — directly informs the MRA's tool layer (structured `pytest`-JSON feedback, deterministic codemods, a clean file-status view). **Gap:** SWE-agent targets single-issue resolution and does not build an explicit cross-file dependency graph to order edits, which is central to migration.

### 3.2 OpenHands (formerly OpenDevin) — CodeAct and the event stream
*Wang et al. "OpenHands: An Open Platform for AI Software Developers as Generalist Agents." ICLR 2025. arXiv:2407.16741. MIT license.*

OpenHands is a general agent platform. Two ideas are relevant. First, **CodeAct**: instead of exposing many bespoke JSON tools, give the agent bash + Python + a browser and let it express any action as executable code — empirically this generalises better and reduces parsing errors, at the cost of relying on a strong code-generating model. Second, the **event-stream architecture**: user, agent, and a Docker-sandboxed runtime never call each other directly; each reads from and appends to one chronological log, so every run is replayable by construction and the agent reduces to a pure function `step(state) → action` looped until done. Reported performance reached the ~70s% range on SWE-bench Verified with frontier models by 2026.

**Relevance to MRA:** the event stream is the same idea as the MRA's **checkpointer-as-audit-log** — persist every transition so the trajectory is a first-class, replayable deliverable. The Docker-sandboxed runtime is the MRA's sandbox. **Gap:** OpenHands is a *generalist* platform; it does not specialise in contract-driven, dependency-ordered migration, and its "give it a shell" action space is deliberately unconstrained, which is riskier and less inspectable than a bounded state machine for a graded academic build.

### 3.3 Agentless — the pipeline counter-argument
*Xia, Deng, Dunn, Zhang. "Agentless: Demystifying LLM-based Software Engineering Agents." FSE 2025. arXiv:2407.01489.*

Agentless asks whether full autonomy is necessary and answers "often not." It fixes a **three-phase pipeline — hierarchical localization → repair → patch validation** — without letting the LLM choose future actions. Localization narrows from files to classes/functions to exact edit lines; repair samples multiple candidate diffs; validation runs regression and reproduction tests, then re-ranks. It reached the top open-source result on SWE-bench Lite at the time (~32%) at very low cost (well under a dollar per issue), and was adopted by OpenAI and DeepSeek as an evaluation harness.

**Relevance to MRA:** Agentless validates two MRA design choices — (1) **localize before you edit** (the MRA does this with a static dependency graph, which is even stronger than heuristic localization because the migration pattern is known), and (2) **validate patches with tests and re-rank**, which is the MRA's TEST/CORRECT loop. **Gap:** Agentless is stateless per issue and does not manage long-horizon, cross-file state across dozens of coupled edits — precisely the memory problem the MRA must solve.

### 3.4 Summary comparison

| System | Control model | Cross-file dependency graph | Self-verification loop | Explicit long-horizon memory | Specialised for migration |
|---|---|---|---|---|---|
| `pyupgrade` / `ruff` / `2to3` | Fixed rules | No | No | No | No (fixed patterns) |
| `libcst` codemod | Fixed transform | No (single tree) | No | No | Partly (custom rules) |
| SWE-agent | Autonomous (ReAct + ACI) | No (implicit) | Partial (runs tests) | Conversation history | No |
| OpenHands / CodeAct | Autonomous (code actions) | No (implicit) | Yes (test in loop) | Event stream | No |
| Agentless | Fixed pipeline | Heuristic localization | Yes (validate + re-rank) | No (stateless) | No |
| **MRA (this project)** | **Explicit state machine (LangGraph)** | **Yes (`libcst` + `networkx`, topological order)** | **Yes (TEST↔CORRECT loop)** | **Yes (`MigrationState` + summaries)** | **Yes (contract-driven)** |

## 4. Evaluation methodology in the field

The community standard is **execution-based** evaluation, established by SWE-bench.

*Jimenez, Yang, et al. "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" 2024.* SWE-bench provides 2,294 task instances drawn from real GitHub issues and their fixing pull requests across 12 popular Python repositories. An agent receives the issue and repository state and must emit a **git-diff patch**; success is decided by whether the repository's **test suite passes** after the patch is applied in a **containerized (Docker) harness**. **SWE-bench Verified** is a 500-instance, human-filtered subset that removes under-specified or unfair tasks; frontier systems reported roughly 54–81%+ on it through 2025–2026, and independent audits note contamination and test-design caveats as scores approach saturation.

**Why this is the MRA's template:** the MRA's evaluation is structurally identical — repository + migration contract → git-diff patch → test suite must pass in Docker — with two additions the MRA can measure that issue-resolution benchmarks cannot: **Migration Completeness** against a hand-authored ground truth (§Data Protocol M1), and **token/step overhead** per task (M3). The MRA also adopts SWE-bench's most rigorous idea for its Tier B corpus: **the human migration pull-request is the gold patch**, and its parent commit is the "before" state.

## 5. Positioning and the research gap

The literature shows that (a) deterministic tools cannot reason across files or recover from failure; (b) autonomous agents (SWE-agent, OpenHands) can edit and test but do not build an explicit dependency graph to order migration edits and keep their long-horizon state implicit; and (c) pipeline methods (Agentless) validate patches but are stateless per task.

**The gap the MRA fills:** a **contract-driven, dependency-graph-ordered, self-correcting agent specialised for cross-file version migration**, with an explicit, inspectable state machine and a compact persistent memory, evaluated on completeness, test-pass-rate, and cost. No surveyed system combines all four of: a real cross-file dependency graph for edit ordering, a test-driven recovery loop, explicit long-horizon memory, and a migration-contract planning input. Demonstrating this combination — and quantifying, via ablation, how much the recovery loop and the dependency ordering each contribute — is the project's academic contribution.

## 6. Primary references

1. Jimenez, C. E., Yang, J., et al. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* 2024. arXiv:2310.06770.
2. Chowdhury, N., et al. (OpenAI). *Introducing SWE-bench Verified.* 2024.
3. Yang, J., Jimenez, C. E., et al. *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.* NeurIPS 2024. arXiv:2405.15793.
4. Wang, X., et al. *OpenHands: An Open Platform for AI Software Developers as Generalist Agents.* ICLR 2025. arXiv:2407.16741.
5. Xia, C. S., et al. *Agentless: Demystifying LLM-based Software Engineering Agents.* FSE 2025. arXiv:2407.01489.
6. SQLAlchemy. *SQLAlchemy 2.0 — Major Migration Guide.* Official docs (en/20/changelog/migration_20).
7. Pydantic. *Migration Guide (v1 → v2).* Official docs (latest/migration).
8. Instagram/Meta. *LibCST — Codemods.* Official docs.
9. `pyupgrade`, `ruff` (`UP` rules) — tool documentation, used as deterministic baselines.

*(Verify arXiv IDs and page numbers against the primary source before final submission; SOTA numbers move — cite the version/date you used.)*
