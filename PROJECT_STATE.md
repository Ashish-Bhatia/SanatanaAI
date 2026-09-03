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
- Active implementation branch: `feature/agent-governance` (completed and merged; next implementation branch pending)
- Repository visibility: private
- PR #1: merged into `main` with merge commit `1bfa255511b1083562d1a0c4033507474c556f34`
- PR #2: merged into `foundation/phase-0`
- PR #14: merged into `main` with merge commit `56d975cfcdfc7425f5c0493dc39ec381702cdd31`
- PR #15: merged into `main` with merge commit `e7f03a59aeb57559fa163db607883cb12b25ee73`
- Issue #3: completed and closed through PR #14
- Issue #5: open, with core runtime governance merged; execution-control semantics remain
- Conversation records exist under `governance/conversations/`
- GitHub issues #4 through #13 remain the principal open Foundation and post-Foundation workstreams.

## Foundation completed

- Project README, state, roadmap, and architecture baseline
- ADR-0001 for multi-agent, provenance-first architecture
- ADR-0002 for storage-neutral checkpoint persistence and resumability
- ADR-0003 for runtime agent governance
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
- CI validation for JSON, foundation files, agent/artifact registries, backend tests, and secret patterns
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
- CI run 63 passed on main state commit `3ae48550b041c07855267ffb78195882e8e0bec1`.
- CI run 67 failed during an intermediate artifact-schema change; the failing test fixture was corrected.
- CI run 68 failed on an input/output artifact-type fixture mismatch; runtime governance was intentionally not weakened and the fixture was corrected in commit `5695d0316c90657fb2645094fcf059f930f041af`.
- CI run 69 passed on the corrected agent-governance head before final governance-log synchronization.
- CI run 70 passed on the final agent-governance head `7d3c240ae94d734cf2643c1014a4139c3bcc3332`.
- PR #15 was reviewed and merged into `main` with merge commit `e7f03a59aeb57559fa163db607883cb12b25ee73`.
- Main CI validation after PR #14 passed before the project-state synchronization commit.
- Issue #4 remains open because the broader quality-gate scope is not yet complete.

## Current work

1. Finish Issue #5 execution-control semantics for retry, timeout, cancellation, and richer failure policy.
2. Complete CI quality gates under issue #4 in parallel with feature delivery.
3. Validate and merge the Issue #5 execution-control increment before closing the issue.
4. Continue through provenance, mission orchestration, knowledge, research, validation, editorial, application, and autonomous-engineering workstreams tracked by issues #6 through #13.
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

Other similarly named branches are accidental historical artifacts from earlier connector failures. The current GitHub integration does not expose branch deletion, so they are not being mutated or represented as development branches.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, current PR/CI state, GitHub issues, and conversation records.
