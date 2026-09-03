from sanatana_ai.missions.task import TaskState, resolve_task_readiness


def _task(task_id: str, dependencies: tuple[str, ...] = ()) -> TaskState:
    return TaskState(
        task_id=task_id,
        mission_id="mission-cycle",
        objective=task_id,
        agent_id="orchestration.mission",
        dependencies=dependencies,
    )


def test_two_task_dependency_cycle_is_rejected() -> None:
    tasks = [_task("task-a", ("task-b",)), _task("task-b", ("task-a",))]

    try:
        resolve_task_readiness(tasks)
    except ValueError as exc:
        assert "cycle" in str(exc).lower()
    else:
        raise AssertionError("expected cyclic dependency graph to be rejected")


def test_three_task_dependency_cycle_is_rejected() -> None:
    tasks = [
        _task("task-a", ("task-c",)),
        _task("task-b", ("task-a",)),
        _task("task-c", ("task-b",)),
    ]

    try:
        resolve_task_readiness(tasks)
    except ValueError as exc:
        assert "cycle" in str(exc).lower()
    else:
        raise AssertionError("expected cyclic dependency graph to be rejected")


def test_acyclic_dependency_graph_remains_supported() -> None:
    tasks = [_task("task-a"), _task("task-b", ("task-a",))]

    resolve_task_readiness(tasks)

    assert tasks[0].status.value == "ready"
    assert tasks[1].status.value == "blocked"
