import json
from pathlib import Path

import pytest

from sanatana_ai.agents.registry import AgentRegistryError, load_registry

ROOT = Path(__file__).parents[2]
REGISTRY = ROOT / "agents/registry/foundation.agents.json"
SCHEMA = ROOT / "agents/schemas/agent-contract.schema.json"


def test_registry_rejects_duplicate_ids_deterministically(tmp_path: Path) -> None:
    document = json.loads(REGISTRY.read_text(encoding="utf-8"))
    document["agents"].append(document["agents"][0].copy())
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(AgentRegistryError, match="duplicate agent id"):
        load_registry(registry, SCHEMA)
