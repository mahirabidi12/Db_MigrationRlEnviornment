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

**[Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/techsas/db-migration-env)**

An **OpenEnv-compliant** reinforcement learning environment where AI agents learn to perform **real database migrations** using SQL. The agent receives an initial database (schema + data) and must transform it to match a target state — exactly the way developers and DBAs handle production migrations.

## Why Database Migration?

Database migration is one of the most **high-stakes, error-prone** tasks in software engineering. A wrong migration can corrupt data, break applications, or cause hours of downtime. This environment models that challenge:

- **Real SQL execution** — agents run actual SQLite commands, getting real errors and results
- **Schema + data** — agents must handle both structural changes (DDL) and data transformation (DML)
- **Partial progress** — the reward function tracks incremental progress, not just pass/fail
- **Genuine difficulty progression** — from table restructuring to full enterprise schema overhauls with computed columns, deduplication, and cross-table joins

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
    current_schema: SchemaSnapshot    # Current DB schema with row counts
    target_schema: SchemaSnapshot     # Target schema to reach
    schema_diff: List[SchemaDiffItem] # Structured diff (missing tables, columns, type mismatches...)
    last_sql_result: Optional[str]    # Output of the last SQL command
    last_sql_error: bool              # Whether the last command failed
    step_count: int                   # Current step number
    max_steps: int                    # Maximum steps for this task
    task_id: str                      # Task identifier
    task_description: str             # Human-readable task description
    reward: Optional[float]           # Step reward (progress delta)
    done: bool                        # Episode complete?
```

Each `SchemaSnapshot` contains detailed table info: columns (name, type, constraints), foreign keys, indexes, and row counts.

## Reward Function — 7-Dimensional Signal

The reward pipeline provides **dense, multi-signal feedback at every step** across 7 dimensions — not just a binary end score. Each step returns a full breakdown in `metadata.reward_breakdown`:

| Signal | Weight | Description |
|--------|--------|-------------|
| **Schema Progress** | 35% | Delta in structural similarity (tables, columns, types, FKs) |
| **Data Progress** | 40% | Delta in row-level data correctness (harder, so weighted more) |
| **Diff Reduction** | 10% | Bonus for reducing the number of schema diff items |
| **Milestone Bonus** | absolute | One-time rewards for key sub-goals (see below) |
| **Error Penalty** | absolute | Escalating penalty for consecutive errors (-0.02, -0.04, -0.06...) |
| **Efficiency Cost** | absolute | Quadratic time-pressure curve (cheap early, costly near deadline) |
| **Safety Penalty** | absolute | Penalizes data-destructive actions (DROP with data, DELETE without WHERE) |

### Milestone System (8 one-time bonuses)
| Milestone | Bonus | Triggered When |
|-----------|-------|----------------|
| `first_target_table` | +0.05 | First target table created |
| `all_tables_exist` | +0.08 | All target tables now exist |
| `first_fk_correct` | +0.03 | First foreign key matches target |
| `all_fks_correct` | +0.06 | All foreign keys correct |
| `first_data_match` | +0.04 | First table's data fully matches target |
| `all_data_match` | +0.10 | All target data matches (biggest bonus) |
| `schema_perfect` | +0.06 | Schema score hits 1.0 |
| `source_tables_dropped` | +0.04 | All legacy source tables removed |

### Design Properties
- **Dense gradient**: Every step has meaningful signal (not sparse end-of-episode)
- **Progress-aware**: Positive reward for moving closer to target, negative for regression
- **Escalating errors**: First error is mild (-0.02), but 5 consecutive errors cost -0.10 total
- **Time pressure**: Quadratic cost curve encourages finishing early without being punishing at the start
- **Safety-aware**: Agents learn that `DROP TABLE` on tables with data is dangerous
- **Milestone momentum**: Sub-goal bonuses provide clear intermediate objectives for the agent

---

## Tasks

### Task 1: Restructure Employee Database (Easy)
- **Initial**: 1 table (`employees` with 10 rows, embedded department info)
- **Target**: 3 tables — `departments` (deduplicated), restructured `employees` (FK, computed `hire_year`, status column), `audit_log`
- **Skills**: Deduplication, table recreation (SQLite no DROP COLUMN), `SUBSTR()` for date parsing, INSERT...SELECT with JOINs, FK management
- **Expected steps**: 8-15

### Task 2: School Database Normalization (Medium)
- **Initial**: 2 denormalized tables (`student_courses` 15 rows, `student_contacts` 7 rows with duplicates)
- **Target**: 5 normalized tables — `students` (with computed GPA), `courses`, `enrollments` (junction), `contacts`, `course_stats` (aggregated)
- **Skills**: Multi-source deduplication, many-to-many junction tables, computed aggregates (`AVG`, `COUNT`), NULL handling, cross-table data reconciliation
- **Expected steps**: 15-25

### Task 3: Enterprise SaaS Platform Overhaul (Hard)
- **Initial**: 3 denormalized tables (`billing_records` 13 rows, `support_tickets` 8 rows, `activity_log` 8 rows)
- **Target**: 7 normalized tables — `customers` (with computed `total_spent` and `ticket_count`), `plans`, `subscriptions`, `invoices`, `payments`, `agents`, `tickets`
- **Skills**: Cross-table deduplication (customers in all 3 sources), complex computed columns (SUM, COUNT across tables), multi-level FK chains (7 tables with interdependencies), NULL payment handling, FK ordering, string extraction, date handling
- **Expected steps**: 25-45

---

## Setup & Usage

### Prerequisites
- Python 3.10+
- (Optional) `HF_TOKEN` / `API_KEY` for LLM-based baseline

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
# With LLM (set env vars per hackathon spec):
API_BASE_URL=https://router.huggingface.co/v1 \
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
HF_TOKEN=hf_... \
python inference.py

# Against a running server (uses HTTP client):
python inference.py --url http://localhost:8000
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
| `/grader` | POST | Grade current episode (returns 0.0-1.0 breakdown) |
| `/baseline` | POST | Run baseline inference on all tasks |
| `/ws` | WebSocket | Persistent session (reset/step/state/close messages) |

### Example: cURL

```bash
# Reset with a specific task
curl -X POST http://localhost:8000/reset -H 'Content-Type: application/json' \
  -d '{"task_id": "easy_restructure_employees"}'

# Execute a SQL statement
curl -X POST http://localhost:8000/step -H 'Content-Type: application/json' \
  -d '{"sql": "CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, floor INTEGER NOT NULL)"}'

# Grade current episode
curl -X POST http://localhost:8000/grader

# List all tasks
curl http://localhost:8000/tasks
```

### Example: Python Client

```python
from db_migration_env.client import MigrationClient

with MigrationClient("http://localhost:8000") as client:
    obs = client.reset(task_id="easy_restructure_employees")
    obs = client.step("CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, floor INTEGER NOT NULL)")
    obs = client.step("INSERT INTO departments SELECT ROW_NUMBER() OVER (ORDER BY MIN(id)), department_name, department_floor FROM employees GROUP BY department_name")
    print(f"Schema diff remaining: {len(obs.schema_diff)} items")
    print(client.grade())
```

---

## Baseline Scores

| Task | Heuristic Score | Schema | Data | Efficiency |
|------|----------------|--------|------|------------|
| easy_restructure_employees | **0.474** | 0.81 | 0.04 | 0.87 |
| medium_school_normalize | **0.524** | 1.0 | 0.0 | 0.98 |
| hard_saas_overhaul | **0.523** | 1.0 | 0.0 | 0.95 |

*The heuristic baseline creates missing tables/columns from the schema diff but **cannot** perform data migration, deduplication, computed columns, or table restructuring. This demonstrates the significant gap that LLM agents must bridge. Perfect scores require understanding SQL semantics, JOIN logic, aggregation, and FK ordering.*

**Achievable scores with optimal play:**
| Task | Max Score | Steps Required |
|------|-----------|---------------|
| easy_restructure_employees | ~0.96 | 9 |
| medium_school_normalize | ~0.94 | 14 |
| hard_saas_overhaul | ~0.94 | 19 |

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
│   ├── db_engine.py                 # SQLite engine + schema diffing + scoring
│   ├── client.py                    # HTTP client for the environment
│   ├── tasks/
│   │   ├── registry.py              # Task registry
│   │   ├── task_easy.py             # Task 1: Restructure employees (easy)
│   │   ├── task_medium.py           # Task 2: School normalization (medium)
│   │   └── task_hard.py             # Task 3: SaaS overhaul (hard)
│   ├── graders/
│   │   └── migration_grader.py      # Deterministic grader (0.0-1.0)
│   └── server/
│       ├── app.py                   # FastAPI application (14 endpoints)
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
  |                          |--- compute_diff(current,      |
  |                          |       target) --------------->|
  |                          |--- compute_score() ---------->|
  |                          |                               |
  |<-- MigrationObservation -|                               |
  |    (schema, diff,        |                               |
  |     reward, done)        |                               |
```

Each episode creates **two** in-memory SQLite databases: one for the agent to modify (current) and one as ground truth (target). The grader compares them structurally and data-wise at any point.

---

## What Makes This Hard for Frontier Models

1. **SQLite quirks** — No `DROP COLUMN`, no `ALTER TABLE MODIFY`. Agents must use the rename-and-recreate pattern.
2. **FK ordering** — Tables must be created in dependency order. Dropping tables requires disabling FK checks first.
3. **Deduplication** — Source tables contain duplicates that must be resolved via `GROUP BY` / `DISTINCT`.
4. **Computed columns** — GPA averages, payment totals, ticket counts must be calculated correctly with proper NULL handling.
5. **Cross-table joins** — Data scattered across multiple source tables must be reconciled by email/name matching.
6. **Partial payments** — Some invoices have NULL payments; agents must handle this in their INSERT logic.
7. **Window functions** — `ROW_NUMBER() OVER (...)` needed for deterministic ID assignment.
8. **Transaction awareness** — Long migration sequences where one error can cascade.

---

## License

MIT
