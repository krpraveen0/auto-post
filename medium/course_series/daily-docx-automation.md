# Daily DOCX Automation

This repository includes a GitHub Actions workflow that generates one Medium course lesson per day as Markdown and DOCX.

## Schedule

Workflow: `.github/workflows/daily-medium-course-docx.yml`

Cron: `30 0 * * *`

Local time: 06:00 Asia/Kolkata

## Required Secret

Add this repository secret in GitHub:

```text
OPENAI_API_KEY
```

The workflow uses the OpenAI Responses API to draft each lesson. The default model is set in the workflow as `gpt-5`.

## What The Workflow Does

1. Reads `medium/course_series/agentic-ai-engineering-map.md`.
2. Finds the next lesson from `medium/course_series/agentic-ai-engineering-state.json`.
3. Generates a Medium-ready lesson.
4. Writes Markdown and DOCX files under `medium/generated/agentic-ai-engineering/`.
5. Renders the DOCX to PDF and PNG pages with LibreOffice and Poppler.
6. Uploads the DOCX, Markdown, manifest, PDF, and rendered pages as workflow artifacts.
7. Commits generated files and state back to the repository.
8. Opens a GitHub issue with the daily article details.

## End Of Series Behavior

When the final lesson is complete, the workflow opens a GitHub issue asking for the next series topic, target reader, starting skill level, final learner outcome, and preferred lesson count. It records that notification in the state file so the request is not repeated every day.

## Manual Run

Use GitHub Actions -> Daily Medium Course DOCX -> Run workflow.
