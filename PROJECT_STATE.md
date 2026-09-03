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
- Dependency graph validation with multi-node cycle detection
- Agent registry loading and validation
- Storage-neutral execution service boundary
- Unit tests for checkpoint, schema, registry, task lifecycle, execution, and dependency-cycle behavior
- CI validation for JSON, foundation files, backend tests, and secret patterns

## Validation status

- CI runs 22, 23, 24, and 29 passed on earlier corrected heads.
- The current `foundation/orchestration-core` head includes the execution-boundary and dependency-cycle increments and requires fresh CI validation.
- PR #2 remains draft until the current implementation is reviewed and its current head passes CI.

## Current work

1. Obtain fresh CI validation for the current orchestration-core head.
2. Review orchestration-core lifecycle, identity, failure, dependency, and checkpoint semantics.
3. Define persistent checkpoint transaction and recovery semantics before production persistence.
4. Strengthen formatting, typing, dependency, security, provenance, agent-contract, documentation, and regression gates.
5. Resolve native branch/ruleset enforcement capability.
6. Complete and review Foundation Phase 0 before integration.

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

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, current PR/CI state, and conversation records.
