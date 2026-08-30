# Agents SDK Migration Notes

## Decision

The daily course pipeline uses a partial Agents SDK migration. Deterministic scheduling, state files, DOCX writing, rendering, commits, artifacts, and GitHub issues remain in Python and GitHub Actions. Lesson generation uses `GENERATION_BACKEND=agents` by default, with `GENERATION_BACKEND=responses` retained as the rollback path.

## Current Backends

- `responses`: direct HTTP call to `/v1/responses`.
- `agents`: code-sequenced Agents SDK workflow.
- `--dry-run`: deterministic local/cloud validation without OpenAI API calls.

## Agents

- Course lesson draft agent
- Technical reviewer agent
- Course continuity reviewer agent
- Publishing editor agent
- Course generation manager with handoff definitions for future interactive routing

The scheduled job uses code-driven orchestration to preserve predictable daily output. Handoffs are defined on the manager but not used as the primary cron control path.

## Tracing

Agent runs use workflow name `Daily Medium Course DOCX` and group IDs shaped like `agentic-ai-engineering:part-01`. Set `OPENAI_AGENTS_DISABLE_TRACING=1` to disable trace export.

## Rollback

Set this workflow environment variable:

```yaml
GENERATION_BACKEND: responses
```

No DOCX, render, artifact, state, or notification code needs to change.

## Validation

Run locally:

```bash
.venv/bin/python -m unittest discover -s tests
GITHUB_OUTPUT=/tmp/out.txt .venv/bin/python scripts/daily_course_article.py \
  --series-map medium/course_series/agentic-ai-engineering-map.md \
  --series-slug agentic-ai-engineering \
  --state-file /tmp/agentic-state.json \
  --out-dir /tmp/agentic-out \
  --backend agents \
  --dry-run
```

Run cloud E2E without API usage:

```bash
gh workflow run daily-medium-course-docx.yml --ref master -f dry_run=true
```

Run production E2E:

```bash
gh workflow run daily-medium-course-docx.yml --ref master
```
