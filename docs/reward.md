# Reward Function — Dense, Per-Step Feedback

## Overview

The reward pipeline provides immediate feedback after every SQL statement, enabling fine-grained credit assignment. Rather than a single score at episode end, the agent receives a detailed reward breakdown at each step.

```
step_reward = (grader_score_after - grader_score_before) - mistake_penalties
```

**Typical range:** -0.01 to +0.02 per step. Cumulative reward tracks total progress across the episode.

---

## Architecture

The reward system is implemented in `reward.py` with two core components:

### RewardState

Maintained across the episode. Initialized at `reset()` by running the grader on the initial database.

```python
@dataclass
class RewardState:
    prev_score: float        # Last grader score (0.0 to 1.0)
    prev_checks_passed: int  # Last passing check count
    prev_checks_total: int   # Total checks (constant per episode)
    prev_mistakes: int       # Structural mistake count after last step
    prev_wrong_data: int     # Wrong data row count after last step
    step: int                # Current step number
```

### RewardBreakdown

Returned by `compute_step_reward()` after every step:

```python
@dataclass
class RewardBreakdown:
    score_before: float          # Grader score before this step
    score_after: float           # Grader score after this step
    checks_passed_before: int
    checks_passed_after: int
    checks_total: int
    new_checks_passed: int       # Delta (can be negative on regression)
    delta: float                 # score_after - score_before
    mistake_penalty: float       # Always <= 0
    mistake_details: str         # Human-readable description
    total: float                 # delta - penalty = final step reward
```

Available to the agent in `metadata.reward_breakdown` on every observation.

---

## Computation Pipeline

After every `step()`, `compute_step_reward()` executes:

1. **Run full grader** on current database → `score_after`, `checks_after`
2. **Compute delta** → `score_after - prev_score`
3. **Count structural mistakes** via `_count_mistakes()` → junk tables, junk columns, wrong types, wrong constraints, junk FKs
4. **Count wrong data rows** via `_count_wrong_data()` → rows in target tables that don't match expected data
5. **Compute penalties for NEW mistakes only** → `max(0, mistakes_now - prev_mistakes)`
6. **Add SQL error penalty** if the statement failed
7. **Return breakdown** → `total = delta - penalty`
8. **Update RewardState** for next step

---

## Penalty Schedule

Defined in the `PENALTIES` dictionary:

| Category | Penalty Type | Amount per instance | Trigger condition |
|---|---|---|---|
| **Structural** | `junk_table` | -0.05 | Table created that exists in neither target nor initial schema |
| **Structural** | `junk_column` | -0.02 | Column in a target table that doesn't exist in the target specification |
| **Structural** | `junk_fk` | -0.02 | Foreign key on a target table that isn't in the target specification |
| **Constraint** | `wrong_type` | -0.01 | Column exists but type doesn't match (after normalization) |
| **Constraint** | `wrong_notnull` | -0.01 | Target says NOT NULL, current column allows NULL |
| **Constraint** | `wrong_default` | -0.01 | DEFAULT value doesn't match (after normalization) |
| **Constraint** | `wrong_pk` | -0.01 | Target says PRIMARY KEY, current column isn't PK |
| **Data** | `wrong_data` | -0.005 per row | Row in current DB doesn't match any expected target row |
| **Execution** | `sql_error` | -0.01 flat | SQL statement failed to execute |

**Note:** The actual penalty computation uses a flat `0.02` per structural mistake rather than looking up individual penalty values from the dictionary. Data penalties use `0.005` per wrong row as specified.

### Delta-Based Penalty Model

Only **new** mistakes are penalized each step:

```python
new_mistakes = max(0, mistakes_now - prev_mistakes)
new_wrong_data = max(0, wrong_data_now - prev_wrong_data)
penalty = new_mistakes * 0.02 + new_wrong_data * 0.005 + (0.01 if sql_error)
```

| Step | Event | Penalty |
|---|---|---|
| Step 5 | Agent creates a junk table | -0.02 (penalized once) |
| Step 6 | Junk table still exists | 0.0 (not re-penalized) |
| Step 7 | Agent drops the junk table | 0.0 (mistake count decreases, no penalty) |

---

## Mistake Detection

### `_count_mistakes()` — Structural Inspection

Iterates over all tables in the current database and counts:

| Mistake | Detection logic |
|---|---|
| Junk table | Table name not in target schema AND not in initial schema. (Initial tables that haven't been dropped yet are not penalized — they're just "not done yet") |
| Junk column | Column exists in a target table but isn't in the target's column list |
| Wrong type | Column exists, types don't match after `_normalize_type()` (`INT` = `INTEGER`, `BOOL` = `INTEGER`, etc.) |
| Missing NOT NULL | Target column has `notnull=True`, current column doesn't |
| Missing PK | Target column has `is_pk=True`, current column doesn't |
| Wrong DEFAULT | Target column has a DEFAULT, current column has a different value after `_normalize_default()` |
| Junk FK | Foreign key exists on a target table but isn't in the target's FK set |

Returns `(total_mistakes, details_string)`. Details are capped at 10 items for readability.

### `_count_wrong_data()` — Row-Level Data Inspection

For every table in the target schema:

1. Retrieve all rows from both current and target databases
2. Build a target **multiset** (handles duplicate rows)
3. For each row in the current database, check if it matches any remaining target row using `_normalize_value()`
4. Rows that don't match = wrong data

Value normalization handles integer/float equivalence (`1` = `1.0`), float rounding to 2 decimal places, and NULL-safe comparison.

---

## Initialization

`init_reward_state()` is called at episode reset:

1. Runs the full grader on the initial database to get the starting score
2. Counts pre-existing structural mistakes
3. Returns a `RewardState` with these as the baseline

This ensures the agent is never penalized for the starting state. In our acquisition-themed tasks, the initial score is always 0.0 (zero table name overlap), and pre-existing mistakes are 0 (no junk tables at start).

---

## Examples

**Positive reward — agent creates a correct table:**
```json
{
  "score_before": 0.10,
  "score_after": 0.15,
  "checks_before": 147,
  "checks_after": 154,
  "checks_total": 171,
  "new_checks_passed": 7,
  "delta": 0.05,
  "mistake_penalty": 0.0,
  "total": 0.05
}
```

**Mixed reward — progress with data errors:**
```json
{
  "score_before": 0.45,
  "score_after": 0.50,
  "new_checks_passed": 5,
  "delta": 0.05,
  "mistake_penalty": -0.01,
  "mistake_details": "2 new wrong data row(s)",
  "total": 0.04
}
```

**Negative reward — SQL failure:**
```json
{
  "score_before": 0.450,
  "score_after": 0.450,
  "new_checks_passed": 0,
  "delta": 0.0,
  "mistake_penalty": -0.01,
  "mistake_details": "SQL error",
  "total": -0.01
}
```

**Regression — agent drops a table it already built:**
```json
{
  "score_before": 0.45,
  "score_after": 0.35,
  "new_checks_passed": -18,
  "delta": -0.10,
  "mistake_penalty": 0.0,
  "total": -0.10
}
```

---

## Design Principles

| Principle | Implementation |
|---|---|
| **Dense signal** | Every step gets a meaningful reward — not sparse end-of-episode |
| **Progress-aware** | Positive delta for new checks, negative delta for regression |
| **No double-counting** | Delta-based penalties charge each new mistake exactly once |
| **Regression-sensitive** | Dropping a correctly-built table immediately produces negative delta |
| **Transparent** | `mistake_details` explains every penalty in human-readable text |
| **Cumulative tracking** | `metadata.cumulative_reward` provides running total across the episode |
| **Consistent with grader** | Reward delta is derived directly from the same grader that produces the final score |
