import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_course_lesson as vcl


def publishable_lesson(paragraphs: int = 195) -> str:
    filler = "\n\n".join(
        "A bounded explanation connects the decision to observable behavior and keeps each technical step close to its reason."
        for _ in range(paragraphs)
    )
    return f"""---
publishing_schema_version: 3
title: Build a Bounded Tool-Using Agent
subtitle: Trace and test the control loop before it reaches production
author: Praveen Kumar
slug: bounded-tool-using-agent
status: reviewed-draft
tags: agents, python, testing, ai
canonical_strategy: set-on-first-publication
ai_assistance: AI-assisted draft with human technical review
last_verified: 2026-09-01
---
# Build a Bounded Tool-Using Agent

Series navigation: Previous: Agent boundaries. Course index: Agentic AI Engineering. Next: Test the loop.

This article was developed with AI assistance and reviewed by the named author. When you debug an agent in production, the difficult question is often where a decision should stop. In this article, you will build and test that boundary.

## Learning Outcomes

1. Explain the boundary around a tool call.
2. Trace one request through the control loop.
3. Implement a bounded stop condition.

## Before You Start

You should know Python functions and JavaScript Object Notation (JSON). Recall: what should happen when a tool fails?

## Mental Model

Treat the loop as a state machine with a visible stop condition.

![A request moving through decide, act, observe, and stop states](visuals/bounded-loop.svg)

Figure 1: A visible stop condition prevents an unbounded control loop.

## Reading Path

Read the worked example first for the implementation, then use the exercise and
self-check to verify that you can transfer the boundary to another system.

## Worked Example

The implementation chooses a maximum because a tool can fail repeatedly. That trade-off favors safety over unlimited recovery.

```python
for step in range(3):
    result = run_tool()
    if result.ok:
        break
```

{filler}

## Tested Environment

Verified with Python 3.12.13 on 2026-09-01. The example and failure test completed locally.

## Exercise

Add a stop condition and one failure test. Expected output: a Python file and a passing test that proves the third attempt stops.

## Check Your Work

- The test observes no more than three calls.
- A successful call exits early.
- The failure path returns a useful error.

## Retrieval Practice

1. Why is a stop condition part of the agent boundary?
2. What state must survive between attempts?
3. Which failure would your test expose?

Transfer prompt: apply this boundary to a network retry loop in one of your own projects.

## Recap

A bounded loop makes autonomy inspectable and limits failure impact.

## Next Lesson

Next, use the same test artifact to evaluate tool-result validation.

## Sources

- [Python control-flow documentation](https://docs.python.org/3/tutorial/controlflow.html)
- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
"""


class ValidateCourseLessonTests(unittest.TestCase):
    def test_publishable_schema_three_lesson_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lesson.md"
            path.write_text(publishable_lesson(), encoding="utf-8")
            report = vcl.score_lesson(path, require_schema=3)

        self.assertTrue(report.publishable)
        self.assertGreaterEqual(report.total_score, 90)
        self.assertEqual(report.critical_issues, [])

    def test_long_article_is_not_penalized_for_word_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lesson.md"
            article = publishable_lesson(paragraphs=320).replace(
                "## Learning Outcomes", "## In This Article\n\nUse the sections below as a reading path.\n\n## Learning Outcomes"
            )
            path.write_text(article, encoding="utf-8")
            report = vcl.score_lesson(path, require_schema=3)

        self.assertGreater(report.word_count, 3000)
        self.assertTrue(report.publishable)

    def test_article_below_depth_floor_is_not_publishable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lesson.md"
            path.write_text(publishable_lesson(paragraphs=50), encoding="utf-8")
            report = vcl.score_lesson(path, require_schema=3)

        self.assertLess(report.word_count, 3000)
        self.assertFalse(report.publishable)
        self.assertTrue(any("at least 3000 words" in issue for issue in report.critical_issues))

    def test_long_article_requires_reading_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lesson.md"
            article = publishable_lesson().replace(
                "## Reading Path\n\nRead the worked example first for the implementation, then use the exercise and\nself-check to verify that you can transfer the boundary to another system.\n\n",
                "",
            )
            path.write_text(article, encoding="utf-8")
            report = vcl.score_lesson(path, require_schema=3)

        self.assertFalse(report.publishable)
        self.assertTrue(any("reading path" in issue.casefold() for issue in report.critical_issues))

    def test_placeholder_visual_and_missing_feedback_block_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lesson.md"
            path.write_text(
                publishable_lesson()
                .replace(
                    "![A request moving through decide, act, observe, and stop states](visuals/bounded-loop.svg)",
                    "Visual Guidance: create a diagram later.",
                )
                .replace("## Check Your Work", "## Notes"),
                encoding="utf-8",
            )
            report = vcl.score_lesson(path, require_schema=3)

        self.assertFalse(report.publishable)
        self.assertTrue(any("real explanatory visual" in issue for issue in report.critical_issues))
        self.assertTrue(any("self-check criteria" in issue for issue in report.critical_issues))

    def test_missing_disclosure_and_metadata_block_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lesson.md"
            article = publishable_lesson().replace("author: Praveen Kumar\n", "").replace(
                "This article was developed with AI assistance and reviewed by the named author. ", ""
            )
            path.write_text(article, encoding="utf-8")
            report = vcl.score_lesson(path, require_schema=3)

        self.assertFalse(report.publishable)
        self.assertTrue(any("front-matter metadata" in issue for issue in report.critical_issues))
        self.assertTrue(any("AI assistance" in issue for issue in report.critical_issues))

    def test_manifest_can_declare_current_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lesson.md"
            article = publishable_lesson().replace("publishing_schema_version: 3\n", "")
            path.write_text(article, encoding="utf-8")
            path.with_suffix(".json").write_text(
                '{"publishing_schema_version": 3}\n', encoding="utf-8"
            )
            self.assertEqual(vcl.schema_version(path, path.read_text()), 3)

    def test_invalid_platform_metadata_blocks_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "lesson.md"
            article = (
                publishable_lesson()
                .replace("slug: bounded-tool-using-agent", "slug: Not Portable")
                .replace("tags: agents, python, testing, ai", "tags: one, two, three, four, five")
                .replace("last_verified: 2026-09-01", "last_verified: September 1")
            )
            path.write_text(article, encoding="utf-8")
            report = vcl.score_lesson(path, require_schema=3)

        self.assertFalse(report.publishable)
        self.assertTrue(any("one to four" in issue for issue in report.critical_issues))
        self.assertTrue(any("kebab-case" in issue for issue in report.critical_issues))
        self.assertTrue(any("YYYY-MM-DD" in issue for issue in report.critical_issues))


if __name__ == "__main__":
    unittest.main()
