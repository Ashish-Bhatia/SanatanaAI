from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from sanatana_ai.contracts.agent import AgentRequest, AgentResult
from sanatana_ai.missions.checkpoint import CheckpointStore, new_checkpoint
from sanatana_ai.missions.task import TaskState, TaskStatus


class AgentExecutor(Protocol):
    """Execution boundary for a specialized agent implementation."""

    def execute(self, request: AgentRequest) -> AgentResult:
        ...


@dataclass
class ExecutionService:
    """Coordinates task execution without coupling orchestration to an AI provider."""

    checkpoint_store: CheckpointStore

    def execute_task(
        self,
        task: TaskState,
        executor: AgentExecutor,
        request: AgentRequest,
        checkpoint_id: str,
    ) -> AgentResult:
        self._validate_request(task, request)
        if task.status != TaskStatus.READY:
            raise ValueError(f"task {task.task_id} is not ready: {task.status}")

        # Durable checkpoint first. Task state must never advance beyond the last
        # successfully persisted checkpoint.
        running_checkpoint = new_checkpoint(
            checkpoint_id, task.mission_id, task.task_id, TaskStatus.RUNNING.value
        )
        self.checkpoint_store.save(running_checkpoint)
        task.transition_to(TaskStatus.RUNNING)

        try:
            result = executor.execute(request)
            self._validate_result(task, result)
        except Exception as exc:
            failed_checkpoint = new_checkpoint(
                f"{checkpoint_id}-failed",
                task.mission_id,
                task.task_id,
                TaskStatus.FAILED.value,
            )
            self.checkpoint_store.save(failed_checkpoint)
            task.transition_to(TaskStatus.FAILED)
            if isinstance(exc, ValueError):
                raise
            raise RuntimeError(f"agent execution failed for task {task.task_id}") from exc

        terminal_status = _terminal_status(result.status)
        terminal_checkpoint = new_checkpoint(
            f"{checkpoint_id}-result",
            task.mission_id,
            task.task_id,
            terminal_status.value,
        )
        self.checkpoint_store.save(terminal_checkpoint)
        task.transition_to(terminal_status)
        return result

    @staticmethod
    def _validate_request(task: TaskState, request: AgentRequest) -> None:
        if request.task_id != task.task_id or request.mission_id != task.mission_id:
            raise ValueError("agent request does not match task identity")
        if request.agent_id != task.agent_id:
            raise ValueError("agent request does not match task agent")

    @staticmethod
    def _validate_result(task: TaskState, result: AgentResult) -> None:
        if result.mission_id != task.mission_id or result.task_id != task.task_id:
            raise ValueError("agent result does not match task identity")
        if result.agent_id != task.agent_id:
            raise ValueError("agent result does not match task agent")
        if result.status not in {status.value for status in TaskStatus}:
            raise ValueError(f"agent result has invalid status: {result.status}")


def _terminal_status(status: str) -> TaskStatus:
    if status == TaskStatus.COMPLETED.value:
        return TaskStatus.COMPLETED
    if status == TaskStatus.FAILED.value:
        return TaskStatus.FAILED
    return TaskStatus.BLOCKED
