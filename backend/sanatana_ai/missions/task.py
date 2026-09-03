from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class TaskStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InvalidTaskTransition(ValueError):
    """Raised when a task lifecycle transition is not permitted."""


@dataclass
class TaskState:
    task_id: str
    mission_id: str
    objective: str
    agent_id: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: tuple[str, ...] = ()
    checkpoint_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    _TRANSITIONS = {
        TaskStatus.PENDING: {TaskStatus.READY, TaskStatus.BLOCKED, TaskStatus.CANCELLED},
        TaskStatus.READY: {TaskStatus.RUNNING, TaskStatus.BLOCKED, TaskStatus.CANCELLED},
        TaskStatus.RUNNING: {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.BLOCKED},
        TaskStatus.BLOCKED: {TaskStatus.READY, TaskStatus.CANCELLED},
        TaskStatus.FAILED: {TaskStatus.READY, TaskStatus.CANCELLED},
        TaskStatus.COMPLETED: set(),
        TaskStatus.CANCELLED: set(),
    }

    def transition_to(self, status: TaskStatus) -> None:
        if status == self.status:
            return
        if status not in self._TRANSITIONS[self.status]:
            raise InvalidTaskTransition(f"cannot transition task {self.task_id} from {self.status} to {status}")
        self.status = status


def _validate_dependency_graph(tasks: list[TaskState]) -> dict[str, TaskState]:
    by_id = {task.task_id: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("duplicate task_id detected")

    for task in tasks:
        missing = [dependency for dependency in task.dependencies if dependency not in by_id]
        if missing:
            raise ValueError(f"task {task.task_id} has missing dependencies: {missing}")
        if task.task_id in task.dependencies:
            raise ValueError(f"task {task.task_id} cannot depend on itself")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            raise ValueError(f"dependency cycle detected at task {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in by_id[task_id].dependencies:
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task in tasks:
        visit(task.task_id)

    return by_id


def resolve_task_readiness(tasks: list[TaskState]) -> None:
    """Update task readiness from dependency state, failing closed on invalid graphs."""
    by_id = _validate_dependency_graph(tasks)

    for task in tasks:
        if task.status in {TaskStatus.COMPLETED, TaskStatus.CANCELLED, TaskStatus.RUNNING}:
            continue
        dependencies = [by_id[dependency] for dependency in task.dependencies]
        if any(dep.status in {TaskStatus.FAILED, TaskStatus.CANCELLED} for dep in dependencies):
            if task.status in {TaskStatus.PENDING, TaskStatus.READY}:
                task.transition_to(TaskStatus.BLOCKED)
        elif all(dep.status == TaskStatus.COMPLETED for dep in dependencies):
            if task.status in {TaskStatus.PENDING, TaskStatus.BLOCKED, TaskStatus.FAILED}:
                task.transition_to(TaskStatus.READY)
        elif task.status == TaskStatus.READY:
            task.transition_to(TaskStatus.BLOCKED)
        elif task.status == TaskStatus.PENDING and dependencies:
            task.transition_to(TaskStatus.BLOCKED)
