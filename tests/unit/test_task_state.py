import pytest
from sanatana_ai.missions.task import (
    InvalidTaskTransition,
    TaskState,
    TaskStatus,
    resolve_task_readiness,
)


def make_task(task_id: str, dependencies: tuple[str, ...] = ()) -> TaskState:
    return TaskState(
        task_id=task_id,
        mission_id="mission-test",
        objective=task_id,
        agent_id="validation.schema",
        dependencies=dependencies,
    )


def test_task_transitions_follow_lifecycle() -> None:
    task = make_task("task-a")
    task.transition_to(TaskStatus.READY)
    task.transition_to(TaskStatus.RUNNING)
    task.transition_to(TaskStatus.COMPLETED)
    assert task.status == TaskStatus.COMPLETED


def test_completed_task_cannot_restart() -> None:
    task = make_task("task-a")
    task.transition_to(TaskStatus.READY)
    task.transition_to(TaskStatus.RUNNING)
    task.transition_to(TaskStatus.COMPLETED)
    with pytest.raises(InvalidTaskTransition):
        task.transition_to(TaskStatus.RUNNING)


def test_readiness_requires_completed_dependencies() -> None:
    first = make_task("task-a")
    second = make_task("task-b", ("task-a",))
    resolve_task_readiness([first, second])
    assert first.status == TaskStatus.READY
    assert second.status == TaskStatus.BLOCKED

    first.transition_to(TaskStatus.RUNNING)
    first.transition_to(TaskStatus.COMPLETED)
    resolve_task_readiness([first, second])
    assert second.status == TaskStatus.READY


def test_failed_dependency_blocks_downstream_task() -> None:
    first = make_task("task-a")
    second = make_task("task-b", ("task-a",))
    first.transition_to(TaskStatus.READY)
    first.transition_to(TaskStatus.RUNNING)
    first.transition_to(TaskStatus.FAILED)
    resolve_task_readiness([first, second])
    assert second.status == TaskStatus.BLOCKED


def test_missing_dependency_fails_closed() -> None:
    task = make_task("task-b", ("task-missing",))
    with pytest.raises(ValueError, match="missing dependencies"):
        resolve_task_readiness([task])


def test_duplicate_task_ids_fail_closed() -> None:
    with pytest.raises(ValueError, match="duplicate task_id"):
        resolve_task_readiness([make_task("task-a"), make_task("task-a")])
