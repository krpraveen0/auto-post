# Codex Daily Medium Course Automation

Use this runbook to create a Codex Automation that writes one reviewed Medium course lesson every day without calling the OpenAI API from the repository workflow.

## Automation Settings

Name: `Daily Medium Course DOCX`

Schedule: `06:00 Asia/Kolkata`, every day

Repository: `krpraveen0/auto-post`

Branch: `master`

Expected output mode: Codex review queue or pull request branch named `codex/daily-medium-course-part-XX`.

## Automation Prompt

```text
You are working in krpraveen0/auto-post.

Do not call api.openai.com and do not require OPENAI_API_KEY. Use this Codex automation session to author the content.

Every run:
1. Read AGENTS.md, README-agent-skills.md if present, .github/instructions/, and the relevant .github/skills/ Medium writing skills.
2. Read medium/course_series/agentic-ai-engineering-map.md and medium/course_series/agentic-ai-engineering-state.json.
3. Select the next lesson from next_part. If the state file is missing, start at part 1.
4. If next_part is greater than the lesson count, do not generate an article. Open or prepare a review item asking for the next series topic, target reader, starting skill level, learner outcome, and lesson count.
5. Draft exactly one complete Medium lesson in Markdown for the selected part.
6. Create matching .md, .docx, and .json manifest files under medium/generated/agentic-ai-engineering/.
7. Update medium/course_series/agentic-ai-engineering-state.json only after the Markdown, DOCX, manifest, and validation checks pass.
8. Run .venv/bin/python -m unittest discover -s tests. If .venv is missing, create it and install requirements.txt first.
9. Run .venv/bin/python scripts/validate_generated_docx.py --root medium/generated/agentic-ai-engineering --render when LibreOffice and Poppler are available. If rendering tools are unavailable, still run archive validation and explain the missing renderer in the review summary.
10. Commit changes to a Codex review branch or open a pull request. Do not push directly to master.

Quality bar:
- Target 1400-2200 words.
- Teach one primary concept deeply.
- Include Learning Outcomes, Worked Example, Exercise, Recap, and Next Lesson.
- Include previous/course index/next navigation near the top.
- Include concrete expected output for the exercise.
- Include visual guidance with caption and alt text.
- Mark claims needing verification with [SOURCE NEEDED: short note].
- Do not invent URLs, citations, benchmarks, or product claims.
- Preserve continuity with earlier generated lessons and the course map.
```

## Validation

Codex output should pass the `Validate Medium Output` GitHub workflow on pull requests. That workflow runs unit tests, checks each generated DOCX is a valid Office archive, and renders DOCX pages to PNG when LibreOffice and Poppler are available.

The existing `Daily Medium Course DOCX` GitHub Action remains as an API-backed fallback and dry-run validator. Use `dry_run=true` there to test rendering without consuming API credits.
