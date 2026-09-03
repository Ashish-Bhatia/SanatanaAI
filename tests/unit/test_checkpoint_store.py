import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from sanatana_ai.missions.checkpoint import Checkpoint, InMemoryCheckpointStore, new_checkpoint
from sanatana_ai.storage.sqlite_checkpoints import SQLiteCheckpointStore, open_sqlite_checkpoint_store


def test_checkpoint_round_trip() -> None:
    store = InMemoryCheckpointStore()
    checkpoint = Checkpoint(
        checkpoint_id="cp-1",
        mission_id="mission-test",
        task_id="task-a",
        state="completed",
        created_at=datetime.now(timezone.utc),
    )
    store.save(checkpoint)
    assert store.latest("mission-test", "task-a") == checkpoint


def test_checkpoint_save_is_idempotent_for_same_checkpoint() -> None:
    store = InMemoryCheckpointStore()
    checkpoint = new_checkpoint("cp-1", "mission-test", "task-a", "running")
    store.save(checkpoint)
    store.save(checkpoint)
    assert store.latest("mission-test", "task-a") == checkpoint


def test_checkpoint_store_keeps_latest_checkpoint_for_task() -> None:
    store = InMemoryCheckpointStore()
    first = new_checkpoint("cp-1", "mission-test", "task-a", "running")
    second = new_checkpoint("cp-2", "mission-test", "task-a", "completed")
    store.save(first)
    store.save(second)
    assert store.latest("mission-test", "task-a") == second


def test_checkpoint_latest_uses_creation_time_not_insert_order() -> None:
    store = InMemoryCheckpointStore()
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    older = Checkpoint("cp-old", "mission-test", "task-a", "running", base)
    newer = Checkpoint("cp-new", "mission-test", "task-a", "completed", base + timedelta(seconds=1))
    store.save(newer)
    store.save(older)
    assert store.latest("mission-test", "task-a") == newer


def test_checkpoint_rejects_conflicting_checkpoint_id() -> None:
    store = InMemoryCheckpointStore()
    store.save(new_checkpoint("cp-1", "mission-test", "task-a", "running"))
    conflicting = Checkpoint(
        checkpoint_id="cp-1",
        mission_id="mission-test",
        task_id="task-a",
        state="completed",
        created_at=datetime.now(timezone.utc),
    )
    with pytest.raises(ValueError, match="checkpoint id already exists"):
        store.save(conflicting)


def test_new_checkpoint_rejects_empty_state() -> None:
    with pytest.raises(ValueError, match="state must not be empty"):
        new_checkpoint("cp-1", "mission-test", "task-a", " ")


def test_sqlite_checkpoint_round_trip_survives_reopen(tmp_path) -> None:
    database = tmp_path / "checkpoints.sqlite3"
    first_store = open_sqlite_checkpoint_store(str(database))
    checkpoint = new_checkpoint("cp-1", "mission-test", "task-a", "running")
    first_store.save(checkpoint)
    first_store.close()

    second_store = open_sqlite_checkpoint_store(str(database))
    assert second_store.latest("mission-test", "task-a") == checkpoint
    second_store.close()


def test_sqlite_checkpoint_save_is_idempotent() -> None:
    store = SQLiteCheckpointStore(sqlite3.connect(":memory:"))
    checkpoint = new_checkpoint("cp-1", "mission-test", "task-a", "running")
    store.save(checkpoint)
    store.save(checkpoint)
    assert store.latest("mission-test", "task-a") == checkpoint


def test_sqlite_checkpoint_rejects_conflicting_id() -> None:
    store = SQLiteCheckpointStore(sqlite3.connect(":memory:"))
    checkpoint = new_checkpoint("cp-1", "mission-test", "task-a", "running")
    store.save(checkpoint)
    conflicting = Checkpoint(
        checkpoint_id="cp-1",
        mission_id="mission-test",
        task_id="task-a",
        state="completed",
        created_at=checkpoint.created_at + timedelta(seconds=1),
    )
    with pytest.raises(ValueError, match="checkpoint id already exists"):
        store.save(conflicting)


def test_sqlite_latest_uses_creation_time_not_insert_order() -> None:
    store = SQLiteCheckpointStore(sqlite3.connect(":memory:"))
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    older = Checkpoint("cp-old", "mission-test", "task-a", "running", base)
    newer = Checkpoint("cp-new", "mission-test", "task-a", "completed", base + timedelta(seconds=1))
    store.save(newer)
    store.save(older)
    assert store.latest("mission-test", "task-a") == newer


def test_sqlite_rejects_naive_checkpoint_timestamp() -> None:
    store = SQLiteCheckpointStore(sqlite3.connect(":memory:"))
    checkpoint = Checkpoint(
        "cp-1", "mission-test", "task-a", "running", datetime(2026, 1, 1)
    )
    with pytest.raises(ValueError, match="timezone-aware"):
        store.save(checkpoint)


def test_sqlite_rejects_corrupt_checkpoint_row() -> None:
    connection = sqlite3.connect(":memory:")
    store = SQLiteCheckpointStore(connection)
    connection.execute(
        "INSERT INTO checkpoints VALUES (?, ?, ?, ?, ?)",
        ("cp-corrupt", "mission-test", "task-a", "running", "not-a-timestamp"),
    )
    with pytest.raises(ValueError, match="created_at is corrupt"):
        store.latest("mission-test", "task-a")


def test_sqlite_transaction_rolls_back_injected_failure() -> None:
    connection = sqlite3.connect(":memory:")
    store = SQLiteCheckpointStore(connection)
    connection.execute(
        """
        CREATE TRIGGER fail_checkpoint_insert
        BEFORE INSERT ON checkpoints
        WHEN NEW.state = 'boom'
        BEGIN
            SELECT RAISE(ABORT, 'injected checkpoint failure');
        END;
        """
    )
    failing = new_checkpoint("cp-boom", "mission-test", "task-a", "boom")

    with pytest.raises(sqlite3.IntegrityError, match="injected checkpoint failure"):
        store.save(failing)

    assert store.latest("mission-test", "task-a") is None
