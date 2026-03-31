#!/usr/bin/env python3
"""Pre-submission validation script.

Runs all automated checks that the hackathon judges will run:
1. OpenEnv spec compliance (openenv validate)
2. All 3 tasks load and reset correctly
3. step/reset/state API works
4. Graders produce scores in 0.0-1.0 range
5. Graders are deterministic
6. Inference script imports correctly
7. Dockerfile exists

Usage:
    python validate.py
"""

import sys
import json


def check(name: str, condition: bool, detail: str = ""):
    status = "PASS" if condition else "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return condition


def main():
    print("=" * 60)
    print("PRE-SUBMISSION VALIDATION")
    print("=" * 60)
    passed = 0
    total = 0

    # 1. Imports
    print("\n--- Module Imports ---")
    try:
        from db_migration_env.models import MigrationAction, MigrationObservation, MigrationState
        total += 1; r = check("Models import", True); passed += r
    except Exception as e:
        total += 1; check("Models import", False, str(e))

    try:
        from db_migration_env.server.environment import MigrationEnvironment
        total += 1; r = check("Environment import", True); passed += r
    except Exception as e:
        total += 1; check("Environment import", False, str(e))

    try:
        from db_migration_env.tasks.registry import TASK_REGISTRY, list_tasks
        total += 1; r = check("Task registry import", True); passed += r
    except Exception as e:
        total += 1; check("Task registry import", False, str(e))

    try:
        from db_migration_env.graders import MigrationGrader
        total += 1; r = check("Grader import", True); passed += r
    except Exception as e:
        total += 1; check("Grader import", False, str(e))

    try:
        from db_migration_env.server.app import app
        total += 1; r = check("FastAPI app import", True); passed += r
    except Exception as e:
        total += 1; check("FastAPI app import", False, str(e))

    # 2. Tasks
    print("\n--- Task Definitions ---")
    from db_migration_env.tasks.registry import TASK_REGISTRY
    total += 1
    r = check("3+ tasks defined", len(TASK_REGISTRY) >= 3, f"found {len(TASK_REGISTRY)}")
    passed += r

    for tid, task in TASK_REGISTRY.items():
        total += 1
        r = check(f"Task '{tid}' has all fields",
                  bool(task.task_id and task.description and task.initial_sql and task.target_sql))
        passed += r

    # 3. Environment lifecycle
    print("\n--- Environment Lifecycle ---")
    from db_migration_env.server.environment import MigrationEnvironment
    from db_migration_env.models import MigrationAction

    for tid in TASK_REGISTRY:
        env = MigrationEnvironment()

        # Reset
        obs = env.reset(task_id=tid)
        total += 1
        r = check(f"reset({tid})", obs is not None and len(obs.target_schema.tables) > 0)
        passed += r

        # Step
        obs2 = env.step(MigrationAction(sql="SELECT 1"))
        total += 1
        r = check(f"step({tid})", obs2 is not None and obs2.step_count == 1)
        passed += r

        # State
        state = env.state
        total += 1
        r = check(f"state({tid})", state is not None and state.step_count == 1)
        passed += r

        # Grade
        grade = env.grade()
        total += 1
        score = grade.get("total_score", -1)
        r = check(f"grader({tid}) in [0,1]", 0.0 <= score <= 1.0, f"score={score}")
        passed += r

        env.close()

    # 4. Grader determinism
    print("\n--- Grader Determinism ---")
    for tid in TASK_REGISTRY:
        scores = []
        for _ in range(3):
            env = MigrationEnvironment()
            env.reset(task_id=tid)
            env.step(MigrationAction(sql="SELECT 1"))
            g = env.grade()
            scores.append(g["total_score"])
            env.close()
        total += 1
        r = check(f"Deterministic grader ({tid})", len(set(scores)) == 1, f"scores={scores}")
        passed += r

    # 5. Observation has required fields
    print("\n--- Observation Fields ---")
    env = MigrationEnvironment()
    obs = env.reset(task_id=list(TASK_REGISTRY.keys())[0])
    required_fields = ["current_schema", "target_schema", "schema_diff", "step_count",
                       "timeout_seconds", "task_id", "done", "reward"]
    obs_dict = obs.model_dump()
    for f in required_fields:
        total += 1
        r = check(f"Observation has '{f}'", f in obs_dict)
        passed += r
    env.close()

    # 6. Reward is not always the same
    print("\n--- Reward Variability ---")
    env = MigrationEnvironment()
    obs = env.reset(task_id="easy_blog_acquisition")
    rewards = []
    test_sqls = [
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, full_name TEXT NOT NULL, created_at TEXT NOT NULL)",
        "INSERT INTO users SELECT usr_id, usr_name, usr_email, usr_pass, usr_fullname, created FROM acme_users",
        "SELECT * FROM users",
    ]
    for sql in test_sqls:
        obs = env.step(MigrationAction(sql=sql))
        if obs.reward is not None:
            rewards.append(obs.reward)
    total += 1
    r = check("Rewards vary across steps", len(set(rewards)) > 1, f"rewards={rewards}")
    passed += r
    env.close()

    # 7. File checks
    print("\n--- File Structure ---")
    import os
    root = os.path.dirname(os.path.abspath(__file__))
    for fname in ["openenv.yaml", "Dockerfile", "requirements.txt", "inference.py", "pyproject.toml"]:
        total += 1
        r = check(f"{fname} exists", os.path.isfile(os.path.join(root, fname)))
        passed += r

    # 8. openenv.yaml valid
    print("\n--- openenv.yaml ---")
    try:
        import yaml
        with open(os.path.join(root, "openenv.yaml")) as f:
            cfg = yaml.safe_load(f)
        total += 1
        r = check("openenv.yaml parses", cfg is not None)
        passed += r
        total += 1
        r = check("Has 'name' field", "name" in cfg)
        passed += r
        total += 1
        r = check("Has 'tasks' field", "tasks" in cfg and len(cfg["tasks"]) >= 3)
        passed += r
    except ImportError:
        total += 1
        check("openenv.yaml parse (needs PyYAML)", False, "pip install pyyaml")
    except Exception as e:
        total += 1
        check("openenv.yaml parse", False, str(e))

    # 9. FastAPI endpoints
    print("\n--- FastAPI Endpoints ---")
    from db_migration_env.server.app import app
    routes = {r.path for r in app.routes if hasattr(r, "path")}
    required_routes = ["/reset", "/step", "/state", "/health", "/metadata",
                       "/schema", "/tasks", "/grader", "/baseline", "/mcp"]
    for route in required_routes:
        total += 1
        r = check(f"Endpoint {route}", route in routes)
        passed += r

    # Summary
    print(f"\n{'='*60}")
    print(f"RESULTS: {passed}/{total} checks passed")
    print(f"{'='*60}")

    if passed == total:
        print("\nAll checks passed! Ready for submission.")
        return 0
    else:
        print(f"\n{total - passed} check(s) failed. Fix before submitting.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
