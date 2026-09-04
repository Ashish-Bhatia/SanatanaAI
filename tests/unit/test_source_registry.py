from datetime import datetime, timezone

import pytest

from sanatana_ai.source_registry import AcquisitionRecord, SourceRecord, SourceRegistry


def source() -> SourceRecord:
    return SourceRecord(
        id="source-1",
        title="Representative text",
        source_type="text",
        metadata={"language": "sa"},
    )


def acquisition(
    source_id: str = "source-1", acquisition_id: str = "acq-1"
) -> AcquisitionRecord:
    return AcquisitionRecord(
        id=acquisition_id,
        source_id=source_id,
        retrieved_at=datetime(2026, 9, 4, tzinfo=timezone.utc),
        retrieval_method="fixture",
        locator="fixtures/source-1.txt",
        content_digest="sha256:example",
        metadata={"tool": "test"},
    )


def test_register_source_is_idempotent_for_identical_record() -> None:
    registry = SourceRegistry()
    first = registry.register_source(source())
    second = registry.register_source(source())
    assert first == second
    assert registry.get_source("source-1") == first


def test_source_id_conflict_fails_closed() -> None:
    registry = SourceRegistry()
    registry.register_source(source())
    conflicting = SourceRecord("source-1", "Different", "text", {"language": "sa"})
    with pytest.raises(ValueError, match="different content"):
        registry.register_source(conflicting)


def test_acquisition_requires_registered_source() -> None:
    registry = SourceRegistry()
    with pytest.raises(ValueError, match="unknown source"):
        registry.register_acquisition(acquisition(source_id="missing"))


def test_acquisition_is_linked_to_source() -> None:
    registry = SourceRegistry()
    registry.register_source(source())
    record = registry.register_acquisition(acquisition())
    assert registry.get_acquisition("acq-1") == record
    assert registry.acquisitions_for_source("source-1") == (record,)


def test_acquisition_requires_timezone_aware_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        AcquisitionRecord(
            id="acq-1",
            source_id="source-1",
            retrieved_at=datetime(2026, 9, 4, tzinfo=timezone.utc),
            retrieval_method="fixture",
            locator="fixtures/source-1.txt",
            content_digest="sha256:example",
            metadata={"tool": "test"},
        )
