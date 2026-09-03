"""A deterministic state machine for the control boundary taught in Part 01."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Callable


TERMINAL_STATES = {"succeeded", "stopped", "failed"}


class ToolFailure(RuntimeError):
    """The tool reports that the requested operation failed."""


class UnknownOutcome(RuntimeError):
    """The caller cannot tell whether a mutating operation completed."""


@dataclass(frozen=True)
class Proposal:
    name: str
    arguments: dict[str, Any]
    logical_operation: str
    mutating: bool = False


@dataclass
class TaskState:
    task_id: str
    goal: str
    allowed_actions: set[str]
    remaining_steps: int = 8
    max_tool_failures: int = 2
    status: str = "running"
    tool_failures: int = 0
    denied_actions: int = 0
    pending_approval: str | None = None
    approved_operations: set[str] = field(default_factory=set)
    operation_ids: dict[str, str] = field(default_factory=dict)
    completed_steps: list[str] = field(default_factory=list)
    stop_reason: str | None = None
    trace: list[dict[str, Any]] = field(default_factory=list)

    def operation_id(self, logical_operation: str) -> str:
        """Return one stable ID for every retry of the same logical operation."""
        if logical_operation not in self.operation_ids:
            material = f"{self.task_id}:{logical_operation}".encode()
            self.operation_ids[logical_operation] = hashlib.sha256(material).hexdigest()[:16]
        return self.operation_ids[logical_operation]


class Policy:
    def authorize(self, state: TaskState, proposal: Proposal) -> tuple[str, str]:
        if proposal.name not in state.allowed_actions:
            return "deny", "action is outside the allow-list"
        if proposal.mutating and proposal.logical_operation not in state.approved_operations:
            return "require_approval", "mutating operation needs approval"
        return "allow", "action is within the current boundary"


Tool = Callable[[dict[str, Any], str], dict[str, Any]]


class BoundedAgent:
    def __init__(self, state: TaskState, tools: dict[str, Tool], policy: Policy | None = None):
        self.state = state
        self.tools = tools
        self.policy = policy or Policy()

    def _record(self, event: str, **details: Any) -> dict[str, Any]:
        item = {"event": event, "status": self.state.status, **details}
        self.state.trace.append(item)
        return item

    def _stop(self, status: str, reason: str) -> dict[str, Any]:
        self.state.status = status
        self.state.stop_reason = reason
        return self._record("stopped", reason=reason)

    def step(self, proposal: Proposal) -> dict[str, Any]:
        if self.state.status != "running":
            raise RuntimeError(f"cannot step a task in {self.state.status!r} state")
        if self.state.remaining_steps <= 0:
            return self._stop("stopped", "step_budget_exhausted")

        self.state.remaining_steps -= 1
        decision, reason = self.policy.authorize(self.state, proposal)
        self._record(
            "decision",
            action=proposal.name,
            logical_operation=proposal.logical_operation,
            decision=decision,
            reason=reason,
            remaining_steps=self.state.remaining_steps,
        )

        if decision == "deny":
            self.state.denied_actions += 1
            return self._stop("stopped", "policy_denied")

        if decision == "require_approval":
            self.state.status = "waiting_for_approval"
            self.state.pending_approval = proposal.logical_operation
            return self._record("approval_requested", operation=proposal.logical_operation)

        operation_id = self.state.operation_id(proposal.logical_operation)
        try:
            result = self.tools[proposal.name](proposal.arguments, operation_id)
        except UnknownOutcome as exc:
            return self._record(
                "unknown_outcome",
                action=proposal.name,
                operation_id=operation_id,
                error=str(exc),
            )
        except ToolFailure as exc:
            self.state.tool_failures += 1
            self._record(
                "tool_failed",
                action=proposal.name,
                operation_id=operation_id,
                failures=self.state.tool_failures,
                error=str(exc),
            )
            if self.state.tool_failures >= self.state.max_tool_failures:
                return self._stop("failed", "tool_failure_budget_exhausted")
            return self.state.trace[-1]

        self.state.tool_failures = 0
        self.state.completed_steps.append(proposal.logical_operation)
        return self._record(
            "tool_completed",
            action=proposal.name,
            operation_id=operation_id,
            result=result,
        )

    def approve(self, logical_operation: str) -> dict[str, Any]:
        if self.state.status != "waiting_for_approval":
            raise RuntimeError("task is not waiting for approval")
        if self.state.pending_approval != logical_operation:
            raise ValueError("approval does not match the pending operation")
        self.state.approved_operations.add(logical_operation)
        self.state.pending_approval = None
        self.state.status = "running"
        return self._record("approval_received", operation=logical_operation)

    def finish(self, *, goal_verified: bool) -> dict[str, Any]:
        if self.state.status != "running":
            raise RuntimeError(f"cannot finish a task in {self.state.status!r} state")
        if not goal_verified:
            return self._stop("failed", "goal_not_verified")
        self.state.status = "succeeded"
        return self._record("goal_satisfied")


def demo() -> list[dict[str, Any]]:
    def lookup(arguments: dict[str, Any], operation_id: str) -> dict[str, Any]:
        return {"employee_id": arguments["employee_id"], "active": True}

    state = TaskState(
        task_id="access-E-1042",
        goal="verify the employee before preparing an access request",
        allowed_actions={"lookup_employee", "create_access_ticket"},
    )
    agent = BoundedAgent(state, {"lookup_employee": lookup})
    agent.step(Proposal("lookup_employee", {"employee_id": "E-1042"}, "lookup-employee"))
    agent.finish(goal_verified=True)
    return state.trace


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))
