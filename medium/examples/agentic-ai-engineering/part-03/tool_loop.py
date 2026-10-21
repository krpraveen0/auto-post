#!/usr/bin/env python3
"""A deterministic, provider-neutral tool-call loop for Course Part 3.

The example deliberately uses a scripted model adapter. It exercises the host
loop without a network request, API key, or dependency on a model provider.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any, Callable, Protocol

from jsonschema import Draft202012Validator


class ModelAdapter(Protocol):
    def decide(self, task: str, trace: list[dict[str, Any]]) -> dict[str, Any]: ...


ToolHandler = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: ToolHandler
    read_only: bool = True


@dataclass(frozen=True)
class RunPolicy:
    max_steps: int = 6
    max_tool_failures: int = 2


class ScriptedModel:
    """Return predefined decisions so loop behavior can be tested exactly."""

    def __init__(self, decisions: list[dict[str, Any]]) -> None:
        self._decisions = decisions
        self._index = 0

    def decide(self, task: str, trace: list[dict[str, Any]]) -> dict[str, Any]:
        del task, trace
        if self._index >= len(self._decisions):
            return {
                "type": "final",
                "text": "The scripted model produced no further decision.",
            }
        decision = self._decisions[self._index]
        self._index += 1
        return decision


class ToolLoop:
    """Validate, execute, record, and replay model-proposed tool calls."""

    def __init__(self, tools: list[Tool], policy: RunPolicy = RunPolicy()) -> None:
        self._tools = {tool.name: tool for tool in tools}
        if len(self._tools) != len(tools):
            raise ValueError("tool names must be unique")
        self._policy = policy

    def run(self, task: str, model: ModelAdapter) -> dict[str, Any]:
        trace: list[dict[str, Any]] = [{"type": "task", "text": task}]
        completed_calls: dict[str, dict[str, Any]] = {}
        failures = 0

        for step in range(1, self._policy.max_steps + 1):
            decision = model.decide(task, list(trace))
            trace.append({"type": "model_decision", "step": step, **decision})

            if decision.get("type") == "final":
                text = decision.get("text")
                if not isinstance(text, str) or not text.strip():
                    return self._stop("invalid_final_response", step, trace)
                return {
                    "status": "completed",
                    "steps": step,
                    "answer": text,
                    "trace": trace,
                }

            if decision.get("type") != "tool_call":
                failures += 1
                trace.append(self._error_result(decision, "invalid_decision_type"))
            else:
                result = self._execute(decision, completed_calls)
                trace.append(result)
                if not result["ok"]:
                    failures += 1

            if failures > self._policy.max_tool_failures:
                return self._stop("tool_failure_budget_exhausted", step, trace)

        return self._stop("step_budget_exhausted", self._policy.max_steps, trace)

    def _execute(
        self,
        call: dict[str, Any],
        completed_calls: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        call_id = call.get("call_id")
        name = call.get("name")
        arguments = call.get("arguments")
        if not isinstance(call_id, str) or not call_id:
            return self._error_result(call, "missing_call_id")
        if not isinstance(name, str) or not name:
            return self._error_result(call, "missing_tool_name")
        if not isinstance(arguments, dict):
            return self._error_result(call, "arguments_must_be_an_object")

        fingerprint = {"name": name, "arguments": arguments}
        if call_id in completed_calls:
            previous = completed_calls[call_id]
            if previous["fingerprint"] != fingerprint:
                return self._error_result(call, "call_id_collision")
            replay = dict(previous["result"])
            replay["replayed"] = True
            return replay

        tool = self._tools.get(name)
        if tool is None:
            result = self._error_result(call, "unknown_tool")
            completed_calls[call_id] = {"fingerprint": fingerprint, "result": result}
            return result
        errors = sorted(Draft202012Validator(tool.input_schema).iter_errors(arguments), key=lambda error: list(error.path))
        if errors:
            message = errors[0].message
            result = self._error_result(call, "invalid_arguments", message)
            completed_calls[call_id] = {"fingerprint": fingerprint, "result": result}
            return result

        try:
            output = tool.handler(**arguments)
            result = {
                "type": "tool_result",
                "call_id": call_id,
                "name": name,
                "ok": True,
                "output": output,
                "replayed": False,
            }
        except Exception as exc:  # The loop converts tool exceptions into data.
            result = self._error_result(call, "tool_execution_failed", str(exc))

        completed_calls[call_id] = {"fingerprint": fingerprint, "result": result}
        return result

    @staticmethod
    def _error_result(call: dict[str, Any], code: str, message: str | None = None) -> dict[str, Any]:
        return {
            "type": "tool_result",
            "call_id": call.get("call_id"),
            "name": call.get("name"),
            "ok": False,
            "error": {"code": code, "message": message or code.replace("_", " ")},
            "replayed": False,
        }

    @staticmethod
    def _stop(reason: str, step: int, trace: list[dict[str, Any]]) -> dict[str, Any]:
        return {"status": "stopped", "reason": reason, "steps": step, "trace": trace}


RELEASES = {
    "2.5": {
        "notes": ["Replace the session cache", "Add release audit fields"],
        "tests": {"passed": 148, "failed": 0, "skipped": 2},
    }
}


def read_release_notes(release_id: str) -> dict[str, Any]:
    if release_id not in RELEASES:
        raise LookupError(f"release {release_id!r} was not found")
    return {"release_id": release_id, "notes": RELEASES[release_id]["notes"]}


def read_test_summary(release_id: str) -> dict[str, Any]:
    if release_id not in RELEASES:
        raise LookupError(f"release {release_id!r} was not found")
    return {"release_id": release_id, **RELEASES[release_id]["tests"]}


def request_clarification(question: str) -> dict[str, Any]:
    return {"question": question, "status": "waiting_for_user"}


RELEASE_ID_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["release_id"],
    "properties": {"release_id": {"type": "string", "pattern": r"^[0-9]+\.[0-9]+$"}},
}

QUESTION_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["question"],
    "properties": {"question": {"type": "string", "minLength": 10}},
}


def default_tools() -> list[Tool]:
    return [
        Tool("read_release_notes", "Read notes for one release.", RELEASE_ID_SCHEMA, read_release_notes),
        Tool("read_test_summary", "Read test counts for one release.", RELEASE_ID_SCHEMA, read_test_summary),
        Tool("request_clarification", "Ask the user for missing task context.", QUESTION_SCHEMA, request_clarification),
    ]


def success_script() -> list[dict[str, Any]]:
    return [
        {"type": "tool_call", "call_id": "call-1", "name": "read_release_notes", "arguments": {"release_id": "2.5"}},
        {"type": "tool_call", "call_id": "call-2", "name": "read_test_summary", "arguments": {"release_id": "2.5"}},
        {"type": "final", "text": "Release 2.5 has two documented changes; 148 tests passed, 0 failed, and 2 were skipped."},
    ]


def invalid_script() -> list[dict[str, Any]]:
    bad_call = {"type": "tool_call", "call_id": "call-1", "name": "read_test_summary", "arguments": {"release": "2.5"}}
    return [bad_call, bad_call, {"type": "final", "text": "The test summary could not be verified."}]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", choices=("success", "invalid"), default="success", nargs="?")
    args = parser.parse_args()
    decisions = success_script() if args.scenario == "success" else invalid_script()
    result = ToolLoop(default_tools()).run("Review release 2.5", ScriptedModel(decisions))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
