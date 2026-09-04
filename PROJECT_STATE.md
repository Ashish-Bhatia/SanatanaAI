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
- PR #1, #14, #15, and #16 are merged into `main`.
- PR #17 is the single active pull request and is the current CI gate.
- Issues #3 and #5 are completed. Issue #4 remains open until PR #17 passes and merges. Issues #6 through #13 are the next product workstreams.

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

## Current CI gate

PR #17, `ci: strengthen Foundation quality gates`, adds formatting, linting, mypy, dependency auditing, package build, ADR structure validation, existing schema/registry/tests, and secret scanning.

The latest observed CI run #145 tested PR merge ref `b815eda2a485522cb35ea779019736ea98504243` for head `0c5f9220dc5db3258eaf7d99255ee04f7a00a92c`.

Observed results:
- JSON validation: passed
- dependency installation: passed
- required project files: passed
- agent/artifact registry validation: passed
- ADR structure validation: passed
- Ruff formatting: passed
- Ruff linting: passed
- mypy: passed
- backend tests: failed, 2 failed and 55 passed
- dependency audit, package build, and secret scan were skipped because CI fails closed

Root cause of the two failing tests: `ExecutionPolicy` did not expose the `cancellation_enabled` field expected by the existing cancellation contract tests.

Corrective commit on `feature/ci-quality-gates`:
- `1e015f189ce99402e6a406e7c7a51d513ef8a3bb`, `fix: enforce cancellation policy in execution control`

The correction adds explicit cancellation policy state, makes cancellation require contextual execution, and creates an execution token when cancellation is enabled without an injected token.

Fresh CI for the corrected head is required. Do not bypass the failing test gate.

## Current work

1. Validate the cancellation fix through fresh PR #17 CI.
2. If green, complete review and merge PR #17, then close Issue #4.
3. Immediately proceed with Issue #6, execution provenance and validation-outcome persistence.
4. Continue through mission orchestration, knowledge, research, validation, editorial, applications, and autonomous engineering.

## Issue maintenance policy

GitHub Issues are the operational backlog. Maintain existing issues rather than creating duplicates. Update scope, acceptance criteria, blockers, implementation links, and completion state as work progresses. Close only after implementation, validation, documentation, review, and merge gates pass.

Substantive conversations and decisions are recorded under `governance/conversations/`. Architectural decisions require ADRs. Requirement changes require requirements documentation updates.

## Constraints

- No substantive changes directly on `main`.
- No unnecessary branches.
- No paid infrastructure without approval.
- Prefer free/open-source tooling.
- Never bypass CI gates.
- Never commit secrets.

## Branch state

Genuine project branches currently used by the project:

- `main`
- `foundation/phase-0`
- `foundation/orchestration-core`
- `feature/checkpoint-recovery`
- `feature/agent-governance`
- `feature/execution-controls`
- `feature/ci-quality-gates`

Other similarly named branches are historical artifacts from earlier connector failures. Branch deletion is not exposed through the current integration, so they are not being mutated.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, ADRs, agent contracts, current PR/CI state, GitHub issues, and conversation records before changing project state.
