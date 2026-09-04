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

## Validation
A fresh CI run is required for the new branch before merge. No local test result is asserted here because execution has not been performed in this session.

## Review and gate
The branch must follow the normal PR, CI, independent review, gate, and merge sequence. PR #21 remains open and still requires independent review.

## Result
The next Issue #6 increment is implemented on a dedicated branch without changing `main`. Source identity and acquisition history are now represented as separate governed artifacts.
