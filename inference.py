"""
Inference Script
===================================
MANDATORY
- Before submitting, ensure the following variables are defined in your environment configuration:
    API_BASE_URL   The API endpoint for the LLM.
    MODEL_NAME     The model identifier to use for inference.
    HF_TOKEN       Your Hugging Face / API key.

- The inference script must be named `inference.py` and placed in the root directory of the project
- Participants must use OpenAI Client for all LLM calls using above variables
"""

import os
import re
import json
import sys
import textwrap
from typing import List, Dict, Optional

from openai import OpenAI

from db_migration_env.models import MigrationAction, MigrationObservation
from db_migration_env.server.environment import MigrationEnvironment
from db_migration_env.tasks.registry import TASK_REGISTRY

# ---------------------------------------------------------------------------
# Configuration — reads from environment variables per hackathon spec
# ---------------------------------------------------------------------------

API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
TEMPERATURE = 0.0
MAX_TOKENS = 1024
FALLBACK_SQL = "SELECT name FROM sqlite_master WHERE type='table'"
BENCHMARK = "db-migration-env"

DEBUG = True


# ---------------------------------------------------------------------------
# Mandatory stdout logging helpers — [START], [STEP], [END]
# ---------------------------------------------------------------------------

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.4f} done={done_val} error={error_val}", flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    success_val = str(success).lower()
    rewards_str = ",".join(f"{r:.4f}" for r in rewards)
    print(f"[END] success={success_val} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


# ---------------------------------------------------------------------------
# System prompt — expert-level SQL migration agent
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = textwrap.dedent("""
You are an expert database migration agent for SQLite. You execute SQL statements
one at a time to transform a database from its current schema+data to match a target.

## CRITICAL SQLITE RULES
- SQLite does NOT support DROP COLUMN, ALTER COLUMN, or MODIFY COLUMN.
- To restructure a table: (1) PRAGMA foreign_keys=OFF, (2) CREATE new_table,
  (3) INSERT INTO new_table SELECT ... FROM old_table, (4) DROP TABLE old_table,
  (5) ALTER TABLE new_table RENAME TO old_table, (6) PRAGMA foreign_keys=ON.
- Foreign keys must be enabled with PRAGMA foreign_keys=ON. If you need to drop
  a table referenced by FKs, first PRAGMA foreign_keys=OFF.
- Use ROW_NUMBER() OVER (ORDER BY ...) for deterministic ID assignment in INSERT...SELECT.
- SQLite uses CAST(SUBSTR(date_col,1,4) AS INTEGER) to extract year from dates.
- NULL handling: AVG() ignores NULLs. Use CASE WHEN col IS NOT NULL THEN col END for explicit.
- ROUND(value, 2) for rounding to 2 decimal places.

## STRATEGY (follow this order)
1. FIRST analyze: compare current vs target schemas and data requirements.
2. PLAN the dependency order: create tables with no FKs first, then tables that reference them.
3. For deduplication: GROUP BY the unique key, use aggregate functions for computed columns.
4. Populate junction/linking tables last (they depend on both parent tables existing).
5. Compute aggregated columns (totals, counts, averages) during INSERT...SELECT.
6. Drop source/legacy tables only after all data is migrated.
7. If restructuring an existing table (removing columns), use the rename-recreate pattern.

## RESPONSE FORMAT
Reply with EXACTLY ONE SQL statement. No explanations, no markdown, no comments.
If the migration is complete (all differences resolved, data matches), reply: DONE
""").strip()


# ---------------------------------------------------------------------------
# Build context-rich observation prompt
# ---------------------------------------------------------------------------

def format_observation(obs: MigrationObservation, include_data_sample: bool = True, include_description: bool = True) -> str:
    lines = []
    lines.append(f"=== Task: {obs.task_id} | Step {obs.step_count} | Time remaining: {obs.time_remaining:.0f}s ===")
    if include_description:
        lines.append(f"Description: {obs.task_description}")
    lines.append("")

    for label, schema in [("CURRENT DATABASE", obs.current_schema), ("TARGET DATABASE", obs.target_schema)]:
        lines.append(f"--- {label} ---")
        if not schema.tables:
            lines.append("  (no tables)")
        for table in schema.tables:
            cols = []
            for c in table.columns:
                parts = [f"{c.name} {c.type}"]
                if c.is_pk:
                    parts.append("PRIMARY KEY")
                if c.notnull:
                    parts.append("NOT NULL")
                if c.default_value is not None:
                    parts.append(f"DEFAULT {c.default_value}")
                cols.append(" ".join(parts))
            lines.append(f"  TABLE {table.name} ({', '.join(cols)})  -- {table.row_count} rows")
            for fk in table.foreign_keys:
                lines.append(f"    FOREIGN KEY ({fk.from_column}) REFERENCES {fk.to_table}({fk.to_column})")
            # Data preview — crucial for agents to understand the data
            if include_data_sample and table.data_preview:
                col_names = [c.name for c in table.columns]
                lines.append(f"    Sample data ({min(len(table.data_preview), 3)} of {table.row_count} rows):")
                for row in table.data_preview[:3]:
                    vals = [str(row.get(c, "")) for c in col_names]
                    lines.append(f"      | {' | '.join(vals)} |")
        lines.append("")

    if obs.schema_diff:
        lines.append(f"--- REMAINING DIFFERENCES ({len(obs.schema_diff)}) ---")
        for d in obs.schema_diff:
            lines.append(f"  [{d.category}] {d.table}: {d.detail}")
        lines.append("")
    else:
        lines.append("--- NO SCHEMA DIFFERENCES (check if data also matches) ---")
        lines.append("")

    if obs.last_sql_result:
        status = "ERROR" if obs.last_sql_error else "SUCCESS"
        lines.append(f"--- LAST SQL [{status}] ---")
        # Truncate long results
        result = obs.last_sql_result
        if len(result) > 500:
            result = result[:500] + "\n... (truncated)"
        lines.append(f"  {result}")
        lines.append("")

    # --- Reward feedback so the agent knows how it's doing ---
    meta = obs.metadata or {}
    bd = meta.get("reward_breakdown", {})
    if bd:
        reward = obs.reward or 0
        cum = meta.get("cumulative_reward") or 0
        checks_after = bd.get("checks_after", 0)
        checks_total = bd.get("checks_total", 0)
        new_checks = bd.get("new_checks_passed", 0)
        mistake_pen = bd.get("mistake_penalty", 0)
        mistake_det = bd.get("mistake_details", "")

        lines.append(f"--- STEP FEEDBACK ---")
        lines.append(f"  Reward: {reward:+.4f} | Cumulative: {cum:+.4f} | Checks passed: {checks_after}/{checks_total}")
        if new_checks > 0:
            lines.append(f"  +{new_checks} new checks passed")
        elif new_checks < 0:
            lines.append(f"  WARNING: Lost {abs(new_checks)} checks — you broke something!")
        if mistake_pen < 0:
            lines.append(f"  Penalty ({mistake_pen:.4f}): {mistake_det}")
        if obs.last_sql_error:
            lines.append(f"  SQL error penalty applied — fix the query")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Parse LLM response
# ---------------------------------------------------------------------------

SQL_KEYWORD_RE = re.compile(
    r"^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|PRAGMA|WITH|EXPLAIN)\b",
    re.IGNORECASE,
)


def parse_model_sql(response_text: str) -> str:
    if not response_text:
        return FALLBACK_SQL

    text = response_text.strip()

    # Remove markdown code fences
    text = re.sub(r"```(?:sql)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    text = text.strip()

    if text.upper() == "DONE":
        return FALLBACK_SQL

    # If entire text starts with SQL, send it all (multi-statement supported)
    if SQL_KEYWORD_RE.match(text):
        return text

    # Try to extract all SQL lines
    sql_lines = []
    for line in text.split("\n"):
        line = line.strip()
        if SQL_KEYWORD_RE.match(line):
            sql_lines.append(line)
    if sql_lines:
        return "; ".join(sql_lines)

    return FALLBACK_SQL


# ---------------------------------------------------------------------------
# Run one task
# ---------------------------------------------------------------------------

def run_task(task_id: str, client: OpenAI) -> dict:
    env = MigrationEnvironment()
    obs = env.reset(task_id=task_id, timeout_override=372)

    task = env.task
    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)

    planning_prompt = format_observation(obs)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": planning_prompt},
    ]

    step = 0
    rewards: List[float] = []
    success = False

    try:
        while True:
            step += 1
            if obs.done:
                break
            if obs.time_remaining <= 0:
                break

            try:
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                    stream=False,
                )
                response_text = completion.choices[0].message.content or ""
            except Exception as exc:
                response_text = FALLBACK_SQL

            sql = parse_model_sql(response_text)

            # Record in conversation
            messages.append({"role": "assistant", "content": sql})

            action = MigrationAction(sql=sql)
            obs = env.step(action)

            # Track reward
            step_reward = obs.reward if obs.reward is not None else 0.0
            rewards.append(step_reward)

            # Mandatory [STEP] log
            error_str = obs.last_sql_result if obs.last_sql_error else None
            if error_str and "Timeout" in error_str:
                error_str = "timeout"
            log_step(
                step=step,
                action=sql.replace("\n", " ")[:200],
                reward=step_reward,
                done=obs.done,
                error=error_str,
            )

            # Build follow-up prompt with result (skip description after first turn)
            result_prompt = format_observation(obs, include_description=False)
            messages.append({"role": "user", "content": result_prompt})

            # Context window management — keep system + last N exchanges
            if len(messages) > 30:
                messages = [messages[0]] + messages[-20:]

        # Final grade
        grade = env.grade()
        score = grade.get("total_score", 0.0)
        success = score >= 0.85

        print(f"\n  --- GRADE ---")
        print(f"  Total:      {grade['total_score']}")
        print(f"  Checks:     {grade.get('checks_passed', 0)}/{grade.get('checks_total', 0)}")
        print(f"  Steps:      {grade.get('steps_taken', 0)}")
        print(f"  Errors:     {grade.get('error_count', 0)}")

    except Exception as exc:
        grade = env.grade()
        score = grade.get("total_score", 0.0)
        success = False
    finally:
        env.close()
        log_end(success=success, steps=len(rewards), score=score, rewards=rewards)

    return grade


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not HF_TOKEN:
        print("WARNING: No HF_TOKEN set. LLM calls may fail.")

    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

    task_ids = list(TASK_REGISTRY.keys())
    all_results = {}

    import time as _time
    global_start = _time.time()

    for task_id in task_ids:
        try:
            grade = run_task(task_id, client)
            all_results[task_id] = grade
        except Exception as e:
            print(f"\n  FAILED: {e}")
            all_results[task_id] = {"total_score": 0.0, "error": str(e)}

    total_elapsed = _time.time() - global_start

    # Summary
    print(f"\n{'='*60}")
    print("BASELINE RESULTS SUMMARY")
    print(f"{'='*60}")
    for tid, res in all_results.items():
        score = res.get("total_score", 0.0)
        print(f"  {tid:40s} {score:.4f}")

    scores = [r.get("total_score", 0.0) for r in all_results.values()]
    avg = sum(scores) / max(len(scores), 1)
    print(f"\n  {'Average':40s} {avg:.4f}")
    print(f"\n  Total time: {total_elapsed:.1f}s")

    # Save results to outputs/
    os.makedirs("outputs", exist_ok=True)
    output = {
        "model": MODEL_NAME,
        "total_time_seconds": round(total_elapsed, 1),
        "average_score": round(avg, 4),
        "results": {tid: {"total_score": r.get("total_score", 0.0), "checks_passed": r.get("checks_passed", 0), "checks_total": r.get("checks_total", 0)} for tid, r in all_results.items()},
    }
    with open("outputs/baseline_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved to outputs/baseline_results.json")


if __name__ == "__main__":
    main()
