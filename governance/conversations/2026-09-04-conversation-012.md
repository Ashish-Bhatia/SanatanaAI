# Conversation 012

Date: 2026-09-04

## Objective
Continue Issue #6 after the provenance contract increment, implementing stable source registration and explicit acquisition metadata without introducing storage or infrastructure coupling.

## Requirements
- Stable source identity and explicit source metadata.
- Separate acquisition identity from source identity.
- Record retrieval time, method, locator, content digest, and metadata.
- Reject acquisitions for unknown sources.
- Reject conflicting reuse of source or acquisition identifiers.
- Preserve timezone-aware retrieval timestamps.
- Keep the registry storage-neutral and deterministic.

## Analysis
PR #21 established versioned source, passage, claim, evidence-reference, processing-record, and provenance contracts and passed CI run #191 on its validated head. The next incomplete Issue #6 scope item is source registry and acquisition/retrieval metadata.

## Implementation
- Created `feature/provenance-source-registry` from PR #21 head `c2d18ee14f6c42e1f793e076d2a544071c802bdb`.
- Added `SourceRecord`, `AcquisitionRecord`, and storage-neutral `SourceRegistry`.
- Added versioned acquisition JSON Schema.
- Added unit tests for idempotency, conflicting identifiers, source linkage, and timezone-aware retrieval.
- Updated architecture and project state to record the new boundary.
- Corrected CI workflow targeting so dependent pull requests into `feature/provenance-evidence-pipeline` receive the mandatory validation workflow.
- CI run #195 verified the first formatting failure on PR #22. Ruff identified two unformatted files: `backend/sanatana_ai/source_registry.py` and `tests/unit/test_source_registry.py`.
- Corrected both files on `feature/provenance-source-registry` in commits `f5f30d22a1d87f0a2f9c8e342e81d2de563f3399` and `023db184f23ec636430c739463788b6b1206bed8`.
- Synchronized project state with the verified PR #21 CI result and current PR #22 CI state.

## Validation
PR #21 CI run #192 passed for head `dfea857e4ac2eda862bba05902d49c216ef95453`.

PR #22 CI run #195 failed at formatting. The verified failure was limited to two Ruff formatting violations. Fresh CI run #197 is now in progress for corrected head `023db184f23ec636430c739463788b6b1206bed8`. No result is asserted until it completes.

No local test result is asserted here because execution has not been performed in this session.

## Review and gate
The branch must follow the normal PR, CI, independent review, gate, and merge sequence. PR #21 remains open and still requires independent review. PR #22 requires its own successful CI and independent review before integration.

## Result
The formatting blocker in PR #22 was fixed at source without weakening the CI gate. The corrected branch remains dedicated to Issue #6 and does not modify `main` directly.
