from datetime import datetime, timezone

import pytest
from sanatana_ai.provenance import validate_provenance


def valid_record() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "id": "prov-1",
        "artifact_id": "claim-1",
        "artifact_type": "claim",
        "source_ids": ["source-1"],
        "evidence_class": "primary_textual_evidence",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "processing_steps": [
            {
                "step_id": "step-1",
                "operation": "extract",
                "agent_id": "claim-extractor",
            }
        ],
    }


def test_valid_provenance_is_accepted() -> None:
    record = validate_provenance(valid_record())
    assert record.artifact_id == "claim-1"
    assert record.schema_version == "1.0"


@pytest.mark.parametrize(
    "field",
    [
        "schema_version",
        "id",
        "artifact_id",
        "source_ids",
        "evidence_class",
        "processing_steps",
    ],
)
def test_missing_required_provenance_fails(field: str) -> None:
    record = valid_record()
    del record[field]
    with pytest.raises(ValueError):
        validate_provenance(record)


def test_unknown_schema_version_fails() -> None:
    record = valid_record()
    record["schema_version"] = "2.0"
    with pytest.raises(ValueError, match="unsupported provenance schema version"):
        validate_provenance(record)


def test_unknown_evidence_class_fails() -> None:
    record = valid_record()
    record["evidence_class"] = "unsupported"
    with pytest.raises(ValueError, match="invalid evidence class"):
        validate_provenance(record)


def test_duplicate_sources_fail() -> None:
    record = valid_record()
    record["source_ids"] = ["source-1", "source-1"]
    with pytest.raises(ValueError, match="unique source"):
        validate_provenance(record)


def test_non_list_sources_fail() -> None:
    record = valid_record()
    record["source_ids"] = "source-1"
    with pytest.raises(TypeError, match="source_ids must be a list"):
        validate_provenance(record)


def test_malformed_processing_step_fails() -> None:
    record = valid_record()
    record["processing_steps"] = [{"step_id": "step-1", "operation": "extract"}]
    with pytest.raises(ValueError, match="agent_id is required"):
        validate_provenance(record)
