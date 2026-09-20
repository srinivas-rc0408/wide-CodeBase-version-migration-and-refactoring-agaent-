# Benchmark results — Tier A

Generated 2026-09-20T17:26:25.912132+00:00 · 3 repeat(s) per (task, config) · mean ±spread across repeats.

Every row is one agent configuration on one task. `baseline` is the reference (recovery on, dependency-ordered batches of 3, deterministic corrector); every other configuration changes exactly one thing about it (docs/05 §3).

## 1. Per task, per configuration

### task01_datetime

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.74 ±0.04 |
| `no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.02 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.02 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.02 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.01 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.74 ±0.11 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.01 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.69 ±0.01 |

### task02_datetime_aliased

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.45 ±0.11 |
| `no-recovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 0.69 ±0.01 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.71 ±0.04 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.43 ±0.17 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.44 ±0.17 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.38 ±0.01 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.38 ±0.02 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.37 ±0.02 |

### task03_half_migration

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.48 ±0.03 |
| `no-recovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 0.73 ±0.01 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.77 ±0.02 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.48 ±0.01 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 1.89 ±0.26 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 1.81 ±0.04 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 1.80 ±0.02 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.54 ±0.18 |

### task04_multimodule

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.23 ±0.01 |
| `no-recovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 1.58 ±0.01 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 7 | 0 | 0.0000 | 1.30 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 3.94 ±0.20 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 3.44 ±0.62 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 3.71 ±0.04 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.30 ±0.19 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.26 ±0.05 |

## 2. Ablations

### A. Recovery loop ON vs OFF — the headline

The only variable is whether the CORRECT loop may run. Both arms use the deterministic corrector, so this contrast is reproducible without an API key: the loop's *mechanics* are what is being measured, not the model's.

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.74 ±0.04 |
| `no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.02 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.45 ±0.11 |
| `no-recovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 0.69 ±0.01 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.48 ±0.03 |
| `no-recovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 0.73 ±0.01 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.23 ±0.01 |
| `no-recovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 1.58 ±0.01 |

### B. Dependency-ordered batching vs arbitrary order

`baseline`/`batch-1` use the FR-3 order; the `order-alphabetical` arms ignore the graph; the `order-fr3-violating` arms are `plan_batches` on the *reversed* graph — dependents before their dependencies, the inversion docs/04 §3.4's pseudocode produces if its missing `.reverse()` is taken literally. Recovery is on in every arm, so an order is charged for in corrective edits (`corr`) and steps before it is charged for in a failed run.

Read the two groups separately. At batch 3 a Tier-A task is only one or two batches wide, so edit order and batch size are confounded — an order that happens to put a producer and its consumer in the same batch never exposes the intermediate state at all. The `-b1` group edits one file per batch, where sequence is the only variable left.

#### batch size 3

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.74 ±0.04 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.02 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.02 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.45 ±0.11 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.71 ±0.04 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.43 ±0.17 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.48 ±0.03 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.77 ±0.02 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.48 ±0.01 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.23 ±0.01 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 7 | 0 | 0.0000 | 1.30 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 3.94 ±0.20 |

#### batch size 1

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.01 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.01 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.74 ±0.11 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.38 ±0.02 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.44 ±0.17 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.38 ±0.01 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 1.80 ±0.02 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 1.89 ±0.26 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 1.81 ±0.04 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.30 ±0.19 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 3.44 ±0.62 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 3.71 ±0.04 |

#### What the data says

Corrective edits per task, one file per batch (lower is better):

- **task01_datetime** — dependency order 0, file-name order 0, dependents-first 0
- **task02_datetime_aliased** — dependency order 1, file-name order 1, dependents-first 1
- **task03_half_migration** — dependency order 1, file-name order 1, dependents-first 1
- **task04_multimodule** — dependency order 2, file-name order 1, dependents-first 3

Two findings, one of them not the expected one.

1. **The dependents-first order is never cheaper and is sometimes the most expensive arm run** — on `task04_multimodule` it spends the full NFR-1 retry ceiling of 3 attempts where the dependency order spends 2, i.e. it finishes one attempt away from failing the task. That is what violating FR-3 costs here: not a wrong answer, a thinner margin.

2. **File-name order is not a worse order on this corpus.** At batch 3 a Tier-A task is one or two batches wide, so alphabetical order degenerates into a near big-bang migration that never exposes an intermediate state and needs no recovery at all. That is a property of a six-file corpus, not evidence that the graph is unnecessary — but it is the honest reading of these numbers, and the textbook result (an arbitrary order causing a regression the dependency order avoids) is **not reproduced here**. Getting it would need a task whose break is a *signature* change rather than a semantic one, where editing a caller before its callee raises on import instead of producing a wrong value. Tier A has no such task yet; that is the gap to close before this ablation can carry the claim docs/05 §3 assigns it.

### D. Batch size 1 vs 3 vs 5

Batch size caps how many files one EDIT touches before the suite runs again (NFR-5): smaller batches localize a failure more precisely and cost more TEST steps.

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.70 ±0.01 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.74 ±0.04 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 0.69 ±0.01 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.38 ±0.02 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.45 ±0.11 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.37 ±0.02 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 1.80 ±0.02 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.48 ±0.03 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 1.54 ±0.18 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.30 ±0.19 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.23 ±0.01 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 3.26 ±0.05 |

### C. Edit model — V4-Pro vs V4-Flash

**Requires a key — not run.** `edit-v4-flash`, `edit-v4-pro` needs `DEEPSEEK_API_KEY`; the offline matrix above is complete without it.

Caveat for when it does run: `Router.TIER` bills an *edit* to the pro tier whatever `MRA_EDIT_MODEL` names, so the cost column for the V4-Flash arm is an upper bound, not a quote.

## 3. Deterministic baselines — ruff (DTZ) and pyupgrade

The honesty check (docs/05, RESOURCE_PACK §2.2): what do the existing static tools already do on these tasks?

| task | tool | detected | \|A\| | detect recall | fixed | M1 recall after fix | suite after fix |
|---|---|---|---|---|---|---|---|
| task01_datetime | `ruff (DTZ)` | 1 | 1 | 100% | 0 | 0% | 5/5 passed |
| task01_datetime | `pyupgrade` | 0 | 1 | 0% | 0 | 0% | 5/5 passed |
| task02_datetime_aliased | `ruff (DTZ)` | 2 | 2 | 100% | 0 | 0% | 5/5 passed |
| task02_datetime_aliased | `pyupgrade` | 0 | 2 | 0% | 0 | 0% | 5/5 passed |
| task03_half_migration | `ruff (DTZ)` | 3 | 3 | 100% | 0 | 0% | 7/7 passed |
| task03_half_migration | `pyupgrade` | 0 | 3 | 0% | 0 | 0% | 7/7 passed |
| task04_multimodule | `ruff (DTZ)` | 6 | 6 | 100% | 0 | 0% | 11/11 passed |
| task04_multimodule | `pyupgrade` | 0 | 6 | 0% | 0 | 0% | 11/11 passed |

`detected` counts sites the tool reported; `fixed` counts files it rewrote. A tool that reports a site but cannot rewrite it scores 0 on M1 however good its detection is — and none of them can repair the cross-file break that task03/task04 are built around, because they never edit anything.

## 4. Configuration key

| config | what it changes |
|---|---|
| `baseline` | recovery on, dependency order, batch 3, deterministic corrector |
| `no-recovery` | CORRECT loop disabled (MRA_MAX_FIX_ATTEMPTS=0) |
| `order-alphabetical` | batches by file name instead of the dependency graph |
| `order-fr3-violating` | plain topological order — dependents before dependencies, the docs/04 §3.4 pseudocode defect |
| `order-alphabetical-b1` | file-name order, one file per EDIT |
| `order-fr3-violating-b1` | dependents-first order, one file per EDIT |
| `batch-1` | one file per EDIT |
| `batch-5` | five files per EDIT |
| `edit-v4-pro` | live corrective edits from the strong model |
| `edit-v4-flash` | live corrective edits from the cheap model |

*Generated by `python -m mra.benchmark`.*
