# Claim Register: What Makes an AI Agent Different from a Chatbot?

Verified: 2026-09-03

## Claim 1

Claim: Workflows follow predefined code paths, while agents let a model
dynamically direct process and tool use.

Source: [Anthropic: Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)

Source type: Official engineering guidance

Confidence: High for Anthropic's stated architectural distinction

Safe wording: Anthropic distinguishes workflows with predefined code paths from
agents whose models dynamically direct their processes and tool usage.

Risk if overstated: Presenting one vendor's distinction as a universal standard

Use in article: Explain why the course uses an operational, traceable definition

## Claim 2

Claim: Agent configuration commonly includes instructions, tools, model settings,
guardrails, handoffs, and structured outputs.

Source: [OpenAI Agents SDK: Agents](https://openai.github.io/openai-agents-python/agents/)

Source type: Official SDK documentation

Confidence: High for the documented SDK

Safe wording: OpenAI's Agents SDK exposes these as configurable agent/runtime
surfaces; other frameworks may organize them differently.

Risk if overstated: Treating an SDK's object model as a universal agent definition

Use in article: Show that a prompt alone does not define deployed behavior

## Claim 3

Claim: Agentic tool use should be constrained through least privilege, permission
and context validation, and human oversight for high-risk operations.

Source: [OWASP: LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

Source type: Security guidance

Confidence: High as defense-in-depth guidance

Safe wording: OWASP recommends these controls as layers of defense; none alone
eliminates prompt-injection risk.

Risk if overstated: Claiming prompt injection is solved by sanitization or one
guardrail

Use in article: Support the outer-boundary and untrusted-tool-output guidance

## Claim 4

Claim: Agent definitions may use the broad environment-and-actions frame, while
application engineering guidance may distinguish fixed workflows from
model-directed runtime control.

Sources: [Chip Huyen: Agents](https://huyenchip.com/2025/01/07/agents.html) and
[Anthropic: Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)

Source type: Experienced-practitioner synthesis plus official engineering guidance

Confidence: High that the sources use different but overlapping operational frames

Safe wording: Definitions vary by analytical purpose; declare the operational
definition and expose the control graph instead of claiming universal terminology.

Risk if overstated: Presenting either definition as the only accepted meaning of
agent or misrepresenting a fixed retrieval pipeline as universally non-agentic

Use in article: Explain why the course deliberately uses runtime control
ownership to distinguish workflows from bounded agents

## Claim 5

Claim: Retried mutating operations need an explicit idempotency contract because
a timeout can leave the caller uncertain whether the side effect occurred.

Source: [AWS Builders' Library: Making Retries Safe with Idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Source type: Primary institutional engineering guidance

Confidence: High for the distributed-systems pattern described

Safe wording: Caller-provided request identifiers and a correctly implemented
service contract can make retries auditable and prevent duplicate side effects.

Risk if overstated: Claiming an idempotency key alone guarantees exactly-once
execution across every failure mode

Use in article: Support the partial-write and unknown-outcome failure analysis

## Claim 6

Claim: Traces, metrics, and logs provide different observability signals.

Source: [OpenTelemetry: Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/)

Source type: Primary open observability documentation

Confidence: High

Safe wording: Metrics aggregate measurements, logs record events, and traces
connect execution paths; useful agent diagnostics correlate these signals.

Risk if overstated: Suggesting that telemetry alone proves correctness or that
every private model-internal thought should be recorded

Use in article: Define the minimum operational trace without requesting hidden
chain-of-thought

## Claim 7

Claim: The lesson's reference state machine stops on denial or exhausted step
budget, waits for a matching approval, rejects unverified completion, and reuses
one operation identifier after an unknown mutation outcome.

Source: [Part 01 executable tests](../../examples/agentic-ai-engineering/part-01/test_bounded_agent.py)

Source type: Original reproducible experiment

Confidence: High for the checked-in deterministic implementation

Safe wording: Seven tests passed with Python 3.12.13 on 2026-09-03; the example
demonstrates control-state behavior and does not implement production identity,
storage, or distributed transaction guarantees.

Risk if overstated: Treating an instructional state machine as a production
authorization service

Use in article: Support the worked state transitions, expected trace, tested
environment, and explicit implementation limitations
