# Grader — Checklist-Based (0.0 to 1.0)

The grader uses a flat checklist system. Every check is worth exactly 1 point.

**Score = checks_passed / total_checks**

## 12 Check Types

| # | Check Type | What it verifies |
|---|---|---|
| 1 | `table_exists` | Target table is present |
| 2 | `column_exists` | Target column exists in the table |
| 3 | `column_type_correct` | Column has the correct type (INTEGER, TEXT, REAL) |
| 4 | `column_nullable_correct` | NOT NULL constraint matches |
| 5 | `column_primary_key_correct` | PRIMARY KEY flag matches |
| 6 | `column_default_correct` | DEFAULT value matches |
| 7 | `fk_exists` | Foreign key constraint is present |
| 8 | `index_exists` | Index exists with correct columns and uniqueness |
| 9 | `table_removed` | Legacy table has been dropped |
| 10 | `column_removed` | Old column no longer exists in restructured table |
| 11 | `fk_removed` | Old FK constraint has been removed |
| 12 | `data_row_correct` | Target row exists in current DB (row-level multiset match) |

## Properties
- **Deterministic** — same inputs always produce the same score
- **Continuous** — scores range from 0.0 to 1.0 with fine granularity (1000+ checks per task)
- **Comprehensive** — checks schema structure AND data correctness
- **No weights** — every check counts equally, making the score transparent
