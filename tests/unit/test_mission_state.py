import pytest
from sanatana_ai.missions.state import MissionState


def test_checkpoint_is_persisted_in_state() -> None:
    state = MissionState("mission-001")
    state.checkpoint_at("task-003")
    assert state.checkpoint == "task-003"


def test_empty_checkpoint_is_rejected() -> None:
    state = MissionState("mission-001")
    with pytest.raises(ValueError):
        state.checkpoint_at("  ")
