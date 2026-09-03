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
- Conversation records exist under `governance/conversations/`

## Foundation completed in this increment

- Project README and repository map
- Project state and phased roadmap
- Architecture baseline
- ADR-0001 for multi-agent, provenance-first architecture
- Agent contract schema and registry rules
- Requirements governance
- Mission schema
- Provenance record schema
- Codespaces/devcontainer baseline
- Initial CI validation workflow

## Architecture baseline

SanatanaAI uses specialized micro-agents coordinated by a shared mission/task orchestration model. Real-time and batch execution share core orchestration primitives. Knowledge follows Source -> Text/Manuscript -> Passage -> Claim -> Entity/Relationship -> Article, with provenance required for substantive claims.

## Current work

Foundation Phase 0 is not complete. Remaining work:

1. Add executable backend/package scaffolding.
2. Add richer schema validation and contract tests.
3. Add mission/task and checkpoint implementation primitives.
4. Add branch/PR governance documentation and automation where supported.
5. Open and validate the foundation pull request.

## Constraints

- Avoid paid infrastructure unless explicitly approved.
- Prefer open-source tooling.
- Do not commit secrets.
- Do not bypass validation gates.
- Do not make substantive changes directly on `main`.

## Continuity

At the beginning of each substantive session, inspect this file, `ROADMAP.md`, `ARCHITECTURE.md`, active missions, ADRs, agent contracts, and current PR/CI state.
