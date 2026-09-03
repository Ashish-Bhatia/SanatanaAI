# Conversation Record: 2026-09-04-001

## Project
SanatanaAI

## Repository
Ashish-Bhatia/SanatanaAI

## Date
2026-09-04

## Participants
- User: Ashish Bhatia
- Assistant: ChatGPT

## Purpose
Establish SanatanaAI as a fully automated, agentic AI encyclopedia and research platform for Sanatana Dharma.

## User Requirements
- SanatanaAI is an agentic AI system for an encyclopedia of Sanatana Dharma.
- Every activity/task should be performed by micro-agents. Avoid single-agent/manual workflows.
- Resources available: GitHub repository, GitHub Codespaces, OpenAI Platform.
- Everything should be automated, including real-time and batch execution.
- Development must follow software engineering best practices, CI/CD, and gated check-in/check-out.
- Development should be performed through ChatGPT GitHub integration with no manual development activity.
- The end product should be readied through automation.
- Frontends: website/webapp and Android application.
- Additional development resources should be freeware/open-source and usable through GitHub/Codespaces.
- Project continuity must not depend on conversation context. Documentation must run in parallel with development.
- Every important decision and conversation/discussion should be logged into the repository.
- ChatGPT Project name: SanatanaAI.

## Repository State Verified
- Repository: Ashish-Bhatia/SanatanaAI
- Visibility: private
- Default branch: main
- Repository currently at starting/foundation stage.

## Architectural Direction Established
- Treat SanatanaAI as a software product and autonomous knowledge-engineering platform, not as a single chatbot.
- Use a multi-agent architecture with specialized micro-agents.
- Use an orchestration layer for mission/task decomposition and execution.
- Support both real-time and batch execution using the same underlying agent/task engine.
- Use source -> text/manuscript -> passage -> claim -> entity/relationship -> article as a provenance-first knowledge model.
- Separate textual facts, traditional interpretations, scholarly interpretations, and AI synthesis.
- Require provenance for knowledge claims.
- Store project memory in GitHub rather than relying on ChatGPT conversation memory.
- Use GitHub as the system of record.
- Use branches, PRs, CI, validation gates, and controlled merges.
- Use Codespaces as the reproducible development environment.
- Use OpenAI as the intelligence layer while retaining orchestration ownership within SanatanaAI.
- Build the knowledge/research platform before prioritizing polished frontend work.

## Proposed Agent Categories
- Orchestration: mission, planning, delegation.
- Research: source discovery, source acquisition, extraction, translation, claim extraction, evidence, cross-reference.
- Knowledge: ontology, entity, relationship, chronology, geography, terminology.
- Validation: citation, source quality, contradiction, provenance, hallucination safeguards.
- Editorial: article, encyclopedia, summary, multilingual.
- Engineering: code, test, security, documentation, release.

## Proposed Governance Rules
- No architectural decision without an ADR.
- No knowledge claim without provenance.
- No source without a source record.
- No agent without a contract.
- No merge without CI.
- No release without validation.
- No generated article without evidence.

## Proposed Repository Areas
- .devcontainer/
- .github/workflows/
- apps/web/
- apps/android/
- backend/api/
- backend/orchestration/
- backend/agents/
- backend/knowledge/
- backend/provenance/
- backend/validation/
- backend/retrieval/
- backend/storage/
- data/sources/
- data/texts/
- data/passages/
- data/claims/
- data/entities/
- missions/
- agents/registry/
- agents/prompts/
- agents/schemas/
- agents/policies/
- governance/decisions/
- governance/conversations/
- governance/requirements/
- governance/architecture/
- governance/policies/
- docs/
- tests/
- scripts/
- config/
- PROJECT_STATE.md
- ROADMAP.md
- ARCHITECTURE.md
- CONTRIBUTING.md
- SECURITY.md
- README.md

## Continuity Protocol
A new ChatGPT session should reconstruct project state from repository artifacts, especially PROJECT_STATE.md, ROADMAP.md, active mission state, ADRs, agent registry, and current PR/CI state.

## Current Conversation Continuation
User requested that this conversation and every subsequent conversation/discussion be logged. User also asked whether this conversation should be moved into the ChatGPT Project and how the ChatGPT Project Instructions, limited to 7000 characters, should be configured.

## Important Limitation
Repository logging of a conversation is automated only when the assistant has access to the conversation content and performs the repository write. ChatGPT cannot guarantee that an arbitrary future conversation outside the project will be automatically captured unless the conversation is conducted in a context where the logging workflow is available and invoked. The project instructions should therefore require explicit repository logging at the beginning/end of substantive sessions.

## Next Planned Work
Foundation Phase 0: inspect repository state, establish project constitution, architecture, ADR framework, agent/task contracts, knowledge/provenance schemas, documentation protocol, development container, CI/CD foundation, and project state mechanism.
