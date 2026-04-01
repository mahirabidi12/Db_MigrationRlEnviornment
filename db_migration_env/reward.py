"""
Reward Pipeline — Checklist-Delta + Mistake Penalties
======================================================

reward = (grader_after - grader_before) - mistake_penalty

Positive: passing new grader checks.
Negative: any mistake — wrong type, wrong constraint, wrong FK,
junk tables/columns, SQL errors, wrong data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from db_migration_env.db_engine import DatabaseEngine, _normalize_type, _normalize_default
from db_migration_env.models import SchemaSnapshot


@dataclass
class RewardState:
    prev_score: float = 0.0
    prev_checks_passed: int = 0
    prev_checks_total: int = 0
    prev_mistakes: int = 0
    prev_wrong_data: int = 0
    step: int = 0


@dataclass
class RewardBreakdown:
    score_before: float = 0.0
    score_after: float = 0.0
    checks_passed_before: int = 0
    checks_passed_after: int = 0
    checks_total: int = 0
    new_checks_passed: int = 0
    delta: float = 0.0
    mistake_penalty: float = 0.0
    mistake_details: str = ""
    total: float = 0.0

    def to_dict(self) -> dict:
        d = {
            "score_before": round(self.score_before, 5),
            "score_after": round(self.score_after, 5),
            "checks_before": self.checks_passed_before,
            "checks_after": self.checks_passed_after,
            "checks_total": self.checks_total,
            "new_checks_passed": self.new_checks_passed,
            "delta": round(self.delta, 5),
            "mistake_penalty": round(self.mistake_penalty, 5),
            "total": round(self.total, 5),
        }
        if self.mistake_details:
            d["mistake_details"] = self.mistake_details
        return d


# Penalty per mistake type
PENALTIES = {
    "junk_table": 0.005,        # Table not in target
    "junk_column": 0.002,       # Column not in target
    "junk_fk": 0.002,           # FK not in target
    "wrong_type": 0.001,        # Column exists but wrong type
    "wrong_notnull": 0.001,     # Column exists but wrong NOT NULL
    "wrong_default": 0.001,     # Column exists but wrong DEFAULT
    "wrong_pk": 0.001,          # Column exists but missing PK
    "wrong_data": 0.0005,       # Row inserted but doesn't match target
    "sql_error": 0.001,         # SQL failed
}


def _count_mistakes(
    current_db: DatabaseEngine,
    target_schema: SchemaSnapshot,
    initial_schema: Optional[SchemaSnapshot],
) -> tuple:
    """Count all mistakes: junk + wrong types/constraints/data."""

    target_tables = {t.name: t for t in target_schema.tables}
    initial_table_names = {t.name for t in initial_schema.tables} if initial_schema else set()
    allowed_table_names = set(target_tables.keys()) | initial_table_names

    current_schema = current_db.get_schema_snapshot(include_data_preview=False)

    mistakes = 0
    details = []

    for ctable in current_schema.tables:
        # Junk table
        if ctable.name not in allowed_table_names:
            mistakes += 1
            details.append(f"junk table '{ctable.name}'")
            continue

        if ctable.name not in target_tables:
            continue  # Initial table still exists — not a mistake (just not dropped yet)

        ttable = target_tables[ctable.name]
        tcols = {c.name: c for c in ttable.columns}
        ccols = {c.name: c for c in ctable.columns}

        # Junk columns
        for cname in ccols:
            if cname not in tcols:
                mistakes += 1
                details.append(f"junk col '{ctable.name}.{cname}'")

        # Wrong type, NOT NULL, DEFAULT, PK for columns that exist
        for cname, tcol in tcols.items():
            if cname not in ccols:
                continue
            ccol = ccols[cname]

            if _normalize_type(ccol.type) != _normalize_type(tcol.type):
                mistakes += 1
                details.append(f"wrong type '{ctable.name}.{cname}' ({ccol.type}!={tcol.type})")

            if tcol.notnull and not ccol.notnull:
                mistakes += 1
                details.append(f"missing NOT NULL '{ctable.name}.{cname}'")

            if tcol.is_pk and not ccol.is_pk:
                mistakes += 1
                details.append(f"missing PK '{ctable.name}.{cname}'")

            if tcol.default_value is not None:
                if _normalize_default(ccol.default_value) != _normalize_default(tcol.default_value):
                    mistakes += 1
                    details.append(f"wrong default '{ctable.name}.{cname}'")

        # Junk FKs
        target_fk_set = {
            (fk.from_column, fk.to_table, fk.to_column)
            for fk in ttable.foreign_keys
        }
        current_fk_set = {
            (fk.from_column, fk.to_table, fk.to_column)
            for fk in ctable.foreign_keys
        }
        for fk in current_fk_set - target_fk_set:
            mistakes += 1
            details.append(f"junk FK '{ctable.name}.{fk[0]}→{fk[1]}'")

        # Wrong data — rows in current that don't match any target row
        from db_migration_env.db_engine import _normalize_value
        target_data = []
        # Get target DB data for this table
        # We need to pass target_db separately — can't access from here
        # So we count wrong data in the main function instead

    return mistakes, "; ".join(details[:10])


def _count_wrong_data(
    current_db: DatabaseEngine,
    target_db: DatabaseEngine,
    target_schema: SchemaSnapshot,
) -> int:
    """Count rows in current DB that exist in target tables but don't match any target row."""
    from db_migration_env.db_engine import _normalize_value

    wrong_rows = 0
    for ttable in target_schema.tables:
        current_data = current_db.get_table_data(ttable.name)
        target_data = target_db.get_table_data(ttable.name)

        if not current_data or not target_data:
            continue

        cols = [c.name for c in ttable.columns]

        # Build target multiset
        t_multiset = {}
        for row in target_data:
            key = tuple(_normalize_value(row.get(c)) for c in cols)
            t_multiset[key] = t_multiset.get(key, 0) + 1

        # Check each current row
        t_copy = dict(t_multiset)
        for row in current_data:
            key = tuple(_normalize_value(row.get(c)) for c in cols)
            if t_copy.get(key, 0) > 0:
                t_copy[key] -= 1
            else:
                wrong_rows += 1  # This row doesn't match any target row

    return wrong_rows


def init_reward_state(
    current_db: DatabaseEngine,
    target_db: DatabaseEngine,
    target_schema: SchemaSnapshot,
    initial_schema: Optional[SchemaSnapshot],
    grader,
) -> RewardState:
    result = grader.detailed_grade(
        current_db=current_db,
        target_db=target_db,
        target_schema=target_schema,
        steps_taken=0,
        max_steps=1,
        error_count=0,
        initial_schema=initial_schema,
    )
    m, _ = _count_mistakes(current_db, target_schema, initial_schema)
    return RewardState(
        prev_score=result["total_score"],
        prev_checks_passed=result["checks_passed"],
        prev_checks_total=result["checks_total"],
        prev_mistakes=m,
        step=0,
    )


def compute_step_reward(
    reward_state: RewardState,
    current_db: DatabaseEngine,
    target_db: DatabaseEngine,
    target_schema: SchemaSnapshot,
    initial_schema: Optional[SchemaSnapshot],
    grader,
    sql: str,
    success: bool,
) -> RewardBreakdown:
    """
    reward = (grader_after - grader_before) - new_mistake_penalty
    """
    reward_state.step += 1

    # Run grader
    result = grader.detailed_grade(
        current_db=current_db,
        target_db=target_db,
        target_schema=target_schema,
        steps_taken=reward_state.step,
        max_steps=1,
        error_count=0,
        initial_schema=initial_schema,
    )

    score_after = result["total_score"]
    checks_after = result["checks_passed"]
    checks_total = result["checks_total"]
    delta = score_after - reward_state.prev_score
    new_checks = checks_after - reward_state.prev_checks_passed

    # Count all mistakes (junk + wrong types/constraints)
    mistakes_now, mistake_details = _count_mistakes(current_db, target_schema, initial_schema)
    new_mistakes = max(0, mistakes_now - reward_state.prev_mistakes)

    # Count wrong data rows — only penalize NEW ones
    wrong_data = _count_wrong_data(current_db, target_db, target_schema)
    new_wrong_data = max(0, wrong_data - reward_state.prev_wrong_data)

    # Calculate penalty
    penalty = new_mistakes * 0.002  # avg penalty per structural mistake
    penalty += new_wrong_data * PENALTIES["wrong_data"]
    if not success:
        penalty += PENALTIES["sql_error"]

    # Build details
    parts = []
    if new_mistakes > 0:
        parts.append(f"{new_mistakes} new mistake(s): {mistake_details}")
    if wrong_data > 0:
        parts.append(f"{wrong_data} wrong data row(s)")
    if not success:
        parts.append("SQL error")

    total = delta - penalty

    breakdown = RewardBreakdown(
        score_before=reward_state.prev_score,
        score_after=score_after,
        checks_passed_before=reward_state.prev_checks_passed,
        checks_passed_after=checks_after,
        checks_total=checks_total,
        new_checks_passed=new_checks,
        delta=delta,
        mistake_penalty=-penalty if penalty > 0 else 0.0,
        mistake_details="; ".join(parts),
        total=total,
    )

    # Update state
    reward_state.prev_score = score_after
    reward_state.prev_checks_passed = checks_after
    reward_state.prev_checks_total = checks_total
    reward_state.prev_mistakes = mistakes_now
    reward_state.prev_wrong_data = wrong_data

    return breakdown
