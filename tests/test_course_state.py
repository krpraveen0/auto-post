import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import course_state


class CourseStateTests(unittest.TestCase):
    def test_pending_human_review_blocks_generation(self):
        state = {
            "generation_enabled": True,
            "workflow_status": "awaiting_human_review",
            "unresolved_revisions": [],
            "pending_human_review": [1, 2],
            "next_part": 3,
        }
        with self.assertRaisesRegex(course_state.StateBlocked, "await human review"):
            course_state.assert_generation_eligible(state)

    def test_disabled_generation_blocks_before_next_part(self):
        state = {"generation_enabled": False, "workflow_status": "quality-remediation", "next_part": 3}
        with self.assertRaisesRegex(course_state.StateBlocked, "generation is disabled"):
            course_state.assert_generation_eligible(state)

    def test_eligible_state_returns_next_part(self):
        state = {
            "generation_enabled": True,
            "unresolved_revisions": [],
            "pending_human_review": [],
            "next_part": 3,
        }
        self.assertEqual(course_state.assert_generation_eligible(state), 3)

    def test_atomic_write_replaces_complete_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            course_state.write_atomic(path, {"next_part": 4})
            self.assertEqual(json.loads(path.read_text()), {"next_part": 4})


if __name__ == "__main__":
    unittest.main()
