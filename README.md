---
title: DB Migration RL Environment
emoji: 🗄️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
tags:
  - openenv
---

# DB Migration RL Environment

An **OpenEnv-compliant** reinforcement learning environment where AI agents learn to perform **real database migrations** using SQL. The agent receives an initial database (schema + data) described in natural language and must transform it to match a target state — exactly the way developers and DBAs handle production migrations.

## Why Database Migration?

Database migration is one of the most **high-stakes, error-prone** tasks in software engineering. A wrong migration can corrupt data, break applications, or cause hours of downtime. This environment models that challenge:

- **Real SQL execution** — agents run actual SQLite commands, getting real errors and results
- **Schema + data** — agents must handle both structural changes (DDL) and data transformation (DML)
- **Narrative mode** — target schema is described in natural language, not shown structurally. Agents must parse specifications to understand what to build
- **Partial progress** — the reward function tracks incremental progress, not just pass/fail
- **Genuine difficulty progression** — from 31-table hospital migrations to 55-table e-commerce platform overhauls

---

## Action Space

The agent sends one SQL statement per step:

```python
class MigrationAction(BaseModel):
    sql: str        # A single SQL statement (DDL or DML)
    metadata: dict   # Optional metadata
```

**Supported SQL operations:**
| Category | Commands |
|----------|----------|
| DDL | `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` |
| DML | `INSERT`, `UPDATE`, `DELETE`, `SELECT` |
| Queries | `SELECT` (for inspecting data), `PRAGMA` (for schema info) |

## Observation Space

After each step, the agent sees:

```python
class MigrationObservation(BaseModel):
    current_schema: SchemaSnapshot    # Current DB schema with row counts and data preview
    target_schema: SchemaSnapshot     # Target schema (empty in narrative mode)
    schema_diff: List[SchemaDiffItem] # Structured diff (empty in narrative mode)
    last_sql_result: Optional[str]    # Output of the last SQL command
    last_sql_error: bool              # Whether the last command failed
    step_count: int                   # Current step number
    timeout_seconds: int              # Timeout for this task
    time_remaining: float             # Seconds remaining before timeout
    task_id: str                      # Task identifier
    task_description: str             # Detailed narrative specification
    reward: Optional[float]           # Step reward (progress delta)
    done: bool                        # Episode complete?
    metadata: Dict[str, Any]          # Episode ID, cumulative reward, reward breakdown
```

Each `SchemaSnapshot` contains detailed table info: columns (name, type, constraints), foreign keys, indexes, row counts, and data preview (first 5 rows).

In **narrative mode** (all tasks), the `target_schema` is empty and `schema_diff` is empty. The agent must read the `task_description` — a detailed natural language specification — to understand what tables, columns, FKs, constraints, and data mappings to create.

## State

The full internal environment state is accessible via the `state()` API:

```python
class MigrationState(BaseModel):
    episode_id: Optional[str]         # Unique episode identifier
    task_id: str                      # Current task name
    step_count: int                   # Steps taken so far
    timeout_seconds: int              # Task timeout limit
    time_remaining: float             # Seconds left
    done: bool                        # Episode terminated?
    cumulative_reward: float          # Total reward accumulated
    current_schema: SchemaSnapshot    # Current DB state
    target_schema: SchemaSnapshot     # Target DB state
    sql_history: List[str]            # All SQL executed
    error_count: int                  # Number of failed SQL statements
```

---

## Reward Function — Checklist-Delta with Mistake Penalties

The reward pipeline provides **dense feedback at every step**:

```
step_reward = (grader_score_after - grader_score_before) - mistake_penalties
```

| Signal | How it works |
|--------|-------------|
| **Positive delta** | Agent passes new grader checks (created a table, fixed a column type, migrated data) |
| **Negative delta** | Agent broke something that was previously correct |
| **Structural mistake penalty** | 0.002 per new junk table/column, wrong type, missing constraint |
| **Wrong data penalty** | 0.0005 per new row that doesn't match the target |
| **SQL error penalty** | 0.001 per failed SQL statement |

### Design Properties
- **Dense gradient**: Every step has meaningful signal — not sparse end-of-episode
- **Progress-aware**: Positive reward for passing new checks, negative for regression
- **Mistake tracking**: Only penalizes NEW mistakes introduced by the current step, not pre-existing ones
- **Cumulative tracking**: `metadata.cumulative_reward` tracks total reward across the episode
- **Detailed breakdown**: Each step includes `metadata.reward_breakdown` with checks passed, delta, and penalty details

---

## Grader — Checklist-Based (0.0 to 1.0)

The grader uses a flat checklist system. Every check is worth exactly 1 point.

**Score = checks_passed / total_checks**

### 12 Check Types

| # | Check Type | What it verifies |
|---|---|---|
| 1 | `table_exists` | Target table is present |
| 2 | `column_exists` | Target column exists in the table |
| 3 | `column_type_correct` | Column has the correct type (INTEGER, TEXT, REAL) |
| 4 | `column_nullable_correct` | NOT NULL constraint matches |
| 5 | `column_primary_key_correct` | PRIMARY KEY flag matches |
| 6 | `column_default_correct` | DEFAULT value matches |
| 7 | `fk_exists` | Foreign key constraint is present |
| 8 | `index_exists` | Index exists with correct columns and uniqueness |
| 9 | `table_removed` | Legacy table has been dropped |
| 10 | `column_removed` | Old column no longer exists in restructured table |
| 11 | `fk_removed` | Old FK constraint has been removed |
| 12 | `data_row_correct` | Target row exists in current DB (row-level multiset match) |

### Properties
- **Deterministic** — same inputs always produce the same score
- **Continuous** — scores range from 0.0 to 1.0 with fine granularity (1000+ checks per task)
- **Comprehensive** — checks schema structure AND data correctness
- **No weights** — every check counts equally, making the score transparent

---

## Tasks

### Task 1: Hospital Migration (Easy) — `easy_hospital_migration`
- **Scenario**: HealthFirst Community Clinic acquired by MedCore Enterprise Hospital System
- **Initial**: 31 tables (`hc_*` prefix), ~350 rows, email-based references, abbreviated column names
- **Target**: 41 tables (no prefix), ~400 rows, 63 FKs, 48 indexes
- **Key challenges**: Split monolithic `hc_reports` into 6 specialized report tables, resolve email references to integer FKs, add NOT NULL/DEFAULT/UNIQUE constraints
- **Grader checks**: ~1,635
- **Timeout**: 360 seconds

### Task 2: Social Media Migration (Medium) — `medium_instagram_migration`
- **Scenario**: Meta consolidating Facebook into Instagram-style unified schema
- **Initial**: 25 tables (`fb_*` prefix), ~300 rows
- **Target**: 44 tables (no prefix), ~450 rows
- **Key challenges**: Convert bidirectional friendships to directional follows, create computed engagement metrics, migrate privacy settings, handle media type transformations
- **Grader checks**: ~1,468
- **Timeout**: 360 seconds

### Task 3: E-Commerce Platform Overhaul (Hard) — `hard_shoplocal_formulas`
- **Scenario**: ShopLocal artisan marketplace acquired by NexGenMart enterprise platform
- **Initial**: 35 tables (`sl_*` prefix), ~404 rows
- **Target**: 55 tables (no prefix), ~701 rows
- **Key challenges**: Computed summary tables (user_stats, product_stats with AVG/SUM/COUNT), self-referential FKs (categories), multi-source address consolidation, order lifecycle tracking, inventory management, coupon/discount systems
- **Grader checks**: ~2,336
- **Timeout**: 360 seconds

### Difficulty Progression
| Metric | Easy | Medium | Hard |
|--------|------|--------|------|
| Source tables | 31 | 25 | 35 |
| Target tables | 41 | 44 | 55 |
| Total rows | ~400 | ~450 | ~701 |
| Grader checks | 1,635 | 1,468 | 2,336 |
| Computed tables | 0 | ~5 | ~8 |
| FK complexity | email→ID | email→ID + directional | email→ID + self-ref + multi-source |

---

## Setup & Usage

### Prerequisites
- Python 3.10+
- `HF_TOKEN` for LLM-based inference

### Install

```bash
pip install -e .
```

### Run the Server

```bash
uvicorn db_migration_env.server.app:app --host 0.0.0.0 --port 8000
```

### Run Baseline Inference

```bash
API_BASE_URL=https://router.huggingface.co/v1 \
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
HF_TOKEN=hf_... \
python inference.py
```

### Docker

```bash
docker build -t db-migration-env .
docker run -p 8000:8000 db-migration-env
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reset` | POST | Start a new episode (accepts `task_id`, `seed`, `episode_id`) |
| `/step` | POST | Execute a SQL action (accepts `sql`, `metadata`) |
| `/state` | GET | Get current episode state |
| `/health` | GET | Health check |
| `/metadata` | GET | Environment metadata |
| `/schema` | GET | JSON schemas for Action/Observation/State |
| `/tasks` | GET | List tasks with action schema |
| `/grader` | POST | Grade current episode (returns 0.0-1.0 with detailed checks) |
| `/baseline` | POST | Run baseline inference on all tasks |
| `/mcp` | POST | MCP JSON-RPC endpoint for OpenEnv compatibility |
| `/ws` | WebSocket | Persistent session (reset/step/state/close messages) |

### Example: cURL

```bash
# Reset with a specific task
curl -X POST http://localhost:8000/reset -H 'Content-Type: application/json' \
  -d '{"task_id": "easy_hospital_migration"}'

# Execute a SQL statement
curl -X POST http://localhost:8000/step -H 'Content-Type: application/json' \
  -d '{"sql": "CREATE TABLE patients (id INTEGER PRIMARY KEY, first_name TEXT NOT NULL)"}'

# Grade current episode
curl -X POST http://localhost:8000/grader

# List all tasks
curl http://localhost:8000/tasks
```

---

## Baseline Scores

Baseline scores using `Qwen/Qwen2.5-72B-Instruct` with 360-second timeout per task:

| Task | Score | Checks Passed | Total Checks |
|------|-------|---------------|--------------|
| `easy_hospital_migration` | TBD | TBD | 1,635 |
| `medium_instagram_migration` | TBD | TBD | 1,468 |
| `hard_shoplocal_formulas` | TBD | TBD | 2,336 |

*Scores will be populated after running `python inference.py` with a valid `HF_TOKEN`.*

**Note**: All tasks use narrative mode — the agent receives a detailed natural language specification instead of seeing the target schema directly. This makes the tasks significantly harder, as the agent must parse and understand prose descriptions to construct correct SQL.

---

## Project Structure

```
.
├── openenv.yaml                     # OpenEnv manifest
├── Dockerfile                       # Container definition
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Package metadata
├── inference.py                     # Baseline inference script (hackathon-compliant)
├── db_migration_env/
│   ├── __init__.py
│   ├── models.py                    # Pydantic models (Action, Observation, State)
│   ├── db_engine.py                 # SQLite engine + schema diffing
│   ├── reward.py                    # Reward pipeline (delta + penalties)
│   ├── client.py                    # HTTP client for the environment
│   ├── tasks/
│   │   ├── registry.py              # Task registry
│   │   ├── task_easy.py             # Hospital migration (easy)
│   │   ├── task_medium.py           # Facebook→Instagram migration (medium)
│   │   └── task_hard.py             # ShopLocal→NexGenMart migration (hard)
│   ├── graders/
│   │   └── migration_grader.py      # Checklist-based grader (12 check types)
│   └── server/
│       ├── app.py                   # FastAPI application
│       ├── environment.py           # Core environment logic
│       └── baseline_runner.py       # Server-side baseline runner
└── README.md
```

---

## Architecture

```
Agent                    Environment                    SQLite (in-memory)
  |                          |                               |
  |--- MigrationAction ----->|                               |
  |    (sql: "CREATE...")    |--- execute(sql) ------------->|
  |                          |<-- (success, result) ---------|
  |                          |                               |
  |                          |--- get_schema_snapshot() ---->|
  |                          |<-- SchemaSnapshot ------------|
  |                          |                               |
  |                          |--- compute_step_reward() ---->|
  |                          |    (grader delta + penalties)  |
  |                          |                               |
  |<-- MigrationObservation -|                               |
  |    (schema, reward,      |                               |
  |     done, breakdown)     |                               |
```

Each episode creates **two** in-memory SQLite databases: one for the agent to modify (current) and one as ground truth (target). The grader compares them structurally and data-wise at every step.

---

## What Makes This Hard for Frontier Models

1. **Narrative parsing** — Target schema is described in natural language (30K+ characters), not shown structurally. Agents must extract table definitions, column types, FK relationships, and data mapping rules from prose.
2. **SQLite quirks** — No `DROP COLUMN`, no `ALTER TABLE MODIFY`. Agents must use the rename-and-recreate pattern.
3. **FK ordering** — Tables must be created in dependency order. Dropping tables requires disabling FK checks first.
4. **Email-to-ID resolution** — Source tables use email strings as references. Agents must JOIN against created tables to resolve integer FKs.
5. **Computed columns** — Summary tables require correct `SUM()`, `COUNT()`, `AVG()`, `ROUND()` with proper NULL handling (`CASE WHEN ... THEN ... ELSE NULL END`).
6. **Monolithic table splitting** — A single source table (e.g., `hc_reports`) must be split into multiple specialized target tables based on a type column.
7. **Self-referential FKs** — Categories tables with `parent_id` referencing themselves require careful insert ordering.
8. **Window functions** — `ROW_NUMBER() OVER (ORDER BY ...)` needed for deterministic ID assignment in `INSERT...SELECT`.
9. **Scale** — 2,336 individual grader checks on the hard task. Every column type, every constraint, every FK, every data row must be exactly correct.

---

## License

MIT
