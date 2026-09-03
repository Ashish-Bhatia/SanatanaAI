# Conversation 011

Date: 2026-09-04

## Objective
Complete the remaining execution-control semantics associated with Issue #5 without introducing unsafe hard-kill behavior.

## Requirements
- Explicit retry, timeout, and cancellation semantics.
- Bounded retries with deterministic classification.
- Safe timeout and cancellation behavior.
- No false claim that arbitrary synchronous Python execution is safely killable.
- Preserve provider-neutral executor boundaries.
- Document architectural consequences and test the controls.

## Decisions
- Retry only failures explicitly marked `RetryableAgentError`.
- Bound retries through `ExecutionPolicy.max_attempts`.
- Expose attempt-scoped timeout deadlines through `ExecutionContext.check()`.
- Use thread-safe cooperative cancellation tokens.
- Require `execute_with_context` when timeout or cancellation is requested. Legacy executors remain supported without those controls.
- Do not implement thread termination as a hard timeout mechanism.
- Hard process-level isolation remains a future worker-runtime decision if production requirements demand it.

## Actions
- Created `feature/execution-controls` from the current main baseline.
- Added execution-control policy, cancellation token, cooperative execution context, and controlled executor wrapper.
- Added retry, timeout, cancellation, capability, and policy validation tests.
- Added ADR-0004 for cooperative execution controls.
- Updated architecture and CI to gate ADR-0004.

## Validation
- The branch is ready for fresh PR CI validation after documentation and test updates.
- Issue #5 remains open until this execution-control increment is validated and merged, after which its remaining acceptance criteria will be re-evaluated.

## Unresolved
- Mission-level scheduling must integrate these controls with checkpoint and retry policy.
- Hard isolation remains an explicit future decision, not an implicit guarantee.
- Issue #4 still requires broader CI quality gates.

## Result
Execution control is explicit, bounded, and fail-closed. The platform does not claim stronger cancellation or timeout guarantees than the executor contract provides.
