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
- Main baseline: `1cc6fe93611b5e0b058c9d53aebe294284bebadc`
- PR #21, `feat: establish provenance evidence contracts`, is merged into `main`.
- Issue #4 is complete.
- Issue #6 is the active product workstream.
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

## Validated increment merged to main

PR #21 established the first provenance evidence-contract increment and is merged into `main` at `1cc6fe93611b5e0b058c9d53aebe294284bebadc`.

It includes versioned `1.0` JSON Schemas for source, passage, claim, evidence reference, processing record, and provenance record, strict fail-closed validation, cross-artifact identity validation, evidence-class separation, representative fixtures, and automated tests.

## Current implementation increment

PR #22, `feat: add source registry and acquisition metadata`, is open against `main`.

Branch: `feature/provenance-source-registry`
Head: `444c9fe4b5e03010a5707bc7d7489fbe4193bcfd`

Scope:
- storage-neutral `SourceRegistry`
- stable `SourceRecord` validation and idempotent registration
- fail-closed conflicting source identifiers
- separate `AcquisitionRecord` linked to a registered source
- timezone-aware retrieval timestamps
- locator, retrieval method, content digest, and metadata
- versioned acquisition schema
- unit coverage for identity, linkage, idempotency, and timestamp invariants

PR #22 was retargeted to `main` after PR #21 merged. Fresh CI after retargeting is required and no result is claimed until GitHub reports it.

PR #23 remains open for text representations and addressable passages, based on the earlier source-registry branch. It should be reconciled after PR #22 integration rather than merged as an independent parallel path.

## Validation status

- Main contains merged PR #21.
- PR #22 requires fresh CI after retargeting and review before merge.
- PR #23 requires reconciliation with the clean `main` integration path before merge.

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
