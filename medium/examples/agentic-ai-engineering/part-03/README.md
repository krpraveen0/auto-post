# Part 03: Minimal Tool-Using Agent

This provider-neutral example makes the host-side tool loop testable without a
model API or API key. A scripted model proposes the same structured decisions a
provider adapter would normalize: tool calls or a final response.

## Environment

- Python 3.12.13
- jsonschema 4.26.0
- Verified on macOS on 2026-09-05
- CI contract: Ubuntu with dependencies from `requirements.txt`

## Run

```bash
.venv/bin/python medium/examples/agentic-ai-engineering/part-03/tool_loop.py success
.venv/bin/python medium/examples/agentic-ai-engineering/part-03/tool_loop.py invalid
.venv/bin/python -m unittest discover -s medium/examples/agentic-ai-engineering/part-03 -v
```

The success scenario calls `read_release_notes`, calls `read_test_summary`, and
then returns a final answer in three model decisions. The invalid scenario sends
`release` instead of the required `release_id`; the loop records a schema error,
replays the identical failed result for the repeated call ID, and then returns a
bounded final response.

No command in this example contacts a model provider or external service.
