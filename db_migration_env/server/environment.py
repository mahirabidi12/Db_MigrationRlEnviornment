"""Core environment: manages episodes, executes SQL, computes rewards."""

from __future__ import annotations

import uuid
from typing import Optional

from db_migration_env.db_engine import (
    DatabaseEngine,
    compute_schema_diff,
)
from db_migration_env.graders.migration_grader import MigrationGrader
from db_migration_env.models import (
    MigrationAction,
    MigrationObservation,
    MigrationState,
    SchemaSnapshot,
)
from db_migration_env.reward import (
    RewardState,
    compute_step_reward,
    init_reward_state,
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
        self._initial_schema: Optional[SchemaSnapshot] = None
        self._reward_state: Optional[RewardState] = None
        self._last_reward_breakdown: Optional[dict] = None

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
        if self.current_db:
            self.current_db.close()
        if self.target_db:
            self.target_db.close()

        task_id = task_id or "easy_blog_acquisition"
        self.task = get_task(task_id)

        self.current_db = DatabaseEngine()
        self.current_db.execute_script(self.task.initial_sql)

        self.target_db = DatabaseEngine()
        self.target_db.execute_script(self.task.target_sql)
        self._target_schema = self.target_db.get_schema_snapshot()

        self._episode_id = episode_id or str(uuid.uuid4())
        self._step_count = 0
        self._done = False
        self._cumulative_reward = 0.0
        self._error_count = 0
        self._sql_history = []
        self._last_reward_breakdown = None
        self._initial_schema = self.current_db.get_schema_snapshot(include_data_preview=False)

        # Initialize reward — runs grader once to get baseline score (0.0)
        self._reward_state = init_reward_state(
            current_db=self.current_db,
            target_db=self.target_db,
            target_schema=self._target_schema,
            initial_schema=self._initial_schema,
            grader=self.grader,
        )

        return self._build_observation(
            last_result="Episode started. Execute SQL to migrate the database.",
            last_error=False,
        )

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

        success, result = self.current_db.execute(action.sql)
        if not success:
            self._error_count += 1

        # reward = grader_after - grader_before
        breakdown = compute_step_reward(
            reward_state=self._reward_state,
            current_db=self.current_db,
            target_db=self.target_db,
            target_schema=self._target_schema,
            initial_schema=self._initial_schema,
            grader=self.grader,
            sql=action.sql,
            success=success,
        )
        step_reward = breakdown.total
        self._cumulative_reward += step_reward
        self._last_reward_breakdown = breakdown.to_dict()

        # Check termination
        if self._step_count >= self.task.max_steps:
            self._done = True
        elif self._reward_state.prev_score >= 0.99:
            self._done = True

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
    # grade
    # ------------------------------------------------------------------

    def grade(self) -> dict:
        """Grade the current episode using the checklist grader."""
        if not self.current_db or not self.target_db or not self._target_schema:
            return {"error": "No active episode. Call reset() first.", "total_score": 0.0}
        result = self.grader.detailed_grade(
            current_db=self.current_db,
            target_db=self.target_db,
            target_schema=self._target_schema,
            steps_taken=self._step_count,
            max_steps=self.task.max_steps if self.task else 1,
            error_count=self._error_count,
            initial_schema=self._initial_schema,
        )
        if self._last_reward_breakdown:
            result["last_reward_breakdown"] = self._last_reward_breakdown
        return result

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

        metadata = {
            "episode_id": self._episode_id,
            "cumulative_reward": round(self._cumulative_reward, 4),
            "error_count": self._error_count,
        }
        if self._last_reward_breakdown:
            metadata["reward_breakdown"] = self._last_reward_breakdown

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
            metadata=metadata,
        )

    def close(self) -> None:
        if self.current_db:
            self.current_db.close()
        if self.target_db:
            self.target_db.close()
