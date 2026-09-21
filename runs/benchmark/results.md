# Benchmark results — Tier A

Generated 2026-09-21T05:49:48.150512+00:00 · 3 repeat(s) per (task, config) · mean ±spread across repeats.

Every row is one agent configuration on one task. `baseline` is the reference (recovery on, dependency-ordered batches of 3, deterministic corrector); every other configuration changes exactly one thing about it (docs/05 §3).

## 1. The whole offline matrix

Every (task, configuration) pair in one table — the paper's reference grid. The per-task breakdowns below are the same rows, split for reading. Live-model rows are absent by design; see §2C.

| task / config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `task01_datetime / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.14 |
| `task01_datetime / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.05 |
| `task01_datetime / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.74 ±0.05 |
| `task01_datetime / no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.74 ±0.09 |
| `task01_datetime / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.06 |
| `task01_datetime / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.05 |
| `task01_datetime / order-alphabetical-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.03 |
| `task01_datetime / order-dependency-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.05 |
| `task01_datetime / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.06 |
| `task01_datetime / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.11 |
| `task01_datetime / order-fr3-violating-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.76 ±0.02 |
| `task02_datetime_aliased / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.53 ±0.09 |
| `task02_datetime_aliased / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.09 |
| `task02_datetime_aliased / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.38 ±0.10 |
| `task02_datetime_aliased / no-recovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.09 |
| `task02_datetime_aliased / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.03 |
| `task02_datetime_aliased / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.46 ±0.25 |
| `task02_datetime_aliased / order-alphabetical-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.71 ±0.08 |
| `task02_datetime_aliased / order-dependency-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.69 ±0.02 |
| `task02_datetime_aliased / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.12 |
| `task02_datetime_aliased / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.48 ±0.25 |
| `task02_datetime_aliased / order-fr3-violating-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.69 ±0.02 |
| `task03_half_migration / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.70 ±0.13 |
| `task03_half_migration / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.54 ±0.12 |
| `task03_half_migration / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.72 ±0.33 |
| `task03_half_migration / no-recovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 1.81 ±0.01 |
| `task03_half_migration / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.04 |
| `task03_half_migration / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.49 ±0.07 |
| `task03_half_migration / order-alphabetical-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 85.7 | 1 | 0 | 7 | 0 | 0.0000 | 2.71 ±0.09 |
| `task03_half_migration / order-dependency-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 1.85 ±0.07 |
| `task03_half_migration / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.63 ±0.25 |
| `task03_half_migration / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.44 ±0.08 |
| `task03_half_migration / order-fr3-violating-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 85.7 | 1 | 0 | 7 | 0 | 0.0000 | 2.66 ±0.04 |
| `task04_multimodule / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.06 ±0.08 |
| `task04_multimodule / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 7.92 ±0.09 |
| `task04_multimodule / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.42 ±0.27 |
| `task04_multimodule / no-recovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 3.97 ±0.17 |
| `task04_multimodule / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 7 | 0 | 0.0000 | 3.21 ±0.08 |
| `task04_multimodule / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 7.74 ±0.22 |
| `task04_multimodule / order-alphabetical-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 11 | 0 | 0.0000 | 4.73 ±0.24 |
| `task04_multimodule / order-dependency-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 3.92 ±0.08 |
| `task04_multimodule / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 9.16 ±0.18 |
| `task04_multimodule / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 9.14 ±0.04 |
| `task04_multimodule / order-fr3-violating-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 72.7 | 3 | 0 | 7 | 0 | 0.0000 | 2.97 ±0.10 |
| `task05_signature_break / baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.81 ±0.24 |
| `task05_signature_break / batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.26 ±0.09 |
| `task05_signature_break / batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.93 ±0.27 |
| `task05_signature_break / no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.72 ±0.08 |
| `task05_signature_break / order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 4.53 ±0.15 |
| `task05_signature_break / order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 19 | 0 | 0.0000 | 9.07 ±0.04 |
| `task05_signature_break / order-alphabetical-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 0.0 | 14 | 0 | 7 | 0 | 0.0000 | 3.12 ±0.06 |
| `task05_signature_break / order-dependency-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.25 ±0.02 |
| `task05_signature_break / order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 13 | 0 | 0.0000 | 5.91 ±0.06 |
| `task05_signature_break / order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 7.43 ±0.07 |
| `task05_signature_break / order-fr3-violating-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 78.6 | 3 | 0 | 9 | 0 | 0.0000 | 3.72 ±0.03 |

## 1b. Per task, per configuration

### task01_datetime

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.14 |
| `no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.74 ±0.09 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.06 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.06 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.05 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.11 |
| `order-dependency-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.05 |
| `order-alphabetical-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.03 |
| `order-fr3-violating-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.76 ±0.02 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.05 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.74 ±0.05 |

### task02_datetime_aliased

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.53 ±0.09 |
| `no-recovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.09 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.03 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.12 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.46 ±0.25 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.48 ±0.25 |
| `order-dependency-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.69 ±0.02 |
| `order-alphabetical-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.71 ±0.08 |
| `order-fr3-violating-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.69 ±0.02 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.09 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.38 ±0.10 |

### task03_half_migration

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.70 ±0.13 |
| `no-recovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 1.81 ±0.01 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.04 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.63 ±0.25 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.49 ±0.07 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.44 ±0.08 |
| `order-dependency-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 1.85 ±0.07 |
| `order-alphabetical-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 85.7 | 1 | 0 | 7 | 0 | 0.0000 | 2.71 ±0.09 |
| `order-fr3-violating-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 85.7 | 1 | 0 | 7 | 0 | 0.0000 | 2.66 ±0.04 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.54 ±0.12 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.72 ±0.33 |

### task04_multimodule

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.06 ±0.08 |
| `no-recovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 3.97 ±0.17 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 7 | 0 | 0.0000 | 3.21 ±0.08 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 9.16 ±0.18 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 7.74 ±0.22 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 9.14 ±0.04 |
| `order-dependency-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 3.92 ±0.08 |
| `order-alphabetical-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 11 | 0 | 0.0000 | 4.73 ±0.24 |
| `order-fr3-violating-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 72.7 | 3 | 0 | 7 | 0 | 0.0000 | 2.97 ±0.10 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 7.92 ±0.09 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.42 ±0.27 |

### task05_signature_break

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.81 ±0.24 |
| `no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.72 ±0.08 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 4.53 ±0.15 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 13 | 0 | 0.0000 | 5.91 ±0.06 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 19 | 0 | 0.0000 | 9.07 ±0.04 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 7.43 ±0.07 |
| `order-dependency-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.25 ±0.02 |
| `order-alphabetical-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 0.0 | 14 | 0 | 7 | 0 | 0.0000 | 3.12 ±0.06 |
| `order-fr3-violating-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 78.6 | 3 | 0 | 9 | 0 | 0.0000 | 3.72 ±0.03 |
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.26 ±0.09 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.93 ±0.27 |

## 2. Ablations

### A. Recovery loop ON vs OFF — the headline

The only variable is whether the CORRECT loop may run. Both arms use the deterministic corrector, so this contrast is reproducible without an API key: the loop's *mechanics* are what is being measured, not the model's.

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.14 |
| `no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.74 ±0.09 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.53 ±0.09 |
| `no-recovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.09 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.70 ±0.13 |
| `no-recovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 1.81 ±0.01 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.06 ±0.08 |
| `no-recovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 3.97 ±0.17 |

**task05_signature_break**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.81 ±0.24 |
| `no-recovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.72 ±0.08 |

### B. Dependency-ordered batching vs arbitrary order

`baseline`/`batch-1` use the FR-3 order; the `order-alphabetical` arms ignore the graph; the `order-fr3-violating` arms are `plan_batches` on the *reversed* graph — dependents before their dependencies, the inversion docs/04 §3.4's pseudocode produces if its missing `.reverse()` is taken literally.

Read the three groups separately. At batch 3 a small task is only one or two batches wide, so edit order and batch size are confounded — an order that happens to put a producer and its consumer in the same batch never exposes the intermediate state at all. The `-b1` group edits one file per batch, where sequence is the only variable left. The `-norecovery` group then removes the loop, which is the only way to see what an order costs when nothing is there to repair it.

#### batch size 3, recovery on

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.14 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.06 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.06 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.53 ±0.09 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.03 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.12 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.70 ±0.13 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.04 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.63 ±0.25 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.06 ±0.08 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 7 | 0 | 0.0000 | 3.21 ±0.08 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 9.16 ±0.18 |

**task05_signature_break**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.81 ±0.24 |
| `order-alphabetical` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 4.53 ±0.15 |
| `order-fr3-violating` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 13 | 0 | 0.0000 | 5.91 ±0.06 |

#### batch size 1, recovery on

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.05 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.05 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.11 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.09 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.46 ±0.25 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.48 ±0.25 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.54 ±0.12 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.49 ±0.07 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.44 ±0.08 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 7.92 ±0.09 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 7.74 ±0.22 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 3 | 19 | 0 | 0.0000 | 9.14 ±0.04 |

**task05_signature_break**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.26 ±0.09 |
| `order-alphabetical-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 19 | 0 | 0.0000 | 9.07 ±0.04 |
| `order-fr3-violating-b1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 17 | 0 | 0.0000 | 7.43 ±0.07 |

#### batch size 1, recovery OFF

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `order-dependency-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.73 ±0.05 |
| `order-alphabetical-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.03 |
| `order-fr3-violating-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.76 ±0.02 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `order-dependency-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.69 ±0.02 |
| `order-alphabetical-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.71 ±0.08 |
| `order-fr3-violating-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 80.0 | 1 | 0 | 5 | 0 | 0.0000 | 1.69 ±0.02 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `order-dependency-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 85.7 | 1 | 0 | 5 | 0 | 0.0000 | 1.85 ±0.07 |
| `order-alphabetical-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 85.7 | 1 | 0 | 7 | 0 | 0.0000 | 2.71 ±0.09 |
| `order-fr3-violating-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 85.7 | 1 | 0 | 7 | 0 | 0.0000 | 2.66 ±0.04 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `order-dependency-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 9 | 0 | 0.0000 | 3.92 ±0.08 |
| `order-alphabetical-b1-norecovery` | 3× gave_up | 66.7 | 100.0 | 80.0 | 72.7 | 3 | 0 | 11 | 0 | 0.0000 | 4.73 ±0.24 |
| `order-fr3-violating-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 72.7 | 3 | 0 | 7 | 0 | 0.0000 | 2.97 ±0.10 |

**task05_signature_break**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `order-dependency-b1-norecovery` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.25 ±0.02 |
| `order-alphabetical-b1-norecovery` | 3× gave_up | 33.3 | 100.0 | 50.0 | 0.0 | 14 | 0 | 7 | 0 | 0.0000 | 3.12 ±0.06 |
| `order-fr3-violating-b1-norecovery` | 3× gave_up | 50.0 | 100.0 | 66.7 | 78.6 | 3 | 0 | 9 | 0 | 0.0000 | 3.72 ±0.03 |

#### What the data says

Corrective edits per task, one file per batch, recovery on (lower is better):

- **task01_datetime** — dependency order 0, file-name order 0, dependents-first 0
- **task02_datetime_aliased** — dependency order 1, file-name order 1, dependents-first 1
- **task03_half_migration** — dependency order 1, file-name order 1, dependents-first 1
- **task04_multimodule** — dependency order 2, file-name order 1, dependents-first 3
- **task05_signature_break** — dependency order 0, file-name order 2, dependents-first 1

Outcome with the loop off, one file per batch — the same three orders with nothing to repair them:

- **task01_datetime** — dependency 3× success (M1 100%, 0 regr), file-name 3× success (M1 100%, 0 regr), dependents-first 3× success (M1 100%, 0 regr)
- **task02_datetime_aliased** — dependency 3× gave_up (M1 50%, 1 regr), file-name 3× gave_up (M1 50%, 1 regr), dependents-first 3× gave_up (M1 50%, 1 regr)
- **task03_half_migration** — dependency 3× gave_up (M1 33%, 1 regr), file-name 3× gave_up (M1 67%, 1 regr), dependents-first 3× gave_up (M1 67%, 1 regr)
- **task04_multimodule** — dependency 3× gave_up (M1 67%, 3 regr), file-name 3× gave_up (M1 67%, 3 regr), dependents-first 3× gave_up (M1 33%, 3 regr)
- **task05_signature_break** — dependency 3× success (M1 100%, 0 regr), file-name 3× gave_up (M1 33%, 14 regr), dependents-first 3× gave_up (M1 50%, 3 regr)

Three findings.

1. **Edit order alone decides the outcome on `task05_signature_break`.** With the CORRECT loop off, the dependency order finishes green with no regression while the file-name and dependents-first orders both give up with a red suite. The fixture's break is asymmetric by construction: `pkg.timebase` upgrades a naive stamp it is handed but refuses to strip a `tzinfo`, so migrating the contract owner first is always safe and migrating a caller first is not. `pkg.boot` does that handback at module scope, so the wrong order raises during **import** and pytest reports collection errors rather than test failures — the hard break this ablation was missing.

2. **The dependents-first order is never cheaper and is sometimes the most expensive arm run** — on `task04_multimodule` it spends the full NFR-1 retry ceiling of 3 attempts where the dependency order spends 2, i.e. it finishes one attempt away from failing the task. That is what violating FR-3 costs when a loop is there to absorb it: not a wrong answer, a thinner margin.

3. **With the loop on, order is a cost and not a verdict.** Every order completes every Tier-A task, `task05_signature_break` included. Dependency order is never the most expensive arm and the dependents-first order is never the cheapest, but the ranking is not uniform: file-name order is the cheapest arm on `task04` (1 corrective edit against the dependency order's 2), which is luck about which files that particular alphabet happens to group, and the same order costs 2 where the dependency order costs 0 on `task05`. The ordering claim this corpus supports is therefore conditional: *dependency order removes the corrective edits on the task built to expose ordering, and without a recovery loop it is the difference between a green migration and a failed one.*

One honest caveat on `task01`–`task04`: file-name order is not a worse order there. Those tasks are one or two batches wide at batch 3, so alphabetical order degenerates into a near big-bang migration that never exposes an intermediate state. That is a property of a small corpus, not evidence that the graph is unnecessary — `task05` exists precisely because the four earlier tasks could not separate the orders.

### D. Batch size 1 vs 3 vs 5

Batch size caps how many files one EDIT touches before the suite runs again (NFR-5): smaller batches localize a failure more precisely and cost more TEST steps.

**task01_datetime**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.72 ±0.05 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.90 ±0.14 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 5 | 0 | 0.0000 | 1.74 ±0.05 |

**task02_datetime_aliased**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.37 ±0.09 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.53 ±0.09 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.38 ±0.10 |

**task03_half_migration**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 11 | 0 | 0.0000 | 4.54 ±0.12 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.70 ±0.13 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 1 | 9 | 0 | 0.0000 | 3.72 ±0.33 |

**task04_multimodule**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 7.92 ±0.09 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.06 ±0.08 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 2 | 17 | 0 | 0.0000 | 8.42 ±0.27 |

**task05_signature_break**

| config | outcome | M1 recall | M1 prec | M1 F1 | M2 % | regr | corr | steps | tokens | cost $ | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `batch-1` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 15 | 0 | 0.0000 | 6.26 ±0.09 |
| `baseline` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.81 ±0.24 |
| `batch-5` | 3× success | 100.0 | 100.0 | 100.0 | 100.0 | 0 | 0 | 11 | 0 | 0.0000 | 4.93 ±0.27 |

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
| task05_signature_break | `ruff (DTZ)` | 7 | 6 | 100% | 0 | 0% | 14/14 passed |
| task05_signature_break | `pyupgrade` | 0 | 6 | 0% | 0 | 0% | 14/14 passed |

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
| `order-dependency-b1-norecovery` | dependency order, one file per EDIT, CORRECT loop disabled |
| `order-alphabetical-b1-norecovery` | file-name order, one file per EDIT, CORRECT loop disabled |
| `order-fr3-violating-b1-norecovery` | dependents-first order, one file per EDIT, CORRECT loop disabled |
| `batch-1` | one file per EDIT |
| `batch-5` | five files per EDIT |
| `edit-v4-pro` | live corrective edits from the strong model |
| `edit-v4-flash` | live corrective edits from the cheap model |

*Generated by `python -m mra.benchmark`.*
