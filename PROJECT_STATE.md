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
- Initial conversation record exists under `governance/conversations/`

## Established direction

SanatanaAI will use a multi-agent architecture with specialized micro-agents, a shared orchestration model for real-time and batch work, provenance-first knowledge artifacts, automated validation, and PR-based delivery.

## Current work

Foundation Phase 0 establishes:

1. Project governance
2. Architecture baseline
3. ADR process
4. Agent contract baseline
5. Knowledge/provenance model
6. Mission/task state model
7. CI foundation
8. Development environment conventions

## Next gates

- Complete foundation documentation and schemas.
- Add executable project scaffolding.
- Add CI validation for schemas, documentation, formatting, tests, and security.
- Open a pull request from `foundation/phase-0` to `main`.
- Review CI results before merge.

## Constraints

- Avoid paid infrastructure unless explicitly approved.
- Prefer open-source tooling.
- Do not commit secrets.
- Do not bypass validation gates.
- Do not make substantive changes directly on `main`.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, and current PR/CI state.
