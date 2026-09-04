# SanatanaAI Architecture

## Architectural objective

Build a provenance-first, autonomous knowledge-engineering platform. The system must not depend on an LLM's latent memory as its knowledge database.

## System model

```text
User / API
   |
   v
Mission & Query Orchestration
   |
   +--> Planning / Delegation
   |
   +--> Specialized Micro-Agents
   |       +--> Research
   |       +--> Knowledge
   |       +--> Validation
   |       +--> Editorial
   |       +--> Engineering
   |
   v
Structured Artifacts
   |
   +--> Evidence / Provenance Store
   +--> Knowledge Store
   +--> Mission / Checkpoint Store
   |
   v
Validated Output
   |
   +--> Real-time Q&A
   +--> Encyclopedia
   +--> Web / Android
```

## Agent architecture

Agents are specialized units with explicit contracts. A contract defines identity, version, responsibility, inputs, outputs, permissions, validation rules, failure behavior, and provenance requirements.

Critical communication uses structured artifacts. Free-form model output is not treated as authoritative state.

## Orchestration execution boundary

The orchestration layer owns task lifecycle and checkpoint sequencing. Agent implementations sit behind an `AgentExecutor` protocol. This keeps orchestration independent of OpenAI or another provider and permits deterministic test doubles.

Execution flow:

```text
READY task
   |
   v
Validate task/request identity
   |
   v
Persist RUNNING checkpoint
   |
   v
Transition task to RUNNING
   |
   v
AgentExecutor
   |
   +--> exception/invalid result --> Persist FAILED checkpoint -> FAILED
   |
   +--> completed --> Persist COMPLETED checkpoint -> COMPLETED
   |
   +--> other status --> Persist BLOCKED checkpoint -> BLOCKED
```

The durable checkpoint is the recovery boundary. Task state must not advance beyond the last successfully persisted checkpoint. If terminal checkpoint persistence fails, the task remains `running` and the durable `running` checkpoint remains authoritative for recovery. If execution is interrupted before a terminal checkpoint is committed, recovery treats the task as incomplete rather than inventing a terminal result.

The execution service does not publish knowledge. It returns a typed `AgentResult`; downstream validators remain responsible for accepting or rejecting artifacts.

## Execution controls

Retry, timeout, and cancellation are explicit policy controls rather than implicit executor behavior.

- Retry is allowed only for failures explicitly classified as `RetryableAgentError`.
- `max_attempts` is bounded and explicit.
- Timeout is an attempt-scoped deadline exposed through `ExecutionContext.check()`.
- Cancellation uses a thread-safe `CancellationToken` and is cooperative.
- Timeout or cancellation control requires an executor implementing `execute_with_context`.
- Legacy executors remain valid only when no cooperative timeout or cancellation is requested.
- Timeout and cancellation are not retried implicitly.

The platform does not claim to safely kill arbitrary Python execution. Hard process-level isolation belongs to a future worker runtime if production requirements demand it. See ADR-0004.

## Checkpoint persistence and recovery

Checkpoint persistence is storage-neutral. The foundation provides an in-memory implementation for deterministic tests and a transactional SQLite reference adapter for durable local persistence.

Checkpoint invariants:

- checkpoint IDs are immutable and unique within the persistence scope
- identical replays are idempotent
- conflicting reuse of an ID fails closed
- checkpoints are append-only snapshots
- latest state is selected by UTC creation time with a deterministic ID tie-breaker
- each persistent save is atomic
- missing, corrupt, or ambiguous recovery state fails closed
- retention must never remove the checkpoint required for recovery before a replacement is durably committed

The persistent adapter is a storage implementation detail. PostgreSQL or another durable backend may replace SQLite without changing the orchestration contract. See ADR-0002 for the complete transaction, recovery, retention, and versioning decision.

## Evidence and provenance pipeline

The evidence model is versioned independently from runtime implementation. Version `1.0` currently defines source, passage, claim, evidence-reference, processing-record, and provenance-record contracts under `schemas/`.

The intended chain is:

```text
Source
  -> Text / Manuscript
  -> Passage
  -> Claim
  -> Evidence Reference
  -> Provenance / Processing History
```

Evidence contracts require stable identifiers and explicit metadata. Claims carry an evidence class and provenance identifier. Evidence references connect a claim to an addressable passage. Processing records preserve the operation, responsible agent, inputs, outputs, and timestamp needed to reproduce transformations. Provenance validation fails closed when identity, source linkage, evidence classification, processing history, or schema version is invalid.

Original-language text, transliteration, and translation remain separate representations. Competing translations and interpretations are retained as distinct evidence artifacts. AI synthesis remains explicitly classified as synthesis and never becomes primary textual evidence.

## Execution model

Real-time and batch execution use the same orchestration primitives.

Real-time policy:
- minimize latency
- use bounded research depth
- prioritize relevant evidence
- fail closed when evidence is insufficient

Batch policy:
- maximize safe parallelism
- checkpoint every critical stage
- retry transient failures
- support resume without repeating valid work
- optimize throughput and cost

## Knowledge model

```text
Source
  -> Text / Manuscript
  -> Passage
  -> Claim
  -> Entity / Relationship
  -> Article
```

Every substantive claim retains provenance to supporting evidence.

Evidence classes remain explicit:

1. Primary textual evidence
2. Traditional interpretation
3. Scholarly interpretation
4. Historical inference
5. AI synthesis
6. Uncertainty

Contradictions and competing interpretations are represented rather than silently resolved.

## Core data boundaries

- Source: bibliographic and acquisition identity.
- Text/Manuscript: textual work or manuscript representation.
- Passage: addressable evidence segment.
- Claim: atomic knowledge assertion.
- Entity: identifiable person, place, text, school, concept, event, practice, or other domain object.
- Relationship: typed connection between entities.
- Article: editorial representation derived from validated knowledge artifacts.
- Provenance: immutable or versioned link from assertion to evidence and processing history.

## Governance boundaries

No agent may publish directly to the public knowledge layer without validation. No article may be treated as evidence. AI synthesis must remain distinguishable from source evidence.

## Technology direction

Baseline technologies are selected for portability and open-source compatibility:

- Python and FastAPI for backend services.
- OpenAI APIs and agent capabilities as the intelligence layer.
- PostgreSQL-compatible persistence, with SQLite where appropriate for local development.
- pgvector or equivalent open-source retrieval where required.
- React and TypeScript for web.
- Kotlin for Android.
- Docker/dev containers and GitHub Codespaces for reproducible development.
- GitHub Actions for CI/CD.
- JSON Schema and OpenAPI for machine-readable contracts.

Technology choices remain subject to ADR review and should avoid unnecessary infrastructure.

## Security model

Secrets are supplied through approved secret-management mechanisms and environment variables. Secrets must never appear in source, artifacts, logs, issues, PRs, or conversation records.

## Delivery model

```text
Requirement
 -> Analysis
 -> Architecture
 -> Plan
 -> Branch
 -> Implementation
 -> Tests
 -> Security
 -> Documentation
 -> Pull Request
 -> CI
 -> Review
 -> Gate
 -> Merge
 -> Release
```

`main` is protected by process and, where repository plan capabilities permit, native GitHub branch/ruleset controls.
