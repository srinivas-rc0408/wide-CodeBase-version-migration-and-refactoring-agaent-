# task03_half_migration — Tier-A recovery test bed

Same contract as [`task01_datetime`](../task01_datetime/README.md):
`datetime.utcnow()` → `datetime.now(timezone.utc)`, from-import style
throughout. Difficulty: medium. **|A| = 3 call sites** across three modules.

Tasks 01 and 02 ask *can the analyzer find the sites?* This one asks a
different question: **what happens when only some of them are migrated, and
can the agent finish the job from the failure alone?** It exists to be broken
on purpose.

## The three modules

| File | Call site | Mixes two clock readings? |
|---|---|---|
| `src/pkg/core.py` | `make_timestamp()` | — defines the contract |
| `src/pkg/report.py` | `stamp_age_seconds()` | **yes** — its own reading minus `core`'s |
| `src/pkg/audit.py` | `audit_window()` | no — both ends from one reading |

`report.py` and `audit.py` both import `pkg.core`, so the dependency graph is
a fan-in on `core.py`. Only `report.py` subtracts across the module boundary,
and that is deliberate: it makes the break attributable to one file rather
than to the sheer number of edits.

## The half-migration

Migrate `core.py` and `audit.py`, leave `report.py` alone, and the tree goes
red in exactly one place:

```
tests/test_report.py::test_stamp_age_is_non_negative
E   TypeError: can't subtract offset-naive and offset-aware datetimes
src/pkg/report.py:20: TypeError
```

`make_timestamp()` now returns an aware datetime; `stamp_age_seconds()` still
reads a naive one and subtracts. The failure is **semantic, not syntactic** —
the tree parses, imports, and lints clean. A syntax-checking or type-checking
gate would call this migration done. Only running the suite catches it.

Three properties make it a usable recovery bed:

1. **One failing test, one signature.** The retry cap in the CORRECT loop
   counts attempts per failure signature, so a fixture with one stable
   signature is what makes "stopped at exactly `MAX_FIX_ATTEMPTS`" a
   meaningful assertion.
2. **The trace names the guilty file.** The `TypeError` is raised at
   `src/pkg/report.py:20`, which is the unmigrated call site itself — so
   localization has a real signal to work from rather than a lucky guess.
3. **Finishing the migration is the fix.** The correct repair is the same
   codemod applied to the file that was skipped. After recovery the tree is
   identical to `gold/`, so M1 and M2 both reach 100% — no partial credit
   that hides a wrong fix.

## What `old/` and `gold/` are

`old/` is fully naive and **green** (7 tests). NB-10 requires it: without a
green baseline, M2 measures nothing. No assertion in `old/tests/` depends on
the migration having happened.

`gold/` is the hand-verified migrated tree — all three sites moved, `timezone`
added to all three from-imports — and carries one extra test,
`test_make_timestamp_is_timezone_aware`, which fails against `old/`. That test
is the semantic check: it is how "the suite is green" is distinguished from
"the migration actually happened".

`expected_import_changes` lists `add: ["timezone"]` for all three files. Unlike
[task02](../task02_datetime_aliased/README.md), where the module binding already
carries `timezone` and adding an import is over-editing, the from-import form
here genuinely needs it in every file.

## Running the two states

`old/` and `gold/` are siblings in one commit and both declare `name = "pkg"`,
so installing both into one environment silently replaces the first. See the
[task01 README](../task01_datetime/README.md) for the full note. Real runs
install per task inside the sandbox; locally, point the interpreter at the
tree you mean:

```bash
PYTHONPATH=old/src  pytest old/tests  -q   # 7 passed, deprecation warnings
PYTHONPATH=gold/src pytest gold/tests -q   # 8 passed, silent
PYTHONPATH=old/src  pytest gold/tests -q   # 1 failed — the semantic check
```
