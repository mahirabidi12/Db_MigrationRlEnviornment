"""Deterministic grader for DB migration tasks.

Produces a score 0.0-1.0 by comparing the agent's final DB state against
the target state across FOUR dimensions:

  1. Schema Correctness (30%)  — tables, columns, types, constraints, FKs, defaults
  2. Data Correctness (35%)    — row-level content matching with numeric tolerance
  3. Referential Integrity (20%) — FK constraints satisfied (no orphan rows)
  4. Efficiency (15%)          — step count + error penalty

The integrity dimension is critical: an agent that creates correct tables
but inserts data with broken foreign key references will be penalized.
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

    SCHEMA_WEIGHT = 0.30
    DATA_WEIGHT = 0.35
    INTEGRITY_WEIGHT = 0.20
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
        return self.detailed_grade(
            current_db, target_db, target_schema,
            steps_taken, max_steps, error_count,
        )["total_score"]

    def detailed_grade(
        self,
        current_db: DatabaseEngine,
        target_db: DatabaseEngine,
        target_schema: SchemaSnapshot,
        steps_taken: int,
        max_steps: int,
        error_count: int,
    ) -> dict:
        """Return full breakdown alongside total score."""

        # 1. Schema correctness
        schema_score = compute_schema_score(
            current_db.get_schema_snapshot(include_data_preview=False),
            target_schema,
        )

        # 2. Data correctness (row-level comparison with numeric tolerance)
        data_score = compute_data_score(current_db, target_db, target_schema)

        # 3. Referential integrity — are FK constraints satisfied in the data?
        integrity_score = current_db.compute_integrity_score()
        # Also check against the target's integrity for comparison
        target_integrity = target_db.compute_integrity_score()
        # If the target itself has no FKs, don't penalize
        target_fk_count = sum(
            len(t.foreign_keys) for t in target_schema.tables
        )
        if target_fk_count == 0:
            integrity_score = 1.0

        # Get FK violation details for the report
        fk_violations = current_db.check_referential_integrity()

        # 4. Efficiency: reward finishing in fewer steps, penalise errors
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
            + self.INTEGRITY_WEIGHT * integrity_score
            + self.EFFICIENCY_WEIGHT * efficiency_score
        )
        total = round(max(0.0, min(1.0, total)), 4)

        return {
            "total_score": total,
            "schema_score": round(schema_score, 4),
            "data_score": round(data_score, 4),
            "integrity_score": round(integrity_score, 4),
            "efficiency_score": round(efficiency_score, 4),
            "steps_taken": steps_taken,
            "max_steps": max_steps,
            "error_count": error_count,
            "fk_violations": fk_violations,
            "weights": {
                "schema": self.SCHEMA_WEIGHT,
                "data": self.DATA_WEIGHT,
                "integrity": self.INTEGRITY_WEIGHT,
                "efficiency": self.EFFICIENCY_WEIGHT,
            },
        }
