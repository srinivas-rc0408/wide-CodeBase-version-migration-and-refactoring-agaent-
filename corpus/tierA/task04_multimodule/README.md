# task04_multimodule — Tier-A batching and scale fixture

Same contract as [`task01_datetime`](../task01_datetime/README.md):
`datetime.utcnow()` → `datetime.now(timezone.utc)`, from-import style
throughout. Difficulty: hard. **|A| = 6 call sites across seven modules.**

Tasks 01–03 vary one factor each (import style, then partial migration). This
one adds the factor none of them can: **a repo big enough to need a plan.**

## The import DAG

```
        clock.py        config.py
         ^     ^            ^
         |     |            |
    ledger.py <-> audit.py  |
         ^          ^       |
         |          |       |
    invoice.py      |       |
         ^          |       |
         |          |       |
     report.py -----+-------+
         ^
         |
       api.py
```

`ledger.py` and `audit.py` import each other — a real cycle, importable only
because each uses `import pkg.<other>` and defers the attribute read to call
time. `clock.py` is the most depended-upon module; `api.py` is the deepest.

## What each module contributes

| File | Call site in | Role |
|---|---|---|
| `clock.py` | `make_timestamp()` | the shared clock, migrated first |
| `ledger.py` | `snapshot_window()` | cycle half; its own reading, self-contained |
| `audit.py` | `reconcile()` | cycle half; its own reading, self-contained |
| `invoice.py` | `issue()` | stamps `issued_at` from its **own** clock |
| `report.py` | `invoice_age_seconds()` | **subtracts `issued_at`** — the break |
| `api.py` | `handle()` | its own reading, self-contained |
| `config.py` | — | no clock; a second root in the graph |

## The expected batch plan

```
batch 0: [src/pkg/clock.py]
batch 1: [src/pkg/audit.py, src/pkg/ledger.py]   <- the cycle, collapsed
batch 2: [src/pkg/invoice.py]
batch 3: [src/pkg/report.py]
batch 4: [src/pkg/api.py]
```

Two properties the planner must satisfy, both asserted programmatically in
`tests/test_p4_graph.py`:

1. **FR-3 ordering.** No file is edited while something it imports is still
   unmigrated and scheduled for a later batch. Note the direction: the graph's
   edges run `importer -> imported`, so this is the *reverse* topological
   order, not the plain one.
2. **Cycle atomicity.** `audit.py` and `ledger.py` share a batch. Editing one
   without the other leaves half a cycle calling the old contract, and there
   is no internal order that avoids it — so they are tested once, together.

## The cross-batch break

This is the point of the fixture, and it is placed carefully.
`invoice.issue()` stamps with its **own** `utcnow()`, not with
`clock.make_timestamp()`. So migrating the clock (batch 0) and the cycle
(batch 1) breaks nothing — the suite stays green and the run keeps going.

Then batch 2 migrates `invoice.py`, and `issued_at` becomes aware while
`report.invoice_age_seconds()` is still reading a naive clock:

```
tests/test_report.py::test_invoice_age_is_non_negative
E   TypeError: can't subtract offset-naive and offset-aware datetimes
```

A correct dependency order *causes* this: the dependency has to move first,
which necessarily opens a window where its caller has not. That window is
exactly what the CORRECT loop exists to close, and closing it mid-run —
rather than discovering it at the end — is what batching buys.

After recovery, batches 3 and 4 find `report.py` already migrated and change
nothing, which is the correct no-op rather than a double edit.

## Running the two states

`old/` and `gold/` are siblings in one commit and both declare `name = "pkg"`,
so installing both into one environment silently replaces the first. See the
[task01 README](../task01_datetime/README.md) for the full note.

```bash
PYTHONPATH=old/src  pytest old/tests  -q   # 11 passed, deprecation warnings
PYTHONPATH=gold/src pytest gold/tests -q   # 13 passed, silent
PYTHONPATH=old/src  pytest gold/tests -q   # 2 failed — the semantic checks
```

`gold/` carries two extra assertions beyond the shared suite: the clock is
timezone-aware, and **every** stamp in one `api.handle()` response is aware —
so a migration that leaves any single module behind fails the gold check even
if the shared suite is green.
