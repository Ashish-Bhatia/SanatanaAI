import json
from pathlib import Path

from jsonschema import validate

from sanatana_ai.provenance import validate_evidence_chain

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "data" / "fixtures" / "provenance"
SCHEMA_DIR = ROOT / "schemas"



def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))



def test_representative_provenance_fixtures_match_schemas() -> None:
    fixture_schema_pairs = {
        "source": "source_record.schema.json",
        "passage": "passage_record.schema.json",
        "claim": "claim_record.schema.json",
        "evidence_reference": "evidence_reference.schema.json",
        "provenance": "provenance_record.schema.json",
    }

    for fixture_name, schema_name in fixture_schema_pairs.items():
        validate(load_json(FIXTURE_DIR / f"{fixture_name}.json"), load_json(SCHEMA_DIR / schema_name))



def test_representative_fixture_forms_valid_source_to_claim_chain() -> None:
    validate_evidence_chain(
        load_json(FIXTURE_DIR / "source.json"),
        load_json(FIXTURE_DIR / "passage.json"),
        load_json(FIXTURE_DIR / "claim.json"),
        load_json(FIXTURE_DIR / "evidence_reference.json"),
        load_json(FIXTURE_DIR / "provenance.json"),
    )
