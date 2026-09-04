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
- Active implementation branch: `feature/ci-quality-gates`
- Repository visibility: private
- PR #1: merged into `main` with merge commit `1bfa255511b1083562d1a0c4033507474c556f34`
- PR #2: merged into `foundation/phase-0`
- PR #14: merged into `main` with merge commit `56d975cfcdfc7425f5c0493dc39ec381702cdd31`
- PR #15: merged into `main` with merge commit `e7f03a59aeb57559fa163db607883cb12b25ee73`
- PR #16: merged into `main` with merge commit `f57332adc1642647ca767ac4b02c3809060dce9e`
- Issue #3: completed and closed through PR #14
- Issue #5: completed and closed after PR #15 and PR #16
- Issue #4: open, CI quality-gate expansion in progress
- Conversation records exist under `governance/conversations/`
- GitHub issues #6 through #13 remain the principal open post-Foundation workstreams.

## Foundation completed

- Project README, state, roadmap, and architecture baseline
- ADR-0001 for multi-agent, provenance-first architecture
- ADR-0002 for storage-neutral checkpoint persistence and resumability
- ADR-0003 for runtime agent governance
- ADR-0004 for cooperative execution controls
- Agent contract schema and registry governance
- Mission schema and provenance record schema
- Reproducible Codespaces/devcontainer baseline
- Python backend package scaffold
- Agent request/result contracts
- Structured artifact contract with explicit artifact type
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
- Runtime agent registration, permission, artifact schema, declared artifact type, ownership, provenance, and duplicate-artifact enforcement primitives
- Artifact schema registry
- Cooperative retry, timeout, and cancellation control primitives
- CI validation for JSON, foundation files, agent/artifact registries, backend tests, and secret patterns
- GitHub issue backlog for principal engineering workstreams

## Validation status

- Earlier Foundation and orchestration validation runs passed through CI run 75 and PR #16 merge.
- CI run #129 failed on the PR #17 merge ref, not the latest feature-branch commit. The merge ref contained two Ruff I001 import-order violations in execution-control and schema-validation tests.
- CI run #129 passed JSON validation, dependency installation, required-file validation, agent/artifact registry validation, ADR structure validation, and Ruff formatting before failing Ruff linting.
- The two import-order failures were corrected on `feature/ci-quality-gates` in commits `f86b9a57ff311cc48228f0f41a4b605a187e9f3d` and `88e85401368ca3e9860ac470befa78db672ef53a`.
- The latest branch head is `88e85401368ca3e9860ac470befa78db672ef53a`, with both corrected import groups committed.
- Fresh PR CI for the latest branch head has not yet been observed. CI therefore remains unverified.
- Issue #4 remains open until the expanded quality gates pass on the current PR head and the PR review/merge gates complete.

## Current work

1. Complete the CI quality-gate expansion under issue #4.
2. Validate and merge the CI gate increment.
3. Implement execution provenance and validation-outcome persistence under issue #6.
4. Continue through mission orchestration, knowledge, research, validation, editorial, application, and autonomous-engineering workstreams tracked by issues #7 through #13.
5. Keep GitHub issues, project state, ADRs, architecture, and conversation records synchronized with implementation progress.

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
- `feature/agent-governance`
- `feature/execution-controls`
- `feature/ci-quality-gates`

Other similarly named branches are accidental historical artifacts from earlier connector failures. The current GitHub integration does not expose branch deletion, so they are not being mutated or represented as development branches.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, current PR/CI state, GitHub issues, and conversation records.
