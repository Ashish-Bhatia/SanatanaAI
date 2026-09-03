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
RUNNING + checkpoint
   |
   v
AgentExecutor
   |
   +--> exception --> FAILED + checkpoint
   |
   +--> completed --> COMPLETED + checkpoint
   |
   +--> failed --> FAILED + checkpoint
   |
   +--> other status --> BLOCKED + checkpoint
```

The execution service does not publish knowledge. It returns a typed `AgentResult`; downstream validators remain responsible for accepting or rejecting artifacts.

Checkpoint persistence is storage-neutral. The foundation uses an in-memory implementation for deterministic tests. Persistent storage requires a later adapter and transaction/recovery design.

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
