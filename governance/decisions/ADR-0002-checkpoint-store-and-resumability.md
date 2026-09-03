# ADR-0002: Checkpoint Store and Resumability Boundary

Status: Accepted
Date: 2026-09-04

## Context

SanatanaAI executes long-running missions through multiple agents. Execution must survive process interruption and support deterministic resumption from the last valid checkpoint. The orchestration layer must not depend on a particular storage engine.

## Problem

Checkpoint state needs a stable contract for saving and retrieving the latest valid task checkpoint while keeping persistence implementation replaceable. Persistence must also define idempotency, atomicity, crash recovery, corruption handling, concurrency behavior, and retention boundaries.

## Options

1. Persist checkpoints directly inside the orchestration implementation.
2. Use a storage-neutral checkpoint interface with an in-memory implementation for foundation testing and replaceable persistent adapters.
3. Store only mutable task state without checkpoint history.

## Decision

Use a storage-neutral `CheckpointStore` boundary. The foundation provides `InMemoryCheckpointStore` for deterministic tests and `SQLiteCheckpointStore` as the first durable reference adapter. Production storage remains replaceable without changing orchestration semantics.

Checkpoints are immutable value objects identified by `checkpoint_id`. Re-saving identical checkpoint content is idempotent. Reusing an identifier with different content fails closed. The latest checkpoint for a mission/task pair is selected by UTC `created_at`, with `checkpoint_id` as a deterministic tie-breaker.

Task-state transitions must never advance beyond the last successfully persisted checkpoint. The orchestration sequence is therefore:

1. Persist the checkpoint representing the intended next durable state.
2. Commit the persistence transaction.
3. Advance the in-memory task state to the same state.
4. Invoke the next execution stage only after the durable checkpoint exists.

A process interruption before a terminal checkpoint leaves the latest durable state at `running`. Recovery must treat that task as incomplete and retry or otherwise resolve it according to mission policy. A terminal `completed`, `failed`, or `blocked` checkpoint is the durable terminal outcome.

Missing checkpoints, corrupt records, invalid timestamps, conflicting checkpoint identities, and ambiguous recovery state fail closed. The system must not invent prior execution state.

Persistent adapters must make each checkpoint save atomic. A failed write must leave no partial checkpoint visible. The reference SQLite adapter uses a database transaction for each save and preserves the checkpoint contract across process reopen.

## Rationale

This separates orchestration semantics from persistence technology, supports resumability, enables deterministic unit tests, and establishes a durable reference implementation without committing the platform to SQLite for production scale.

Persist-before-transition makes the durable checkpoint the recovery boundary. A crash after a successful checkpoint but before the corresponding in-memory transition is safe because recovery reconstructs state from the durable checkpoint. A crash before the checkpoint commits leaves the previous checkpoint authoritative.

## Consequences

- Orchestration code depends on the checkpoint contract rather than a database.
- SQLite provides a portable durable reference adapter for development and small deployments.
- A PostgreSQL or other production adapter may replace SQLite without changing the orchestration contract.
- Checkpoint identifiers must remain stable and unique within the persistence scope.
- Checkpoint records are append-only and immutable.
- Versioning is represented by successive immutable checkpoint IDs rather than mutable rows.
- Retention is an explicit storage-policy concern. Automatic pruning is not performed by the foundation adapter. Any future pruning policy must preserve the latest checkpoint required for recovery and must not delete a checkpoint before its replacement is durably committed.
- Concurrent retries using the same checkpoint ID are safe only when their checkpoint content is identical. Conflicting content is rejected.
- Recovery must surface missing or ambiguous state rather than guessing.

## Validation

The checkpoint test suite covers round-trip persistence, persistence across reopen, idempotent save, conflicting identifier rejection, deterministic latest-checkpoint selection, timezone validation, transaction rollback under injected database failure, and execution recovery when running or terminal checkpoint persistence fails.

## Follow-up

Define a production-scale persistence adapter and explicit mission-level recovery policy when the execution infrastructure requires it. The production adapter must preserve the transaction, idempotency, immutability, recovery, and retention invariants defined here.
