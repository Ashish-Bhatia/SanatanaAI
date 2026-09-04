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
- PR #23 remains open against `feature/provenance-source-registry`.
- PR #23 current head is `ba6aa84a0cd1fd7f4c512b36e767908c10122667`.
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
- Corrected formatting failures reported by CI #221.

## Pull request
Opened PR #23 from `feature/provenance-text-passages` to `feature/provenance-source-registry`.
Current PR #23 head after formatting remediation and governance synchronization is `7c603038cab41a18445ff8349d47e76b50b9893d`.

## Validation
PR #23 CI run #221 failed at the formatting gate for earlier head `6077c0a00b57884fa3a0d734624687ab16abf72a`. The failure was corrected in commit `ba6aa84a0cd1fd7f4c512b36e767908c10122667`.

The current head has not yet produced a completed CI run. No CI success is claimed for PR #23.

## Gate
PR #21 and PR #22 remain independently review-gated. PR #23 must pass its applicable CI and independent review before integration.

## Next action
Inspect the next CI result for PR #23. Fix any verified failure at source. Continue the remaining Issue #6 provenance processing-record work only after the representation/passage increment clears its required gates.
