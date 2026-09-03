# Conversation 009

Date: 2026-09-04

## Objective
Begin Issue #5, runtime enforcement of agent contracts, permissions, and structured artifact governance.

## Requirements
- Keep specialized micro-agents behind explicit contracts.
- Reject unregistered agents and undeclared permissions.
- Validate structured input and output artifacts against registered schemas.
- Enforce artifact ownership and immutability boundaries.
- Enforce provenance when the agent contract requires it.
- Preserve provider-neutral execution boundaries.
- Keep retry, timeout, and cancellation semantics explicit and separately testable.
- Update governance documentation, CI, tests, and project state in the same cycle.

## Decisions
- Add `AgentGovernance` as a shared deterministic runtime policy boundary.
- Add `GovernedAgentExecutor` as a wrapper around the provider-neutral executor protocol.
- Represent inter-agent data as immutable `StructuredArtifact` values.
- Add a stable artifact schema registry keyed by schema IDs and repository schema paths.
- Preserve the existing agent contract schema and add enforcement without coupling orchestration to an AI provider.
- Keep the current foundation artifact schema generic; domain-specific artifact schemas will be introduced by provenance and knowledge workstreams.
- Defer retry, timeout, and cancellation policy implementation to the execution-control portion of the orchestration workstream rather than inventing overlapping semantics here.

## Actions
- Created `feature/agent-governance` from the validated main baseline.
- Added structured artifact and extended agent request/result contracts.
- Added runtime contract, permission, schema, ownership, provenance, and duplicate-artifact enforcement.
- Added the artifact schema registry and registered structured-artifact schema.
- Added governance regression tests.
- Added ADR-0003 for runtime agent governance.
- Strengthened CI to validate ADR-0003 and the artifact schema registry.

## Validation
- Main CI run #63 passed on the checkpoint-recovery completion baseline before this branch was created.
- PR validation for the agent-governance branch is pending.

## Unresolved
- Full execution-control semantics for retry, timeout, cancellation, and richer failure policies remain open.
- Domain-specific artifact schemas remain open for provenance and knowledge phases.
- Issue #4 still requires broader formatting, typing, dependency/security, provenance, documentation, regression/integration, and build gates.

## Resulting changes
- Runtime governance is now a reusable enforcement boundary rather than a convention embedded in individual agents.
- Invalid or unauthorized agent execution fails closed before downstream stages receive governed artifacts.
