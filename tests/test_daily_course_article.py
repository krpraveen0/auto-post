import os
import subprocess
import sys
import unittest
from pathlib import Path

from agents.testing import ScriptedModel, assistant_message

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import daily_course_article as dca
from course_agents import build_course_agents, run_course_generation_with_agents


VALID_ARTICLE = """# What Makes an AI Agent Different from a Chatbot?

Series navigation: Previous: Course index. Course index: Agentic AI Engineering. Next: The Six Configuration Surfaces of an Agent.

## Learning Outcomes

1. Define the concept.
2. Apply it to the project.
3. Complete the exercise.

## Worked Example

An agent combines a model, tools, state, and a bounded loop. This example compares a chatbot, a deterministic workflow, and a tool-using agent.

## Exercise

Classify three systems and explain the required guardrails.

## Recap

The core distinction is controlled autonomy.

## Next Lesson

Next, we break the agent into configuration surfaces.
"""


def long_article() -> str:
    filler = "This paragraph keeps the validation article long enough for the course quality gate. "
    return VALID_ARTICLE + "\n" + filler * 170


class DailyCourseArticleTests(unittest.TestCase):
    def test_parse_lessons_from_series_map(self):
        lessons = dca.parse_lessons((ROOT / "medium/course_series/agentic-ai-engineering-map.md").read_text())
        self.assertEqual(len(lessons), 15)
        self.assertEqual(lessons[0]["part"], "1")
        self.assertEqual(lessons[-1]["title"], "Capstone: Ship and Roll Back a Production Agent")

    def test_quality_gate_accepts_complete_lesson(self):
        self.assertEqual(dca.quality_issues(long_article()), [])

    def test_quality_gate_rejects_missing_sections(self):
        issues = dca.quality_issues("short draft")
        self.assertTrue(any("too short" in issue for issue in issues))
        self.assertTrue(any("Learning Outcomes" in issue for issue in issues))

    def test_agents_are_constructed_with_specialists(self):
        agents = build_course_agents("gpt-5.6-terra")
        self.assertEqual(
            set(agents),
            {
                "manager",
                "draft",
                "technical_review",
                "continuity_review",
                "publishing_editor",
            },
        )
        self.assertEqual(len(agents["manager"].handoffs), 4)

    def test_agents_backend_with_scripted_model(self):
        model = ScriptedModel(
            [
                [assistant_message(long_article(), item_id="draft")],
                [assistant_message("No technical blockers.", item_id="technical")],
                [assistant_message("Continuity looks correct.", item_id="continuity")],
                [assistant_message(long_article(), item_id="final")],
            ]
        )
        result = run_course_generation_with_agents(
            "Write part 1.",
            model="gpt-5.6-terra",
            tracing_disabled=True,
            scripted_model=model,
        )
        self.assertIn("Learning Outcomes", result.article)
        self.assertIn("No technical blockers", result.technical_review)

    def test_cli_dry_run_creates_docx_and_state(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output_file = tmp_path / "github-output.txt"
            env = os.environ.copy()
            env["GITHUB_OUTPUT"] = str(output_file)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/daily_course_article.py"),
                    "--series-map",
                    str(ROOT / "medium/course_series/agentic-ai-engineering-map.md"),
                    "--series-slug",
                    "agentic-ai-engineering",
                    "--state-file",
                    str(tmp_path / "state.json"),
                    "--out-dir",
                    str(tmp_path / "out"),
                    "--dry-run",
                    "--backend",
                    "agents",
                ],
                check=True,
                env=env,
            )
            self.assertTrue(list((tmp_path / "out").glob("*.docx")))
            self.assertIn("generated=true", output_file.read_text())


if __name__ == "__main__":
    unittest.main()
