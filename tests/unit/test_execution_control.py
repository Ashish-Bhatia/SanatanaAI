import time

import pytest
from sanatana_ai.contracts.agent import AgentRequest, AgentResult
from sanatana_ai.orchestration.control import (
    CancellationToken,
    ControlledAgentExecutor,
    ExecutionCancelled,
    ExecutionContext,
    ExecutionControlError,
    ExecutionPolicy,
    ExecutionTimedOut,
    RetryableAgentError,
)


REQUEST = AgentRequest("mission-test", "task-a", "validation.schema")
RESULT = AgentResult("mission-test", "task-a", "validation.schema", "completed")


class RetryThenSuccess:
    def __init__(self) -> None:
        self.attempts = 0

    def execute(self, request: AgentRequest) -> AgentResult:
        self.attempts += 1
        if self.attempts < 3:
            raise RetryableAgentError("transient")
        return RESULT


class AlwaysRetryable:
    def __init__(self) -> None:
        self.attempts = 0

    def execute(self, request: AgentRequest) -> AgentResult:
        self.attempts += 1
        raise RetryableAgentError("transient")


class ContextualExecutor:
    def __init__(self, *, cancel: bool = False) -> None:
        self.attempts: list[int] = []
        self.cancel = cancel

    def execute_with_context(
        self, request: AgentRequest, context: ExecutionContext
    ) -> AgentResult:
        self.attempts.append(context.attempt)
        if self.cancel:
            context.cancellation_token.cancel()
        context.check()
        return RESULT


def test_retry_policy_retries_only_marked_transient_failures() -> None:
    executor = RetryThenSuccess()
    result = ControlledAgentExecutor(executor, ExecutionPolicy(max_attempts=3)).execute(
        REQUEST
    )

    assert result == RESULT
    assert executor.attempts == 3


def test_retry_policy_stops_at_max_attempts() -> None:
    executor = AlwaysRetryable()

    with pytest.raises(RetryableAgentError):
        ControlledAgentExecutor(executor, ExecutionPolicy(max_attempts=2)).execute(
            REQUEST
        )

    assert executor.attempts == 2


def test_non_retryable_failure_is_not_retried() -> None:
    class FailingExecutor:
        attempts = 0

        def execute(self, request: AgentRequest) -> AgentResult:
            self.attempts += 1
            raise RuntimeError("permanent")

    executor = FailingExecutor()
    with pytest.raises(RuntimeError, match="permanent"):
        ControlledAgentExecutor(executor, ExecutionPolicy(max_attempts=3)).execute(
            REQUEST
        )

    assert executor.attempts == 1


def test_timeout_requires_cooperative_context() -> None:
    class LegacyExecutor:
        def execute(self, request: AgentRequest) -> AgentResult:
            return RESULT

    with pytest.raises(
        ExecutionControlError,
        match="requires an executor implementing execute_with_context",
    ):
        ControlledAgentExecutor(
            LegacyExecutor(), ExecutionPolicy(timeout_seconds=1)
        ).execute(REQUEST)


def test_contextual_timeout_is_enforced_by_context_check() -> None:
    class SlowExecutor:
        def execute_with_context(
            self, request: AgentRequest, context: ExecutionContext
        ) -> AgentResult:
            time.sleep(0.01)
            context.check()
            return RESULT

    with pytest.raises(ExecutionTimedOut):
        ControlledAgentExecutor(
            SlowExecutor(), ExecutionPolicy(timeout_seconds=0.001)
        ).execute(REQUEST)


def test_cancellation_before_execution_is_fail_closed() -> None:
    token = CancellationToken()
    token.cancel()
    executor = ContextualExecutor()

    with pytest.raises(ExecutionCancelled):
        ControlledAgentExecutor(executor, cancellation_token=token).execute(REQUEST)

    assert executor.attempts == []


def test_cancellation_during_execution_is_observed() -> None:
    token = CancellationToken()
    executor = ContextualExecutor(cancel=True)

    with pytest.raises(ExecutionCancelled):
        ControlledAgentExecutor(executor, cancellation_token=token).execute(REQUEST)

    assert executor.attempts == [1]


def test_timeout_and_cancellation_require_positive_policy_values() -> None:
    with pytest.raises(ValueError, match="max_attempts"):
        ExecutionPolicy(max_attempts=0)
    with pytest.raises(ValueError, match="timeout_seconds"):
        ExecutionPolicy(timeout_seconds=0)
