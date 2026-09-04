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
- Fixed both violations at source. The datetime fixture now uses `timezone.utc`, preserving the timezone-aware acquisition contract. Commit `ed5661adac49521c5afbcdd3db2a4e1ad300caf7` contains the correction.
- Synchronized project state with the verified failure and remediation.

## Validation
PR #21 CI run #191 passed for head `c2d18ee14f6c42e1f793e076d2a544071c802bdb`.
PR #21 CI run #192 passed for head `dfea857e4ac2eda862bba05902d49c216ef95453`.

PR #22 CI run #199 failed at linting. Formatting passed. The verified lint failures were `I001` import ordering and `DTZ001` naive datetime use. The source was corrected without changing CI rules.

Fresh CI run #200 was queued for corrected head `ed5661adac49521c5afbcdd3db2a4e1ad300caf7` before the project-state synchronization commit. No result is asserted until a workflow run for the final current head completes.

No local test result is asserted here because execution has not been performed in this session.

## Review and gate
The branch must follow the normal PR, CI, independent review, gate, and merge sequence. PR #21 remains open and still requires independent review. PR #22 requires its own successful CI and independent review before integration.

## Result
The verified lint blocker in PR #22 was fixed at source without weakening the CI gate. Fresh validation is required for the corrected current branch head. The branch remains dedicated to Issue #6 and does not modify `main` directly.
