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
- Active implementation branch: `foundation/orchestration-core`
- Repository visibility: private
- Open PR #1: draft, foundation integration into `main`
- Open PR #2: draft, orchestration-core integration into `foundation/phase-0`
- Conversation records exist under `governance/conversations/`

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
- Agent registry loading and validation
- Storage-neutral execution service boundary
- Unit tests for checkpoint, schema, registry, task lifecycle, and execution behavior
- CI validation for JSON, foundation files, backend tests, and secret patterns

## Validation status

- CI run 22 passed for the corrected task-readiness head.
- CI runs 23 and 24 passed for the subsequent registry/conversation corrections.
- The execution-boundary increment is now on `foundation/orchestration-core` and requires its own fresh CI validation.
- PR #2 remains draft until the implementation is reviewed and its current head passes CI.

## Current work

1. Validate the execution-boundary increment in CI.
2. Review orchestration-core implementation for lifecycle, identity, failure, and checkpoint semantics.
3. Strengthen checkpoint/resume tests, including recovery from the latest valid checkpoint.
4. Add stronger formatting, typing, dependency, security, provenance, agent-contract, and documentation gates.
5. Resolve native branch/ruleset enforcement capability.
6. Complete and review Foundation Phase 0 before merge.

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

Other similarly named branches are accidental artifacts from earlier connector failures. The current GitHub integration does not expose branch deletion, so they are not being mutated or represented as development branches.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, current PR/CI state, and conversation records.
