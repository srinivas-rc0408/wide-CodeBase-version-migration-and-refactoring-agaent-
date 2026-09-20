# Product Requirements Document (PRD)
### Codebase-Wide Version Migration & Refactoring Agent (MRA)

| Field | Value |
|---|---|
| **Author** | Srinivas RC | **Guide** | Dr Nimrita Koul |
| **Version** | 0.1 | **Date** | 24 August 2026 |
| **Status** | Draft |

> **Relationship to other docs (read this):** for a research project the PRD overlaps with the Project Charter. This PRD is deliberately kept to a **one-page "what/why/for-whom/done"** framing that sits *above* the technical docs. Detailed scope lives in the [Charter](docs/01_PROJECT_CHARTER.md); requirements in the [SRS](docs/03_SRS.md); design in the [Architecture doc](docs/04_ARCHITECTURE_HLD_LLD.md). Do not duplicate those here.

---

## 1. Problem
Upgrading a real codebase across a breaking library/language change is cross-file and partly semantic: one changed contract breaks many callers, and some breaks surface only at test time. Deterministic tools apply fixed rules and cannot reason across files or recover from failure; generic LLM agents edit in unsafe order and cannot reliably verify their own changes.

## 2. Goal
Deliver an autonomous agent that migrates a multi-module Python codebase across a specified version change **correctly and verifiably** — finding every affected call site, editing in a safe order, and self-correcting against the test suite until it passes — and quantify its quality on completeness, test-pass-rate, and cost.

## 3. Non-goals
Not a general coding assistant; not a product/website; not multi-language; not a business-logic rewriter; not a test generator. It performs *specified* version migrations on Python repos with an existing passing test suite. (Full boundaries: SRS §5.)

## 4. Users / personas
| Persona | Need | How the MRA serves it |
|---|---|---|
| **Operator** (the student) | Run a migration and get a scored result | CLI: repo + task in → patch + trajectory + metrics out |
| **Evaluator** (the guide) | Judge correctness and rigor | Deterministic metrics, ablations, audit trajectory, paper |
| **Downstream reader** (recruiter / researcher) | Understand the contribution fast | README, one-sentence story, paper, clean repo |

## 5. User stories
- *As the operator*, I give the agent a repo and a migration contract, and it returns a green, migrated repo plus a unified `.patch`.
- *As the operator*, when an edit breaks a test, the agent diagnoses the trace, patches it, and re-tests without my intervention.
- *As the operator*, I can read exactly what the agent did and why from the trajectory log.
- *As the evaluator*, I can reproduce any run and see M1/M2/M3 for every task and ablation.

## 6. Scope (in / out)
**In:** the 5-stage agent (MAP/PLAN/EDIT/TEST/CORRECT); 3–5 migration tasks (T1 datetime → T5 SQLAlchemy 2.0); Tier A controlled corpus + Tier B real repo(s); benchmarking report; paper.
**Out:** everything in §3 and SRS §5.

## 7. Success metrics
| Metric | Definition (formal: Data & Evaluation Protocol) | Target |
|---|---|---|
| **M1 — Migration Completeness** | recall / precision / F1 over affected call sites | TBD with guide (e.g. F1 ≥ X%) |
| **M2 — Test Pass Rate** | % of suite passing post-migration (green precondition) | 100% on Tier A |
| **M3 — Token / Step Overhead** | tokens, tool calls, cost per completed task | Report + minimize |
| **Headline result** | Ablation: with vs without the recovery loop | Recovery loop shows large M2 gain |

## 8. Milestones (release plan)
| Milestone | Definition of done |
|---|---|
| M0 Skeleton | Dockerized `pytest`+`git` tools; agent reads a test result |
| M1 Analyzer | Call sites + dep graph match ground truth on T1 |
| M2 Edit+verify | One file migrated, tested, scored end-to-end |
| M3 Recovery | Injected break auto-repaired to green within N attempts |
| M4 Multi-file | Full repo migrated with state tracker + summarization |
| M5 Benchmark | All tasks run, metrics + ablations + failure analysis |
| M6 Paper | Manuscript drafted and submitted |

## 9. Dependencies & assumptions
LangGraph 1.x · libcst · networkx · pytest/ruff · Docker/Podman · DeepSeek V4 API (key + budget). Target repos have a green pre-migration suite. Compute per guide. (Stack detail: Resource Pack.)

## 10. Risks
Recovery loop under-built (loses ~80% of value) · context/token blow-up on long horizons · semantic breaks passing unit tests · corpus without ground truth · scope creep on real repos. Mitigations: Charter §8.
