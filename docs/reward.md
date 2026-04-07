# Reward Function — Checklist-Delta with Mistake Penalties

**Reward range: -1.0 to +1.0**

The reward pipeline provides **dense feedback at every step**:

```
step_reward = (grader_score_after - grader_score_before) - mistake_penalties
```

---

## How It Works

After every `step()`, the environment:

1. Runs the full grader on the current DB state → gets `score_after`
2. Computes `delta = score_after - score_before`
3. Counts all structural mistakes and wrong data rows in the current DB
4. Computes penalties for only the **NEW** mistakes introduced by this step (not pre-existing ones)
5. Returns `total = delta - penalty`

The reward can be **positive** (agent made progress), **negative** (agent broke something or introduced mistakes), or **zero** (no-op SQL like a SELECT).

---

## Penalty Categories

The code defines 9 distinct penalty types in `reward.py`:

| Penalty Type | Amount | Triggered When |
|---|---|---|
| `junk_table` | 0.005 | Agent created a table that doesn't exist in the target schema |
| `junk_column` | 0.002 | Agent added a column that doesn't exist in the target |
| `junk_fk` | 0.002 | Agent added a foreign key not in the target |
| `wrong_type` | 0.001 | Column exists but has the wrong data type |
| `wrong_notnull` | 0.001 | Column exists but NOT NULL constraint is wrong |
| `wrong_default` | 0.001 | Column exists but DEFAULT value is wrong |
| `wrong_pk` | 0.001 | Column exists but PRIMARY KEY flag is missing |
| `wrong_data` | 0.0005 | A row in a target table doesn't match any expected row |
| `sql_error` | 0.001 | The SQL statement failed to execute |

### Only NEW mistakes are penalized

The environment tracks `prev_mistakes` and `prev_wrong_data` from the previous step. Only the **difference** is penalized:

```
new_mistakes = max(0, mistakes_now - prev_mistakes)
new_wrong_data = max(0, wrong_data_now - prev_wrong_data)
penalty = new_mistakes * 0.002 + new_wrong_data * 0.0005 + (0.001 if sql_error)
```

This means:
- If the agent creates a junk table on step 5, it gets penalized once on step 5
- On step 6, that junk table still exists but is NOT penalized again
- If the agent drops the junk table on step 7, `mistakes_now` decreases — no penalty, and the delta improves

---

## Mistake Detection — `_count_mistakes()`

The reward function inspects the current DB and counts structural violations:

- **Junk tables** — any table that's not in the target schema AND not in the initial schema (tables from the initial schema that haven't been dropped yet are not mistakes — they're just "not done yet")
- **Junk columns** — columns in a target table that don't exist in the target's column list
- **Wrong types** — column exists but type doesn't match (after normalization: `INT` = `INTEGER`, etc.)
- **Missing NOT NULL** — target says NOT NULL, current doesn't have it
- **Missing PK** — target says PRIMARY KEY, current doesn't have it
- **Wrong DEFAULT** — target has a DEFAULT value, current has a different one (after normalization)
- **Junk FKs** — foreign keys on a target table that don't exist in the target FK list

Details are capped at 10 items per step in the breakdown string to keep it readable.

---

## Wrong Data Detection — `_count_wrong_data()`

For every table in the target schema, the function:

1. Gets all rows from the current DB and target DB for that table
2. Builds a **multiset** of target rows (handles duplicate rows correctly)
3. For each row in the current DB, checks if it matches any remaining target row
4. Rows that don't match anything = wrong data

Row matching uses `_normalize_value()` which handles:
- Integer/float equivalence (`1` matches `1.0`)
- NULL handling
- String normalization

---

## RewardBreakdown — What Gets Returned

Every step returns a `RewardBreakdown` with these fields:

| Field | Type | Description |
|---|---|---|
| `score_before` | float | Grader score before this step (0.0–1.0) |
| `score_after` | float | Grader score after this step (0.0–1.0) |
| `checks_passed_before` | int | Number of grader checks passing before |
| `checks_passed_after` | int | Number of grader checks passing after |
| `checks_total` | int | Total number of grader checks |
| `new_checks_passed` | int | Delta: `checks_after - checks_before` (can be negative) |
| `delta` | float | Raw score change: `score_after - score_before` |
| `mistake_penalty` | float | Penalty applied this step (always <= 0) |
| `mistake_details` | str | Human-readable list of new mistakes |
| `total` | float | Final step reward: `delta - penalty` |

This breakdown is available in the observation at `metadata.reward_breakdown`.

### Example breakdown

Agent creates a correct table with 3 columns, passing 7 new checks out of 1,468 total:

```json
{
  "score_before": 0.10014,
  "score_after": 0.10491,
  "checks_before": 147,
  "checks_after": 154,
  "checks_total": 1468,
  "new_checks_passed": 7,
  "delta": 0.00477,
  "mistake_penalty": 0.0,
  "total": 0.00477
}
```

Agent runs a bad INSERT that introduces 3 wrong data rows:

```json
{
  "score_before": 0.45,
  "score_after": 0.452,
  "checks_before": 661,
  "checks_after": 664,
  "checks_total": 1468,
  "new_checks_passed": 3,
  "delta": 0.002,
  "mistake_penalty": -0.0015,
  "mistake_details": "3 new wrong data row(s)",
  "total": 0.0005
}
```

Agent runs invalid SQL:

```json
{
  "score_before": 0.45,
  "score_after": 0.45,
  "checks_before": 661,
  "checks_after": 661,
  "checks_total": 1468,
  "new_checks_passed": 0,
  "delta": 0.0,
  "mistake_penalty": -0.001,
  "mistake_details": "SQL error",
  "total": -0.001
}
```

---

## RewardState — Tracking Across Steps

The environment maintains a `RewardState` object across the episode:

| Field | Purpose |
|---|---|
| `prev_score` | Last grader score — used to compute delta |
| `prev_checks_passed` | Last checks passed count |
| `prev_checks_total` | Total checks (stays constant within an episode) |
| `prev_mistakes` | Structural mistake count after last step |
| `prev_wrong_data` | Wrong data row count after last step |
| `step` | Current step number |

This state is initialized at `reset()` by running the grader on the initial DB and counting pre-existing mistakes. This ensures the agent is never penalized for the starting state.

---

## Design Properties

- **Dense gradient**: Every step has meaningful signal — not sparse end-of-episode
- **Progress-aware**: Positive reward for passing new checks, negative for regression
- **Only penalizes NEW mistakes**: Tracks previous state so pre-existing issues don't get re-penalized
- **Cumulative tracking**: `metadata.cumulative_reward` tracks total reward across the episode
- **Detailed breakdown**: Each step includes `metadata.reward_breakdown` with full details
- **No double-counting**: A junk table created on step 5 is penalized once, not every subsequent step
- **Regression-sensitive**: If the agent drops a table it already built correctly, `delta` goes negative
