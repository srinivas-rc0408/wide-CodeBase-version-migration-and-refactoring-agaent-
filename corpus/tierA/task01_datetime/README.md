# task01_datetime — Tier-A controlled task

`datetime.utcnow()` → `datetime.now(timezone.utc)`, from-import style
(`from datetime import datetime`). Difficulty: easy. |A| = 1 call site.

## The two states live in one commit

`old/` and `gold/` are sibling directories, so a single commit holds both
states. The tags `task01/old` and `task01/gold` therefore point at the same
commit (`78cc544`); the state you want is selected by directory, not by
checkout:

```bash
git checkout task01/old   # then read corpus/tierA/task01_datetime/old/
git checkout task01/gold  # then read corpus/tierA/task01_datetime/gold/
```

`gold_commit` in `ground_truth.json` records that SHA. The agent always runs
against a fresh copy of `old/`; scoring diffs its result against `gold/`.

## The `pkg` name-collision gotcha

`old/` and `gold/` both declare `name = "pkg"`. Installing one and then the
other into the same environment **silently replaces** the first — the second
`pip install -e .` wins and the earlier tree is no longer importable. Every
Tier-A task reuses the name, so tasks collide with each other too.

Real runs install each task inside its own sandbox container, one per run
(SRS NFR-8), never into the host `.venv`. For a quick local check, skip
installing altogether and point the interpreter at the tree you mean:

```bash
PYTHONPATH=old/src  pytest old/tests  -q   # pre-migration:  passes, warns
PYTHONPATH=gold/src pytest gold/tests -q   # post-migration: passes, silent
```

## Test-oracle rule

No assertion in `old/tests/` may depend on the migration having happened —
the suite must be green before the agent touches anything (NB-10). The
timezone-aware assertion lives only in `gold/tests/test_core.py`; it fails
against `old/`, which is what makes it a discriminating `semantic_check`.
