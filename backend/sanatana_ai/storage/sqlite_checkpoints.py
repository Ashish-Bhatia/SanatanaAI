from __future__ import annotations

import sqlite3
from collections.abc import Callable
from datetime import UTC, datetime

from sanatana_ai.missions.checkpoint import (
    Checkpoint,
    CheckpointStore,
    validate_checkpoint,
)


class SQLiteCheckpointStore(CheckpointStore):
    """Transactional SQLite adapter for the storage-neutral checkpoint contract.

    Each save is atomic. A checkpoint ID is immutable: replaying identical data is
    idempotent, while conflicting data fails closed. Recovery selects the newest
    checkpoint by UTC creation time and then checkpoint ID as a deterministic tie-breaker.
    """

    def __init__(
        self,
        connection: sqlite3.Connection,
        *,
        initialize: bool = True,
    ) -> None:
        self._connection = connection
        self._connection.row_factory = sqlite3.Row
        if initialize:
            self._initialize_schema()

    def _initialize_schema(self) -> None:
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    mission_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            self._connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_checkpoints_task_latest
                ON checkpoints (mission_id, task_id, created_at DESC, checkpoint_id DESC)
                """
            )

    def save(self, checkpoint: Checkpoint) -> None:
        """Atomically persist a checkpoint with idempotent replay semantics."""
        validate_checkpoint(checkpoint)
        created_at = _utc_iso(checkpoint.created_at)
        try:
            with self._connection:
                self._connection.execute(
                    """
                    INSERT INTO checkpoints
                        (checkpoint_id, mission_id, task_id, state, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        checkpoint.checkpoint_id,
                        checkpoint.mission_id,
                        checkpoint.task_id,
                        checkpoint.state,
                        created_at,
                    ),
                )
        except sqlite3.IntegrityError:
            existing = self._connection.execute(
                """
                SELECT checkpoint_id, mission_id, task_id, state, created_at
                FROM checkpoints
                WHERE checkpoint_id = ?
                """,
                (checkpoint.checkpoint_id,),
            ).fetchone()
            if existing is None:
                raise
            stored = _row_to_checkpoint(existing)
            if _checkpoint_identity(stored) != _checkpoint_identity(checkpoint):
                raise ValueError(f"checkpoint id already exists: {checkpoint.checkpoint_id}")

    def latest(self, mission_id: str, task_id: str) -> Checkpoint | None:
        row = self._connection.execute(
            """
            SELECT checkpoint_id, mission_id, task_id, state, created_at
            FROM checkpoints
            WHERE mission_id = ? AND task_id = ?
            ORDER BY created_at DESC, checkpoint_id DESC
            LIMIT 1
            """,
            (mission_id, task_id),
        ).fetchone()
        return _row_to_checkpoint(row) if row is not None else None

    def close(self) -> None:
        self._connection.close()


def open_sqlite_checkpoint_store(
    database: str,
    *,
    connection_factory: Callable[[str], sqlite3.Connection] = sqlite3.connect,
) -> SQLiteCheckpointStore:
    """Open a checkpoint store using the standard-library SQLite driver."""
    connection = connection_factory(database)
    connection.execute("PRAGMA foreign_keys = ON")
    if database != ":memory:":
        connection.execute("PRAGMA journal_mode = WAL")
    return SQLiteCheckpointStore(connection)


def _utc_iso(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("checkpoint created_at must be timezone-aware")
    return value.astimezone(UTC).isoformat(timespec="microseconds")


def _checkpoint_identity(checkpoint: Checkpoint) -> tuple[str, str, str, str, str]:
    return (
        checkpoint.checkpoint_id,
        checkpoint.mission_id,
        checkpoint.task_id,
        checkpoint.state,
        _utc_iso(checkpoint.created_at),
    )


def _row_to_checkpoint(row: sqlite3.Row) -> Checkpoint:
    try:
        created_at = datetime.fromisoformat(row["created_at"])
    except ValueError as exc:
        raise ValueError("checkpoint created_at is corrupt") from exc
    checkpoint = Checkpoint(
        checkpoint_id=row["checkpoint_id"],
        mission_id=row["mission_id"],
        task_id=row["task_id"],
        state=row["state"],
        created_at=created_at,
    )
    validate_checkpoint(checkpoint)
    return checkpoint
