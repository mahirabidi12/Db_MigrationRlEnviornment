"""EnvClient implementation for the DB Migration environment.

Usage:
    from db_migration_env.client import MigrationClient

    client = MigrationClient("http://localhost:8000")
    obs = client.reset(task_id="easy_add_columns")
    obs = client.step(sql="ALTER TABLE users ADD COLUMN age INTEGER")
    state = client.state()
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from db_migration_env.models import MigrationAction, MigrationObservation, MigrationState


class MigrationClient:
    """Synchronous HTTP client for the DB Migration environment."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(base_url=self.base_url, timeout=timeout)

    def reset(
        self,
        task_id: Optional[str] = None,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
    ) -> MigrationObservation:
        payload: Dict[str, Any] = {}
        if task_id:
            payload["task_id"] = task_id
        if seed is not None:
            payload["seed"] = seed
        if episode_id:
            payload["episode_id"] = episode_id
        resp = self._http.post("/reset", json=payload)
        resp.raise_for_status()
        return MigrationObservation(**resp.json()["observation"])

    def step(self, sql: str, metadata: Optional[Dict[str, Any]] = None) -> MigrationObservation:
        payload = {"sql": sql}
        if metadata:
            payload["metadata"] = metadata
        resp = self._http.post("/step", json=payload)
        resp.raise_for_status()
        return MigrationObservation(**resp.json()["observation"])

    def state(self) -> MigrationState:
        resp = self._http.get("/state")
        resp.raise_for_status()
        return MigrationState(**resp.json())

    def grade(self) -> dict:
        resp = self._http.post("/grader")
        resp.raise_for_status()
        return resp.json()

    def tasks(self) -> dict:
        resp = self._http.get("/tasks")
        resp.raise_for_status()
        return resp.json()

    def health(self) -> dict:
        resp = self._http.get("/health")
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
