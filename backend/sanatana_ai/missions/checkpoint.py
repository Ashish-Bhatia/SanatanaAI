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

    def save(self, checkpoint: Checkpoint) -> None:
        validate_checkpoint(checkpoint)
        existing = self._checkpoints.get(checkpoint.checkpoint_id)
        if existing is not None and existing != checkpoint:
            raise ValueError(f"checkpoint id already exists: {checkpoint.checkpoint_id}")
        self._checkpoints[checkpoint.checkpoint_id] = checkpoint

    def latest(self, mission_id: str, task_id: str) -> Checkpoint | None:
        candidates = (
            checkpoint
            for checkpoint in self._checkpoints.values()
            if checkpoint.mission_id == mission_id and checkpoint.task_id == task_id
        )
        return max(candidates, key=lambda item: (item.created_at, item.checkpoint_id), default=None)


def validate_checkpoint(checkpoint: Checkpoint) -> None:
    if not checkpoint.checkpoint_id.strip():
        raise ValueError("checkpoint_id must not be empty")
    if not checkpoint.mission_id.strip() or not checkpoint.task_id.strip():
        raise ValueError("checkpoint identifiers must not be empty")
    if not checkpoint.state.strip():
        raise ValueError("checkpoint state must not be empty")
    if checkpoint.created_at.tzinfo is None or checkpoint.created_at.utcoffset() is None:
        raise ValueError("checkpoint created_at must be timezone-aware")


def new_checkpoint(checkpoint_id: str, mission_id: str, task_id: str, state: str) -> Checkpoint:
    checkpoint = Checkpoint(
        checkpoint_id=checkpoint_id,
        mission_id=mission_id,
        task_id=task_id,
        state=state,
        created_at=datetime.now(timezone.utc),
    )
    validate_checkpoint(checkpoint)
    return checkpoint
