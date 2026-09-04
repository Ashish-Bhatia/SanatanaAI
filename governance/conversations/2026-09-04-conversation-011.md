# Conversation 011

Date: 2026-09-04

## Decision

Foundation CI recovery is complete through merged PR #20. The active implementation workstream remains Issue #6, Provenance: implement source-to-claim evidence pipeline.

## Verified baseline

- PR #17 is merged.
- PR #20 is merged at `bd4c2386b225ee0439ce22b1766fe4da355a14ab`.
- Issue #4 is complete.
- Issue #6 remains open and is the active product workstream.

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

- Versioned `1.0` schemas for source, passage, claim, evidence reference, processing record, and provenance record.
- Strict version and type/invariant validation in `backend/sanatana_ai/provenance.py`.
- Cross-artifact source-to-claim identity validation.
- Fail-closed rejection of translation sources as primary textual evidence.
- Representative provenance fixtures and end-to-end evidence-chain tests.
- Architecture and REQ-006 documentation.

## CI remediation

CI run #176 failed at `ruff format --check backend tests` on head `5a6cd856216143973374a7543178515e9fbe4fd0`. The configured Ruff line length is 120. The provenance condition was corrected to the formatter-compatible single-line form in commit `f135c1068fcc1bdb9417f76d8f53df66c3cc1352`.

A fresh CI run has not yet been reported for the corrective head. The workstream remains blocked at CI validation until GitHub reports all required gates passing.

## Governance

No substantive change was made directly to `main`. No secrets or paid infrastructure were introduced. CI remains fail-closed.
