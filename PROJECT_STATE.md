# SanatanaAI Project State

## Status

Phase: Foundation / Phase 0
State: In progress
Last updated: 2026-09-04

## Source of truth

GitHub repository state is authoritative. ChatGPT conversation context is not authoritative when repository artifacts exist.

## Current baseline

- Repository: `Ashish-Bhatia/SanatanaAI`
- Default branch: `main`
- Foundation branch: `foundation/phase-0`
- Active implementation branch: `feature/checkpoint-recovery` (completed and merged; next implementation branch pending)
- Repository visibility: private
- PR #1: merged into `main` with merge commit `1bfa255511b1083562d1a0c4033507474c556f34`
- PR #2: merged into `foundation/phase-0`
- PR #14: merged into `main` with merge commit `56d975cfcdfc7425f5c0493dc39ec381702cdd31`
- Conversation records exist under `governance/conversations/`
- GitHub issues #4 through #13 remain the principal open Foundation and post-Foundation workstreams.

## Foundation completed

- Project README, state, roadmap, and architecture baseline
- ADR-0001 for multi-agent, provenance-first architecture
- ADR-0002 for storage-neutral checkpoint persistence and resumability
- Agent contract schema and registry governance
- Mission schema and provenance record schema
- Reproducible Codespaces/devcontainer baseline
- Python backend package scaffold
- Agent request/result contracts
- Mission checkpoint state primitive
- Executable JSON Schema validation package
- Mission task contract schema
- Task lifecycle and dependency-readiness primitives
- Dependency graph validation with multi-node cycle detection
- Agent registry loading and validation
- Storage-neutral execution service boundary
- Durable SQLite checkpoint reference adapter
- Persist-before-transition execution semantics
- Deterministic checkpoint ordering, corruption, rollback, and recovery tests
- Unit tests for checkpoint, schema, registry, task lifecycle, execution, and dependency-cycle behavior
- CI validation for JSON, foundation files, backend tests, and secret patterns
- GitHub issue backlog for principal engineering workstreams

## Validation status

- CI runs 22, 23, 24, and 29 passed on earlier corrected heads.
- CI run 50 passed on the orchestration execution increment.
- CI run 51 passed on the validated orchestration-core head before PR #2 integration.
- CI run 52 passed on Foundation head `14a019b538836171e31a932f23d3e68879608bd0` before PR #1 integration.
- PR #2 was reviewed and merged into `foundation/phase-0`.
- PR #1 was merged into `main` after its merge conflict was reconciled.
- CI run 61 passed on PR #14 head `69f68991207072a357fc772d4b9675de2481df9c`.
- CI run 62 passed on main merge commit `56d975cfcdfc7425f5c0493dc39ec381702cdd31`.
- Issue #3 was completed and automatically closed through PR #14.
- Issue #4 remains open because the broader quality-gate scope is not yet complete.

## Current work

1. Complete CI quality gates under issue #4 in parallel with feature delivery.
2. Implement agent contract, permission, and artifact governance under issue #5.
3. Continue through provenance, mission orchestration, knowledge, research, validation, editorial, application, and autonomous-engineering workstreams tracked by issues #6 through #13.
4. Keep GitHub issues, project state, ADRs, architecture, and conversation records synchronized with implementation progress.

## Issue maintenance policy

- GitHub issues are the operational backlog for substantive SanatanaAI work.
- New requirements, defects, architectural work, validation work, and follow-up work should receive explicit GitHub issue records when not already represented.
- Meaningful issues should state objective, scope, constraints, dependencies, and acceptance criteria.
- Update issue scope and acceptance criteria when requirements change.
- Link implementation PRs to relevant issues.
- Close issues only after implementation, validation, documentation, and required review gates are complete.
- Record blockers in GitHub issue state or comments.
- Split issues when scope becomes independently executable.
- Avoid duplicate issues for the same requirement.
- Conversation records remain mandatory under `governance/conversations/`.
- Architectural decisions require ADRs.
- Requirement changes require requirements documentation updates.

## Constraints

- Avoid paid infrastructure unless explicitly approved.
- Prefer open-source tooling.
- Do not commit secrets.
- Do not bypass validation gates.
- Do not make substantive changes directly on `main`.
- Do not create additional development branches unless explicitly required.

## Branch state

Genuine project branches:

- `main`
- `foundation/phase-0`
- `foundation/orchestration-core`
- `feature/checkpoint-recovery`

Other similarly named branches are accidental historical artifacts from earlier connector failures. The current GitHub integration does not expose branch deletion, so they are not being mutated or represented as development branches.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, current PR/CI state, GitHub issues, and conversation records.
