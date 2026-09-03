# ADR-0001: Multi-Agent Provenance-First Architecture

## Status

Accepted

## Date

2026-09-04

## Context

SanatanaAI must support research, encyclopedia generation, real-time Q&A, batch processing, and autonomous engineering. The system must preserve evidence and remain recoverable across ChatGPT sessions.

## Problem

A monolithic agent or an LLM-centric knowledge store would make responsibilities unclear, weaken validation boundaries, reduce reproducibility, and increase the risk of unsupported claims.

## Options

1. Monolithic agent with an LLM-managed knowledge base.
2. Service-oriented application with limited agent specialization.
3. Multi-agent knowledge-engineering platform with explicit contracts, provenance, and centralized orchestration.

## Decision

Choose option 3.

SanatanaAI will use specialized micro-agents coordinated by a mission/task orchestration layer. Critical agent communication will use versioned structured contracts. Knowledge will be represented as provenance-linked artifacts from source through passage, claim, entity/relationship, and article.

The LLM is an inference component. It is not the authoritative knowledge database.

## Rationale

- Separates responsibilities and validation boundaries.
- Supports parallel and resumable batch work.
- Supports low-latency real-time execution using the same core orchestration model.
- Preserves evidence and processing provenance.
- Enables independent testing of agent behavior.
- Reduces project drift by keeping state in repository artifacts.
- Allows agent implementations to evolve without changing domain contracts.

## Consequences

Positive:
- Stronger provenance and auditability.
- Better fault isolation.
- Explicit permissions and validation.
- Reusable orchestration primitives.

Negative:
- More initial design and contract work.
- More components to test and observe.
- Requires disciplined versioning and migration of schemas.

## Rejected alternatives

The monolithic-agent approach is rejected because it conflicts with the required micro-agent model and creates a weak boundary between research, knowledge construction, validation, and editorial generation.

## Follow-up

Define agent contract schemas, mission/task schemas, provenance schemas, and CI validation in Foundation Phase 0.

## Validation

This decision is validated through the Foundation architecture, registered agent contracts, structured artifact schemas, mission/task schemas, provenance schema, runtime governance tests, checkpoint/recovery tests, and CI quality gates. Future architectural changes must preserve the multi-agent boundary, provider-neutral orchestration, and provenance-first knowledge model or supersede this ADR through a new documented decision.
