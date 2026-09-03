from __future__ import annotations

import time
from dataclasses import dataclass, field
from threading import Event
from typing import Protocol

from sanatana_ai.contracts.agent import AgentRequest, AgentResult


class ExecutionControlError(RuntimeError):
    """Base error for execution-control policy violations."""


class ExecutionCancelled(ExecutionControlError):
    """Raised when cooperative cancellation is requested."""


class ExecutionTimedOut(ExecutionControlError):
    """Raised when a cooperative execution deadline expires."""


class RetryableAgentError(RuntimeError):
    """Marker error for failures eligible for policy-controlled retry."""


@dataclass
class CancellationToken:
    """Thread-safe cooperative cancellation signal."""

    _event: Event = field(default_factory=Event, init=False, repr=False)

    def cancel(self) -> None:
        self._event.set()

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()


@dataclass(frozen=True)
class ExecutionContext:
    """Attempt-scoped cooperative execution controls."""

    attempt: int
    deadline_monotonic: float | None
    cancellation_token: CancellationToken | None = None

    def check(self) -> None:
        if self.cancellation_token is not None and self.cancellation_token.is_cancelled:
            raise ExecutionCancelled("agent execution was cancelled")
        if self.deadline_monotonic is not None and time.monotonic() >= self.deadline_monotonic:
            raise ExecutionTimedOut("agent execution exceeded its deadline")


class ContextualAgentExecutor(Protocol):
    def execute_with_context(
        self, request: AgentRequest, context: ExecutionContext
    ) -> AgentResult:
        ...


class AgentExecutor(Protocol):
    def execute(self, request: AgentRequest) -> AgentResult:
        ...


@dataclass(frozen=True)
class ExecutionPolicy:
    """Explicit retry, timeout, and cancellation policy for one agent execution."""

    max_attempts: int = 1
    timeout_seconds: float | None = None

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")

    @property
    def requires_context(self) -> bool:
        return self.timeout_seconds is not None


@dataclass
class ControlledAgentExecutor:
    """Apply cooperative retry, timeout, and cancellation semantics to an executor."""

    executor: AgentExecutor
    policy: ExecutionPolicy = field(default_factory=ExecutionPolicy)
    cancellation_token: CancellationToken | None = None

    def execute(self, request: AgentRequest) -> AgentResult:
        contextual = getattr(self.executor, "execute_with_context", None)
        if self.policy.requires_context and contextual is None:
            raise ExecutionControlError(
                "timeout policy requires an executor implementing execute_with_context"
            )

        for attempt in range(1, self.policy.max_attempts + 1):
            deadline = (
                time.monotonic() + self.policy.timeout_seconds
                if self.policy.timeout_seconds is not None
                else None
            )
            context = ExecutionContext(attempt, deadline, self.cancellation_token)
            context.check()
            try:
                if contextual is not None:
                    result = contextual(request, context)
                else:
                    result = self.executor.execute(request)
                context.check()
                return result
            except RetryableAgentError:
                if attempt == self.policy.max_attempts:
                    raise

        raise AssertionError("execution policy exhausted without returning or raising")
