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

Current implementation increment:
- Versioned `1.0` JSON Schemas for source, passage, claim, evidence reference, processing record, and provenance record.
- Strict provenance validation with schema-version enforcement and fail-closed type/invariant checks.
- Cross-artifact validation enforcing source, passage, claim, evidence-reference, and provenance identity links.
- Fail-closed protection against classifying a translation source as primary textual evidence.
- Representative source, passage, claim, evidence-reference, and provenance fixtures.
- Automated fixture schema validation and end-to-end source-to-claim chain validation.
- Unit coverage for malformed provenance and broken cross-artifact links.
- Architecture and requirement documentation updated on the feature branch.

## Validation status

PR #21 is open against `main`. CI run #176 failed at `ruff format --check backend tests` for head `5a6cd856216143973374a7543178515e9fbe4fd0`. The configured Ruff line length is 120, so the provenance condition was corrected to the formatter-compatible single-line form. Corrective commit: `f135c1068fcc1bdb9417f76d8f53df66c3cc1352`. Fresh CI for this head has not yet been reported.

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
