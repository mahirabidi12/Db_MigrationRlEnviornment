"""Pydantic models for the DB Migration environment — Action, Observation, State."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Action
# ---------------------------------------------------------------------------

class MigrationAction(BaseModel):
    """An action the agent can take — execute a SQL statement."""

    sql: str = Field(
        ...,
        description="A single SQL statement to execute against the database. "
                    "Supports DDL (CREATE, ALTER, DROP) and DML (INSERT, UPDATE, DELETE, SELECT).",
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Schema / Data description helpers  (returned inside Observation)
# ---------------------------------------------------------------------------

class ColumnInfo(BaseModel):
    """Describes a single column in a table."""
    name: str
    type: str
    notnull: bool = False
    default_value: Optional[str] = None
    is_pk: bool = False


class ForeignKeyInfo(BaseModel):
    """Describes a foreign-key constraint."""
    from_column: str
    to_table: str
    to_column: str


class IndexInfo(BaseModel):
    """Describes an index on a table."""
    name: str
    columns: List[str]
    unique: bool = False


class TableSchema(BaseModel):
    """Full schema description for one table."""
    name: str
    columns: List[ColumnInfo]
    foreign_keys: List[ForeignKeyInfo] = Field(default_factory=list)
    indexes: List[IndexInfo] = Field(default_factory=list)
    row_count: int = 0


class SchemaSnapshot(BaseModel):
    """Complete database schema snapshot."""
    tables: List[TableSchema] = Field(default_factory=list)


class SchemaDiffItem(BaseModel):
    """One item in a schema diff."""
    category: str = Field(
        ..., description="One of: missing_table, extra_table, missing_column, "
                         "extra_column, type_mismatch, constraint_mismatch, "
                         "missing_fk, extra_fk, row_count_mismatch, data_mismatch"
    )
    table: str
    detail: str


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------

class MigrationObservation(BaseModel):
    """What the agent sees after each step (or on reset)."""

    current_schema: SchemaSnapshot = Field(
        description="Current database schema with row counts."
    )
    target_schema: SchemaSnapshot = Field(
        description="Target database schema the agent must reach."
    )
    schema_diff: List[SchemaDiffItem] = Field(
        default_factory=list,
        description="Structured diff between current and target schemas.",
    )
    last_sql_result: Optional[str] = Field(
        default=None,
        description="Result of the last SQL command (rows returned, rows affected, or error message).",
    )
    last_sql_error: bool = Field(
        default=False,
        description="Whether the last SQL command raised an error.",
    )
    step_count: int = Field(default=0)
    max_steps: int = Field(default=50)
    task_id: str = Field(default="")
    task_description: str = Field(default="")
    reward: Optional[float] = Field(default=None)
    done: bool = Field(default=False)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class MigrationState(BaseModel):
    """Internal environment state — returned by state()."""

    episode_id: Optional[str] = Field(default=None)
    task_id: str = Field(default="")
    step_count: int = Field(default=0, ge=0)
    max_steps: int = Field(default=50)
    done: bool = Field(default=False)
    cumulative_reward: float = Field(default=0.0)
    current_schema: SchemaSnapshot = Field(default_factory=SchemaSnapshot)
    target_schema: SchemaSnapshot = Field(default_factory=SchemaSnapshot)
    sql_history: List[str] = Field(default_factory=list)
    error_count: int = Field(default=0)
