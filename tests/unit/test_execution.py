import pytest

from sanatana_ai.contracts.agent import AgentRequest, AgentResult
from sanatana_ai.missions.checkpoint import CheckpointStore, InMemoryCheckpointStore
from sanatana_ai.missions.task import TaskState, TaskStatus
from sanatana_ai.orchestration.execution import ExecutionService


class SuccessfulExecutor:
    def execute(self, request: AgentRequest) -> AgentResult:
        return AgentResult(
            mission_id=request.mission_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            status=TaskStatus.COMPLETED.value,
            output={"ok": True},
        )


class FailingExecutor:
    def execute(self, request: AgentRequest) -> AgentResult:
        raise RuntimeError("provider failure")


class InvalidResultExecutor:
    def execute(self, request: AgentRequest) -> AgentResult:
        return AgentResult(
            mission_id=request.mission_id,
            task_id=request.task_id,
            agent_id=request.agent_id,
            status="not-a-task-status",
        )


class FailingCheckpointStore(InMemoryCheckpointStore):
    def __init__(self, failing_checkpoint_id: str) -> None:
        super().__init__()
        self.failing_checkpoint_id = failing_checkpoint_id

    def save(self, checkpoint) -> None:
        if checkpoint.checkpoint_id == self.failing_checkpoint_id:
            raise RuntimeError("checkpoint persistence failure")
        super().save(checkpoint)


def make_ready_task() -> TaskState:
    task = TaskState(
        task_id="task-a",
        mission_id="mission-test",
        objective="execute task",
        agent_id="validation.schema",
    )
    task.transition_to(TaskStatus.READY)
    return task


def make_request() -> AgentRequest:
    return AgentRequest(
        mission_id="mission-test",
        task_id="task-a",
        agent_id="validation.schema",
    )


def test_execution_service_checkpoints_running_and_completed_states() -> None:
    store = InMemoryCheckpointStore()
    task = make_ready_task()
    result = ExecutionService(store).execute_task(task, SuccessfulExecutor(), make_request(), "cp-1")

    assert result.status == TaskStatus.COMPLETED.value
    assert task.status == TaskStatus.COMPLETED
    assert store.latest("mission-test", "task-a").state == TaskStatus.COMPLETED.value


def test_execution_service_records_failure_checkpoint() -> None:
    store = InMemoryCheckpointStore()
    task = make_ready_task()

    with pytest.raises(RuntimeError, match="agent execution failed"):
        ExecutionService(store).execute_task(task, FailingExecutor(), make_request(), "cp-1")

    assert task.status == TaskStatus.FAILED
    assert store.latest("mission-test", "task-a").state == TaskStatus.FAILED.value


def test_execution_service_rejects_non_ready_task() -> None:
    store = InMemoryCheckpointStore()
    task = TaskState(
        task_id="task-a",
        mission_id="mission-test",
        objective="execute task",
        agent_id="validation.schema",
    )

    with pytest.raises(ValueError, match="is not ready"):
        ExecutionService(store).execute_task(task, SuccessfulExecutor(), make_request(), "cp-1")


def test_execution_service_rejects_request_identity_mismatch() -> None:
    store = InMemoryCheckpointStore()
    task = make_ready_task()
    request = AgentRequest("mission-test", "task-a", "other.agent")

    with pytest.raises(ValueError, match="does not match task agent"):
        ExecutionService(store).execute_task(task, SuccessfulExecutor(), request, "cp-1")


def test_execution_service_rejects_invalid_result_and_checkpoints_failure() -> None:
    store = InMemoryCheckpointStore()
    task = make_ready_task()

    with pytest.raises(ValueError, match="invalid status"):
        ExecutionService(store).execute_task(task, InvalidResultExecutor(), make_request(), "cp-1")

    assert task.status == TaskStatus.FAILED
    assert store.latest("mission-test", "task-a").state == TaskStatus.FAILED.value


def test_execution_service_does_not_advance_task_when_running_checkpoint_fails() -> None:
    store: CheckpointStore = FailingCheckpointStore("cp-1")
    task = make_ready_task()

    with pytest.raises(RuntimeError, match="checkpoint persistence failure"):
        ExecutionService(store).execute_task(task, SuccessfulExecutor(), make_request(), "cp-1")

    assert task.status == TaskStatus.READY
