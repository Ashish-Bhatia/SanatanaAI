from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MissionStatus(StrEnum):
    PLANNED = "planned"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class MissionState:
    mission_id: str
    status: MissionStatus = MissionStatus.PLANNED
    checkpoint: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def checkpoint_at(self, checkpoint: str) -> None:
        if not checkpoint.strip():
            raise ValueError("checkpoint must not be empty")
        self.checkpoint = checkpoint
