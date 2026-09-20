# task02_datetime_aliased — Tier-A controlled task

Same migration as [`task01_datetime`](../task01_datetime/README.md):
`datetime.utcnow()` → `datetime.now(timezone.utc)`. Difficulty: easy.
|A| = 2 call sites.

## The one factor that varies: import style

| | task01 | task02 |
|---|---|---|
| `core.py` | `from datetime import datetime` → `datetime.utcnow()` | `import datetime` → `datetime.datetime.utcnow()` |
| `report.py` | (no direct call site) | `import datetime as dt` → `dt.datetime.utcnow()` |

Everything else — package layout, test bodies, the cross-file edge, the
semantic check — is unchanged, so any difference in M1 between the two tasks
is attributable to import style alone (§1.1 rule 5).

**Why this task exists.** A matcher tuned to task01 looks for
`Attribute(value=Name("datetime"), attr=Name("utcnow"))`. In task02 the
receiver is an `Attribute`, not a `Name`, so that matcher finds **zero** of
the two sites here — and a `datetime\.utcnow\(` regex misses both as well.
Correct enumeration requires reading the `import` statements first and
resolving `dt` back to the `datetime` module. This is the trap described in
`docs/RESOURCE_PACK.md` §2.1, and it is what justifies the static analyzer.

Both sites therefore carry the same fully-qualified `symbol`,
`datetime.datetime.utcnow`, even though they are spelled differently.

## Import changes: deliberately empty

`expected_import_changes` lists both files with `add: []`. Under a module
import, `datetime.timezone` / `dt.timezone` is already in scope, so the
correct migration adds **no** import — unlike task01, where `timezone` must
be added to the `from datetime import ...` line. An agent that blindly
appends `from datetime import timezone` here has over-edited and should lose
M1 precision.

## The cross-file break

`report.build_report()` stamps its record with `core.make_timestamp()`, while
`report.stamp_age_seconds()` reads the clock through its own aliased call.
Migrate one and not the other and the subtraction raises
`TypeError: can't subtract offset-naive and offset-aware datetimes` — a real
cross-file regression, caught by `test_stamp_age_is_non_negative`.

## Running the two states

`old/` and `gold/` are sibling directories in one commit, and both declare
`name = "pkg"` — installing both into one environment silently replaces the
first. See the [task01 README](../task01_datetime/README.md) for the full
note. Real runs install per task inside the sandbox; locally, just point the
interpreter at the tree you mean:

```bash
PYTHONPATH=old/src  pytest old/tests  -q   # pre-migration:  passes, warns
PYTHONPATH=gold/src pytest gold/tests -q   # post-migration: passes, silent
```

No assertion in `old/tests/` depends on the migration having happened
(NB-10). The timezone-aware assertion lives only in
`gold/tests/test_core.py`; it fails against `old/`.
