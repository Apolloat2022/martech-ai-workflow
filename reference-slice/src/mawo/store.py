"""SQLite persistence for trace and feedback records - the reference-slice
stand-in for D4's Trace Store. Zero new dependencies (sqlite3 is stdlib),
matching "no database beyond the vector store and SQLite".

Uses a single persistent connection per process rather than opening and
closing one per call: SQLite's ":memory:" path creates a brand-new, empty
database for every connection, so opening a fresh connection per operation
would silently lose everything written by the previous call whenever
MAWO_DB_PATH=":memory:" (as the test suite and latency harness both use).
"""
from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

from .schemas import FeedbackRequest, InvokeResponse

_connection: sqlite3.Connection | None = None


def _db_path() -> str:
    return os.environ.get("MAWO_DB_PATH", "data/mawo.db")


def _get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        path = _db_path()
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        _connection = sqlite3.connect(path, check_same_thread=False)
    return _connection


def init_db() -> None:
    conn = _get_connection()
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS traces (
                request_id TEXT PRIMARY KEY,
                use_case TEXT NOT NULL,
                retrieved_doc_ids TEXT NOT NULL,
                policy_status TEXT NOT NULL,
                policy_reasons TEXT NOT NULL,
                stage_timings_ms TEXT NOT NULL,
                model TEXT NOT NULL,
                model_version TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                request_id TEXT NOT NULL,
                verdict_outcome TEXT NOT NULL,
                reviewer_id TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def save_trace(response: InvokeResponse) -> None:
    conn = _get_connection()
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO traces
            (request_id, use_case, retrieved_doc_ids, policy_status,
             policy_reasons, stage_timings_ms, model, model_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                response.request_id,
                response.use_case.value,
                json.dumps(response.retrieved_doc_ids),
                response.policy_verdict.status,
                json.dumps(response.policy_verdict.reasons),
                json.dumps(response.trace.stage_timings_ms),
                response.trace.model,
                response.trace.model_version,
            ),
        )


def save_feedback(feedback: FeedbackRequest) -> None:
    conn = _get_connection()
    with conn:
        conn.execute(
            """
            INSERT INTO feedback (request_id, verdict_outcome, reviewer_id, notes)
            VALUES (?, ?, ?, ?)
            """,
            (feedback.request_id, feedback.verdict_outcome, feedback.reviewer_id, feedback.notes),
        )
