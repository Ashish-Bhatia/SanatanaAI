from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Checkpoint:
    checkpoint_id: str
    mission_id: str
    task_id: str
    state: str
    created_at: datetime


class CheckpointStore:
    """Persistence boundary for resumable execution checkpoints."""

    def save(self, checkpoint: Checkpoint) -> None:
        raise NotImplementedError

    def latest(self, mission_id: str, task_id: str) -> Checkpoint | None:
        raise NotImplementedError


class InMemoryCheckpointStore(CheckpointStore):
    def __init__(self) -> None:
        self._checkpoints: dict[tuple[str, str], Checkpoint] = {}

    def save(self, checkpoint: Checkpoint) -> None:
        key = (checkpoint.mission_id, checkpoint.task_id)
        existing = self._checkpoints.get(key)
        if existing is not None and existing.checkpoint_id != checkpoint.checkpoint_id:
            raise ValueError("checkpoint already exists for mission/task; use a new task checkpoint sequence")
        self._checkpoints[key] = checkpoint

    def latest(self, mission_id: str, task_id: str) -> Checkpoint | None:
        return self._checkpoints.get((mission_id, task_id))


def new_checkpoint(checkpoint_id: str, mission_id: str, task_id: str, state: str) -> Checkpoint:
    if not checkpoint_id.strip() or not mission_id.strip() or not task_id.strip():
        raise ValueError("checkpoint identifiers must not be empty")
    if not state.strip():
        raise ValueError("checkpoint state must not be empty")
    return Checkpoint(
        checkpoint_id=checkpoint_id,
        mission_id=mission_id,
        task_id=task_id,
        state=state,
        created_at=datetime.now(timezone.utc),
    )
