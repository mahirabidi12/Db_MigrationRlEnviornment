"""
Reward Pipeline — Multi-Signal Reward Shaping for DB Migration
===============================================================

Provides dense, informative reward at every step across 7 dimensions.
Designed so an RL agent receives clear gradient toward the optimal migration path.

Signal Dimensions:
  1. Schema Progress   — delta in structural similarity to target
  2. Data Progress     — delta in row-level data correctness
  3. Diff Reduction    — bonus for reducing the number of schema diff items
  4. Milestone Bonus   — one-time rewards for key sub-goals (first table, first data, etc.)
  5. Error Penalty     — escalating penalty for consecutive errors
  6. Efficiency Cost   — small per-step cost that increases over time (urgency signal)
  7. Safety Penalty    — penalise data-destructive actions (DROP TABLE with data, DELETE)

The step reward is a weighted combination of all signals, normalized to roughly [-0.2, +0.5]
so the agent always has meaningful gradient.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from db_migration_env.db_engine import (
    DatabaseEngine,
    SchemaSnapshot,
    compute_data_score,
    compute_schema_diff,
    compute_schema_score,
)


@dataclass
class RewardState:
    """Tracks all state needed for reward computation across steps."""

    # Previous scores (for delta computation)
    prev_schema_score: float = 0.0
    prev_data_score: float = 0.0
    prev_diff_count: int = 999

    # Milestone tracking (one-time bonuses)
    milestones_achieved: Set[str] = field(default_factory=set)

    # Consecutive error tracking (escalating penalty)
    consecutive_errors: int = 0

    # Data safety tracking
    tables_with_data_at_start: Set[str] = field(default_factory=set)

    # Step counter for time-pressure curve
    step: int = 0
    max_steps: int = 50


@dataclass
class RewardBreakdown:
    """Full breakdown of reward components for transparency."""

    schema_progress: float = 0.0
    data_progress: float = 0.0
    diff_reduction: float = 0.0
    milestone_bonus: float = 0.0
    error_penalty: float = 0.0
    efficiency_cost: float = 0.0
    safety_penalty: float = 0.0
    total: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {
            "schema_progress": round(self.schema_progress, 5),
            "data_progress": round(self.data_progress, 5),
            "diff_reduction": round(self.diff_reduction, 5),
            "milestone_bonus": round(self.milestone_bonus, 5),
            "error_penalty": round(self.error_penalty, 5),
            "efficiency_cost": round(self.efficiency_cost, 5),
            "safety_penalty": round(self.safety_penalty, 5),
            "total": round(self.total, 5),
        }


# ── Milestones ──────────────────────────────────────────────────────────────

MILESTONES = {
    "first_target_table":    0.05,   # First target table created
    "all_tables_exist":      0.08,   # All target tables now exist
    "first_fk_correct":      0.03,   # First foreign key matches target
    "all_fks_correct":       0.06,   # All foreign keys match
    "first_data_match":      0.04,   # First table's data fully matches
    "all_data_match":        0.10,   # All target data matches (big bonus)
    "schema_perfect":        0.06,   # Schema score hits 1.0
    "source_tables_dropped": 0.04,   # All non-target source tables removed
}


# ── Reward Weights ──────────────────────────────────────────────────────────

W_SCHEMA_PROGRESS = 0.35     # Reward for schema improvement
W_DATA_PROGRESS = 0.40       # Reward for data improvement (harder, so weighted more)
W_DIFF_REDUCTION = 0.10      # Reward for reducing diff item count
W_MILESTONE = 1.0            # Milestones are absolute bonuses (not weighted further)
W_ERROR_PENALTY = 1.0        # Errors are absolute penalties
W_EFFICIENCY_COST = 1.0      # Step cost is absolute
W_SAFETY_PENALTY = 1.0       # Safety penalty is absolute


def init_reward_state(
    current_db: DatabaseEngine,
    target_schema: SchemaSnapshot,
    target_db: DatabaseEngine,
    max_steps: int,
) -> RewardState:
    """Initialize reward state at the start of an episode."""
    schema_score = compute_schema_score(current_db.get_schema_snapshot(), target_schema)
    data_score = compute_data_score(current_db, target_db, target_schema)
    diffs = compute_schema_diff(current_db.get_schema_snapshot(), target_schema)

    # Track which tables have data at the start (to detect destructive drops)
    tables_with_data = set()
    for tname in current_db.get_tables():
        if current_db.get_row_count(tname) > 0:
            tables_with_data.add(tname)

    return RewardState(
        prev_schema_score=schema_score,
        prev_data_score=data_score,
        prev_diff_count=len(diffs),
        tables_with_data_at_start=tables_with_data,
        step=0,
        max_steps=max_steps,
    )


def compute_step_reward(
    reward_state: RewardState,
    current_db: DatabaseEngine,
    target_db: DatabaseEngine,
    target_schema: SchemaSnapshot,
    sql: str,
    success: bool,
) -> RewardBreakdown:
    """
    Compute the full multi-signal reward for one step.

    Mutates reward_state to track progress across steps.
    Returns a RewardBreakdown with all components.
    """
    reward_state.step += 1
    breakdown = RewardBreakdown()

    current_schema = current_db.get_schema_snapshot()
    schema_score = compute_schema_score(current_schema, target_schema)
    data_score = compute_data_score(current_db, target_db, target_schema)
    diffs = compute_schema_diff(current_schema, target_schema)

    # ── 1. Schema Progress (delta) ──────────────────────────────────────
    schema_delta = schema_score - reward_state.prev_schema_score
    breakdown.schema_progress = W_SCHEMA_PROGRESS * schema_delta

    # ── 2. Data Progress (delta, weighted more since it's harder) ───────
    data_delta = data_score - reward_state.prev_data_score
    breakdown.data_progress = W_DATA_PROGRESS * data_delta

    # ── 3. Diff Reduction ───────────────────────────────────────────────
    diff_count = len(diffs)
    if reward_state.prev_diff_count > 0:
        diff_delta = reward_state.prev_diff_count - diff_count
        # Normalize: each diff item resolved is worth a small bonus
        breakdown.diff_reduction = W_DIFF_REDUCTION * (diff_delta / max(reward_state.prev_diff_count, 1))
    else:
        breakdown.diff_reduction = 0.0

    # ── 4. Milestone Bonuses (one-time) ─────────────────────────────────
    milestone_reward = 0.0
    target_tables = {t.name for t in target_schema.tables}
    current_tables = {t.name for t in current_schema.tables}

    # First target table created
    if "first_target_table" not in reward_state.milestones_achieved:
        if target_tables & current_tables:
            reward_state.milestones_achieved.add("first_target_table")
            milestone_reward += MILESTONES["first_target_table"]

    # All target tables exist
    if "all_tables_exist" not in reward_state.milestones_achieved:
        if target_tables <= current_tables:
            reward_state.milestones_achieved.add("all_tables_exist")
            milestone_reward += MILESTONES["all_tables_exist"]

    # FK milestones
    target_fks = set()
    current_fks = set()
    for t in target_schema.tables:
        for fk in t.foreign_keys:
            target_fks.add((t.name, fk.from_column, fk.to_table, fk.to_column))
    for t in current_schema.tables:
        for fk in t.foreign_keys:
            current_fks.add((t.name, fk.from_column, fk.to_table, fk.to_column))

    if target_fks:
        matched_fks = target_fks & current_fks
        if "first_fk_correct" not in reward_state.milestones_achieved and matched_fks:
            reward_state.milestones_achieved.add("first_fk_correct")
            milestone_reward += MILESTONES["first_fk_correct"]
        if "all_fks_correct" not in reward_state.milestones_achieved and target_fks <= current_fks:
            reward_state.milestones_achieved.add("all_fks_correct")
            milestone_reward += MILESTONES["all_fks_correct"]

    # Data milestones
    tables_with_perfect_data = 0
    for ttable in target_schema.tables:
        tdata = target_db.get_table_data(ttable.name)
        cdata = current_db.get_table_data(ttable.name)
        if tdata and cdata:
            tcols = [c.name for c in ttable.columns]
            t_set = _rows_to_comparable_set(tdata, tcols)
            c_set = _rows_to_comparable_set(cdata, tcols)
            if t_set == c_set:
                tables_with_perfect_data += 1

    if "first_data_match" not in reward_state.milestones_achieved and tables_with_perfect_data > 0:
        reward_state.milestones_achieved.add("first_data_match")
        milestone_reward += MILESTONES["first_data_match"]

    tables_with_target_data = sum(1 for t in target_schema.tables if target_db.get_table_data(t.name))
    if "all_data_match" not in reward_state.milestones_achieved:
        if tables_with_target_data > 0 and tables_with_perfect_data >= tables_with_target_data:
            reward_state.milestones_achieved.add("all_data_match")
            milestone_reward += MILESTONES["all_data_match"]

    # Schema perfect
    if "schema_perfect" not in reward_state.milestones_achieved and schema_score >= 0.999:
        reward_state.milestones_achieved.add("schema_perfect")
        milestone_reward += MILESTONES["schema_perfect"]

    # Source tables dropped (extra tables removed)
    extra_tables = current_tables - target_tables
    if "source_tables_dropped" not in reward_state.milestones_achieved:
        if not extra_tables and len(current_tables) == len(target_tables):
            reward_state.milestones_achieved.add("source_tables_dropped")
            milestone_reward += MILESTONES["source_tables_dropped"]

    breakdown.milestone_bonus = W_MILESTONE * milestone_reward

    # ── 5. Error Penalty (escalating for consecutive errors) ────────────
    if not success:
        reward_state.consecutive_errors += 1
        # Escalating: 1st error = -0.02, 2nd consecutive = -0.04, 3rd = -0.06, etc.
        breakdown.error_penalty = -0.02 * reward_state.consecutive_errors
    else:
        reward_state.consecutive_errors = 0
        breakdown.error_penalty = 0.0

    # ── 6. Efficiency Cost (increases over time — urgency signal) ───────
    # Starts small, grows as the agent uses more of its budget.
    # This creates a "time pressure" that encourages finishing early.
    t = reward_state.step / max(reward_state.max_steps, 1)
    # Quadratic curve: almost free at start, costly near end
    breakdown.efficiency_cost = -0.003 * (1.0 + 2.0 * t * t)

    # ── 7. Safety Penalty (data-destructive actions) ────────────────────
    upper_sql = sql.upper().strip()
    safety_penalty = 0.0

    if success:
        # DROP TABLE on a table that had data and isn't being replaced
        if "DROP TABLE" in upper_sql or "DROP TABLE IF EXISTS" in upper_sql:
            # Extract table name roughly
            for tname in reward_state.tables_with_data_at_start:
                if tname.upper() in upper_sql:
                    # Only penalize if the target schema also doesn't want this table
                    # (dropping source tables is expected and good)
                    if tname not in target_tables:
                        # This is actually GOOD — dropping a source table
                        pass
                    else:
                        # Dropping a target table that had data — dangerous!
                        safety_penalty -= 0.05

        # DELETE without WHERE — blanket data destruction
        if upper_sql.startswith("DELETE") and "WHERE" not in upper_sql:
            safety_penalty -= 0.03

        # UPDATE without WHERE — blanket modification
        if upper_sql.startswith("UPDATE") and "WHERE" not in upper_sql:
            # Mild penalty — sometimes UPDATE all rows is legitimate
            safety_penalty -= 0.01

    breakdown.safety_penalty = W_SAFETY_PENALTY * safety_penalty

    # ── Combine all signals ─────────────────────────────────────────────
    breakdown.total = (
        breakdown.schema_progress
        + breakdown.data_progress
        + breakdown.diff_reduction
        + breakdown.milestone_bonus
        + breakdown.error_penalty
        + breakdown.efficiency_cost
        + breakdown.safety_penalty
    )

    # Update state for next step
    reward_state.prev_schema_score = schema_score
    reward_state.prev_data_score = data_score
    reward_state.prev_diff_count = diff_count

    # Update tables_with_data tracking (for safety checks)
    current_tables_with_data = set()
    for tname in current_db.get_tables():
        if current_db.get_row_count(tname) > 0:
            current_tables_with_data.add(tname)
    reward_state.tables_with_data_at_start = current_tables_with_data

    return breakdown


def _rows_to_comparable_set(rows, cols):
    """Convert rows to a set for quick equality checks in milestone detection."""
    from db_migration_env.db_engine import _normalize_value
    result = set()
    for row in rows:
        vals = tuple(_normalize_value(row.get(c)) for c in cols)
        result.add(vals)
    return result
