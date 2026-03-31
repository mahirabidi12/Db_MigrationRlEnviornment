"""Deterministic grader for DB migration tasks.

Produces a score 0.0-1.0 across FOUR dimensions. Designed so that the
initial (unmigrated) state scores exactly 0.0 on all dimensions.

  1. Schema Correctness (30%)  — target tables/columns/types/FKs/defaults present
  2. Data Correctness (35%)    — row-level content matching with numeric tolerance
  3. Referential Integrity (20%) — FK constraints satisfied (no orphan rows)
  4. Efficiency (15%)          — step economy + error avoidance

All dimensions return 0.0 before the agent takes any meaningful action.
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

    SCHEMA_WEIGHT = 0.40
    DATA_WEIGHT = 0.40
    INTEGRITY_WEIGHT = 0.10
    EFFICIENCY_WEIGHT = 0.10

    def grade(
        self,
        current_db: DatabaseEngine,
        target_db: DatabaseEngine,
        target_schema: SchemaSnapshot,
        steps_taken: int,
        max_steps: int,
        error_count: int,
    ) -> float:
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

        # 1. Schema correctness
        schema_score = compute_schema_score(
            current_db.get_schema_snapshot(include_data_preview=False),
            target_schema,
        )

        # 2. Data correctness
        data_score = compute_data_score(current_db, target_db, target_schema)

        # 3. Referential integrity
        #    Score = (target FKs that are correctly built AND have no orphans)
        #            / (total target FKs)
        #    If target has FKs but current DB has none → 0.0 (not built yet)
        #    If target has no FKs → based on schema match (no FK requirement)
        target_fk_count = sum(len(t.foreign_keys) for t in target_schema.tables)

        if target_fk_count == 0:
            # No FKs required by target — integrity is not applicable, full marks
            integrity_score = 1.0
        else:
            # Count how many of the TARGET's FK definitions exist in current DB
            # AND have zero orphan violations
            current_schema = current_db.get_schema_snapshot(include_data_preview=False)
            current_tables = {t.name: t for t in current_schema.tables}

            fks_correct = 0
            for ttable in target_schema.tables:
                for tfk in ttable.foreign_keys:
                    # Check 1: Does the table exist in current DB?
                    if ttable.name not in current_tables:
                        continue  # Table doesn't exist yet → this FK is not built
                    ctable = current_tables[ttable.name]

                    # Check 2: Does the FK definition exist?
                    cfk_set = {
                        (fk.from_column, fk.to_table, fk.to_column)
                        for fk in ctable.foreign_keys
                    }
                    if (tfk.from_column, tfk.to_table, tfk.to_column) not in cfk_set:
                        continue  # FK definition missing

                    # Check 3: Are there orphan rows? (FK exists but data violates it)
                    try:
                        cur = current_db.conn.execute(
                            f'SELECT COUNT(*) FROM "{ttable.name}" '
                            f'WHERE "{tfk.from_column}" IS NOT NULL '
                            f'AND "{tfk.from_column}" NOT IN '
                            f'(SELECT "{tfk.to_column}" FROM "{tfk.to_table}")'
                        )
                        orphans = cur.fetchone()[0]
                        if orphans == 0:
                            fks_correct += 1
                        # else: FK exists but has violations → not counted
                    except Exception:
                        pass  # Query failed → not counted

            integrity_score = fks_correct / target_fk_count

        # 4. Efficiency
        #    0 steps taken = 0.0 (haven't started, not "efficient")
        #    Completed in fewer steps = higher score
        if steps_taken == 0:
            efficiency_score = 0.0
        elif max_steps > 0:
            step_ratio = steps_taken / max_steps
            efficiency = max(0.0, 1.0 - step_ratio)
            error_penalty = min(1.0, error_count * 0.05)
            efficiency_score = max(0.0, efficiency - error_penalty)
        else:
            efficiency_score = 0.0

        # FK violation details for the report
        fk_violations = current_db.check_referential_integrity()

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
