"""Task registry — central lookup for all migration tasks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from db_migration_env.tasks import task_easy, task_medium, task_hard, task_hard2, task_hard3, task_medium_instagram


@dataclass(frozen=True)
class TaskDefinition:
    task_id: str
    description: str
    difficulty: str
    timeout_seconds: int
    initial_sql: str
    target_sql: str


def _load(mod) -> TaskDefinition:
    return TaskDefinition(
        task_id=mod.TASK_ID,
        description=mod.TASK_DESCRIPTION,
        difficulty=mod.DIFFICULTY,
        timeout_seconds=mod.TIMEOUT_SECONDS,
        initial_sql=mod.INITIAL_SQL,
        target_sql=mod.TARGET_SQL,
    )


TASK_REGISTRY: Dict[str, TaskDefinition] = {
    task_easy.TASK_ID: _load(task_easy),
    task_medium.TASK_ID: _load(task_medium),
    task_hard.TASK_ID: _load(task_hard),
    task_hard2.TASK_ID: _load(task_hard2),
    task_hard3.TASK_ID: _load(task_hard3),
    task_medium_instagram.TASK_ID: _load(task_medium_instagram),
}


def get_task(task_id: str) -> TaskDefinition:
    if task_id not in TASK_REGISTRY:
        raise ValueError(f"Unknown task '{task_id}'. Available: {list(TASK_REGISTRY.keys())}")
    return TASK_REGISTRY[task_id]


def list_tasks() -> List[Dict]:
    return [
        {
            "task_id": t.task_id,
            "description": t.description,
            "difficulty": t.difficulty,
            "timeout_seconds": t.timeout_seconds,
        }
        for t in TASK_REGISTRY.values()
    ]