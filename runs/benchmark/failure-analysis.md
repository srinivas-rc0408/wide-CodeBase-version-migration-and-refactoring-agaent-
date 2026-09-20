# Failure analysis

Generated 2026-09-20T17:26:25.912132+00:00. Every run that gave up or finished with M2 < 100 is listed with its failure class (docs/04 §2.5), its normalized signature, and why the loop did not recover it.

9 of 96 runs failed.

## `no-recovery` on task02_datetime_aliased

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 1/2
- **M1 recall:** 50%   **M2:** 80.0% with 1 regression(s)
- **planned batches:** [['src/pkg/core.py'], ['src/pkg/report.py']]
- **files actually migrated:** ['src/pkg/core.py']
- **surviving failures:**
  - `tests/test_report.py::test_stamp_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `7769f4e867263e8d`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation A): the run gives up on the first red suite, so the remaining batches are never edited

## `no-recovery` on task03_half_migration

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 1/2
- **M1 recall:** 33%   **M2:** 85.7% with 1 regression(s)
- **planned batches:** [['src/pkg/core.py'], ['src/pkg/audit.py', 'src/pkg/report.py']]
- **files actually migrated:** ['src/pkg/core.py']
- **surviving failures:**
  - `tests/test_report.py::test_stamp_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `7769f4e867263e8d`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation A): the run gives up on the first red suite, so the remaining batches are never edited

## `no-recovery` on task04_multimodule

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 3/5
- **M1 recall:** 67%   **M2:** 72.7% with 3 regression(s)
- **planned batches:** [['src/pkg/clock.py'], ['src/pkg/audit.py', 'src/pkg/ledger.py'], ['src/pkg/invoice.py'], ['src/pkg/report.py'], ['src/pkg/api.py']]
- **files actually migrated:** ['src/pkg/audit.py', 'src/pkg/clock.py', 'src/pkg/invoice.py', 'src/pkg/ledger.py']
- **surviving failures:**
  - `tests/test_api.py::test_handle_serves_a_complete_response` — **behaviour** break, `TypeError`
    - signature: `2773f89c64a8ae65`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
  - `tests/test_report.py::test_invoice_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `06db386a6ac883bc`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
  - `tests/test_report.py::test_summary_reports_the_invoice_and_its_age` — **behaviour** break, `TypeError`
    - signature: `910006be8e460f47`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation A): the run gives up on the first red suite, so the remaining batches are never edited
