# What the Tier-A benchmark shows

Source: `results.json` generated 2026-09-21T05:49:48Z — 5 tasks × 11 offline
configurations × 3 repeats = 165 runs, every one deterministic (the corrector
is the codemod, not a model, so the spread across repeats is zero on every
metric but wall clock). The two live-model arms (ablation C) are skipped
without `DEEPSEEK_API_KEY` and are marked *requires key*, not estimated.
Full tables in [`results.md`](results.md); every failing run is itemised in
[`failure-analysis.md`](failure-analysis.md).

Each claim below is one sentence plus the cells that back it.

---

## (a) The recovery loop is what finishes a cross-file migration

**Claim.** With the CORRECT loop disabled, 3 of the 5 Tier-A tasks end in
`gave_up` with a regression the agent cannot repair; with it enabled all 5
finish at M1 100 % / M2 100 % / 0 regressions — and the two tasks that do not
move are the two where nothing ever breaks, which is what makes them controls
rather than counter-evidence.

*`results.md` §2A — `baseline` vs `no-recovery`, 3 repeats each:*

| task | loop on | loop off |
|---|---|---|
| `task01_datetime` *(control: single file)* | success, M1 100, 0 regr | success, M1 100, 0 regr |
| `task02_datetime_aliased` | success, M1 100, M2 100, 1 corr | **gave_up, M1 50, M2 80.0, 1 regr** |
| `task03_half_migration` | success, M1 100, M2 100, 1 corr | **gave_up, M1 33, M2 85.7, 1 regr** |
| `task04_multimodule` | success, M1 100, M2 100, 2 corr | **gave_up, M1 67, M2 72.7, 3 regr** |
| `task05_signature_break` *(control: dependency order opens no window)* | success, M1 100, 0 corr | success, M1 100, 0 regr |

The `task05` row is the useful control the corpus was missing: it is a hard
task that the loop does **not** rescue, because in dependency order there is
nothing to rescue. Ablation A's effect therefore tracks "is there a break?",
not "is the task big?".

## (b) The existing static tools detect the work and do none of it

**Claim.** `ruff` (DTZ) reports 100 % of the ground-truth call sites on all
five tasks and rewrites zero of them, so its M1 recall after running with
`--fix` is 0 % on every task — and because it changes nothing, the suite stays
green, which is exactly why M2 alone cannot tell you a migration did not
happen.

*`results.md` §3 — deterministic baselines:*

| task | \|A\| | ruff detected | ruff fixed | M1 after fix | suite after fix | pyupgrade detected |
|---|---|---|---|---|---|---|
| `task01_datetime` | 1 | 1 (100 %) | 0 | 0 % | 5/5 passed | 0 (0 %) |
| `task02_datetime_aliased` | 2 | 2 (100 %) | 0 | 0 % | 5/5 passed | 0 (0 %) |
| `task03_half_migration` | 3 | 3 (100 %) | 0 | 0 % | 7/7 passed | 0 (0 %) |
| `task04_multimodule` | 6 | 6 (100 %) | 0 | 0 % | 11/11 passed | 0 (0 %) |
| `task05_signature_break` | 6 | 7 (100 % recall, 86 % precision) | 0 | 0 % | 14/14 passed | 0 (0 %) |

Two details reported rather than smoothed over. `ruff`'s seventh hit on
`task05` is a real `DTZ001` on the naive constant in `tests/test_timebase.py`
— a false positive against `|A|`, and the only place in the corpus where
detection precision is below 100 %. `pyupgrade` detects nothing at all: this
migration is not in its rule set, so its row is a floor, not a failure.

Neither tool can repair a cross-file break, because neither tool edits across
files at all: on `task03`/`task04`/`task05` the regression the agent recovers
from does not exist for them, since they never create it.

## (c) Dependency-ordered batching: what the data actually supports

**Claim 1 (regression avoidance — new, and only on `task05`).** With the loop
off and one file per batch, dependency order completes `task05_signature_break`
green while both arbitrary orders give up with a red suite; on the other four
tasks all three orders break, so the ordering claim rests on `task05` alone.

*`results.md` §2B, "batch size 1, recovery OFF":*

| task | dependency | file-name | dependents-first |
|---|---|---|---|
| `task01_datetime` | 3× success, 0 regr | 3× success, 0 regr | 3× success, 0 regr |
| `task02_datetime_aliased` | 3× gave_up, M1 50 | 3× gave_up, M1 50 | 3× gave_up, M1 50 |
| `task03_half_migration` | 3× gave_up, M1 33 | 3× gave_up, M1 67 | 3× gave_up, M1 67 |
| `task04_multimodule` | 3× gave_up, M1 67 | 3× gave_up, M1 67 | 3× gave_up, M1 33 |
| **`task05_signature_break`** | **3× success, M1 100, M2 100, 0 regr** | **3× gave_up, M1 33, M2 0.0, 14 regr** | **3× gave_up, M1 50, M2 78.6, 3 regr** |

On `task05` the two arbitrary orders break *differently*, and that difference
is the finding. The file-name order migrates `src/pkg/boot.py` before
`src/pkg/timebase.py`, and `boot.py` hands its own stamp back to the clock at
**module scope**, so the `TypeError` is raised during import: three test
modules never load at all and the failing nodeids in `failure-analysis.md` are
whole files with no `::test_` in them (M2 0.0 %, 14 regressions — the entire
suite). The dependents-first order reaches `boot.py` one batch later and trips
the same contract at call time instead (M2 78.6 %, 3 regressions). Dependency
order reaches neither: 3× success, 0 regressions, 0 corrective edits.

`timebase.elapsed_since` checks the contract before it does any arithmetic, so
the exception is deterministic and self-describing rather than the stdlib's
generic subtraction error:

```
E TypeError: pkg.timebase clock contract violated: the stamp is timezone-aware
  and the package clock is still naive. A caller was migrated before
  pkg/timebase.py; migrate the contract owner first.
```

That is the hard break ablation B was missing, and it is asymmetric by
construction: the clock upgrades a naive stamp it is handed but refuses to
strip a `tzinfo`, so callee-first is always safe and caller-first never is. See [`corpus/tierA/task05_signature_break/README.md`](../../corpus/tierA/task05_signature_break/README.md).

**Claim 2 (corrective-edit cost).** With the loop on, dependency order is
never the most expensive arm and the dependents-first order is never the
cheapest — but the ranking is not uniform, so this is a weaker claim than
claim 1.

*`results.md` §2B, "batch size 1, recovery on" — mean corrective edits, 3 repeats:*

| task | dependency | file-name | dependents-first |
|---|---|---|---|
| `task01_datetime` | 0 | 0 | 0 |
| `task02_datetime_aliased` | 1 | 1 | 1 |
| `task03_half_migration` | 1 | 1 | 1 |
| `task04_multimodule` | 2 | **1** | **3** |
| `task05_signature_break` | **0** | **2** | 1 |

The `task04` row is reported as found: file-name order costs one edit fewer
than dependency order there. That is luck about which files that particular
alphabet groups, not evidence against FR-3 — and the same order costs 2 where
dependency order costs 0 on `task05`. The dependents-first arm on `task04`
spends the full NFR-1 retry ceiling of 3 attempts, i.e. it finishes one
attempt away from failing the task outright.

**Claim 3 (what is *not* shown).** With the loop on, every order completes
every Tier-A task at M1 100 / M2 100, including `task05` — so on this corpus
edit order is a cost and a risk, never a verdict, once recovery is available.
Anyone quoting claim 1 must quote this alongside it.

---

## Scope and honesty notes

- **Deterministic, not LLM.** Every row above uses the codemod corrector. The
  loop mechanics are what is measured; the model's ability to write a patch is
  ablation C and needs a key. Nothing here is an estimate of live behaviour.
- **Five tasks, one contract.** All five migrate `datetime.utcnow()` to
  `datetime.now(timezone.utc)`. Conclusions about *batching* and *recovery*
  generalise no further than a corpus of this size and one migration contract.
- **The ordering result rests on one fixture.** `task05` was built to exercise
  ablation B after `task01`–`task04` failed to separate the orders. It is a
  designed instance, not a sample: it shows that dependency order *can* be the
  difference between green and failed, not how often that happens in the wild.
- **`task05` is a contract break, not an arity break.** The signature that
  moves is the tz-awareness of `timebase.utc_now()`'s return value. The agent
  runs one fixed codemod (golden rule 5) that only rewrites `datetime.utcnow()`
  calls, so a first-party arity change — an added required parameter the
  migration threads through call sites — is **not expressible in this corpus**.
  What `task05` delivers instead is the property that mattered: a caller
  migrated before its callee raises a named, deterministic `TypeError` at
  **import/collection** time. `classify_offline` reserves the `signature` class
  for argument-shaped messages, so it files this as **behaviour** — reported,
  not gamed.
- **Live rows.** `edit-v4-pro` and `edit-v4-flash` read *requires key* in
  `results.md` §2C and are absent from `results.json.rows`. The offline matrix
  is complete without them.
