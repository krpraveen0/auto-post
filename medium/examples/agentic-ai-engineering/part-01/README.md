# Part 01: Bounded Agent State Machine

This standard-library example makes the article's control boundary executable.
It does not call a model or an external service. Tests drive proposed actions so
the policy, state transitions, retry budget, and idempotency behavior remain
deterministic.

Run from the repository root:

```bash
python -m unittest discover -s medium/examples/agentic-ai-engineering/part-01 -v
python medium/examples/agentic-ai-engineering/part-01/bounded_agent.py
```

The demonstration prints JSON trace events. The test suite covers success,
approval, denial, failure exhaustion, unknown mutation outcomes, stable
operation IDs, and step-budget termination.
