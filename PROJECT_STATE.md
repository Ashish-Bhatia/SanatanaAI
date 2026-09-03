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
- Active implementation branch: `foundation/phase-0`
- Repository visibility: private
- Open PR #1: draft, foundation integration into `main`
- PR #2: merged into `foundation/phase-0`
- Conversation records exist under `governance/conversations/`
- GitHub issues #3 through #13 track the principal Foundation and post-Foundation workstreams.

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
- Unit tests for checkpoint, schema, registry, task lifecycle, execution, and dependency-cycle behavior
- CI validation for JSON, foundation files, backend tests, and secret patterns
- GitHub issue backlog for principal engineering workstreams

## Validation status

- CI runs 22, 23, 24, and 29 passed on earlier corrected heads.
- CI run 50 passed on the orchestration execution increment.
- CI run 51 passed on the validated orchestration-core head before PR #2 integration.
- PR #2 was reviewed and merged into `foundation/phase-0`.
- CI quality-gate strengthening has started in commit `e4c8bf9ea301a3123078bddf861a66c1b4e54409`.
- The strengthened CI now validates ADR-0002 and the registered agent contracts.
- Fresh CI validation against the current Foundation integration head is required before PR #1 can be merged into `main`.

## Current work

1. Obtain fresh CI validation for PR #1's integrated Foundation head.
2. Complete final review of Foundation Phase 0 and merge only after required gates pass.
3. Maintain GitHub issues as the operational backlog and keep issue state synchronized with repository progress.
4. Implement persistent checkpoint transaction and recovery semantics under issue #3.
5. Complete CI quality gates under issue #4.
6. Implement agent contract, permission, and artifact governance under issue #5.
7. Continue through provenance, orchestration, knowledge, research, validation, editorial, application, and autonomous-engineering workstreams tracked by issues #6 through #13.

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

Other similarly named branches are accidental historical artifacts from earlier connector failures. The current GitHub integration does not expose branch deletion, so they are not being mutated or represented as development branches.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, current PR/CI state, GitHub issues, and conversation records.
