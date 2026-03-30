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
        """Execute a SQL statement. Returns (success, result_string)."""
        sql = sql.strip().rstrip(";")
        if not sql:
            return False, "Empty SQL statement."

        # Security: block dangerous operations
        upper = sql.upper().replace("\n", " ").replace("\t", " ")
        if any(kw in upper for kw in ["ATTACH", "DETACH", "LOAD_EXTENSION", ".READ", ".IMPORT"]):
            return False, "SQL Error: Operation not permitted in this environment."

        try:
            cursor = self.conn.execute(sql)
            self.conn.commit()
            upper = sql.upper().lstrip()
            if upper.startswith("SELECT") or upper.startswith("PRAGMA") or upper.startswith("WITH"):
                rows = cursor.fetchall()
                if not rows:
                    return True, "Query returned 0 rows."
                cols = [d[0] for d in cursor.description]
                lines = [" | ".join(cols)]
                lines.append("-" * len(lines[0]))
                for row in rows[:100]:  # cap display
                    lines.append(" | ".join(str(v) for v in row))
                if len(rows) > 100:
                    lines.append(f"... ({len(rows)} rows total)")
                return True, "\n".join(lines)
            else:
                return True, f"OK. Rows affected: {cursor.rowcount}"
        except Exception as e:
            self.conn.rollback()
            return False, f"SQL Error: {e}"

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

    def get_schema_snapshot(self) -> SchemaSnapshot:
        tables = []
        for tname in self.get_tables():
            tables.append(TableSchema(
                name=tname,
                columns=self.get_columns(tname),
                foreign_keys=self.get_foreign_keys(tname),
                indexes=self.get_indexes(tname),
                row_count=self.get_row_count(tname),
            ))
        return SchemaSnapshot(tables=tables)

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
                    earned_points += 0.5  # exists
                    ccol = ccols[cname]
                    if _normalize_type(ccol.type) == _normalize_type(tcol.type):
                        earned_points += 0.3  # type matches
                    if ccol.notnull == tcol.notnull and ccol.is_pk == tcol.is_pk:
                        earned_points += 0.2  # constraints match
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
    """Score 0.0-1.0 measuring how well the data matches the target."""
    if not target_schema.tables:
        return 1.0

    total_points = 0.0
    earned_points = 0.0

    for ttable in target_schema.tables:
        tname = ttable.name
        target_data = target_db.get_table_data(tname)
        current_data = current_db.get_table_data(tname)

        if not target_data:
            # No target data for this table — full marks if table exists
            total_points += 1.0
            if current_db.get_row_count(tname) >= 0:
                try:
                    current_db.conn.execute(f"SELECT 1 FROM '{tname}' LIMIT 1")
                    earned_points += 1.0
                except Exception:
                    pass
            continue

        # Row count score
        total_points += 1.0
        t_count = len(target_data)
        c_count = len(current_data)
        if t_count > 0:
            count_ratio = min(c_count, t_count) / t_count
            earned_points += count_ratio * 0.5  # up to 0.5 for row count

        # Data content matching
        # Normalize rows to comparable form (sorted by values)
        target_cols = [c.name for c in ttable.columns]
        t_rows_set = _rows_to_comparable(target_data, target_cols)
        c_rows_set = _rows_to_comparable(current_data, target_cols)

        if t_rows_set:
            total_points += len(t_rows_set)
            matched = len(t_rows_set & c_rows_set)
            earned_points += matched
            # Partial credit for matching the row count
            earned_points += 0.5 * (1.0 - abs(len(c_rows_set) - len(t_rows_set)) / max(len(t_rows_set), 1))
        else:
            total_points += 1.0
            earned_points += 1.0

    if total_points == 0:
        return 1.0
    return max(0.0, min(1.0, earned_points / total_points))


def _rows_to_comparable(rows: List[Dict[str, Any]], cols: List[str]) -> set:
    """Convert rows to a set of tuples for comparison (order-independent)."""
    result = set()
    for row in rows:
        vals = []
        for c in cols:
            v = row.get(c)
            vals.append(str(v).strip() if v is not None else "NULL")
        result.add(tuple(vals))
    return result


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
