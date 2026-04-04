"""SQLite database engine with schema introspection, diffing, and data comparison."""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional, Tuple

from db_migration_env.models import (
    ColumnInfo,
    ForeignKeyInfo,
    IndexInfo,
    SchemaDiffItem,
    SchemaSnapshot,
    TableSchema,
)


class DatabaseEngine:
    """Manages an in-memory SQLite database for one episode."""

    def __init__(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        self.conn.close()

    # ------------------------------------------------------------------
    # Execute SQL
    # ------------------------------------------------------------------

    def execute(self, sql: str) -> Tuple[bool, str]:
        """Execute one or more SQL statements. Returns (success, result_string)."""
        sql = sql.strip()
        if not sql:
            return False, "Empty SQL statement."

        # Security: block dangerous operations
        upper = sql.upper().replace("\n", " ").replace("\t", " ")
        if any(kw in upper for kw in ["ATTACH", "DETACH", "LOAD_EXTENSION", ".READ", ".IMPORT"]):
            return False, "SQL Error: Operation not permitted in this environment."

        # Split into individual statements
        statements = [s.strip() for s in sql.split(";") if s.strip()]
        if not statements:
            return False, "Empty SQL statement."

        results = []
        all_success = True
        for stmt in statements:
            try:
                cursor = self.conn.execute(stmt)
                self.conn.commit()
                stmt_upper = stmt.upper().lstrip()
                if stmt_upper.startswith("SELECT") or stmt_upper.startswith("PRAGMA") or stmt_upper.startswith("WITH"):
                    rows = cursor.fetchall()
                    if not rows:
                        results.append("Query returned 0 rows.")
                    else:
                        cols = [d[0] for d in cursor.description]
                        lines = [" | ".join(cols)]
                        lines.append("-" * len(lines[0]))
                        for row in rows[:100]:
                            lines.append(" | ".join(str(v) for v in row))
                        if len(rows) > 100:
                            lines.append(f"... ({len(rows)} rows total)")
                        results.append("\n".join(lines))
                else:
                    results.append(f"OK. Rows affected: {cursor.rowcount}")
            except Exception as e:
                self.conn.rollback()
                results.append(f"SQL Error: {e}")
                all_success = False

        return all_success, " | ".join(results)

    def execute_script(self, script: str) -> None:
        """Execute multiple SQL statements (for setup). Raises on error."""
        self.conn.executescript(script)

    # ------------------------------------------------------------------
    # Schema introspection
    # ------------------------------------------------------------------

    def get_tables(self) -> List[str]:
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        return [r[0] for r in cur.fetchall()]

    def get_columns(self, table: str) -> List[ColumnInfo]:
        cur = self.conn.execute(f"PRAGMA table_info('{table}')")
        cols = []
        for r in cur.fetchall():
            cols.append(ColumnInfo(
                name=r[1],
                type=r[2].upper() if r[2] else "TEXT",
                notnull=bool(r[3]),
                default_value=r[4],
                is_pk=bool(r[5]),
            ))
        return cols

    def get_foreign_keys(self, table: str) -> List[ForeignKeyInfo]:
        cur = self.conn.execute(f"PRAGMA foreign_key_list('{table}')")
        fks = []
        for r in cur.fetchall():
            fks.append(ForeignKeyInfo(
                from_column=r[3],
                to_table=r[2],
                to_column=r[4],
            ))
        return fks

    def get_indexes(self, table: str) -> List[IndexInfo]:
        cur = self.conn.execute(f"PRAGMA index_list('{table}')")
        idxs = []
        for r in cur.fetchall():
            name = r[1]
            unique = bool(r[2])
            if name.startswith("sqlite_autoindex_"):
                continue
            col_cur = self.conn.execute(f"PRAGMA index_info('{name}')")
            columns = [c[2] for c in col_cur.fetchall()]
            idxs.append(IndexInfo(name=name, columns=columns, unique=unique))
        return idxs

    def get_row_count(self, table: str) -> int:
        try:
            cur = self.conn.execute(f"SELECT COUNT(*) FROM '{table}'")
            return cur.fetchone()[0]
        except Exception:
            return 0

    def get_schema_snapshot(self, include_data_preview: bool = True) -> SchemaSnapshot:
        tables = []
        for tname in self.get_tables():
            preview = []
            if include_data_preview:
                preview = self.get_table_data(tname)[:5]  # First 5 rows
            tables.append(TableSchema(
                name=tname,
                columns=self.get_columns(tname),
                foreign_keys=self.get_foreign_keys(tname),
                indexes=self.get_indexes(tname),
                row_count=self.get_row_count(tname),
                data_preview=preview,
            ))
        return SchemaSnapshot(tables=tables)

    def check_referential_integrity(self) -> List[Dict[str, Any]]:
        """Check all FK constraints and return violations.

        Returns a list of dicts: {table, fk_column, to_table, to_column, orphan_count, sample_orphans}
        """
        violations = []
        for table in self.get_tables():
            fks = self.get_foreign_keys(table)
            for fk in fks:
                try:
                    sql = (
                        f'SELECT COUNT(*) FROM "{table}" '
                        f'WHERE "{fk.from_column}" IS NOT NULL '
                        f'AND "{fk.from_column}" NOT IN '
                        f'(SELECT "{fk.to_column}" FROM "{fk.to_table}")'
                    )
                    cur = self.conn.execute(sql)
                    orphan_count = cur.fetchone()[0]
                    if orphan_count > 0:
                        sample_sql = (
                            f'SELECT DISTINCT "{fk.from_column}" FROM "{table}" '
                            f'WHERE "{fk.from_column}" IS NOT NULL '
                            f'AND "{fk.from_column}" NOT IN '
                            f'(SELECT "{fk.to_column}" FROM "{fk.to_table}") LIMIT 5'
                        )
                        sample_cur = self.conn.execute(sample_sql)
                        samples = [r[0] for r in sample_cur.fetchall()]
                        violations.append({
                            "table": table,
                            "fk_column": fk.from_column,
                            "to_table": fk.to_table,
                            "to_column": fk.to_column,
                            "orphan_count": orphan_count,
                            "sample_orphans": samples,
                        })
                except Exception:
                    pass
        return violations

    def compute_integrity_score(self) -> float:
        """Score 0.0-1.0 for referential integrity of current data.

        1.0 = no FK violations, 0.0 = every FK has orphans.
        """
        tables = self.get_tables()
        if not tables:
            return 1.0

        total_fks = 0
        clean_fks = 0
        for table in tables:
            fks = self.get_foreign_keys(table)
            for fk in fks:
                total_fks += 1
                try:
                    sql = (
                        f'SELECT COUNT(*) FROM "{table}" '
                        f'WHERE "{fk.from_column}" IS NOT NULL '
                        f'AND "{fk.from_column}" NOT IN '
                        f'(SELECT "{fk.to_column}" FROM "{fk.to_table}")'
                    )
                    cur = self.conn.execute(sql)
                    orphans = cur.fetchone()[0]
                    if orphans == 0:
                        clean_fks += 1
                except Exception:
                    pass

        if total_fks == 0:
            return 1.0
        return clean_fks / total_fks

    def get_table_data(self, table: str) -> List[Dict[str, Any]]:
        """Get all rows from a table as list of dicts."""
        try:
            cur = self.conn.execute(f"SELECT * FROM '{table}' ORDER BY rowid")
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
        except Exception:
            return []


# ------------------------------------------------------------------
# Schema diffing
# ------------------------------------------------------------------

def compute_schema_diff(current: SchemaSnapshot, target: SchemaSnapshot) -> List[SchemaDiffItem]:
    """Compute structured diff between current and target schemas."""
    diffs: List[SchemaDiffItem] = []
    current_tables = {t.name: t for t in current.tables}
    target_tables = {t.name: t for t in target.tables}

    # Missing / extra tables
    for tname in target_tables:
        if tname not in current_tables:
            diffs.append(SchemaDiffItem(
                category="missing_table", table=tname,
                detail=f"Table '{tname}' is required but does not exist.",
            ))
    for tname in current_tables:
        if tname not in target_tables:
            diffs.append(SchemaDiffItem(
                category="extra_table", table=tname,
                detail=f"Table '{tname}' exists but is not in the target schema.",
            ))

    # Column-level diffs for matching tables
    for tname, ttable in target_tables.items():
        if tname not in current_tables:
            continue
        ctable = current_tables[tname]
        ccols = {c.name: c for c in ctable.columns}
        tcols = {c.name: c for c in ttable.columns}

        for cname, tcol in tcols.items():
            if cname not in ccols:
                diffs.append(SchemaDiffItem(
                    category="missing_column", table=tname,
                    detail=f"Column '{cname}' ({tcol.type}) is missing.",
                ))
            else:
                ccol = ccols[cname]
                if _normalize_type(ccol.type) != _normalize_type(tcol.type):
                    diffs.append(SchemaDiffItem(
                        category="type_mismatch", table=tname,
                        detail=f"Column '{cname}': current type '{ccol.type}' != target type '{tcol.type}'.",
                    ))
                if ccol.notnull != tcol.notnull or ccol.is_pk != tcol.is_pk:
                    diffs.append(SchemaDiffItem(
                        category="constraint_mismatch", table=tname,
                        detail=f"Column '{cname}': constraint mismatch "
                               f"(notnull={ccol.notnull}->{tcol.notnull}, pk={ccol.is_pk}->{tcol.is_pk}).",
                    ))
                if _normalize_default(ccol.default_value) != _normalize_default(tcol.default_value):
                    diffs.append(SchemaDiffItem(
                        category="constraint_mismatch", table=tname,
                        detail=f"Column '{cname}': default value mismatch "
                               f"('{ccol.default_value}' vs '{tcol.default_value}').",
                    ))

        for cname in ccols:
            if cname not in tcols:
                diffs.append(SchemaDiffItem(
                    category="extra_column", table=tname,
                    detail=f"Column '{cname}' exists but is not in the target schema.",
                ))

        # Foreign key diffs
        cfks = {(fk.from_column, fk.to_table, fk.to_column) for fk in ctable.foreign_keys}
        tfks = {(fk.from_column, fk.to_table, fk.to_column) for fk in ttable.foreign_keys}
        for fk in tfks - cfks:
            diffs.append(SchemaDiffItem(
                category="missing_fk", table=tname,
                detail=f"Missing FK: {fk[0]} -> {fk[1]}({fk[2]}).",
            ))
        for fk in cfks - tfks:
            diffs.append(SchemaDiffItem(
                category="extra_fk", table=tname,
                detail=f"Extra FK: {fk[0]} -> {fk[1]}({fk[2]}).",
            ))

    return diffs


def compute_schema_score(current: SchemaSnapshot, target: SchemaSnapshot) -> float:
    """Score 0.0-1.0 measuring how close the current schema is to the target."""
    if not target.tables:
        return 1.0

    total_points = 0.0
    earned_points = 0.0
    target_tables = {t.name: t for t in target.tables}
    current_tables = {t.name: t for t in current.tables}

    for tname, ttable in target_tables.items():
        # Table existence: 1 point per table
        total_points += 1.0
        if tname in current_tables:
            earned_points += 1.0
            ctable = current_tables[tname]
            tcols = {c.name: c for c in ttable.columns}
            ccols = {c.name: c for c in ctable.columns}

            for cname, tcol in tcols.items():
                # Column existence: 1 point
                total_points += 1.0
                if cname in ccols:
                    earned_points += 0.4  # exists
                    ccol = ccols[cname]
                    if _normalize_type(ccol.type) == _normalize_type(tcol.type):
                        earned_points += 0.25  # type matches
                    if ccol.notnull == tcol.notnull and ccol.is_pk == tcol.is_pk:
                        earned_points += 0.2  # constraints match
                    if _normalize_default(ccol.default_value) == _normalize_default(tcol.default_value):
                        earned_points += 0.15  # default matches
                else:
                    pass  # 0 points

            # Penalty for extra columns not in target
            extra_cols = len(set(ccols) - set(tcols))
            total_points += extra_cols * 0.5
            # Extra cols earn 0 — they drag down the score

            # FK matching
            tfks = {(fk.from_column, fk.to_table, fk.to_column) for fk in ttable.foreign_keys}
            cfks = {(fk.from_column, fk.to_table, fk.to_column) for fk in ctable.foreign_keys}
            for _ in tfks:
                total_points += 0.5
            for fk in tfks:
                if fk in cfks:
                    earned_points += 0.5

            # Penalty for extra FKs
            extra_fks = len(cfks - tfks)
            total_points += extra_fks * 0.3
        else:
            # All columns in missing table count toward total
            total_points += len(ttable.columns)

    # Penalty for extra tables not in target
    extra = len(set(current_tables) - set(target_tables))
    total_points += extra * 1.0  # extra tables count against the score

    if total_points == 0:
        return 1.0
    return max(0.0, min(1.0, earned_points / total_points))


def compute_data_score(
    current_db: DatabaseEngine,
    target_db: DatabaseEngine,
    target_schema: SchemaSnapshot,
) -> float:
    """Score 0.0-1.0 measuring how well the data matches the target.

    Uses numeric-aware comparison with tolerance for floating-point differences,
    and multiset matching to correctly handle duplicate rows.
    """
    if not target_schema.tables:
        return 1.0

    total_points = 0.0
    earned_points = 0.0

    for ttable in target_schema.tables:
        tname = ttable.name
        target_data = target_db.get_table_data(tname)
        current_data = current_db.get_table_data(tname)

        if not target_data:
            # No target data — score based on whether the table exists
            total_points += 1.0
            if tname in [t.name for t in current_db.get_schema_snapshot().tables]:
                earned_points += 1.0
            continue

        t_count = len(target_data)
        c_count = len(current_data)

        # Row count score (1 point)
        total_points += 1.0
        if t_count > 0:
            count_ratio = min(c_count, t_count) / t_count
            count_penalty = abs(c_count - t_count) / max(t_count, 1)
            earned_points += max(0.0, count_ratio - 0.2 * count_penalty)

        # Data content matching using multiset (handles duplicate rows correctly)
        target_cols = [c.name for c in ttable.columns]
        t_rows = _rows_to_multiset(target_data, target_cols)
        c_rows = _rows_to_multiset(current_data, target_cols)

        if t_rows:
            total_points += len(target_data)  # 1 point per target row
            # Match rows greedily: for each target row, find best match in current
            c_remaining = dict(c_rows)  # mutable copy of counts
            for row_key, t_count_for_key in t_rows.items():
                c_available = c_remaining.get(row_key, 0)
                matched = min(t_count_for_key, c_available)
                earned_points += matched
                if c_available > 0:
                    c_remaining[row_key] = c_available - matched
        else:
            total_points += 1.0
            earned_points += 1.0

    if total_points == 0:
        return 1.0
    return max(0.0, min(1.0, earned_points / total_points))


def _normalize_value(v: Any) -> str:
    """Normalize a cell value for comparison with numeric tolerance.

    Handles: int/float equivalence (3 == 3.0), rounding tolerance (3.7 vs 3.7000001),
    NULL normalization, and whitespace stripping.
    """
    if v is None:
        return "NULL"
    if isinstance(v, float):
        # Round to 2 decimal places for tolerance
        rounded = round(v, 2)
        # Represent as integer if it's a whole number (3.0 -> "3")
        if rounded == int(rounded):
            return str(int(rounded))
        return f"{rounded:.2f}"
    if isinstance(v, int):
        return str(v)
    # String: try to parse as number for tolerance
    s = str(v).strip()
    try:
        fval = float(s)
        rounded = round(fval, 2)
        if rounded == int(rounded):
            return str(int(rounded))
        return f"{rounded:.2f}"
    except (ValueError, OverflowError):
        return s


def _rows_to_multiset(rows: List[Dict[str, Any]], cols: List[str]) -> Dict[tuple, int]:
    """Convert rows to a multiset (dict of tuple -> count) for order-independent
    comparison that correctly handles duplicate rows."""
    result: Dict[tuple, int] = {}
    for row in rows:
        vals = tuple(_normalize_value(row.get(c)) for c in cols)
        result[vals] = result.get(vals, 0) + 1
    return result


def _normalize_default(d: Optional[str]) -> str:
    """Normalize default values for comparison."""
    if d is None:
        return ""
    return str(d).strip().strip("'\"")


def _normalize_type(t: str) -> str:
    """Normalize SQL types for comparison."""
    t = t.upper().strip()
    mapping = {
        "INT": "INTEGER",
        "SMALLINT": "INTEGER",
        "BIGINT": "INTEGER",
        "TINYINT": "INTEGER",
        "BOOL": "INTEGER",
        "BOOLEAN": "INTEGER",
        "VARCHAR": "TEXT",
        "CHAR": "TEXT",
        "STRING": "TEXT",
        "NVARCHAR": "TEXT",
        "REAL": "REAL",
        "FLOAT": "REAL",
        "DOUBLE": "REAL",
        "NUMERIC": "REAL",
        "DECIMAL": "REAL",
    }
    # Handle VARCHAR(n), etc.
    base = t.split("(")[0].strip()
    return mapping.get(base, base)
