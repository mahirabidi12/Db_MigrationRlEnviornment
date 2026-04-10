# Grader — Checklist-Based Evaluation

## Scoring Model

The grader evaluates the agent's database against the target schema using a flat checklist of binary checks. Each check verifies one specific property of the migrated database.

```
Score = checks_passed / total_checks    (range: 0.0 to 1.0)
```

---

## Architecture

The grader is implemented in `MigrationGrader` (`db_migration_env/graders/migration_grader.py`). It exposes two methods:

| Method | Returns | Usage |
|---|---|---|
| `grade()` | `float` (0.0 to 1.0) | Simple score — used by reward pipeline |
| `detailed_grade()` | `dict` with full breakdown | Used by `/grader` endpoint and final evaluation |

### `detailed_grade()` Return Structure

```json
{
  "reward": 0.8211,
  "total_score": 0.8211,
  "checks_passed": 1377,
  "checks_total": 1677,
  "summary": {
    "table_exists": {"total": 41, "passed": 41, "failed": 0},
    "column_exists": {"total": 381, "passed": 350, "failed": 31},
    ...
  },
  "failed_checks": [ ... ],
  "metadata": {
    "evaluation_results": [ ... ],
    "total_evaluations": 1677,
    "passed_evaluations": 1377,
    "average_score": 0.8211
  },
  "steps_taken": 109,
  "error_count": 0
}
```

The `metadata.evaluation_results` array contains every individual check in OpenEnv-compatible format — each with `name`, `score` (0 or 1), `passed`, and a `reason` string on failure.

---

## Check Types

The grader defines 12 check types. In practice, `column_removed` and `fk_removed` only fire when a target table also existed in the initial schema with extra columns or FKs — which doesn't happen in our acquisition-themed tasks (zero table name overlap). So effectively **10 check types** are active.

### Schema Structure (6 types)

| # | Check Type | Logic | Condition |
|---|---|---|---|
| 1 | `table_exists` | Is each target table present in the current database? | Always checked for every target table |
| 2 | `column_exists` | Does each expected column exist in its table? | Per column in each target table |
| 3 | `column_type_correct` | Does the column type match after normalization? (`INT` = `INTEGER`, etc.) | Only if column exists |
| 4 | `column_nullable_correct` | Does the NOT NULL constraint match? | Only if target column has `notnull=True` |
| 5 | `column_primary_key_correct` | Is the PRIMARY KEY flag set correctly? | Only if target column has `is_pk=True` |
| 6 | `column_default_correct` | Does the DEFAULT value match after normalization? | Only if target column has a DEFAULT value |

**When a table is missing:** All its column-level checks (types 2-6) and FK checks automatically fail with `actual="table missing"`. This means creating a single table can pass 15+ checks at once.

**When a column is missing:** Its type, nullable, PK, and default checks automatically fail with `actual="column missing"`.

### Referential Integrity (2 types)

| # | Check Type | Logic |
|---|---|---|
| 7 | `fk_exists` | Each target foreign key (from_column, to_table, to_column) must exist as a constraint in the current database |
| 8 | `index_exists` | Each target index (columns, unique flag) must exist. Matched by column tuple and uniqueness, not by index name |

### Legacy Cleanup (3 types)

| # | Check Type | Logic |
|---|---|---|
| 9 | `table_removed` | Every initial table that is NOT in the target schema must be dropped |
| 10 | `column_removed` | If a target table also existed in the initial schema, any initial columns not in the target must be gone |
| 11 | `fk_removed` | If a target table also existed in the initial schema, any initial FKs not in the target must be gone |

In our tasks, initial tables (`hc_*`, `fb_*`, `sl_*`) have zero name overlap with target tables, so `column_removed` and `fk_removed` generate zero checks. `table_removed` generates one check per initial table (31, 25, or 35 depending on task).

### Data Correctness (1 type)

| # | Check Type | Logic |
|---|---|---|
| 12 | `data_row_correct` | For each target table, every expected row must exist in the current database |

Data matching uses **multiset comparison**:

1. For each target table, retrieve all rows from both current and target databases
2. Build a multiset (dictionary with counts) of target rows, keyed by normalized column values
3. For each target row, check if a matching row exists in the current database's multiset
4. Each matched row decrements the count (handles duplicates correctly)

**Value normalization** (`_normalize_value()`):
- Integer/float equivalence: `1` matches `1.0`
- Floats rounded to 2 decimal places: `3.7` matches `3.70`
- NULL matches NULL
- String comparison is exact

Each row generates one check. A table with 12 target rows produces 12 `data_row_correct` checks. Failed row checks include a preview of the first 4 column values for debugging.

---

## Failure Reasons

Every failed check includes a human-readable `reason` string:

| Check Type | Example Reason |
|---|---|
| `table_exists` | `"Table 'patients' does not exist. Run: CREATE TABLE patients (...)"` |
| `column_exists` | `"Column 'patients.blood_type' is missing."` |
| `column_type_correct` | `"Wrong type for 'patients.id'. Expected INTEGER, got TEXT."` |
| `column_nullable_correct` | `"Wrong constraint for 'patients.first_name'. Expected NOT NULL, got NULLABLE."` |
| `fk_exists` | `"Missing FK on 'prescriptions': FK patient_id→patients(id)."` |
| `table_removed` | `"Legacy table 'hc_patients' still exists. Run: DROP TABLE hc_patients"` |
| `data_row_correct` | `"Expected row missing in 'patients': 1 \| Alice \| Chen \| alice.chen@..."` |

These reasons are included in both `failed_checks` and `metadata.evaluation_results`.

---

## Check Distribution Per Task

| Check Type | Easy | Medium | Hard |
|---|---|---|---|
| `table_exists` | 6 | 8 | 9 |
| `column_exists` | 33 | 44 | 50 |
| `column_type_correct` | 33 | 44 | 50 |
| `column_nullable_correct` | 27 | 32 | 36 |
| `column_primary_key_correct` | 6 | 8 | 9 |
| `column_default_correct` | 4 | 6 | 4 |
| `fk_exists` | 7 | 13 | 9 |
| `index_exists` | — | 2 | 2 |
| `table_removed` | 4 | 6 | 7 |
| `data_row_correct` | 17 | 30 | 35 |
| **Total** | **137** | **171** | **209** |

---

## Design Properties

| Property | Description |
|---|---|
| **Deterministic** | Same database state always produces the same score. No randomness or LLM-based evaluation |
| **Granular** | 137-209 checks per task. A single correct `CREATE TABLE` can pass 10+ checks. A single correct `INSERT` can pass several more |
| **Transparent** | Every failed check has a human-readable reason. No black-box scoring |
| **Unweighted** | Every check is worth exactly 1 point. No hidden multipliers or dimension weights |
| **Zero-start** | Acquisition theme ensures zero table name overlap between initial and target schemas. Score starts at 0.0 |
| **Comprehensive** | Covers schema structure (types, constraints, PKs, defaults), referential integrity (FKs, indexes), legacy cleanup (table drops), and row-level data accuracy |
| **OpenEnv-compatible** | `metadata.evaluation_results` follows the OpenEnv standard format for per-check evaluation results |
