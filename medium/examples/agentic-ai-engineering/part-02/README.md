# Part 02: Resolved Agent Configuration

This example resolves a base manifest plus a constrained production overlay,
binds aliases to exact component versions, validates the result against JSON
Schema, checks cross-field policy, and emits a deterministic release record.

Run from the repository root after installing `requirements.txt`:

```bash
python -m unittest discover -s medium/examples/agentic-ai-engineering/part-02 -v
python medium/examples/agentic-ai-engineering/part-02/resolve_config.py \
  medium/examples/agentic-ai-engineering/part-02/base-config.yaml \
  medium/examples/agentic-ai-engineering/part-02/production-overlay.yaml
```

The unsafe overlay is deliberately rejected because it attempts to replace a
security-sensitive tool policy.
