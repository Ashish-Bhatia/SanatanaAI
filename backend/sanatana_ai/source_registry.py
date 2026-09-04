from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

SOURCE_TYPES = frozenset(
    {"text", "manuscript", "edition", "translation", "commentary", "secondary_source"}
)
SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class SourceRecord:
    id: str
    title: str
    source_type: str
    metadata: dict[str, Any]
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("unsupported source schema version")
        if not self.id or not self.title:
            raise ValueError("source identity and title are required")
        if self.source_type not in SOURCE_TYPES:
            raise ValueError("invalid source type")
        if not self.metadata:
            raise ValueError("source metadata is required")


@dataclass(frozen=True)
class AcquisitionRecord:
    id: str
    source_id: str
    retrieved_at: datetime
    retrieval_method: str
    locator: str
    content_digest: str
    metadata: dict[str, Any]
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("unsupported acquisition schema version")
        if not all((self.id, self.source_id, self.retrieval_method, self.locator, self.content_digest)):
            raise ValueError("acquisition identity and retrieval fields are required")
        if not self.metadata:
            raise ValueError("acquisition metadata is required")
        if self.retrieved_at.tzinfo is None:
            raise ValueError("retrieved_at must be timezone-aware")


class SourceRegistry:
    """Storage-neutral registry enforcing stable source identity and acquisition linkage."""

    def __init__(self) -> None:
        self._sources: dict[str, SourceRecord] = {}
        self._acquisitions: dict[str, AcquisitionRecord] = {}

    def register_source(self, source: SourceRecord) -> SourceRecord:
        existing = self._sources.get(source.id)
        if existing is not None and existing != source:
            raise ValueError("source ID already exists with different content")
        self._sources[source.id] = source
        return source

    def register_acquisition(self, acquisition: AcquisitionRecord) -> AcquisitionRecord:
        if acquisition.source_id not in self._sources:
            raise ValueError("acquisition references an unknown source")
        existing = self._acquisitions.get(acquisition.id)
        if existing is not None and existing != acquisition:
            raise ValueError("acquisition ID already exists with different content")
        self._acquisitions[acquisition.id] = acquisition
        return acquisition

    def get_source(self, source_id: str) -> SourceRecord:
        try:
            return self._sources[source_id]
        except KeyError as exc:
            raise KeyError(f"unknown source: {source_id}") from exc

    def get_acquisition(self, acquisition_id: str) -> AcquisitionRecord:
        try:
            return self._acquisitions[acquisition_id]
        except KeyError as exc:
            raise KeyError(f"unknown acquisition: {acquisition_id}") from exc

    def acquisitions_for_source(self, source_id: str) -> tuple[AcquisitionRecord, ...]:
        self.get_source(source_id)
        return tuple(item for item in self._acquisitions.values() if item.source_id == source_id)
