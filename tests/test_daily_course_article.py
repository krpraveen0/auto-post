import os
import subprocess
import sys
import unittest
from pathlib import Path

from agents.testing import ScriptedModel, assistant_message

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import daily_course_article as dca
import validate_generated_docx as vgd
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

## Evidence

- Python documentation: https://docs.python.org/3/reference/
- GitHub Actions documentation: https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions

## Infographic

```mermaid
flowchart LR
    Prompt --> Decision --> Tool --> Result
```

Caption: A bounded agent loop connects a decision to a tool result.

Alt text: A left-to-right flow from prompt to decision, tool, and result.

## Validated Code

```python
def bounded_step(value: int) -> int:
    return value + 1

assert bounded_step(1) == 2
print("validation passed")
```

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
                "evidence_research",
                "draft",
                "technical_review",
                "continuity_review",
                "publishing_editor",
            },
        )
        self.assertEqual(len(agents["manager"].handoffs), 5)

    def test_agents_backend_with_scripted_model(self):
        model = ScriptedModel(
            [
                [assistant_message("Evidence with primary URLs.", item_id="evidence")],
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
        self.assertIn("primary URLs", result.evidence_review)

    def test_validated_content_executes_python_and_extracts_mermaid(self):
        import validate_article_content as vac

        report = vac.validate_article(long_article(), check_urls=False)
        self.assertEqual(report["validated_python_blocks"], 1)
        self.assertEqual(report["mermaid_blocks"], 1)

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

    def test_validate_generated_docx_accepts_written_docx(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            docx_path = Path(tmp) / "lesson.docx"
            dca.write_docx(long_article(), docx_path, "Lesson")
            vgd.validate_docx_archive(docx_path)


if __name__ == "__main__":
    unittest.main()
