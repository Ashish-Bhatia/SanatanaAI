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
- Active implementation branch: `feature/provenance-source-registry`
- PR #17 is merged into `main`.
- Recovery PR #20 is merged into `main` at `bd4c2386b225ee0439ce22b1766fe4da355a14ab`.
- Issue #4 is complete.
- Issue #6 is the active product workstream.
- PR #21 remains open for the first Issue #6 increment.
- PR #21 current head is `dfea857e4ac2eda862bba05902d49c216ef95453`; CI run #192 is in progress for this head.
- PR #22 continues Issue #6 from the PR #21 implementation and targets `feature/provenance-evidence-pipeline`.
- PR #22 current head is `6d147a3091fe0df1bed910f60beb9280e91a293b`.
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

PR #21 establishes the versioned provenance contracts and fail-closed evidence-chain validation.

Branch `feature/provenance-source-registry` continues the requirement with:
- storage-neutral `SourceRegistry`
- stable source identity and idempotent registration
- fail-closed conflicting source-ID reuse
- separate acquisition records linked to registered sources
- retrieval timestamp, method, locator, content digest, and metadata
- timezone-aware acquisition timestamps
- unit coverage for registry and acquisition invariants
- architecture documentation for the new source/acquisition boundary

The CI workflow was corrected so pull requests targeting the provenance integration branch are validated by the same mandatory gate used for `main`.

## Validation status

PR #21 CI run #191 passed for head `c2d18ee14f6c42e1f793e076d2a544071c802bdb`.

PR #21 received CI-trigger synchronization commit `dfea857e4ac2eda862bba05902d49c216ef95453`; CI run #192 is currently in progress. No result is asserted until it completes.

PR #22 has implementation commit `6d147a3091fe0df1bed910f60beb9280e91a293b` after the previously validated PR #21 head and requires its own full CI run before merge.

PR #21 has one implementation review recorded by `Ashish-Bhatia` with state `COMMENTED`. No independent review submission is currently recorded.

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
