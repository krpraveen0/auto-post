import unittest

from tool_loop import RunPolicy, ScriptedModel, ToolLoop, default_tools, invalid_script, success_script


class ToolLoopTests(unittest.TestCase):
    def test_successful_run_uses_two_tools_and_finishes(self):
        result = ToolLoop(default_tools()).run("Review release 2.5", ScriptedModel(success_script()))
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["steps"], 3)
        tool_results = [item for item in result["trace"] if item["type"] == "tool_result"]
        self.assertEqual([item["name"] for item in tool_results], ["read_release_notes", "read_test_summary"])
        self.assertTrue(all(item["ok"] for item in tool_results))

    def test_invalid_arguments_become_visible_error_data(self):
        result = ToolLoop(default_tools()).run("Review release 2.5", ScriptedModel(invalid_script()))
        tool_results = [item for item in result["trace"] if item["type"] == "tool_result"]
        first_result = tool_results[0]
        self.assertFalse(first_result["ok"])
        self.assertEqual(first_result["error"]["code"], "invalid_arguments")
        self.assertTrue(tool_results[1]["replayed"])

    def test_duplicate_call_id_replays_without_reexecution(self):
        calls = {"count": 0}
        tools = default_tools()
        original = tools[0]

        def counted(release_id):
            calls["count"] += 1
            return original.handler(release_id)

        tools[0] = type(original)(original.name, original.description, original.input_schema, counted)
        call = {"type": "tool_call", "call_id": "same", "name": "read_release_notes", "arguments": {"release_id": "2.5"}}
        result = ToolLoop(tools).run("Read twice", ScriptedModel([call, call, {"type": "final", "text": "Done"}]))
        tool_results = [item for item in result["trace"] if item["type"] == "tool_result"]
        self.assertEqual(calls["count"], 1)
        self.assertFalse(tool_results[0]["replayed"])
        self.assertTrue(tool_results[1]["replayed"])

    def test_call_id_collision_is_rejected(self):
        decisions = [
            {"type": "tool_call", "call_id": "same", "name": "read_release_notes", "arguments": {"release_id": "2.5"}},
            {"type": "tool_call", "call_id": "same", "name": "read_test_summary", "arguments": {"release_id": "2.5"}},
            {"type": "final", "text": "Done"},
        ]
        result = ToolLoop(default_tools()).run("Collision", ScriptedModel(decisions))
        errors = [item for item in result["trace"] if item.get("error")]
        self.assertEqual(errors[0]["error"]["code"], "call_id_collision")

    def test_unknown_tools_exhaust_failure_budget(self):
        call = {"type": "tool_call", "call_id": "bad", "name": "delete_release", "arguments": {}}
        result = ToolLoop(default_tools(), RunPolicy(max_steps=4, max_tool_failures=0)).run("Delete", ScriptedModel([call]))
        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["reason"], "tool_failure_budget_exhausted")

    def test_step_budget_stops_endless_tool_calls(self):
        decisions = [
            {"type": "tool_call", "call_id": f"call-{index}", "name": "read_release_notes", "arguments": {"release_id": "2.5"}}
            for index in range(4)
        ]
        result = ToolLoop(default_tools(), RunPolicy(max_steps=2)).run("Loop", ScriptedModel(decisions))
        self.assertEqual(result["status"], "stopped")
        self.assertEqual(result["reason"], "step_budget_exhausted")
        self.assertEqual(result["steps"], 2)


if __name__ == "__main__":
    unittest.main()
