from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentRequest:
    mission_id: str
    task_id: str
    agent_id: str
    input: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentResult:
    mission_id: str
    task_id: str
    agent_id: str
    status: str
    output: dict[str, Any] = field(default_factory=dict)
    artifacts: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
