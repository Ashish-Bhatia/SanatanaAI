import json
from pathlib import Path

import pytest

from sanatana_ai.agents.registry import AgentRegistryError, load_registry

ROOT = Path(__file__).parents[2]
REGISTRY = ROOT / "agents/registry/foundation.agents.json"
SCHEMA = ROOT / "agents/schemas/agent-contract.schema.json"


def test_foundation_registry_loads_and_has_unique_ids() -> None:
    entries = load_registry(REGISTRY, SCHEMA)
    assert len(entries) >= 2
    assert len({entry["id"] for entry in entries}) == len(entries)


def test_registry_rejects_duplicate_ids(tmp_path: Path) -> None:
    source = json.loads(REGISTRY.read_text(encoding="utf-8"))
    source["agents"].append(dict(source["agents"][0]))
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps(source), encoding="utf-8")
    with pytest.raises(AgentRegistryError, match="duplicate agent id"):
        load_registry(registry, SCHEMA)
