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
        self._checkpoints: dict[str, Checkpoint] = {}
        self._latest: dict[tuple[str, str], str] = {}

    def save(self, checkpoint: Checkpoint) -> None:
        existing = self._checkpoints.get(checkpoint.checkpoint_id)
        if existing is not None and existing != checkpoint:
            raise ValueError(f"checkpoint id already exists: {checkpoint.checkpoint_id}")
        self._checkpoints[checkpoint.checkpoint_id] = checkpoint
        self._latest[(checkpoint.mission_id, checkpoint.task_id)] = checkpoint.checkpoint_id

    def latest(self, mission_id: str, task_id: str) -> Checkpoint | None:
        checkpoint_id = self._latest.get((mission_id, task_id))
        return self._checkpoints.get(checkpoint_id) if checkpoint_id else None


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
