"""Gradio UI — beautiful visual interface for the DB Migration environment.

Judges see this first on HF Spaces. It should be impressive.
"""

from __future__ import annotations

import json
import traceback
from typing import Optional

import gradio as gr

from db_migration_env.models import MigrationAction
from db_migration_env.server.environment import MigrationEnvironment
from db_migration_env.tasks.registry import TASK_REGISTRY, list_tasks

# Global env per Gradio session — recreated on reset to avoid SQLite thread issues
_demo_env: Optional[MigrationEnvironment] = None


def _get_env(force_new: bool = False) -> MigrationEnvironment:
    global _demo_env
    if _demo_env is None or force_new:
        _demo_env = MigrationEnvironment()
    return _demo_env


def _format_schema_md(schema, label: str) -> str:
    """Format a SchemaSnapshot as a nice markdown table."""
    if not schema.tables:
        return f"### {label}\n*No tables*\n"
    lines = [f"### {label}"]
    for t in schema.tables:
        lines.append(f"\n**`{t.name}`** ({t.row_count} rows)")
        lines.append("| Column | Type | PK | NOT NULL | Default |")
        lines.append("|--------|------|:--:|:--------:|---------|")
        for c in t.columns:
            pk = "Y" if c.is_pk else ""
            nn = "Y" if c.notnull else ""
            default = c.default_value or ""
            lines.append(f"| `{c.name}` | `{c.type}` | {pk} | {nn} | {default} |")
        if t.foreign_keys:
            for fk in t.foreign_keys:
                lines.append(f"  - FK: `{fk.from_column}` -> `{fk.to_table}({fk.to_column})`")
    return "\n".join(lines)


def _format_diff_md(diffs) -> str:
    if not diffs:
        return "**No differences - migration complete!**"
    lines = ["| Category | Table | Detail |", "|----------|-------|--------|"]
    for d in diffs:
        cat_emoji = {
            "missing_table": "missing table",
            "extra_table": "extra table",
            "missing_column": "missing col",
            "extra_column": "extra col",
            "type_mismatch": "type mismatch",
            "constraint_mismatch": "constraint",
            "missing_fk": "missing FK",
            "extra_fk": "extra FK",
        }.get(d.category, d.category)
        lines.append(f"| `{cat_emoji}` | `{d.table}` | {d.detail} |")
    return "\n".join(lines)


def _format_grade_md(grade: dict) -> str:
    total = grade.get("total_score", 0)
    passed = grade.get("checks_passed", 0)
    total_checks = grade.get("checks_total", 0)
    steps = grade.get("steps_taken", 0)
    errors = grade.get("error_count", 0)

    bar_total = int(total * 20) * "=" + int((1 - total) * 20) * "-"

    summary_lines = ""
    for ctype, counts in grade.get("summary", {}).items():
        p, t = counts["passed"], counts["total"]
        summary_lines += f"| `{ctype}` | {p} / {t} |\n"

    return f"""## Score: **{total:.4f}** ({passed}/{total_checks} checks)

`[{bar_total}]`

| Check Type | Passed |
|---|---|
{summary_lines}
Steps: **{steps}** | Errors: **{errors}**"""


def reset_env(task_id: str):
    """Reset the environment with the selected task."""
    env = _get_env(force_new=True)
    obs = env.reset(task_id=task_id)

    task = TASK_REGISTRY[task_id]
    current_md = _format_schema_md(obs.current_schema, "Current Schema")
    target_md = _format_schema_md(obs.target_schema, "Target Schema")
    diff_md = _format_diff_md(obs.schema_diff)
    grade = env.grade()
    grade_md = _format_grade_md(grade)

    status = f"**Episode started** | Task: `{task_id}` ({task.difficulty})"
    history = ""

    return current_md, target_md, diff_md, grade_md, status, history, ""


def step_env(sql: str, history: str):
    """Execute a SQL statement."""
    env = _get_env()
    if not sql.strip():
        return (
            _format_schema_md(env.state.current_schema, "Current Schema"),
            _format_diff_md([]),
            _format_grade_md(env.grade()),
            "**Error**: Empty SQL statement",
            history,
        )

    obs = env.step(MigrationAction(sql=sql.strip()))
    current_md = _format_schema_md(obs.current_schema, "Current Schema")
    diff_md = _format_diff_md(obs.schema_diff)
    grade = env.grade()
    grade_md = _format_grade_md(grade)

    error_marker = " [ERROR]" if obs.last_sql_error else ""
    reward_str = f" (reward: {obs.reward:+.4f})" if obs.reward is not None else ""
    step_line = f"**Step {obs.step_count}**: `{sql.strip()[:100]}`{error_marker}{reward_str}"
    if obs.last_sql_error:
        step_line += f"\n> {obs.last_sql_result}"
    new_history = (history + "\n\n" + step_line).strip() if history else step_line

    if obs.done:
        status = f"**Episode COMPLETE** | Final score: **{grade['total_score']:.4f}**"
    else:
        status = f"Step {obs.step_count} | Cumulative reward: {obs.metadata.get('cumulative_reward', 0):.4f}"

    return current_md, diff_md, grade_md, status, new_history


def build_gradio_app():
    """Build the Gradio Blocks app."""
    task_choices = [(f"{t['task_id']} ({t['difficulty']})", t["task_id"]) for t in list_tasks()]

    with gr.Blocks(title="DB Migration RL Environment") as demo:
        gr.Markdown("""
# DB Migration RL Environment

An **OpenEnv-compliant** RL environment where AI agents learn to migrate databases using SQL.
Select a task, then execute SQL statements one at a time to transform the source database into the target schema + data.

**Tasks**: Easy (31→41 tables) | Medium (25→44 tables) | Hard (35→55 tables) — narrative mode, all target schemas hidden
        """)

        with gr.Row():
            task_dropdown = gr.Dropdown(
                choices=task_choices,
                value=task_choices[0][1],
                label="Select Task",
                interactive=True,
            )
            reset_btn = gr.Button("Reset Episode", variant="primary", scale=0)

        status_bar = gr.Markdown("*Click 'Reset Episode' to begin*")

        with gr.Row():
            with gr.Column(scale=2):
                sql_input = gr.Textbox(
                    label="SQL Statement",
                    placeholder="Enter a SQL statement (e.g., CREATE TABLE ...)",
                    lines=3,
                )
                step_btn = gr.Button("Execute SQL", variant="primary")

            with gr.Column(scale=1, elem_classes="grade-box"):
                grade_display = gr.Markdown("## Score\n*Reset to begin*")

        with gr.Row():
            with gr.Column():
                current_schema = gr.Markdown("### Current Schema\n*Reset to begin*")
            with gr.Column():
                target_schema = gr.Markdown("### Target Schema\n*Reset to begin*")

        with gr.Accordion("Schema Differences", open=True):
            diff_display = gr.Markdown("*Reset to begin*", elem_classes="diff-box")

        with gr.Accordion("Step History", open=False):
            history_display = gr.Markdown("*No steps yet*")

        # Hidden state for history
        history_state = gr.State("")

        # Wire up events
        reset_btn.click(
            fn=reset_env,
            inputs=[task_dropdown],
            outputs=[current_schema, target_schema, diff_display, grade_display, status_bar, history_state, sql_input],
        )

        step_btn.click(
            fn=step_env,
            inputs=[sql_input, history_state],
            outputs=[current_schema, diff_display, grade_display, status_bar, history_state],
        ).then(
            fn=lambda h: h,
            inputs=[history_state],
            outputs=[history_display],
        ).then(
            fn=lambda: "",
            outputs=[sql_input],
        )

        sql_input.submit(
            fn=step_env,
            inputs=[sql_input, history_state],
            outputs=[current_schema, diff_display, grade_display, status_bar, history_state],
        ).then(
            fn=lambda h: h,
            inputs=[history_state],
            outputs=[history_display],
        ).then(
            fn=lambda: "",
            outputs=[sql_input],
        )

    return demo
