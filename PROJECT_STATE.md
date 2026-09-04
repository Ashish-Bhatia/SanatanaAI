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
- Active implementation branch: `feature/provenance-evidence-pipeline`
- PR #17 is merged into `main`.
- Recovery PR #20 is merged into `main` at `bd4c2386b225ee0439ce22b1766fe4da355a14ab`.
- Issue #4 is complete and ready to be closed after state synchronization.
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

Current implementation increment:
- Versioned `1.0` JSON Schemas for source, passage, claim, evidence reference, processing record, and provenance record.
- Strict provenance validation with schema-version enforcement and fail-closed type/invariant checks.
- Unit coverage for schema version, source list typing, duplicate sources, and malformed processing steps.
- Architecture updated with the source-to-claim evidence chain and provenance invariants.

## Validation status

The provenance implementation is on `feature/provenance-evidence-pipeline`. CI validation is required before merge. No claim of green CI is made until GitHub reports the current PR head as passing all required gates.

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
