import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("bounded_agent.py")
SPEC = importlib.util.spec_from_file_location("bounded_agent", MODULE_PATH)
bounded_agent = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = bounded_agent
SPEC.loader.exec_module(bounded_agent)

BoundedAgent = bounded_agent.BoundedAgent
Policy = bounded_agent.Policy
Proposal = bounded_agent.Proposal
TaskState = bounded_agent.TaskState
ToolFailure = bounded_agent.ToolFailure
UnknownOutcome = bounded_agent.UnknownOutcome


class BoundedAgentTests(unittest.TestCase):
    def state(self, **overrides):
        values = {
            "task_id": "task-1",
            "goal": "prepare an approved change",
            "allowed_actions": {"read", "write"},
            "remaining_steps": 4,
            "max_tool_failures": 2,
        }
        values.update(overrides)
        return TaskState(**values)

    def test_read_only_success_and_verified_finish(self):
        state = self.state()
        agent = BoundedAgent(state, {"read": lambda args, op_id: {"found": True}})
        event = agent.step(Proposal("read", {}, "read-record"))
        self.assertEqual(event["event"], "tool_completed")
        self.assertEqual(state.remaining_steps, 3)
        agent.finish(goal_verified=True)
        self.assertEqual(state.status, "succeeded")

    def test_mutation_waits_for_matching_approval_then_resumes(self):
        calls = []

        def write(args, op_id):
            calls.append(op_id)
            return {"ticket": "T-8821"}

        state = self.state()
        agent = BoundedAgent(state, {"write": write})
        proposal = Proposal("write", {}, "ticket-8821", mutating=True)
        self.assertEqual(agent.step(proposal)["event"], "approval_requested")
        self.assertEqual(state.status, "waiting_for_approval")
        agent.approve("ticket-8821")
        self.assertEqual(agent.step(proposal)["event"], "tool_completed")
        self.assertEqual(len(calls), 1)

    def test_denied_action_stops_instead_of_looping(self):
        state = self.state()
        agent = BoundedAgent(state, {})
        event = agent.step(Proposal("delete_account", {}, "delete"))
        self.assertEqual(event["reason"], "policy_denied")
        self.assertEqual(state.status, "stopped")

    def test_tool_failure_budget_is_enforced(self):
        def fail(args, op_id):
            raise ToolFailure("service unavailable")

        state = self.state()
        agent = BoundedAgent(state, {"read": fail})
        proposal = Proposal("read", {}, "read-record")
        agent.step(proposal)
        event = agent.step(proposal)
        self.assertEqual(event["reason"], "tool_failure_budget_exhausted")
        self.assertEqual(state.status, "failed")

    def test_unknown_outcome_reuses_operation_id(self):
        operation_ids = []

        def uncertain_then_succeed(args, op_id):
            operation_ids.append(op_id)
            if len(operation_ids) == 1:
                raise UnknownOutcome("timeout after request was accepted")
            return {"ticket": "T-8821"}

        state = self.state()
        state.approved_operations.add("ticket-8821")
        agent = BoundedAgent(state, {"write": uncertain_then_succeed})
        proposal = Proposal("write", {}, "ticket-8821", mutating=True)
        self.assertEqual(agent.step(proposal)["event"], "unknown_outcome")
        self.assertEqual(agent.step(proposal)["event"], "tool_completed")
        self.assertEqual(operation_ids[0], operation_ids[1])

    def test_step_budget_terminates_run(self):
        state = self.state(remaining_steps=0)
        agent = BoundedAgent(state, {})
        event = agent.step(Proposal("read", {}, "read-record"))
        self.assertEqual(event["reason"], "step_budget_exhausted")
        self.assertEqual(state.status, "stopped")

    def test_unverified_goal_cannot_succeed(self):
        state = self.state()
        agent = BoundedAgent(state, {})
        agent.finish(goal_verified=False)
        self.assertEqual(state.status, "failed")
        self.assertEqual(state.stop_reason, "goal_not_verified")


if __name__ == "__main__":
    unittest.main()
