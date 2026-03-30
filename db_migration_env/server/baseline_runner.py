"""Baseline runner — runs a model against all tasks via the local environment."""

from __future__ import annotations

import os
from typing import Any, Dict, List

from db_migration_env.server.environment import MigrationEnvironment
from db_migration_env.models import MigrationAction
from db_migration_env.tasks.registry import TASK_REGISTRY


def _format_observation_prompt(obs) -> str:
    """Format an observation into a text prompt for the LLM."""
    lines = []
    lines.append("=== DB Migration Task ===")
    lines.append(f"Task: {obs.task_description}")
    lines.append(f"Step: {obs.step_count}/{obs.max_steps}")
    lines.append("")

    # Current schema
    lines.append("--- CURRENT SCHEMA ---")
    for table in obs.current_schema.tables:
        cols = ", ".join(
            f"{c.name} {c.type}{'  PK' if c.is_pk else ''}{'  NOT NULL' if c.notnull else ''}"
            for c in table.columns
        )
        lines.append(f"  {table.name} ({cols})  [{table.row_count} rows]")
        for fk in table.foreign_keys:
            lines.append(f"    FK: {fk.from_column} -> {fk.to_table}({fk.to_column})")
    lines.append("")

    # Target schema
    lines.append("--- TARGET SCHEMA ---")
    for table in obs.target_schema.tables:
        cols = ", ".join(
            f"{c.name} {c.type}{'  PK' if c.is_pk else ''}{'  NOT NULL' if c.notnull else ''}"
            for c in table.columns
        )
        lines.append(f"  {table.name} ({cols})  [{table.row_count} rows]")
        for fk in table.foreign_keys:
            lines.append(f"    FK: {fk.from_column} -> {fk.to_table}({fk.to_column})")
    lines.append("")

    # Diff
    if obs.schema_diff:
        lines.append("--- DIFFERENCES ---")
        for d in obs.schema_diff:
            lines.append(f"  [{d.category}] {d.table}: {d.detail}")
        lines.append("")

    # Last result
    if obs.last_sql_result:
        lines.append(f"--- LAST SQL RESULT ---")
        lines.append(f"  Error: {obs.last_sql_error}")
        lines.append(f"  {obs.last_sql_result}")

    return "\n".join(lines)


SYSTEM_PROMPT = """You are a database migration agent. Your job is to transform a database from its current schema and data to match a target schema and data.

You can execute ONE SQL statement at a time. Respond with ONLY the SQL statement — no explanations, no markdown, no extra text.

Rules:
- SQLite syntax only
- One statement per response
- Use ALTER TABLE, CREATE TABLE, INSERT, UPDATE, DELETE, DROP TABLE as needed
- SQLite does not support DROP COLUMN — to remove columns, create a new table, copy data, drop old, rename
- Preserve all existing data during migration
- When done (current matches target), respond with exactly: DONE"""


async def run_baseline() -> Dict[str, Any]:
    """Run the baseline agent against all tasks. Returns scores."""
    api_key = os.environ.get("OPENAI_API_KEY", "")

    results: Dict[str, Any] = {}

    if not api_key:
        # Run without LLM — use a scripted heuristic baseline
        results = _run_heuristic_baseline()
        results["method"] = "heuristic (no OPENAI_API_KEY set)"
        return results

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=api_key)

        for task_id, task_def in TASK_REGISTRY.items():
            env = MigrationEnvironment()
            obs = env.reset(task_id=task_id)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            for _ in range(task_def.max_steps):
                prompt = _format_observation_prompt(obs)
                messages.append({"role": "user", "content": prompt})

                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.0,
                    max_tokens=500,
                )
                sql = response.choices[0].message.content.strip()
                messages.append({"role": "assistant", "content": sql})

                if sql.upper() == "DONE":
                    break

                action = MigrationAction(sql=sql)
                obs = env.step(action)

                if obs.done:
                    break

            grade = env.grade()
            results[task_id] = grade
            env.close()

        results["method"] = "gpt-4o-mini"
    except Exception as e:
        results["error"] = str(e)
        results["method"] = "failed"

    return results


def _run_heuristic_baseline() -> Dict[str, Any]:
    """Simple heuristic baseline that doesn't require an LLM."""
    results: Dict[str, Any] = {}

    for task_id, task_def in TASK_REGISTRY.items():
        env = MigrationEnvironment()
        obs = env.reset(task_id=task_id)

        # The heuristic just tries to create missing tables and columns
        for _ in range(task_def.max_steps):
            if obs.done:
                break

            diff = obs.schema_diff
            if not diff:
                break

            # Try to address the first diff item
            item = diff[0]
            sql = None

            if item.category == "missing_table":
                # Find target table definition and try to create it
                for t in obs.target_schema.tables:
                    if t.name == item.table:
                        cols = []
                        for c in t.columns:
                            col_def = f"{c.name} {c.type}"
                            if c.is_pk:
                                col_def += " PRIMARY KEY"
                            if c.notnull and not c.is_pk:
                                col_def += " NOT NULL"
                            if c.default_value is not None:
                                col_def += f" DEFAULT {c.default_value}"
                            cols.append(col_def)
                        # Add FK constraints
                        for fk in t.foreign_keys:
                            cols.append(
                                f"FOREIGN KEY ({fk.from_column}) REFERENCES {fk.to_table}({fk.to_column})"
                            )
                        sql = f"CREATE TABLE {t.name} ({', '.join(cols)})"
                        break

            elif item.category == "missing_column":
                # Extract column name and type from detail
                for t in obs.target_schema.tables:
                    if t.name == item.table:
                        for c in t.columns:
                            if c.name in item.detail:
                                default = ""
                                if c.default_value is not None:
                                    default = f" DEFAULT {c.default_value}"
                                sql = f"ALTER TABLE {t.name} ADD COLUMN {c.name} {c.type}{default}"
                                break
                        break

            elif item.category == "extra_table":
                sql = f"DROP TABLE IF EXISTS {item.table}"

            if sql:
                action = MigrationAction(sql=sql)
                obs = env.step(action)
            else:
                break

        grade = env.grade()
        results[task_id] = grade
        env.close()

    return results
