# ADR-0004: Cooperative Execution Controls

Status: Accepted
Date: 2026-09-04

## Context

SanatanaAI agents require explicit retry, timeout, and cancellation behavior. Silent retries can duplicate side effects. Hard thread termination is unsafe for arbitrary agent code. Execution control must remain deterministic and compatible with provider-neutral agent executors.

## Problem

The runtime needs a safe control model that bounds retries, exposes deadlines, supports cancellation, and does not pretend that an arbitrary synchronous function is safely killable.

## Options

1. Retry every exception and use thread-based hard timeouts.
2. Use process termination for every timeout and cancellation.
3. Use explicit retry policy plus cooperative execution context for timeout and cancellation.

## Decision

Use explicit `ExecutionPolicy` and cooperative `ExecutionContext` controls.

- Retry occurs only for `RetryableAgentError`.
- `max_attempts` is explicit and must be at least one.
- Timeout is an attempt-scoped deadline exposed through `ExecutionContext.check()`.
- Cancellation uses a thread-safe `CancellationToken` exposed through the execution context.
- When timeout or cancellation control is enabled, the executor must implement `execute_with_context` and explicitly cooperate with `context.check()`.
- Legacy executors remain supported only when no cooperative timeout or cancellation control is requested.
- Cancellation and timeout are not retried implicitly.
- Retry policy does not classify arbitrary exceptions as transient.

## Rationale

Thread termination does not safely unwind arbitrary Python code or external side effects. Process termination introduces isolation and lifecycle complexity that belongs in a later worker-execution architecture. Cooperative controls make the contract explicit and fail closed when an executor cannot honor the requested controls.

## Consequences

- Agents must explicitly opt into cooperative execution context support to receive timeout or cancellation controls.
- Timeout enforcement depends on the agent checking its context during execution. This limitation is explicit rather than hidden.
- A future isolated worker runtime may provide hard execution boundaries without changing the policy semantics.
- Retry remains deterministic and limited to explicitly classified transient failures.

## Validation

Tests cover transient retry, retry limits, non-retryable failures, timeout capability enforcement, cooperative timeout detection, cancellation before execution, cancellation during execution, and invalid policy values.

## Follow-up

Integrate execution controls into mission-level scheduling and checkpoint policy. Add isolated worker execution only if hard cancellation or hard timeout guarantees become a production requirement.
