# SanatanaAI

SanatanaAI is an autonomous, agentic knowledge-engineering platform for a provenance-first encyclopedia and research system covering Sanatana Dharma.

## Product scope

- Provenance-first encyclopedia
- Real-time research and Q&A
- Batch research and encyclopedia generation
- Web application
- Android application
- Autonomous multi-agent knowledge engineering

## Engineering principles

- GitHub is the system of record.
- Specialized micro-agents perform domain tasks.
- Critical agent communication uses versioned contracts and structured artifacts.
- Every substantive knowledge claim requires provenance.
- Evidence, interpretation, inference, synthesis, and uncertainty remain distinguishable.
- Real-time and batch execution share the same orchestration model.
- Long-running work is checkpointed and resumable.
- Changes flow through branches, pull requests, CI, review, and validation gates.
- Documentation is part of implementation.

## Repository map

- `apps/` user-facing applications
- `backend/` APIs, orchestration, agents, knowledge, provenance, validation, retrieval, storage
- `agents/` agent registry, contracts, prompts, and policies
- `data/` canonical knowledge-engineering artifacts
- `missions/` mission and task state
- `governance/` requirements, ADRs, policies, and conversation records
- `docs/` supporting technical documentation
- `tests/` automated tests
- `scripts/` development and validation automation

See `PROJECT_STATE.md`, `ROADMAP.md`, and `ARCHITECTURE.md` before starting substantive work.
