# SanatanaAI Project State

## Status

Phase: Evidence and Provenance / Phase 3
State: In progress
Last updated: 2026-09-04

## Source of truth

GitHub repository state is authoritative. ChatGPT conversation context is not authoritative when repository artifacts exist.

## Current baseline

- Repository: `Ashish-Bhatia/SanatanaAI`
- Default branch: `main`
- Active implementation branch: `feature/provenance-text-passages`
- PR #17 is merged into `main`.
- Recovery PR #20 is merged into `main` at `bd4c2386b225ee0439ce22b1766fe4da355a14ab`.
- Issue #4 is complete.
- Issue #6 is the active product workstream.
- PR #21 remains open for the first Issue #6 increment and requires independent review.
- PR #22 continues Issue #6 with source registration and acquisition metadata and targets `feature/provenance-evidence-pipeline`.
- PR #22 current head is `69a1cf09c23771a7e8da569963534b8cbb2f69a9`.
- PR #22 CI run #220 passed for prior head `49e7cf7bb2af2aa218b468fa9bce34a783ee38ee`. The current head contains a CI-trigger correction and has no completed CI run yet.
- PR #23 continues Issue #6 with text representations and addressable passages and targets `feature/provenance-source-registry`.
- PR #23 current head is `6884dbfa68918742799f44c68189e25984db3e31`.
- PR #23 CI run #221 failed at formatting on earlier head `6077c0a00b57884fa3a0d734624687ab16abf72a`.
- PR #23 CI run #223 attempt 1 failed at formatting. The failure was corrected at source.
- PR #23 CI run #223 attempt 3 is queued against the current PR head.
- PR #21 and PR #22 remain review-gated and must not be bypassed.
- Issues #7 through #13 remain subsequent workstreams.

## Foundation completed

- Multi-agent, provenance-first architecture baseline
- ADRs 0001 through 0004
- Agent contract schema and registry governance
- Mission, task, checkpoint, and provenance schemas
- Reproducible Codespaces/devcontainer baseline
- Backend package scaffold
- Agent request/result and structured artifact contracts
- JSON Schema validation
- Task lifecycle, dependency readiness, and cycle detection
- Agent registry loading and validation
- Storage-neutral execution boundary
- Durable SQLite checkpoint adapter
- Persist-before-transition checkpoint semantics
- Checkpoint ordering, corruption, rollback, and recovery tests
- Runtime agent permission, artifact type, ownership, provenance, and duplicate-artifact controls
- Cooperative retry, timeout, and cancellation controls
- Foundation CI quality gates including formatting, linting, mypy, dependency audit, package build, ADR validation, tests, and secret scanning

## Current workstream

Issue #6, `Provenance: implement source-to-claim evidence pipeline`.

Requirement scope:
- source registry and stable source identity
- acquisition and retrieval metadata
- text/manuscript representations
- addressable passages
- atomic claims
- claim-to-passage evidence references
- processing/provenance history
- original-language, transliteration, and translation separation
- explicit evidence classes
- reproducible processing records

## Current implementation increments

PR #21 establishes versioned provenance contracts and fail-closed evidence-chain validation.

PR #22 establishes:
- storage-neutral `SourceRegistry`
- stable source identity and idempotent registration
- fail-closed conflicting source-ID reuse
- separate acquisition records linked to registered sources
- retrieval timestamp, method, locator, content digest, and metadata
- timezone-aware acquisition timestamps
- unit coverage for registry and acquisition invariants
- architecture documentation for the source/acquisition boundary

PR #23 establishes:
- storage-neutral `TextRepresentationRegistry`
- explicit original, transliteration, and translation representation types
- stable representation identity, source linkage, language, and non-empty text
- addressable `PassageRecord` linked to one text representation
- fail-closed unknown-representation and source/language mismatch checks
- idempotent identity handling with conflicting-ID rejection
- versioned text representation schema
- passage schema linkage to text representation identity
- representative text representation fixture and updated passage fixture
- unit coverage for representation and passage invariants
- architecture documentation for text/manuscript and passage boundaries

The CI workflow is configured to validate pull requests targeting the provenance integration branches. PR #22's last completed CI run #220 passed for head `49e7cf7bb2af2aa218b468fa9bce34a783ee38ee`; its current workflow-trigger correction is awaiting fresh validation. PR #23's first CI attempts exposed formatting defects; those defects were corrected at source. Run #223 attempt 3 is queued against the current PR head.

## Validation status

PR #22 CI run #220 completed successfully for head `49e7cf7bb2af2aa218b468fa9bce34a783ee38ee`.

PR #23 CI run #221 failed at formatting on earlier head `6077c0a00b57884fa3a0d734624687ab16abf72a`.
PR #23 CI run #223 attempt 1 failed at formatting because `tests/unit/test_text_representation.py` required Ruff formatting. The source was corrected in `ba6aa84a0cd1fd7f4c512b36e767908c10122667`.
PR #23 CI run #223 attempt 3 is queued against current head `6884dbfa68918742799f44c68189e25984db3e31`. No success is asserted.

PR #21 has one implementation review recorded by `Ashish-Bhatia` with state `COMMENTED`. No independent review approval is recorded.

## Delivery rules

- No substantive changes directly on `main`.
- Use dedicated feature branches for product work.
- CI is a mandatory quality gate.
- Fix failures at source. Never weaken gates.
- Never commit secrets.
- Do not introduce paid infrastructure without approval.

## Issue maintenance policy

GitHub Issues are the operational backlog. Maintain existing issues rather than creating duplicates. Update scope, acceptance criteria, blockers, implementation links, and completion state as work progresses. Close only after implementation, validation, documentation, review, and merge gates pass.

Substantive conversations and decisions are recorded under `governance/conversations/`. Architectural decisions require ADRs. Requirement changes require requirements documentation updates.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, ADRs, agent contracts, current PR/CI state, GitHub issues, and conversation records before changing project state.
