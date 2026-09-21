# Failure analysis

Generated 2026-09-21T05:49:48.150512+00:00. Every run that gave up or finished with M2 < 100 is listed with its failure class (docs/04 §2.5), its normalized signature, and why the loop did not recover it.

42 of 165 runs failed.

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

## `order-dependency-b1-norecovery` on task02_datetime_aliased

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 1/2
- **M1 recall:** 50%   **M2:** 80.0% with 1 regression(s)
- **planned batches:** [['src/pkg/core.py'], ['src/pkg/report.py']]
- **files actually migrated:** ['src/pkg/core.py']
- **surviving failures:**
  - `tests/test_report.py::test_stamp_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `7769f4e867263e8d`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-dependency-b1-norecovery` on task03_half_migration

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 1/3
- **M1 recall:** 33%   **M2:** 85.7% with 1 regression(s)
- **planned batches:** [['src/pkg/core.py'], ['src/pkg/audit.py'], ['src/pkg/report.py']]
- **files actually migrated:** ['src/pkg/core.py']
- **surviving failures:**
  - `tests/test_report.py::test_stamp_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `7769f4e867263e8d`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-dependency-b1-norecovery` on task04_multimodule

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
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-alphabetical-b1-norecovery` on task02_datetime_aliased

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 1/2
- **M1 recall:** 50%   **M2:** 80.0% with 1 regression(s)
- **planned batches:** [['src/pkg/core.py'], ['src/pkg/report.py']]
- **files actually migrated:** ['src/pkg/core.py']
- **surviving failures:**
  - `tests/test_report.py::test_stamp_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `7769f4e867263e8d`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-alphabetical-b1-norecovery` on task03_half_migration

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 2/3
- **M1 recall:** 67%   **M2:** 85.7% with 1 regression(s)
- **planned batches:** [['src/pkg/audit.py'], ['src/pkg/core.py'], ['src/pkg/report.py']]
- **files actually migrated:** ['src/pkg/audit.py', 'src/pkg/core.py']
- **surviving failures:**
  - `tests/test_report.py::test_stamp_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `7769f4e867263e8d`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-alphabetical-b1-norecovery` on task04_multimodule

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 4/6
- **M1 recall:** 67%   **M2:** 72.7% with 3 regression(s)
- **planned batches:** [['src/pkg/api.py'], ['src/pkg/audit.py'], ['src/pkg/clock.py'], ['src/pkg/invoice.py'], ['src/pkg/ledger.py'], ['src/pkg/report.py']]
- **files actually migrated:** ['src/pkg/api.py', 'src/pkg/audit.py', 'src/pkg/clock.py', 'src/pkg/invoice.py']
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
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-alphabetical-b1-norecovery` on task05_signature_break

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 2/6
- **M1 recall:** 33%   **M2:** 0.0% with 14 regression(s)
- **planned batches:** [['src/pkg/api.py'], ['src/pkg/boot.py'], ['src/pkg/handler.py'], ['src/pkg/ledger.py'], ['src/pkg/metrics.py'], ['src/pkg/timebase.py']]
- **files actually migrated:** ['src/pkg/api.py', 'src/pkg/boot.py']
- **surviving failures:**
  - `tests/test_api.py` — **behaviour** break, `TypeError`
    - signature: `1c4bfd56ab1d2704`
    - message: E   TypeError: pkg.timebase clock contract violated: the stamp is timezone-aware and the package clock is still naive. A caller was migrated before pkg/timebase.py; migrate the contract owner first.
  - `tests/test_boot.py` — **behaviour** break, `TypeError`
    - signature: `04034decd7039dbd`
    - message: E   TypeError: pkg.timebase clock contract violated: the stamp is timezone-aware and the package clock is still naive. A caller was migrated before pkg/timebase.py; migrate the contract owner first.
  - `tests/test_handler.py` — **behaviour** break, `TypeError`
    - signature: `0c5704ce49efd65a`
    - message: E   TypeError: pkg.timebase clock contract violated: the stamp is timezone-aware and the package clock is still naive. A caller was migrated before pkg/timebase.py; migrate the contract owner first.
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-fr3-violating-b1-norecovery` on task02_datetime_aliased

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 1/2
- **M1 recall:** 50%   **M2:** 80.0% with 1 regression(s)
- **planned batches:** [['src/pkg/report.py'], ['src/pkg/core.py']]
- **files actually migrated:** ['src/pkg/report.py']
- **surviving failures:**
  - `tests/test_report.py::test_stamp_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `7769f4e867263e8d`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-fr3-violating-b1-norecovery` on task03_half_migration

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 2/3
- **M1 recall:** 67%   **M2:** 85.7% with 1 regression(s)
- **planned batches:** [['src/pkg/audit.py'], ['src/pkg/report.py'], ['src/pkg/core.py']]
- **files actually migrated:** ['src/pkg/audit.py', 'src/pkg/report.py']
- **surviving failures:**
  - `tests/test_report.py::test_stamp_age_is_non_negative` — **behaviour** break, `TypeError`
    - signature: `7769f4e867263e8d`
    - message: TypeError: can't subtract offset-naive and offset-aware datetimes
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-fr3-violating-b1-norecovery` on task04_multimodule

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 2/5
- **M1 recall:** 33%   **M2:** 72.7% with 3 regression(s)
- **planned batches:** [['src/pkg/api.py'], ['src/pkg/report.py'], ['src/pkg/invoice.py'], ['src/pkg/audit.py', 'src/pkg/ledger.py'], ['src/pkg/clock.py']]
- **files actually migrated:** ['src/pkg/api.py', 'src/pkg/report.py']
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
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited

## `order-fr3-violating-b1-norecovery` on task05_signature_break

- **outcome:** gave_up (3/3 repeats) — gave_up after batch 3/6
- **M1 recall:** 50%   **M2:** 78.6% with 3 regression(s)
- **planned batches:** [['src/pkg/api.py'], ['src/pkg/handler.py'], ['src/pkg/metrics.py'], ['src/pkg/boot.py'], ['src/pkg/ledger.py'], ['src/pkg/timebase.py']]
- **files actually migrated:** ['src/pkg/api.py', 'src/pkg/handler.py', 'src/pkg/metrics.py']
- **surviving failures:**
  - `tests/test_api.py::test_serve_returns_the_whole_response` — **behaviour** break, `TypeError`
    - signature: `c3b597d3bed85ab8`
    - message: TypeError: pkg.timebase clock contract violated: the stamp is timezone-aware and the package clock is still naive. A caller was migrated before pkg/timebase.py; migrate the contract owner first.
  - `tests/test_metrics.py::test_snapshot_counts_the_entries` — **behaviour** break, `TypeError`
    - signature: `41b3a5ecc74ff9cc`
    - message: TypeError: pkg.timebase clock contract violated: the stamp is timezone-aware and the package clock is still naive. A caller was migrated before pkg/timebase.py; migrate the contract owner first.
  - `tests/test_metrics.py::test_snapshot_reports_its_own_lag` — **behaviour** break, `TypeError`
    - signature: `568c4f32a23fafe3`
    - message: TypeError: pkg.timebase clock contract violated: the stamp is timezone-aware and the package clock is still naive. A caller was migrated before pkg/timebase.py; migrate the contract owner first.
- **why it was not recovered:** recovery disabled (ablation B): the run gives up on the first red suite, so the remaining batches are never edited
