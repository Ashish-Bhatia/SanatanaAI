from datetime import datetime, timezone

import pytest

from sanatana_ai.missions.checkpoint import Checkpoint, InMemoryCheckpointStore, new_checkpoint


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
