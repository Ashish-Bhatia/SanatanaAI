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


def test_timeout_requires_contextual_executor() -> None:
    with pytest.raises(ExecutionControlError, match="execute_with_context"):
        ControlledAgentExecutor(
            RetryThenSuccess(), ExecutionPolicy(max_attempts=1, timeout_seconds=1)
        ).execute(REQUEST)


def test_cooperative_timeout_is_detected() -> None:
    class SlowExecutor:
        def execute_with_context(
            self, request: AgentRequest, context: ExecutionContext
        ) -> AgentResult:
            time.sleep(0.01)
            context.check()
            return RESULT

    with pytest.raises(ExecutionTimedOut):
        ControlledAgentExecutor(
            SlowExecutor(), ExecutionPolicy(max_attempts=1, timeout_seconds=0.001)
        ).execute(REQUEST)


def test_cancellation_before_execution_is_detected() -> None:
    token = CancellationToken()
    token.cancel()

    class Contextual:
        def execute_with_context(
            self, request: AgentRequest, context: ExecutionContext
        ) -> AgentResult:
            context.check()
            return RESULT

    with pytest.raises(ExecutionCancelled):
        ControlledAgentExecutor(
            Contextual(), ExecutionPolicy(max_attempts=1), cancellation_token=token
        ).execute(REQUEST)


def test_cancellation_during_execution_is_detected() -> None:
    executor = ContextualExecutor(cancel=True)

    with pytest.raises(ExecutionCancelled):
        ControlledAgentExecutor(
            executor,
            ExecutionPolicy(max_attempts=1, cancellation_enabled=True),
        ).execute(REQUEST)

    assert executor.attempts == [1]


def test_invalid_execution_policy_values_are_rejected() -> None:
    with pytest.raises(ValueError, match="max_attempts"):
        ExecutionPolicy(max_attempts=0)
    with pytest.raises(ValueError, match="timeout_seconds"):
        ExecutionPolicy(max_attempts=1, timeout_seconds=0)


def test_cancellation_enabled_requires_contextual_executor() -> None:
    with pytest.raises(ExecutionControlError, match="execute_with_context"):
        ControlledAgentExecutor(
            RetryThenSuccess(),
            ExecutionPolicy(max_attempts=1, cancellation_enabled=True),
        ).execute(REQUEST)
