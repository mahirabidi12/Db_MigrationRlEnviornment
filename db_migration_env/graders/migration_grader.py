"""Deterministic grader for DB migration tasks.

Produces a score 0.0–1.0 by comparing the agent's final DB state against
the target state on two axes: schema correctness and data correctness.
"""

from __future__ import annotations

from db_migration_env.db_engine import (
    DatabaseEngine,
    compute_data_score,
    compute_schema_score,
)
from db_migration_env.models import SchemaSnapshot


class MigrationGrader:
    """Grades a completed migration episode."""

    # Weight split — schema and data are equally important,
    # with a small efficiency component.
    SCHEMA_WEIGHT = 0.40
    DATA_WEIGHT = 0.45
    EFFICIENCY_WEIGHT = 0.15

    def grade(
        self,
        current_db: DatabaseEngine,
        target_db: DatabaseEngine,
        target_schema: SchemaSnapshot,
        steps_taken: int,
        max_steps: int,
        error_count: int,
    ) -> float:
        """Return a score between 0.0 and 1.0."""
        schema_score = compute_schema_score(
            current_db.get_schema_snapshot(), target_schema
        )
        data_score = compute_data_score(current_db, target_db, target_schema)

        # Efficiency: reward finishing in fewer steps, penalise errors
        if max_steps > 0:
            step_ratio = steps_taken / max_steps
            efficiency = max(0.0, 1.0 - step_ratio)
        else:
            efficiency = 1.0
        error_penalty = min(1.0, error_count * 0.05)
        efficiency_score = max(0.0, efficiency - error_penalty)

        total = (
            self.SCHEMA_WEIGHT * schema_score
            + self.DATA_WEIGHT * data_score
            + self.EFFICIENCY_WEIGHT * efficiency_score
        )
        return round(max(0.0, min(1.0, total)), 4)

    def detailed_grade(
        self,
        current_db: DatabaseEngine,
        target_db: DatabaseEngine,
        target_schema: SchemaSnapshot,
        steps_taken: int,
        max_steps: int,
        error_count: int,
    ) -> dict:
        """Return breakdown alongside total score."""
        schema_score = compute_schema_score(
            current_db.get_schema_snapshot(), target_schema
        )
        data_score = compute_data_score(current_db, target_db, target_schema)
        if max_steps > 0:
            step_ratio = steps_taken / max_steps
            efficiency = max(0.0, 1.0 - step_ratio)
        else:
            efficiency = 1.0
        error_penalty = min(1.0, error_count * 0.05)
        efficiency_score = max(0.0, efficiency - error_penalty)

        total = (
            self.SCHEMA_WEIGHT * schema_score
            + self.DATA_WEIGHT * data_score
            + self.EFFICIENCY_WEIGHT * efficiency_score
        )
        total = round(max(0.0, min(1.0, total)), 4)

        return {
            "total_score": total,
            "schema_score": round(schema_score, 4),
            "data_score": round(data_score, 4),
            "efficiency_score": round(efficiency_score, 4),
            "steps_taken": steps_taken,
            "max_steps": max_steps,
            "error_count": error_count,
            "weights": {
                "schema": self.SCHEMA_WEIGHT,
                "data": self.DATA_WEIGHT,
                "efficiency": self.EFFICIENCY_WEIGHT,
            },
        }
