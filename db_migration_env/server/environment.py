"""Core environment: manages episodes, executes SQL, computes rewards."""

from __future__ import annotations

import uuid
from typing import Optional

from db_migration_env.db_engine import (
    DatabaseEngine,
    compute_data_score,
    compute_schema_diff,
    compute_schema_score,
)
from db_migration_env.graders.migration_grader import MigrationGrader
from db_migration_env.models import (
    MigrationAction,
    MigrationObservation,
    MigrationState,
    SchemaSnapshot,
)
from db_migration_env.tasks.registry import TASK_REGISTRY, TaskDefinition, get_task


class MigrationEnvironment:
    """OpenEnv-compatible environment for database migration tasks."""

    def __init__(self) -> None:
        self.current_db: Optional[DatabaseEngine] = None
        self.target_db: Optional[DatabaseEngine] = None
        self.task: Optional[TaskDefinition] = None
        self.grader = MigrationGrader()

        self._episode_id: Optional[str] = None
        self._step_count: int = 0
        self._done: bool = True
        self._cumulative_reward: float = 0.0
        self._error_count: int = 0
        self._sql_history: list[str] = []
        self._target_schema: Optional[SchemaSnapshot] = None
        self._prev_score: float = 0.0

    # ------------------------------------------------------------------
    # reset
    # ------------------------------------------------------------------

    def reset(
        self,
        task_id: Optional[str] = None,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
    ) -> MigrationObservation:
        """Start a new episode. If task_id is None, defaults to easy."""
        # Clean up previous episode
        if self.current_db:
            self.current_db.close()
        if self.target_db:
            self.target_db.close()

        task_id = task_id or "easy_restructure_employees"
        self.task = get_task(task_id)

        # Set up current DB with initial state
        self.current_db = DatabaseEngine()
        self.current_db.execute_script(self.task.initial_sql)

        # Set up target DB (ground truth)
        self.target_db = DatabaseEngine()
        self.target_db.execute_script(self.task.target_sql)
        self._target_schema = self.target_db.get_schema_snapshot()

        # Episode metadata
        self._episode_id = episode_id or str(uuid.uuid4())
        self._step_count = 0
        self._done = False
        self._cumulative_reward = 0.0
        self._error_count = 0
        self._sql_history = []
        self._prev_score = 0.0

        return self._build_observation(last_result="Episode started. Execute SQL to migrate the database.", last_error=False)

    # ------------------------------------------------------------------
    # step
    # ------------------------------------------------------------------

    def step(self, action: MigrationAction) -> MigrationObservation:
        """Execute one SQL action and return the observation."""
        if self._done:
            return self._build_observation(
                last_result="Episode is done. Call reset() to start a new episode.",
                last_error=True,
            )

        self._step_count += 1
        self._sql_history.append(action.sql)

        # Execute SQL
        success, result = self.current_db.execute(action.sql)
        if not success:
            self._error_count += 1

        # Compute current score for reward shaping
        current_schema = self.current_db.get_schema_snapshot()
        schema_score = compute_schema_score(current_schema, self._target_schema)
        data_score = compute_data_score(self.current_db, self.target_db, self._target_schema)
        current_score = 0.45 * schema_score + 0.45 * data_score

        # Reward = progress delta (positive if agent got closer to target)
        step_reward = current_score - self._prev_score
        # Small penalty for errors to discourage random SQL
        if not success:
            step_reward -= 0.02
        # Small step cost to encourage efficiency
        step_reward -= 0.005

        self._prev_score = current_score
        self._cumulative_reward += step_reward

        # Check if done
        if self._step_count >= self.task.max_steps:
            self._done = True
        elif schema_score >= 0.99 and data_score >= 0.99:
            # Perfect migration — end early with bonus
            self._done = True
            self._cumulative_reward += 0.1  # bonus for early completion

        return self._build_observation(
            last_result=result,
            last_error=not success,
            reward=round(step_reward, 4),
        )

    # ------------------------------------------------------------------
    # state
    # ------------------------------------------------------------------

    @property
    def state(self) -> MigrationState:
        current_schema = self.current_db.get_schema_snapshot() if self.current_db else SchemaSnapshot()
        target_schema = self._target_schema or SchemaSnapshot()
        return MigrationState(
            episode_id=self._episode_id,
            task_id=self.task.task_id if self.task else "",
            step_count=self._step_count,
            max_steps=self.task.max_steps if self.task else 0,
            done=self._done,
            cumulative_reward=round(self._cumulative_reward, 4),
            current_schema=current_schema,
            target_schema=target_schema,
            sql_history=self._sql_history.copy(),
            error_count=self._error_count,
        )

    # ------------------------------------------------------------------
    # grade (for /grader endpoint)
    # ------------------------------------------------------------------

    def grade(self) -> dict:
        """Grade the current episode. Can be called at any time."""
        if not self.current_db or not self.target_db or not self._target_schema:
            return {"error": "No active episode. Call reset() first.", "total_score": 0.0}
        return self.grader.detailed_grade(
            current_db=self.current_db,
            target_db=self.target_db,
            target_schema=self._target_schema,
            steps_taken=self._step_count,
            max_steps=self.task.max_steps if self.task else 1,
            error_count=self._error_count,
        )

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------

    def _build_observation(
        self,
        last_result: Optional[str] = None,
        last_error: bool = False,
        reward: Optional[float] = None,
    ) -> MigrationObservation:
        current_schema = self.current_db.get_schema_snapshot() if self.current_db else SchemaSnapshot()
        target_schema = self._target_schema or SchemaSnapshot()
        diff = compute_schema_diff(current_schema, target_schema)
        return MigrationObservation(
            current_schema=current_schema,
            target_schema=target_schema,
            schema_diff=diff,
            last_sql_result=last_result,
            last_sql_error=last_error,
            step_count=self._step_count,
            max_steps=self.task.max_steps if self.task else 0,
            task_id=self.task.task_id if self.task else "",
            task_description=self.task.description if self.task else "",
            reward=reward,
            done=self._done,
            metadata={
                "episode_id": self._episode_id,
                "cumulative_reward": round(self._cumulative_reward, 4),
                "error_count": self._error_count,
            },
        )

    def close(self) -> None:
        if self.current_db:
            self.current_db.close()
        if self.target_db:
            self.target_db.close()
