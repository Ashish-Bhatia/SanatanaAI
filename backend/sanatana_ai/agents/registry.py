from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class AgentRegistryError(ValueError):
    """Raised when the agent registry is invalid or inconsistent."""


def load_registry(registry_path: Path, schema_path: Path) -> tuple[dict[str, Any], ...]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(registry, dict) or not isinstance(registry.get("agents"), list):
        raise AgentRegistryError("agent registry must contain an agents array")

    validator = Draft202012Validator(schema)
    entries: list[dict[str, Any]] = []
    ids: set[str] = set()
    for entry in registry["agents"]:
        errors = sorted(validator.iter_errors(entry), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(error.message for error in errors)
            raise AgentRegistryError(details)
        agent_id = entry["id"]
        if agent_id in ids:
            raise AgentRegistryError(f"duplicate agent id: {agent_id}")
        ids.add(agent_id)
        entries.append(entry)
    return tuple(entries)
