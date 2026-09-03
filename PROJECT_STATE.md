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
- Repository visibility: private
- Open PR: #1, draft
- Conversation records exist under `governance/conversations/`

## Foundation completed

- Project README, state, roadmap, and architecture baseline
- ADR-0001 for multi-agent, provenance-first architecture
- Agent contract schema and registry governance
- Mission schema and provenance record schema
- Reproducible Codespaces/devcontainer baseline
- Python backend package scaffold
- Agent request/result contracts
- Mission checkpoint state primitive
- Executable JSON Schema validation package
- Mission task contract schema
- Unit tests for checkpoint and schema validation
- CI validation for JSON, foundation files, backend tests, and secret patterns

## Validation status

The CI run for the previous head passed. The current head adds schema-validation changes and requires a fresh CI run before this increment is considered validated.

## Current work

1. Validate the current PR head in CI.
2. Add registry entries and registry validation.
3. Add mission/task dependency and checkpoint primitives.
4. Add stronger formatting, typing, dependency, security, and documentation gates.
5. Resolve native branch/ruleset enforcement capability.
6. Complete and review Foundation Phase 0 before merge.

## Constraints

- Avoid paid infrastructure unless explicitly approved.
- Prefer open-source tooling.
- Do not commit secrets.
- Do not bypass validation gates.
- Do not make substantive changes directly on `main`.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, current PR/CI state, and conversation records.
