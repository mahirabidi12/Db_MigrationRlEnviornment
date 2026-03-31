"""
Reward Pipeline — Checklist-Delta Reward
=========================================

reward = grader_score_after - grader_score_before

Same checklist grader used for final evaluation is used for step reward.
No weights, no separate scoring system. Agent optimizes for exactly what
it's graded on.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from db_migration_env.db_engine import DatabaseEngine
from db_migration_env.models import SchemaSnapshot


@dataclass
class RewardState:
    """Tracks grader score between steps."""
    prev_score: float = 0.0
    prev_checks_passed: int = 0
    prev_checks_total: int = 0
    step: int = 0


@dataclass
class RewardBreakdown:
    """Breakdown of reward for transparency."""
    score_before: float = 0.0
    score_after: float = 0.0
    checks_passed_before: int = 0
    checks_passed_after: int = 0
    checks_total: int = 0
    new_checks_passed: int = 0
    delta: float = 0.0
    total: float = 0.0

    def to_dict(self) -> dict:
        return {
            "score_before": round(self.score_before, 5),
            "score_after": round(self.score_after, 5),
            "checks_before": self.checks_passed_before,
            "checks_after": self.checks_passed_after,
            "checks_total": self.checks_total,
            "new_checks_passed": self.new_checks_passed,
            "delta": round(self.delta, 5),
            "total": round(self.total, 5),
        }


def init_reward_state(
    current_db: DatabaseEngine,
    target_db: DatabaseEngine,
    target_schema: SchemaSnapshot,
    initial_schema: Optional[SchemaSnapshot],
    grader,
) -> RewardState:
    """Initialize reward state by running the grader at reset."""
    result = grader.detailed_grade(
        current_db=current_db,
        target_db=target_db,
        target_schema=target_schema,
        steps_taken=0,
        max_steps=1,
        error_count=0,
        initial_schema=initial_schema,
    )
    return RewardState(
        prev_score=result["total_score"],
        prev_checks_passed=result["checks_passed"],
        prev_checks_total=result["checks_total"],
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
    reward = grader_score_after - grader_score_before

    That's it. No weights, no separate scoring.
    """
    reward_state.step += 1

    # Run the same grader used for final evaluation
    result = grader.detailed_grade(
        current_db=current_db,
        target_db=target_db,
        target_schema=target_schema,
        steps_taken=reward_state.step,
        max_steps=1,  # doesn't matter for checklist grader
        error_count=0,
        initial_schema=initial_schema,
    )

    score_after = result["total_score"]
    checks_after = result["checks_passed"]
    checks_total = result["checks_total"]

    delta = score_after - reward_state.prev_score
    new_checks = checks_after - reward_state.prev_checks_passed

    breakdown = RewardBreakdown(
        score_before=reward_state.prev_score,
        score_after=score_after,
        checks_passed_before=reward_state.prev_checks_passed,
        checks_passed_after=checks_after,
        checks_total=checks_total,
        new_checks_passed=new_checks,
        delta=delta,
        total=delta,
    )

    # Update state
    reward_state.prev_score = score_after
    reward_state.prev_checks_passed = checks_after
    reward_state.prev_checks_total = checks_total

    return breakdown
