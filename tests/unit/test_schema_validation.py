import json
from pathlib import Path

import pytest

from sanatana_ai.validation.schema import SchemaValidationError, validate_json_document


ROOT = Path(__file__).parents[2]


def test_agent_contract_schema_accepts_valid_document() -> None:
    schema = ROOT / "agents/schemas/agent-contract.schema.json"
    document = {
        "id": "research.source-discovery",
        "version": "1.0.0",
        "responsibility": "Discover candidate sources for a research task.",
        "inputs": ["research_request"],
        "outputs": ["source_candidates"],
        "permissions": ["source.discovery"],
        "validation": ["source_metadata_check"],
        "failure_handling": ["retry_transient", "fail_closed"],
        "provenance_required": True,
        "forbidden_behaviors": ["fabricate_sources"],
    }
    validate_json_document(document, schema)


def test_provenance_requires_evidence() -> None:
    schema = ROOT / "data/schemas/provenance-record.schema.json"
    document = {
        "provenance_id": "prov-example",
        "claim_id": "claim-example",
        "evidence": [],
        "processing": [],
        "evidence_class": "primary_textual_evidence",
    }
    with pytest.raises(SchemaValidationError):
        validate_json_document(document, schema)


def test_task_schema_is_valid_json() -> None:
    schema = ROOT / "missions/schemas/task.schema.json"
    json.loads(schema.read_text(encoding="utf-8"))
