from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

EVIDENCE_CLASSES = frozenset(
    {
        "primary_textual_evidence",
        "traditional_interpretation",
        "scholarly_interpretation",
        "historical_inference",
        "ai_synthesis",
        "uncertainty",
    }
)

ARTIFACT_TYPES = frozenset(
    {
        "source",
        "text",
        "manuscript",
        "passage",
        "claim",
        "entity",
        "relationship",
        "article",
    }
)

SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class ProvenanceRecord:
    id: str
    artifact_id: str
    artifact_type: str
    source_ids: tuple[str, ...]
    evidence_class: str
    created_at: datetime
    processing_steps: tuple[dict[str, Any], ...]
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("unsupported provenance schema version")
        if not self.id or not self.artifact_id:
            raise ValueError("provenance identity is required")
        if self.artifact_type not in ARTIFACT_TYPES:
            raise ValueError("invalid artifact type")
        if not self.source_ids or len(set(self.source_ids)) != len(self.source_ids):
            raise ValueError("at least one unique source is required")
        if any(not isinstance(value, str) or not value for value in self.source_ids):
            raise ValueError("source IDs must be non-empty strings")
        if self.evidence_class not in EVIDENCE_CLASSES:
            raise ValueError("invalid evidence class")
        if not self.processing_steps:
            raise ValueError("processing history is required")
        if any(not isinstance(step, dict) for step in self.processing_steps):
            raise TypeError("processing steps must be objects")
        for step in self.processing_steps:
            for field in ("step_id", "operation", "agent_id"):
                if not isinstance(step.get(field), str) or not step[field]:
                    raise ValueError(f"processing step {field} is required")


def validate_provenance(record: dict[str, Any]) -> ProvenanceRecord:
    required = {
        "schema_version",
        "id",
        "artifact_id",
        "artifact_type",
        "source_ids",
        "evidence_class",
        "created_at",
        "processing_steps",
    }
    missing = required.difference(record)
    if missing:
        raise ValueError(f"missing provenance fields: {sorted(missing)}")
    if record["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported provenance schema version")
    source_ids = record["source_ids"]
    if not isinstance(source_ids, list):
        raise TypeError("source_ids must be a list")
    try:
        created_at = datetime.fromisoformat(str(record["created_at"]))
    except ValueError as exc:
        raise ValueError("created_at must be ISO-8601") from exc
    steps = record["processing_steps"]
    if not isinstance(steps, list):
        raise TypeError("processing_steps must be a list")
    return ProvenanceRecord(
        id=str(record["id"]),
        artifact_id=str(record["artifact_id"]),
        artifact_type=str(record["artifact_type"]),
        source_ids=tuple(source_ids),
        evidence_class=str(record["evidence_class"]),
        created_at=created_at,
        processing_steps=tuple(steps),
        schema_version=str(record["schema_version"]),
    )
