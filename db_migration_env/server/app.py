"""FastAPI application — exposes the OpenEnv HTTP + WebSocket API.

Endpoints:
  POST /reset          — start a new episode
  POST /step           — execute an action
  GET  /state          — current episode state
  GET  /health         — health check
  GET  /metadata       — environment metadata
  GET  /schema         — JSON schemas for action/observation/state
  GET  /tasks          — list available tasks with action schema
  POST /grader         — grade current episode
  POST /baseline       — run baseline inference (all tasks)
  WS   /ws             — WebSocket session
"""

from __future__ import annotations

import asyncio
import json
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from db_migration_env.models import (
    MigrationAction,
    MigrationObservation,
    MigrationState,
)
from db_migration_env.server.environment import MigrationEnvironment
from db_migration_env.tasks.registry import list_tasks


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class ResetRequest(BaseModel):
    task_id: Optional[str] = None
    seed: Optional[int] = None
    episode_id: Optional[str] = None


class StepRequest(BaseModel):
    sql: str
    metadata: Dict[str, Any] = {}


class ResetResponse(BaseModel):
    observation: MigrationObservation


class StepResponse(BaseModel):
    observation: MigrationObservation
    reward: Optional[float] = None
    done: bool = False


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

# Global env store (keyed by session — for simplicity, single-session default)
_envs: Dict[str, MigrationEnvironment] = {}


def _get_env(session_id: str = "default") -> MigrationEnvironment:
    if session_id not in _envs:
        _envs[session_id] = MigrationEnvironment()
    return _envs[session_id]


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Cleanup
    for env in _envs.values():
        env.close()
    _envs.clear()


app = FastAPI(
    title="DB Migration RL Environment",
    description="OpenEnv environment for training agents to perform database schema & data migrations using SQL.",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount Gradio UI at root
try:
    import gradio as gr
    from db_migration_env.server.gradio_ui import build_gradio_app
    _gradio_app = build_gradio_app()
    app = gr.mount_gradio_app(app, _gradio_app, path="/ui")
except ImportError:
    pass  # Gradio optional — API still works without it


# ---------------------------------------------------------------------------
# Standard OpenEnv endpoints
# ---------------------------------------------------------------------------

@app.post("/reset", response_model=ResetResponse)
async def reset(req: ResetRequest = ResetRequest()):
    env = _get_env()
    obs = env.reset(task_id=req.task_id, seed=req.seed, episode_id=req.episode_id)
    return ResetResponse(observation=obs)


@app.post("/step", response_model=StepResponse)
async def step(req: StepRequest):
    env = _get_env()
    action = MigrationAction(sql=req.sql, metadata=req.metadata)
    obs = env.step(action)
    return StepResponse(observation=obs, reward=obs.reward, done=obs.done)


@app.get("/state")
async def state():
    env = _get_env()
    return env.state.model_dump()


@app.get("/health")
async def health():
    return {"status": "healthy", "environment": "db-migration-env", "version": "1.0.0"}


@app.get("/metadata")
async def metadata():
    return {
        "name": "db-migration-env",
        "version": "1.0.0",
        "description": "RL environment for database migration — agents learn to transform schemas and data using SQL.",
        "action_type": "MigrationAction",
        "observation_type": "MigrationObservation",
        "state_type": "MigrationState",
        "tasks": list_tasks(),
        "supports_concurrent_sessions": True,
    }


@app.get("/schema")
async def schema():
    return {
        "action": MigrationAction.model_json_schema(),
        "observation": MigrationObservation.model_json_schema(),
        "state": MigrationState.model_json_schema(),
    }


# ---------------------------------------------------------------------------
# Hackathon-required endpoints
# ---------------------------------------------------------------------------

@app.get("/tasks")
async def tasks():
    action_schema = MigrationAction.model_json_schema()
    return {
        "tasks": list_tasks(),
        "action_schema": action_schema,
    }


@app.post("/grader")
async def grader():
    env = _get_env()
    return env.grade()


@app.post("/baseline")
async def baseline():
    """Run baseline inference on all tasks and return scores."""
    from db_migration_env.server.baseline_runner import run_baseline
    results = await run_baseline()
    return results


# ---------------------------------------------------------------------------
# MCP (JSON-RPC) endpoint — required by OpenEnv spec
# ---------------------------------------------------------------------------

@app.post("/mcp")
async def mcp_endpoint(request_body: Dict[str, Any] = {}):
    """Minimal MCP JSON-RPC endpoint for OpenEnv compatibility."""
    jsonrpc = request_body.get("jsonrpc", "2.0")
    method = request_body.get("method", "")
    req_id = request_body.get("id", 1)
    params = request_body.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-03-26",
                "serverInfo": {"name": "db-migration-env", "version": "1.0.0"},
                "capabilities": {"tools": {}},
            },
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "reset",
                        "description": "Reset the environment to start a new migration episode.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string", "description": "Task ID to run"},
                            },
                        },
                    },
                    {
                        "name": "step",
                        "description": "Execute a SQL statement against the database.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sql": {"type": "string", "description": "SQL statement to execute"},
                            },
                            "required": ["sql"],
                        },
                    },
                    {
                        "name": "state",
                        "description": "Get the current environment state.",
                        "inputSchema": {"type": "object", "properties": {}},
                    },
                    {
                        "name": "grade",
                        "description": "Grade the current migration episode.",
                        "inputSchema": {"type": "object", "properties": {}},
                    },
                ],
            },
        }
    elif method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        env = _get_env()

        if tool_name == "reset":
            obs = env.reset(task_id=tool_args.get("task_id"))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(obs.model_dump())}]},
            }
        elif tool_name == "step":
            action = MigrationAction(sql=tool_args.get("sql", ""))
            obs = env.step(action)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(obs.model_dump())}]},
            }
        elif tool_name == "state":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(env.state.model_dump())}]},
            }
        elif tool_name == "grade":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(env.grade())}]},
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


# ---------------------------------------------------------------------------
# WebSocket endpoint
# ---------------------------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    session_id = str(id(ws))
    env = MigrationEnvironment()
    _envs[session_id] = env

    try:
        while True:
            raw = await ws.receive_text()
            msg = json.loads(raw)
            msg_type = msg.get("type", "")

            if msg_type == "reset":
                obs = env.reset(
                    task_id=msg.get("task_id"),
                    seed=msg.get("seed"),
                    episode_id=msg.get("episode_id"),
                )
                await ws.send_json({
                    "type": "observation",
                    "data": obs.model_dump(),
                })

            elif msg_type == "step":
                action = MigrationAction(sql=msg.get("sql", ""), metadata=msg.get("metadata", {}))
                obs = env.step(action)
                await ws.send_json({
                    "type": "observation",
                    "data": obs.model_dump(),
                    "reward": obs.reward,
                    "done": obs.done,
                })

            elif msg_type == "state":
                await ws.send_json({
                    "type": "state",
                    "data": env.state.model_dump(),
                })

            elif msg_type == "close":
                await ws.send_json({"type": "closed"})
                break

            else:
                await ws.send_json({
                    "type": "error",
                    "message": f"Unknown message type: {msg_type}",
                })

    except WebSocketDisconnect:
        pass
    finally:
        env.close()
        _envs.pop(session_id, None)
