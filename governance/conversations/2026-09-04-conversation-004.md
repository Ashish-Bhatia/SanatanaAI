# Conversation 004

Date: 2026-09-04

## Objective
Continue Foundation Phase 0 orchestration work while preserving verified repository history and the branch/PR workflow.

## Requirements
- GitHub remains the source of truth.
- Use only the genuine development branches for project work.
- Do not create additional branches for routine changes.
- Preserve the PR and CI gate workflow.
- Continue executable orchestration validation.
- Keep orchestration independent of a specific AI provider.
- Record substantive project decisions and implementation outcomes.

## Decisions
- Treat `main`, `foundation/phase-0`, and `foundation/orchestration-core` as the genuine project branches.
- Treat the other similarly named branches as accidental artifacts from earlier connector failures.
- Continue implementation exclusively on `foundation/orchestration-core` until PR #2 is validated and integrated.
- Do not claim accidental branch deletion because the available GitHub integration does not expose branch deletion.
- Introduce an `AgentExecutor` protocol and `ExecutionService` as the provider-neutral execution boundary.
- Checkpoint task state before agent execution and after terminal execution outcomes.
- Fail closed on task/request identity mismatches and execution exceptions.
- Preserve the historical record in this file when reconciling divergent branch copies; do not silently replace project history with a stale variant.

## Actions
- Re-verified PR #2 and the corrected CI results.
- Corrected the duplicate-agent registry test fixture.
- Corrected dependency readiness so unresolved dependencies transition pending tasks to blocked state and failed dependencies block downstream tasks.
- Added the provider-neutral orchestration execution boundary.
- Added execution tests for success, failure, readiness, identity validation, and checkpoint sequencing.
- Updated architecture and project-state documentation.
- Re-recorded this conversation in the repository.
- Reconciled the divergent `conversation-004` file with the copy on `main` without discarding the branch-specific historical record.

## Validation findings
- CI run 22 passed for the corrected task-readiness head.
- CI runs 23 and 24 passed for subsequent registry/conversation corrections.
- The execution-boundary increment required a fresh CI run on its latest head.

## Unresolved
- PR #2 remained draft until the latest execution increment passed CI and received review.
- Native branch protection/ruleset enforcement remained unresolved.
- Accidental branches remain because branch deletion is not available through the current connector.
- Persistent checkpoint storage and transactional recovery remain future design work.

## Next
1. Verify CI for the latest execution-boundary head.
2. Review orchestration-core lifecycle, identity, failure, and checkpoint semantics.
3. Strengthen recovery tests around the latest valid checkpoint.
4. Add stronger formatting, typing, dependency, security, provenance, agent-contract, and documentation gates.
5. Merge PR #2 only after required validation and review gates pass.
