---
title: DB Migration RL Environment
emoji: 🗃️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8000
pinned: false
tags:
  - openenv
  - database
  - sql
  - migration
  - rl-environment
---

# DB Migration RL Environment

## The Real Pain

You know that feeling. It's 2 AM on a Sunday. You're staring at a production database that was "designed" by a contractor who left the company three years ago. There are no foreign keys. Patient records are linked by email strings scattered across 31 tables. Someone thought `pt_fname` was a perfectly clear column name. And there's one glorious table called `reports` that holds X-rays, blood tests, MRI scans, and pathology results — all in the same pile, distinguished only by a `type` column.

Now your company just got acquired. The parent company's DBA slides a 40-page schema spec across the table and says: *"We need everything migrated to our standard by end of quarter. Every email reference becomes a foreign key. Every table gets renamed. Oh, and don't lose a single row."*

If you've ever done this — rewritten JOINs at midnight, debugged why 3 rows vanished during an INSERT...SELECT, or discovered that `cust_email` in one table doesn't match `customer_email` in another — this environment is for you.

We built it because **no one teaches agents to do the work that keeps engineers up at night**. This isn't a toy puzzle. It's the real thing — messy schemas, ambiguous specs, dependency chains that punish you for creating tables in the wrong order. An RL agent gets dropped into a legacy database with nothing but a natural-language migration spec. No target schema visible. No diff to follow. Just a story that says *"here's what we need"* and a SQL prompt that says *"go."*

## Why This Environment?

| What makes it interesting | Why it matters for RL |
|---|---|
| **Real-world task** — database migrations are a genuine pain point in industry | Agent learns skills with practical value |
| **Narrative mode** — target schema is hidden, described only in natural language | Tests reasoning + planning, not just pattern matching |
| **Dense reward signal** — every SQL statement gets immediate feedback | Enables step-by-step learning, not sparse end-of-episode signal |
| **Combinatorial complexity** — 4-55 tables, FK dependency chains, computed aggregations | Rich action space that scales with difficulty |
| **Zero initial overlap** — legacy and target table names are completely different | Forces structural understanding, not cosmetic renaming |

## How It Works

```
Agent                          Environment
  |                                |
  |-------- POST /reset ---------> |  Start a new episode
  |<------- observation ---------- |  See legacy DB + task description
  |                                |
  |-------- POST /step ----------> |  Execute SQL: CREATE TABLE users (...)
  |<------- observation + reward - |  Updated DB state + grader delta
  |                                |
  |-------- POST /step ----------> |  Execute SQL: INSERT INTO users SELECT ...
  |<------- observation + reward - |  More checks passed, positive reward
  |                                |
  |           ... repeat ...       |
  |                                |
  |-------- POST /grader --------> |  Final evaluation
  |<------- detailed score ------- |  171/194 checks passed = 88%
```

## Action Space

The agent sends **SQL statements per step**:

```json
{
  "sql": "CREATE TABLE patients (id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, ...)"
}
```

| Property | Value |
|---|---|
| **Type** | SQL string — single or multiple statements (semicolon-separated) |
| **Supported operations** | `CREATE TABLE`, `INSERT INTO`, `UPDATE`, `DELETE`, `DROP TABLE`, `ALTER TABLE`, `PRAGMA`, `SELECT` |
| **Multi-statement** | Supported — semicolon-separated statements executed sequentially |
| **Database** | SQLite (in-memory, per-episode isolation) |
| **Constraints** | Standard SQLite rules apply (no `DROP COLUMN`, no `ALTER COLUMN`) |

## Observation Space

After each step, the agent receives:

| Field | Type | Description |
|---|---|---|
| `current_schema` | `SchemaSnapshot` | Full schema of the current database — every table with columns, types, constraints, FKs, indexes, row counts, and a 5-row data preview |
| `target_schema` | `SchemaSnapshot` | **Empty** — all tasks run in narrative mode. The agent must derive the target from the task description |
| `schema_diff` | `List[SchemaDiffItem]` | **Empty** in narrative mode |
| `task_description` | `string` | 30-38K character natural-language specification describing every target table, column, FK, index, constraint, and data mapping |
| `last_sql_result` | `string` | Output of the previous SQL statement (rows affected, query results, or error message) |
| `last_sql_error` | `bool` | Whether the last SQL failed |
| `step_count` | `int` | Steps taken so far |
| `time_remaining` | `float` | Seconds left in the episode |
| `reward` | `float` | Reward from the last step |
| `done` | `bool` | Whether the episode has ended |
| `metadata` | `dict` | Contains `cumulative_reward` and `reward_breakdown` with per-step details |

### SchemaSnapshot structure

Each table in `current_schema` includes:

```
TABLE patients (id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, ...)  -- 12 rows
  FK: department_id -> departments(id)
  INDEX: idx_patients_email ON (email)
  Data (3 of 12 rows):
    | 1 | Alice | Chen | alice.chen@email.com | ... |
    | 2 | Bob   | Rivera | bob.rivera@email.com | ... |
    | 3 | Carol | Zhang | carol.zhang@email.com | ... |
```

### Reward Breakdown

Every step returns a detailed breakdown in `metadata.reward_breakdown`:

```json
{
  "score_before": 0.40,
  "score_after": 0.50,
  "checks_before": 80,
  "checks_after": 100,
  "checks_total": 200,
  "new_checks_passed": 20,
  "delta": 0.10,
  "mistake_penalty": -0.02,
  "total": 0.08
}
```

## Tasks

Six tasks at increasing difficulty — all set in a company acquisition scenario, all in narrative mode. Each scenario has a **compact** variant (4–11 tables) and an **expanded** `_2` variant (25–55 tables) that models the full production operation.

### Compact variants

| | Easy | Medium | Hard |
|---|---|---|---|
| **Task ID** | `easy_hospital_migration` | `medium_instagram_migration` | `hard_shoplocal_formulas` |
| **Story** | HealthFirst Clinic acquired by MedCore Hospital | Facebook migrated to Instagram-style schema | ShopLocal e-commerce acquired by NexGenMart |
| **Initial tables** | 4 (`hc_*`) | 6 (`fb_*`) | 8 (`sl_*`) |
| **Target tables** | 8 | 10 | 11 |
| **Grader checks** | 194 | 217 | 249 |
| **Key challenge** | Split reports into 3 types + computed patient_stats | Polymorphic like splitting, self-ref comments, computed stats | Self-ref categories, 3-way FK, computed aggregates |

### Expanded variants

| | Easy 2 | Medium 2 | Hard 2 |
|---|---|---|---|
| **Task ID** | `easy_hospital_migration_2` | `medium_instagram_migration_2` | `hard_shoplocal_formulas_2` |
| **Story** | HealthFirst Clinic — full 31-table operation → MedCore enterprise | Facebook full 25-table platform → Instagram-style unified schema | ShopLocal full 35-table e-commerce stack → NexGenMart |
| **Initial tables** | 31 (`hc_*`) | 25 (`fb_*`) | 35 (`sl_*`) |
| **Target tables** | 41 | 44 | 55 |
| **Grader checks** | 1,635 | 1,468 | 2,336 |
| **Key challenge** | Split monolithic reports table into 6 specialized types; 48 indexes | Convert bidirectional friendships to directional follows; split polymorphic likes; 6 computed analytics tables | Deep FK chains (3-4 levels), 4 computed analytics tables, multi-source text resolution |

For full task descriptions, schemas, and migration challenges, see [task_desc.md](docs/task_desc.md).

## Grading

Every check is worth exactly 1 point. Score = checks passed / total checks. Compact tasks have 137–249 checks each; expanded `_2` tasks have 1,468–2,336 checks each.

**10 check types:** table_exists, column_exists, column_type_correct, column_nullable_correct, column_primary_key_correct, column_default_correct, fk_exists, index_exists, table_removed, data_row_correct.

For details on each check type, see [grader.md](docs/grader.md).

## Reward

```
reward = (grader_score_after - grader_score_before) - mistake_penalties
```

Positive reward for passing new checks, negative penalties for junk tables, wrong data, SQL errors. Dense, per-step signal — not sparse end-of-episode.

For full reward breakdown and penalty schedule, see [reward.md](docs/reward.md).

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/reset` | POST | Start a new episode. Params: `task_id`, `session_id` |
| `/step` | POST | Execute SQL. Params: `sql`, `session_id` |
| `/grader` | POST | Get detailed grading. Params: `session_id` |
| `/state` | GET | Current episode state |
| `/health` | GET | Health check |
| `/tasks` | GET | List available tasks |
| `/metadata` | GET | Environment metadata |
| `/schema` | GET | Action/observation JSON schemas |
| `/mcp` | POST | MCP JSON-RPC compatibility |
| `/ws` | WebSocket | WebSocket session |
| `/ui` | GET | Interactive Gradio web interface |

## Additional Features

| Feature | Endpoint |
|---|---|
| Gradio Web UI | [`/ui`](https://techsas-db-migration-env.hf.space/ui/) |
| MCP Interface | `POST /mcp` |
| WebSocket | `/ws` |
| Concurrent Sessions | via `session_id` param |
| Narrative Mode | Target schema hidden — agent reads a 30K+ char natural-language spec instead |
| 6 Tasks | compact (easy/medium/hard) and expanded (easy_2/medium_2/hard_2) variants |

## Baseline Scores

Scores from running `inference.py` with Nemotron 3 Super 120B. Full results in [outputs/baseline_results.json](outputs/baseline_results.json).

### Compact tasks

| Task | Score | Checks Passed |
|---|---|---|
| Easy (Hospital) | **0.88** | 171 / 194 |
| Medium (Instagram) | **0.74** | 163 / 219 |
| Hard (ShopLocal) | **0.27** | 68 / 249 |
| **Average** | **0.63** | |

Nemotron averages ~30-60s per response. Easy is nearly solvable within 8 steps; medium requires more complex JOINs and computed tables; hard requires self-referential FK resolution and multi-table aggregations.

### Expanded tasks (`_2`)

| Task | Score | Checks Passed | Cumulative Reward | Steps |
|---|---|---|---|---|
| Easy 2 (Hospital) | **20.8%** | 342 / 1,647 | +0.2077 | 10 |
| Medium 2 (Instagram) | **24.3%** | 357 / 1,468 | +0.2432 | 20 |
| Hard 2 (ShopLocal) | **3.1%** | 72 / 2,336 | +0.0308 | 5 |
| **Average** | **16.1%** | | **+0.1606** | |

The expanded variants are designed to be significantly harder — even with correct schema creation, the agent typically runs out of time before completing data migration and legacy table drops across the 25-35 source tables.

## Setup

### Prerequisites

- Python 3.11+
- An LLM API key (OpenAI, HuggingFace, NVIDIA, or any OpenAI-compatible endpoint)

### Installation

```bash
git clone https://github.com/mahirabidi12/Db_MigrationRlEnviornment.git
cd Db_MigrationRlEnviornment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "from db_migration_env.tasks.registry import list_tasks; [print(t['task_id']) for t in list_tasks()]"
```

Expected output:
```
easy_hospital_migration
medium_instagram_migration
hard_shoplocal_formulas
easy_hospital_migration_2
medium_instagram_migration_2
hard_shoplocal_formulas_2
```

## Usage

### Option 1: Run Baseline Inference

Runs all tasks sequentially (8 steps per task):

```bash
API_BASE_URL=https://integrate.api.nvidia.com/v1 \
MODEL_NAME=nvidia/nemotron-3-super-120b-a12b \
HF_TOKEN=your_token \
python inference.py
```

Output follows the mandatory `[START]`/`[STEP]`/`[END]` format per task, with a summary at the end.

### Option 2: Run via API Endpoints (how agents interact)

Start the server:

```bash
uvicorn db_migration_env.server.app:app --port 8000
```

Then interact via HTTP:

```bash
# Reset — start a new episode
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy_hospital_migration"}'

# Step — execute SQL
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{"sql": "CREATE TABLE patients (id INTEGER PRIMARY KEY, first_name TEXT NOT NULL)"}'

# Grade — get detailed evaluation
curl -X POST http://localhost:8000/grader

# List tasks
curl http://localhost:8000/tasks

# Health check
curl http://localhost:8000/health
```

### Option 3: Run via Docker

```bash
# Build
docker build -t db-migration-env .

# Run the server
docker run -p 8000:8000 db-migration-env

# Run inference inside the container
docker run --rm \
  -e API_BASE_URL=https://integrate.api.nvidia.com/v1 \
  -e MODEL_NAME=nvidia/nemotron-3-super-120b-a12b \
  -e HF_TOKEN=your_token \
  db-migration-env python -u inference.py
```

### Option 4: Use the Deployed HF Space

The environment is live at [https://techsas-db-migration-env.hf.space](https://techsas-db-migration-env.hf.space). Same API endpoints — just replace `localhost:8000` with the Space URL.

```bash
curl https://techsas-db-migration-env.hf.space/health
```

## Project Structure

```
.
├── inference.py                  # Baseline inference script (judges run this)
├── openenv.yaml                  # OpenEnv manifest
├── db_migration_env/
│   ├── server/
│   │   ├── app.py                # FastAPI server (all endpoints)
│   │   └── environment.py        # Core environment (reset/step/grade)
│   ├── graders/
│   │   └── migration_grader.py   # Checklist grader (137-2,336 checks)
│   ├── reward.py                 # Reward pipeline (delta + penalties)
│   ├── db_engine.py              # SQLite engine + schema introspection
│   ├── models.py                 # Pydantic models (Action, Observation, State)
│   └── tasks/
│       ├── task_easy.py           # Hospital migration compact (4→8 tables)
│       ├── task_medium.py         # Instagram migration compact (6→10 tables)
│       ├── task_hard.py           # E-commerce migration compact (8→11 tables)
│       ├── task_easy_2.py         # Hospital migration expanded (31→41 tables)
│       ├── task_medium_2.py       # Instagram migration expanded (25→44 tables)
│       └── task_hard_2.py         # E-commerce migration expanded (35→55 tables)
├── docs/
│   ├── grader.md                 # Grader documentation
│   ├── reward.md                 # Reward function documentation
│   └── task_desc.md              # Detailed task descriptions
└── outputs/
    └── baseline_results.json     # Baseline scores from inference.py
```
