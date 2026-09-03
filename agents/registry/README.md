# Agent Registry

Every production agent must have a registry entry and a validated contract.

## Required identity

- Stable agent ID
- Semantic contract version
- Category
- Responsibility
- Owner subsystem
- Input artifacts
- Output artifacts
- Permissions
- Validators
- Failure and retry behavior
- Provenance requirements

## Rules

1. One agent has one primary responsibility.
2. Agents must not silently expand scope.
3. Agents must not publish unvalidated knowledge.
4. Agent contracts are versioned.
5. Contract-breaking changes require an ADR and migration plan.
6. Agent output is untrusted until the declared validators accept it.
