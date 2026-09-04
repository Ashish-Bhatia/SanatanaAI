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


@dataclass(frozen=True)
class ProvenanceRecord:
    id: str
    artifact_id: str
    artifact_type: str
    source_ids: tuple[str, ...]
    evidence_class: str
    created_at: datetime
    processing_steps: tuple[dict[str, Any], ...]

    def __post_init__(self) -> None:
        if not self.id or not self.artifact_id:
            raise ValueError("provenance identity is required")
        if self.artifact_type not in ARTIFACT_TYPES:
            raise ValueError("invalid artifact type")
        if not self.source_ids or len(set(self.source_ids)) != len(self.source_ids):
            raise ValueError("at least one unique source is required")
        if self.evidence_class not in EVIDENCE_CLASSES:
            raise ValueError("invalid evidence class")
        if not self.processing_steps:
            raise ValueError("processing history is required")


def validate_provenance(record: dict[str, Any]) -> ProvenanceRecord:
    required = {
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
    try:
        created_at = datetime.fromisoformat(str(record["created_at"]).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("created_at must be ISO-8601") from exc
    steps = record["processing_steps"]
    if not isinstance(steps, list):
        raise ValueError("processing_steps must be a list")
    return ProvenanceRecord(
        id=str(record["id"]),
        artifact_id=str(record["artifact_id"]),
        artifact_type=str(record["artifact_type"]),
        source_ids=tuple(str(value) for value in record["source_ids"]),
        evidence_class=str(record["evidence_class"]),
        created_at=created_at,
        processing_steps=tuple(steps),
    )
