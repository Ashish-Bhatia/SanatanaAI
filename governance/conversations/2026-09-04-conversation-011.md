# Conversation 011

Date: 2026-09-04

## Decision

Foundation CI recovery is complete through merged PR #20. The active implementation workstream moves to Issue #6, Provenance: implement source-to-claim evidence pipeline.

## Verified baseline

- PR #17 is merged.
- PR #20 is merged at `bd4c2386b225ee0439ce22b1766fe4da355a14ab`.
- Issue #4 is complete.
- Issue #6 remains open and is the next product workstream.

## Requirement and architecture

REQ-006 defines stable source, passage, claim, evidence-reference, processing-record, and provenance artifacts. Architecture requires a source-to-claim evidence chain, explicit evidence classes, separation of original language, transliteration, and translation, and fail-closed provenance validation.

## Implementation plan

1. Establish versioned evidence artifact schemas.
2. Enforce strict provenance invariants in the backend.
3. Add representative fixtures and fail-closed tests.
4. Document the evidence chain and separation of source, translation, interpretation, and synthesis.
5. Run full CI, including security and package validation.
6. Review and merge only after all required gates pass.

## Current increment

Implemented on `feature/provenance-evidence-pipeline`:

- `schemas/source_record.schema.json`
- `schemas/passage_record.schema.json`
- `schemas/claim_record.schema.json`
- `schemas/evidence_reference.schema.json`
- `schemas/processing_record.schema.json`
- Versioned `schemas/provenance_record.schema.json`
- Strict version and type/invariant validation in `backend/sanatana_ai/provenance.py`
- Unit coverage for schema version, source typing, duplicate sources, and malformed processing steps
- Architecture and REQ-006 documentation

## Governance

No substantive change was made directly to `main`. No secrets or paid infrastructure were introduced. CI remains fail-closed.
