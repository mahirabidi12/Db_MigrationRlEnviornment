"""Checklist-based grader for DB migration tasks.

Every check is worth exactly 1 point. No weights, no dimensions.
Score = checks_passed / total_checks (0.0 to 1.0).

12 check types:
  1.  table_exists           — target table is present
  2.  column_exists          — target column is present in the table
  3.  column_type_correct    — column has correct type
  4.  column_nullable_correct — NOT NULL flag matches
  5.  column_primary_key_correct — PK flag matches
  6.  column_default_correct — DEFAULT value matches
  7.  fk_exists              — target FK (col + ref_table + ref_col) is present
  8.  index_exists           — target index (col + unique flag) is present
  9.  table_removed          — old/legacy table is gone
  10. column_removed         — old column no longer exists in restructured table
  11. fk_removed             — old FK no longer exists
  12. data_row_correct       — target row exists in current DB (row-level match)
"""

from __future__ import annotations

from typing import Dict, List, Optional

from db_migration_env.db_engine import (
    DatabaseEngine,
    _normalize_type,
    _normalize_default,
    _normalize_value,
)
from db_migration_env.models import SchemaSnapshot


class CheckResult:
    """One grader check."""

    def __init__(self, check_type: str, table: str, detail: str, passed: bool, target: str = "", actual: str = ""):
        self.check_type = check_type
        self.table = table
        self.detail = detail
        self.passed = passed
        self.target = target  # what was expected
        self.actual = actual  # what was found

    def to_dict(self) -> dict:
        d = {
            "name": f"{self.check_type}: {self.table}.{self.detail}",
            "check_type": self.check_type,
            "table": self.table,
            "detail": self.detail,
            "score": 1.0 if self.passed else 0.0,
            "passed": self.passed,
            "expected": self.target or "",
            "actual": self.actual or "",
        }
        if not self.passed:
            d["reason"] = self._failure_reason()
        return d

    def _failure_reason(self) -> str:
        """Human-readable explanation of why this check failed."""
        # Extract column name from detail like "Column 'email'" or "Column 'email' type"
        col = self.detail.split("'")[1] if "'" in self.detail else ""

        if self.check_type == "table_exists":
            return f"Table '{self.table}' does not exist. Run: CREATE TABLE {self.table} (...)"
        elif self.check_type == "column_exists":
            return f"Column '{self.table}.{col}' is missing. Expected column '{col}' in table '{self.table}'."
        elif self.check_type == "column_type_correct":
            return f"Wrong type for '{self.table}.{col}'. Expected {self.target}, got {self.actual}."
        elif self.check_type == "column_nullable_correct":
            return f"Wrong constraint for '{self.table}.{col}'. Expected {self.target}, got {self.actual}."
        elif self.check_type == "column_primary_key_correct":
            return f"'{self.table}.{col}' should be PRIMARY KEY but is not."
        elif self.check_type == "column_default_correct":
            return f"Wrong default for '{self.table}.{col}'. Expected DEFAULT {self.target}, got DEFAULT {self.actual}."
        elif self.check_type == "fk_exists":
            return f"Missing FK on '{self.table}': {self.detail}. Need FOREIGN KEY constraint."
        elif self.check_type == "index_exists":
            return f"Missing index on '{self.table}': {self.detail}."
        elif self.check_type == "table_removed":
            return f"Legacy table '{self.table}' still exists. Run: DROP TABLE {self.table}"
        elif self.check_type == "column_removed":
            return f"Old column '{self.table}.{col}' still exists. Must be removed (recreate table in SQLite)."
        elif self.check_type == "fk_removed":
            return f"Old FK on '{self.table}' still exists: {self.detail}. Must be removed."
        elif self.check_type == "index_removed":
            return f"Old index on '{self.table}' still exists: {self.detail}."
        elif self.check_type == "data_row_correct":
            return f"Expected row missing in '{self.table}': {self.detail}. Data not migrated correctly."
        return f"Check failed on '{self.table}': expected={self.target}, actual={self.actual}"


class MigrationGrader:
    """Checklist-based grader. Score = passed / total. No weights."""

    def grade(
        self,
        current_db: DatabaseEngine,
        target_db: DatabaseEngine,
        target_schema: SchemaSnapshot,
        steps_taken: int,
        max_steps: int,
        error_count: int,
        initial_schema: Optional[SchemaSnapshot] = None,
    ) -> float:
        return self.detailed_grade(
            current_db, target_db, target_schema,
            steps_taken, max_steps, error_count,
            initial_schema,
        )["total_score"]

    def detailed_grade(
        self,
        current_db: DatabaseEngine,
        target_db: DatabaseEngine,
        target_schema: SchemaSnapshot,
        steps_taken: int,
        max_steps: int,
        error_count: int,
        initial_schema: Optional[SchemaSnapshot] = None,
    ) -> dict:
        checks: List[CheckResult] = []
        current_schema = current_db.get_schema_snapshot(include_data_preview=False)
        current_tables = {t.name: t for t in current_schema.tables}
        target_tables = {t.name: t for t in target_schema.tables}

        # Also build initial tables map for "removed" checks
        initial_tables = {}
        if initial_schema:
            initial_tables = {t.name: t for t in initial_schema.tables}

        # ── 1. table_exists — target table is present ──────────────────
        for tname in target_tables:
            checks.append(CheckResult(
                check_type="table_exists",
                table=tname,
                detail=f"Table '{tname}' exists",
                passed=tname in current_tables,
                target="exists",
                actual="exists" if tname in current_tables else "missing",
            ))

        # For each target table that exists in current DB, check columns/FKs
        for tname, ttable in target_tables.items():
            if tname not in current_tables:
                # Table missing — all its column/FK checks auto-fail
                for tcol in ttable.columns:
                    checks.append(CheckResult("column_exists", tname, f"Column '{tcol.name}'", False, "exists", "table missing"))
                    checks.append(CheckResult("column_type_correct", tname, f"Column '{tcol.name}' type", False, tcol.type, "table missing"))
                    if tcol.notnull:
                        checks.append(CheckResult("column_nullable_correct", tname, f"Column '{tcol.name}' NOT NULL", False, "NOT NULL", "table missing"))
                    if tcol.is_pk:
                        checks.append(CheckResult("column_primary_key_correct", tname, f"Column '{tcol.name}' PRIMARY KEY", False, "PK", "table missing"))
                    if tcol.default_value is not None:
                        checks.append(CheckResult("column_default_correct", tname, f"Column '{tcol.name}' DEFAULT", False, str(tcol.default_value), "table missing"))
                for tfk in ttable.foreign_keys:
                    checks.append(CheckResult("fk_exists", tname, f"FK {tfk.from_column}→{tfk.to_table}({tfk.to_column})", False, "exists", "table missing"))
                continue

            ctable = current_tables[tname]
            ccols = {c.name: c for c in ctable.columns}
            tcols = {c.name: c for c in ttable.columns}

            # ── 2. column_exists ───────────────────────────────────────
            for cname, tcol in tcols.items():
                exists = cname in ccols
                checks.append(CheckResult(
                    "column_exists", tname, f"Column '{cname}'",
                    passed=exists,
                    target="exists",
                    actual="exists" if exists else "missing",
                ))

                if not exists:
                    # Column missing — type/constraint checks auto-fail
                    checks.append(CheckResult("column_type_correct", tname, f"Column '{cname}' type", False, tcol.type, "column missing"))
                    if tcol.notnull:
                        checks.append(CheckResult("column_nullable_correct", tname, f"Column '{cname}' NOT NULL", False, "NOT NULL", "column missing"))
                    if tcol.is_pk:
                        checks.append(CheckResult("column_primary_key_correct", tname, f"Column '{cname}' PRIMARY KEY", False, "PK", "column missing"))
                    if tcol.default_value is not None:
                        checks.append(CheckResult("column_default_correct", tname, f"Column '{cname}' DEFAULT", False, str(tcol.default_value), "column missing"))
                    continue

                ccol = ccols[cname]

                # ── 3. column_type_correct ─────────────────────────────
                type_match = _normalize_type(ccol.type) == _normalize_type(tcol.type)
                checks.append(CheckResult(
                    "column_type_correct", tname, f"Column '{cname}' type",
                    passed=type_match,
                    target=tcol.type,
                    actual=ccol.type,
                ))

                # ── 4. column_nullable_correct ─────────────────────────
                if tcol.notnull:
                    checks.append(CheckResult(
                        "column_nullable_correct", tname, f"Column '{cname}' NOT NULL",
                        passed=ccol.notnull == tcol.notnull,
                        target="NOT NULL" if tcol.notnull else "NULLABLE",
                        actual="NOT NULL" if ccol.notnull else "NULLABLE",
                    ))

                # ── 5. column_primary_key_correct ──────────────────────
                if tcol.is_pk:
                    checks.append(CheckResult(
                        "column_primary_key_correct", tname, f"Column '{cname}' PRIMARY KEY",
                        passed=ccol.is_pk,
                        target="PK",
                        actual="PK" if ccol.is_pk else "not PK",
                    ))

                # ── 6. column_default_correct ──────────────────────────
                if tcol.default_value is not None:
                    default_match = _normalize_default(ccol.default_value) == _normalize_default(tcol.default_value)
                    checks.append(CheckResult(
                        "column_default_correct", tname, f"Column '{cname}' DEFAULT",
                        passed=default_match,
                        target=str(tcol.default_value),
                        actual=str(ccol.default_value) if ccol.default_value is not None else "none",
                    ))

            # ── 7. fk_exists ───────────────────────────────────────────
            cfk_set = {
                (fk.from_column, fk.to_table, fk.to_column)
                for fk in ctable.foreign_keys
            }
            for tfk in ttable.foreign_keys:
                fk_key = (tfk.from_column, tfk.to_table, tfk.to_column)
                checks.append(CheckResult(
                    "fk_exists", tname,
                    f"FK {tfk.from_column}→{tfk.to_table}({tfk.to_column})",
                    passed=fk_key in cfk_set,
                    target="exists",
                    actual="exists" if fk_key in cfk_set else "missing",
                ))

            # ── 8. index_exists ────────────────────────────────────────
            cidx_set = {
                (tuple(idx.columns), idx.unique)
                for idx in ctable.indexes
            }
            for tidx in ttable.indexes:
                idx_key = (tuple(tidx.columns), tidx.unique)
                checks.append(CheckResult(
                    "index_exists", tname,
                    f"Index on ({','.join(tidx.columns)}) unique={tidx.unique}",
                    passed=idx_key in cidx_set,
                    target="exists",
                    actual="exists" if idx_key in cidx_set else "missing",
                ))

            # ── 10. column_removed — old columns no longer in restructured table ──
            # If this table existed in initial with extra columns not in target
            if tname in initial_tables:
                init_cols = {c.name for c in initial_tables[tname].columns}
                target_cols = {c.name for c in ttable.columns}
                cols_to_remove = init_cols - target_cols
                for col_name in cols_to_remove:
                    checks.append(CheckResult(
                        "column_removed", tname,
                        f"Old column '{col_name}' removed",
                        passed=col_name not in ccols,
                        target="removed",
                        actual="removed" if col_name not in ccols else "still exists",
                    ))

            # ── 11. fk_removed — old FKs no longer exist ──────────────
            if tname in initial_tables:
                init_fks = {
                    (fk.from_column, fk.to_table, fk.to_column)
                    for fk in initial_tables[tname].foreign_keys
                }
                target_fks = {
                    (fk.from_column, fk.to_table, fk.to_column)
                    for fk in ttable.foreign_keys
                }
                fks_to_remove = init_fks - target_fks
                for fk in fks_to_remove:
                    checks.append(CheckResult(
                        "fk_removed", tname,
                        f"Old FK {fk[0]}→{fk[1]}({fk[2]}) removed",
                        passed=fk not in cfk_set,
                        target="removed",
                        actual="removed" if fk not in cfk_set else "still exists",
                    ))

        # ── 9. table_removed — old/legacy tables are gone ─────────────
        if initial_schema:
            tables_to_drop = set(initial_tables.keys()) - set(target_tables.keys())
            for tname in tables_to_drop:
                checks.append(CheckResult(
                    "table_removed", tname,
                    f"Legacy table '{tname}' removed",
                    passed=tname not in current_tables,
                    target="removed",
                    actual="removed" if tname not in current_tables else "still exists",
                ))

        # ── 12. data_row_correct — target rows exist in current DB ────
        for ttable in target_schema.tables:
            tname = ttable.name
            target_data = target_db.get_table_data(tname)
            current_data = current_db.get_table_data(tname)

            if not target_data:
                continue

            target_cols = [c.name for c in ttable.columns]

            # Build multiset of current rows
            c_multiset: Dict[tuple, int] = {}
            for row in current_data:
                key = tuple(_normalize_value(row.get(c)) for c in target_cols)
                c_multiset[key] = c_multiset.get(key, 0) + 1

            # Check each target row
            for i, row in enumerate(target_data):
                key = tuple(_normalize_value(row.get(c)) for c in target_cols)
                found = c_multiset.get(key, 0) > 0
                if found:
                    c_multiset[key] -= 1

                # Build a short preview of the row for the detail
                preview_vals = [str(row.get(c, ""))[:15] for c in target_cols[:4]]
                preview = " | ".join(preview_vals)

                checks.append(CheckResult(
                    "data_row_correct", tname,
                    f"Row {i+1}: {preview}...",
                    passed=found,
                    target="present",
                    actual="present" if found else "missing",
                ))

        # ── Compute score ─────────────────────────────────────────────
        total_checks = len(checks)
        passed_checks = sum(1 for c in checks if c.passed)
        score = passed_checks / total_checks if total_checks > 0 else 0.0

        # Build summary by check type
        summary: Dict[str, Dict[str, int]] = {}
        for c in checks:
            if c.check_type not in summary:
                summary[c.check_type] = {"total": 0, "passed": 0, "failed": 0}
            summary[c.check_type]["total"] += 1
            if c.passed:
                summary[c.check_type]["passed"] += 1
            else:
                summary[c.check_type]["failed"] += 1

        # Failed checks detail — every single one, no cap
        failed = [c.to_dict() for c in checks if not c.passed]
        all_checks = [c.to_dict() for c in checks]

        # ── Evaluation results — every individual check ────────────────
        # Same format as OpenEnv standard: name, score (0/1), passed
        # Every single check is its own evaluation result entry
        evaluation_results = []
        for c in checks:
            entry = {
                "name": c.to_dict()["name"],
                "score": 1 if c.passed else 0,
                "passed": c.passed,
            }
            if not c.passed:
                entry["reason"] = c._failure_reason()
            evaluation_results.append(entry)

        eval_passed = sum(1 for e in evaluation_results if e["passed"])
        eval_total = len(evaluation_results)

        return {
            "reward": round(score, 4),
            "metadata": {
                "evaluation_results": evaluation_results,
                "total_evaluations": eval_total,
                "passed_evaluations": eval_passed,
                "average_score": round(score, 4),
            },
            "total_score": round(score, 4),
            "checks_passed": passed_checks,
            "checks_total": total_checks,
            "summary": summary,
            "failed_checks": failed,
            "steps_taken": steps_taken,
            "max_steps": max_steps,
            "error_count": error_count,
        }
