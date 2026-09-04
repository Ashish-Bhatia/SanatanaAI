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
PR #21 established versioned source, passage, claim, evidence-reference, processing-record, and provenance contracts and passed CI run #192 on its validated head. The next incomplete Issue #6 scope item is source registry and acquisition/retrieval metadata.

## Implementation
- Created `feature/provenance-source-registry` from PR #21 head `c2d18ee14f6c42e1f793e076d2a544071c802bdb`.
- Added `SourceRecord`, `AcquisitionRecord`, and storage-neutral `SourceRegistry`.
- Added versioned acquisition JSON Schema.
- Added unit tests for idempotency, conflicting identifiers, source linkage, and timezone-aware retrieval.
- Updated architecture and project state to record the new boundary.
- Corrected CI workflow targeting so dependent pull requests into `feature/provenance-evidence-pipeline` receive the mandatory validation workflow.
- CI run #199 failed at linting. Ruff identified two violations in `tests/unit/test_source_registry.py`: import ordering (`I001`) and a naive datetime fixture (`DTZ001`).
- CI run #204 reproduced the lint failure on the then-current branch merge ref. The source was corrected without changing CI rules.
- CI run #209 reproduced the import-ordering violation on the PR #22 merge ref. The import block was corrected in commit `7e3a6f9568409b223318a932452692ccaada610f`.
- CI run #212 reproduced the same import-ordering violation on the PR #22 merge ref. The import block was corrected at source in commit `faf3eb4f9ad96a425d0d02f7127debafd0052ef2`.
- Project state was synchronized after the latest remediation in commit `fae73c5fbd9042a01acaa09e95226841a3937550`.
- Conversation record was synchronized after the latest remediation in commit `c039a9cf75301fcab3b6a29a4fe704a2906a0b4a`.

## Validation
PR #21 CI run #191 passed for head `c2d18ee14f6c42e1f793e076d2a544071c802bdb`.
PR #21 CI run #192 passed for head `dfea857e4ac2eda862bba05902d49c216ef95453`.

PR #22 CI run #209 failed at linting on merge ref `91360c2f11e8725b498f5948f4e2f2ae5ecf57e6`. The verified failure was `I001` import ordering in `tests/unit/test_source_registry.py`.

PR #22 CI run #212 failed at linting on merge ref `14e2026914e51b3a69d6ba019c7cb1b8127d6134`. The verified failure was `I001` import ordering in `tests/unit/test_source_registry.py`.

The import-ordering failure was corrected at source in commit `faf3eb4f9ad96a425d0d02f7127debafd0052ef2`. Fresh CI is required for the corrected head and no result is asserted until GitHub exposes it.

No local test result is asserted here because execution has not been performed in this session.

## Review and gate
The branch must follow the normal PR, CI, independent review, gate, and merge sequence. PR #21 remains open and still requires independent review. PR #22 requires its own successful CI and independent review before integration.

## Result
The verified CI lint blocker was fixed at source without weakening the CI gate. Governance records now reflect the latest corrected branch state. Fresh validation remains required. The branch remains dedicated to Issue #6 and does not modify `main` directly.
