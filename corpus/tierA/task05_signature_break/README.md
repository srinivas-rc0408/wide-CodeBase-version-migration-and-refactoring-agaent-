# task05_signature_break — Tier-A edit-order fixture

Same contract as [`task01_datetime`](../task01_datetime/README.md):
`datetime.utcnow()` → `datetime.now(timezone.utc)`, from-import style
throughout. Difficulty: hard. **|A| = 6 call sites across six modules.**

`task04_multimodule` proved that batching plus recovery finishes a cross-file
migration. It could not prove that the *order* matters: its break is
symmetric, so every order opens some window and recovery closes all of them
(see `runs/benchmark/results.md` §2B). This task is the one where order is the
variable that decides the outcome.

## What makes the break asymmetric

`pkg.timebase` owns the clock contract. Anything that compares a stamp it was
*handed* against the current time goes through `elapsed_since`, which
normalizes through `aligned`:

```python
def aligned(stamp: datetime, reference: datetime) -> datetime:
    if stamp.tzinfo is None and reference.tzinfo is not None:
        return stamp.replace(tzinfo=timezone.utc)
    return stamp
```

`elapsed_since` then checks the contract *before* it does any arithmetic, so
the violation is a named, deterministic `TypeError` rather than the stdlib's
generic subtraction error:

```python
def elapsed_since(stamp: datetime) -> float:
    reference = utc_now()
    stamp = aligned(stamp, reference)
    if (stamp.tzinfo is None) != (reference.tzinfo is None):
        raise TypeError("pkg.timebase clock contract violated: ...")
    return (reference - stamp).total_seconds()
```

The shim is one-way on purpose, and that is the whole fixture:

| clock (`timebase`) | caller's stamp | result |
|---|---|---|
| naive (old) | naive (old) | fine — `old/` is green |
| aware (migrated) | aware (migrated) | fine — `gold/` is green |
| **aware (migrated)** | **naive (not yet)** | **fine** — naive-UTC is upgraded |
| **naive (not yet)** | **aware (migrated)** | **`TypeError`** — a `tzinfo` is never dropped |

Upgrading a naive stamp is safe: the old contract *promised* it was UTC.
Downgrading an aware one is not — stripping the `tzinfo` silently reinterprets
the value — so the clock passes it through and `elapsed_since` refuses it. A
caller may be migrated **after** the contract owner. It may not be migrated
**before** it.

## Why it is a hard break, not a test failure

`pkg.boot` does the handback at module scope:

```python
STARTED_AT = datetime.utcnow()             # this module's own reading
STARTUP_LAG_S = elapsed_since(STARTED_AT)  # evaluated at IMPORT
```

Migrate `boot.py` while `timebase.py` has not moved and the `TypeError` is
raised while `pkg.boot` is being imported. Every test module that reaches the
package dies during **collection**:

```
ERROR tests/test_api.py     - TypeError: pkg.timebase clock contract violated...
ERROR tests/test_boot.py    - TypeError: pkg.timebase clock contract violated...
ERROR tests/test_handler.py - TypeError: pkg.timebase clock contract violated...
!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!
```

The traceback points at `src/pkg/boot.py:20` inside the module body, not at a
test — that is what makes it a collection error and not an assertion.

Compare `ledger.py`, which does the same handback inside `age_of()`: migrating
*it* first is the softer half of the same break — one deterministic `TypeError`
at call time, no collection error.

On the taxonomy in docs/04 §2.5 this still classifies as a **behaviour** break,
because the exception is a bare `TypeError` and `classify_offline` reserves
`signature` for argument-shaped ones. The name of the task refers to the
*contract* that moves: the return-type (tz-awareness) signature of
`timebase.utc_now()`, enforced at the package boundary. An arity change is not
expressible here — the agent runs one fixed codemod (golden rule 5), and that
codemod only rewrites `datetime.utcnow()` calls.

## The import DAG

```
              timebase.py
               ^       ^
               |       |
          boot.py   ledger.py
               ^      ^     ^
               |      |     |
          handler.py       metrics.py
               ^                ^
               |                |
               +---- api.py ----+
```

No cycle: that is `task04`'s property, and mixing the two would confound them.

## What each module contributes

| File | Call site in | Role |
|---|---|---|
| `timebase.py` | `utc_now()` | the contract owner; must be migrated first |
| `boot.py` | `STARTED_AT` (module scope) | **hands its stamp back at import — the hard break** |
| `ledger.py` | `post()` | hands its stamp back in `age_of()` — the soft break |
| `metrics.py` | `snapshot()` | hands its stamp back in the same call |
| `handler.py` | `handle()` | self-contained; its stamp never leaves |
| `api.py` | `serve()` | self-contained; the deepest module |

## The three orders

| order | batch 1 plan | boot before timebase? |
|---|---|---|
| dependency | `timebase`, `boot`, `ledger`, `handler`, `metrics`, `api` | no |
| alphabetical | `api`, **`boot`**, `handler`, `ledger`, `metrics`, **`timebase`** | **yes** |
| fr3-violating | `api`, `handler`, `metrics`, **`boot`**, `ledger`, **`timebase`** | **yes** |

The file names were chosen so this holds at batch size 3 as well, where
alphabetical chunking gives `[api, boot, handler]` then
`[ledger, metrics, timebase]` — `boot` still lands a batch ahead of the clock.
Order is therefore the variable at both granularities, not just at one file per
batch.

## Running the two states

`old/` and `gold/` are siblings in one commit and both declare `name = "pkg"`,
so installing both into one environment silently replaces the first. See the
[task01 README](../task01_datetime/README.md) for the full note.

```bash
PYTHONPATH=old/src  pytest old/tests  -q   # 14 passed, deprecation warnings
PYTHONPATH=gold/src pytest gold/tests -q   # 16 passed, silent
PYTHONPATH=old/src  pytest gold/tests -q   # 2 failed — the semantic checks
```

`gold/` carries two assertions beyond the shared suite: the clock is
timezone-aware, and **every** stamp in one `api.serve()` response is aware — so
a migration that leaves any single module behind fails the gold check even
when the shared suite is green.

`gold/` keeps `timezone.utc` rather than the `datetime.UTC` alias, so `ruff`
reports `UP017` on it. That is the contract's spelling (`target_api`), not a
defect; `task04`'s gold has the same finding.
