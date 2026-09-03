# ADR-0003: Agent Runtime Governance

Status: Accepted
Date: 2026-09-04

## Context

SanatanaAI uses specialized micro-agents with explicit contracts. The registry already validates contract documents, but registration alone does not enforce those contracts at runtime. An agent must not execute with undeclared permissions or advance invalid structured artifacts into downstream stages.

## Problem

Runtime execution needs deterministic enforcement for agent identity, semantic contract versioning, permissions, structured artifact validation, provenance requirements, and artifact ownership while keeping provider-specific execution behind the existing `AgentExecutor` boundary.

## Options

1. Trust registry validation and rely on agent implementations to follow contracts.
2. Embed governance checks directly in each agent implementation.
3. Add a shared governance boundary that loads registered contracts and schemas, authorizes requests, validates artifacts, and wraps provider-neutral executors.

## Decision

Use a shared `AgentGovernance` boundary and `GovernedAgentExecutor` wrapper.

The governance layer:

- rejects unregistered agent IDs
- requires semantic-version-formatted agent contracts
- rejects requested permissions not declared by the contract
- validates input artifacts against registered JSON Schemas
- validates output artifacts against registered JSON Schemas
- rejects duplicate output artifact IDs
- requires output ownership to match the executing agent
- enforces provenance on outputs when the contract requires it
- keeps structured artifacts immutable through frozen value objects
- executes the provider-specific implementation only after request authorization
- returns output to the existing orchestration boundary only after governance validation

The artifact schema registry uses stable schema IDs mapped to repository schema files. Domain-specific schemas remain additive and replaceable. The current foundation registers a generic structured-artifact envelope; domain schemas will be introduced by the provenance and knowledge workstreams.

Contract validation remains the responsibility of the registry loader. Runtime governance consumes only validated registry entries.

## Rationale

A single shared enforcement boundary prevents policy duplication across agents and keeps provider-specific intelligence separate from platform governance. Deterministic checks are testable without invoking an LLM or external service.

The wrapper pattern preserves the existing `AgentExecutor` protocol, so orchestration does not need to know how an agent is implemented or which intelligence provider it uses.

## Consequences

- An agent must be registered before execution.
- Permissions are capability declarations, not informal conventions.
- Structured artifacts become explicit inter-agent contracts.
- Invalid or unowned artifacts fail closed before downstream execution.
- Provenance requirements are enforceable at runtime.
- Contract versions remain part of the runtime identity and future compatibility policy.
- Retry, timeout, cancellation, and richer failure policy remain execution-control concerns to be completed in the orchestration workstream.
- Domain artifact schemas will grow as provenance and knowledge models are implemented.

## Validation

Unit tests cover registry-backed governance loading, unregistered agents, undeclared permissions, valid input artifacts, unregistered schemas, invalid output artifacts, ownership violations, provenance requirements, duplicate artifact IDs, and successful governed execution.

## Follow-up

Extend the governance layer with explicit contract compatibility rules, artifact capability/ownership policies across mission stages, and execution-control semantics for retry, timeout, and cancellation. Keep those additions behind explicit contracts and tests.
