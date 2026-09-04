# Conversation 015

Date: 2026-09-04

## Objective
Continue Issue #6 from the authoritative GitHub state after PR #22 reached a verified CI-successful head. Advance the next incomplete provenance boundary without bypassing review or CI gates.

## Repository verification
- `main` remains the protected delivery branch and was not modified directly.
- PR #21 remains open against `main` and still requires independent review approval.
- PR #22 remains open against `feature/provenance-evidence-pipeline`.
- PR #22 current head is `49e7cf7bb2af2aa218b468fa9bce34a783ee38ee`.
- CI run #220 completed successfully for PR #22's current head.
- Issue #6 remains the highest-priority incomplete product workstream.

## Analysis and decision
The remaining Issue #6 requirements explicitly include text/manuscript representations and addressable passages. These are the next implementation boundary after source registration and acquisition metadata. Keep the representation boundary separate from acquisition identity, preserve original/transliteration/translation distinctions, and require passages to bind to one representation while retaining source identity and language.

## Implementation
Created dedicated branch `feature/provenance-text-passages` from the verified PR #22 head.

Implemented:
- `TextRepresentation` and storage-neutral `TextRepresentationRegistry`.
- Explicit representation types: `original`, `transliteration`, and `translation`.
- Stable representation identity, source linkage, language, and non-empty text validation.
- `PassageRecord` with stable representation linkage, source linkage, locator, language, and text.
- Fail-closed checks for unknown representations, source mismatch, language mismatch, and conflicting IDs.
- Idempotent identical registration for representations and passages.
- `schemas/text_representation.schema.json`.
- Extended `schemas/passage_record.schema.json` with `representation_id`.
- Unit tests for registry idempotency and cross-boundary invariants.
- Architecture updates for text/manuscript and passage boundaries.
- CI workflow trigger coverage for provenance feature branches.

## Pull request
Opened PR #23 from `feature/provenance-text-passages` to `feature/provenance-source-registry`.
Current PR #23 head after governance synchronization: `67e201f03f43ae6698d00312d40bc24345d00144`.

## Validation
PR #23 has not yet produced a completed CI run. No CI success is claimed.
The branch contains no secrets and introduces no paid infrastructure.

## Gate
PR #21 and PR #22 remain independently review-gated. PR #23 must pass its applicable CI and independent review before integration.

## Next action
Inspect the CI result for PR #23 when GitHub exposes it. Fix any verified failure at source. Continue the remaining Issue #6 provenance processing-record work only after the representation/passage increment clears its required gates.
