from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StructuredArtifact:
    """Immutable artifact exchanged between specialized agents."""

    artifact_id: str
    schema_id: str
    version: str
    owner_agent_id: str
    payload: dict
    provenance_ids: tuple[str, ...] = ()
