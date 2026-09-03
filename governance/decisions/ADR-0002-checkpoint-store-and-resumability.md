# ADR-0002: Checkpoint Store and Resumability Boundary

Status: Accepted
Date: 2026-09-04

## Context

SanatanaAI executes long-running missions through multiple agents. Execution must survive process interruption and support deterministic resumption from the last valid checkpoint. The orchestration layer must not depend on a particular storage engine.

## Problem

Checkpoint state needs a stable contract for saving and retrieving the latest valid task checkpoint while keeping persistence implementation replaceable.

## Options

1. Persist checkpoints directly inside the orchestration implementation.
2. Use a storage-neutral checkpoint interface with an in-memory implementation for foundation testing and replaceable persistent adapters later.
3. Store only mutable task state without checkpoint history.

## Decision

Use a storage-neutral `CheckpointStore` boundary. The foundation implementation provides `InMemoryCheckpointStore` for deterministic tests. Checkpoints are immutable value objects identified by `checkpoint_id`. Re-saving the same checkpoint is idempotent. Reusing an identifier with different content fails closed. The store tracks the latest checkpoint for each mission/task pair.

## Rationale

This separates orchestration semantics from persistence technology, supports resumability, enables deterministic unit tests, and leaves the production persistence adapter reversible until storage requirements are established.

## Consequences

- Orchestration code depends on the checkpoint contract rather than a database.
- Production storage requires a later adapter and persistence design decision.
- Checkpoint identifiers must remain stable and unique within the persistence scope.
- Recovery logic must treat missing checkpoints as an explicit state rather than inventing prior execution state.

## Validation

Checkpoint round-trip, idempotent save, latest-checkpoint selection, conflicting identifier rejection, and empty-state validation are covered by unit tests.

## Follow-up

Define persistent checkpoint storage, transactional semantics, retention, and recovery policy before production execution infrastructure is introduced.
