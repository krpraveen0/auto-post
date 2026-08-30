# Daily DOCX Automation

This repository includes a GitHub Actions workflow that generates one Medium course lesson per day as Markdown and DOCX.

## Schedule

Workflow: `.github/workflows/daily-medium-course-docx.yml`

Cron: `30 0 * * *`

Local time: 06:00 Asia/Kolkata

GitHub Actions cron expressions use UTC. Asia/Kolkata does not observe daylight-saving time, so `00:30 UTC` maps to `06:00 Asia/Kolkata` throughout the year. The workflow also uses a concurrency group so a delayed run cannot overlap the next daily generation.

## Required Secret

Add this repository secret in GitHub:

```text
OPENAI_API_KEY
```

The workflow uses OpenAI generation to draft each lesson. The current default is `GENERATION_BACKEND=agents` with `gpt-5.6-terra`.

The workflow supports two generation backends:

- `GENERATION_BACKEND=agents` uses the OpenAI Agents SDK for draft, technical review, continuity review, and final edit orchestration.
- `GENERATION_BACKEND=responses` uses the direct Responses API call as the rollback path.

## What The Workflow Does

1. Reads `medium/course_series/agentic-ai-engineering-map.md`.
2. Finds the next lesson from `medium/course_series/agentic-ai-engineering-state.json`.
3. Uses live web search to build a primary-source evidence brief, then generates and reviews a Medium-ready lesson.
4. Writes Markdown and DOCX files under `medium/generated/agentic-ai-engineering/`.
5. Rejects unresolved source markers, fewer than two primary-source links, missing required sections, and lessons outside the configured length range.
6. Fetches every evidence URL during the scheduled run and fails if a source is not reachable.
7. Statically checks and executes each self-contained Python example in an isolated interpreter with a five-second timeout.
8. Extracts the required explanatory Mermaid infographic and renders it to SVG, preserving its caption and alt text in the article.
9. Renders the DOCX to PDF and PNG pages with LibreOffice and Poppler.
10. Uploads the DOCX, Markdown, manifest, validation report, Mermaid source, SVG, PDF, and rendered pages as workflow artifacts.
11. Commits generated files and state back to the repository only after every validation succeeds.
12. Opens a GitHub issue with the daily article details.

The automated checks prove that source URLs were reachable at generation time, Python examples ran successfully, Mermaid syntax rendered, and the structural quality contract passed. They do not replace editorial judgment about whether a source truly supports every sentence or whether a diagram is the clearest possible explanation; the publishing workflow still requires the human review gate.

## End Of Series Behavior

When the final lesson is complete, the workflow opens a GitHub issue asking for the next series topic, target reader, starting skill level, final learner outcome, and preferred lesson count. It records that notification in the state file so the request is not repeated every day.

## Manual Run

Use GitHub Actions -> Daily Medium Course DOCX -> Run workflow.

Use `dry_run=true` to validate DOCX generation, rendering, and artifact upload without consuming OpenAI API credits.
