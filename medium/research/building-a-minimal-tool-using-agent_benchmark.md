# Competitive Content Benchmark: Building a Minimal Tool-Using Agent

Search date: 2026-09-05

Reviewer: Codex course editorial workflow

Reader job: Understand and implement the host-side protocol that turns a model's
structured tool request into a validated result and another bounded model turn.

## Strong Existing Resources

| Resource | Intended reader | What it explains well | What remains difficult or missing | Evidence quality |
|---|---|---|---|---|
| [Anthropic: Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) | Developers using client and server tools | Shows schemas, `tool_use`, application execution, `tool_result`, and the follow-up model call | Provider-specific message shapes can hide the provider-neutral host responsibilities and failure policy | Current official platform documentation |
| [OpenAI: Function Calling in the OpenAI API](https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api) | Developers connecting models to application functions | Separates JSON validity from schema adherence and documents strict structured arguments on supported paths | Does not provide a complete local, deterministic dispatcher with replay and stop-budget tests | Current official platform documentation |
| [Model Context Protocol: Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) | Client and server implementers | Defines named tools with input schemas and states validation, access-control, timeout, result-validation, audit, and human-control guidance | It is a protocol specification, not a small end-to-end teaching implementation | Primary protocol specification |
| [JSON Schema: Object Validation](https://json-schema.org/understanding-json-schema/reference/object) | Developers validating JSON objects | Explains `required`, object types, and control of additional properties | Does not connect object validation to an agent execution boundary or trace | Primary specification documentation |
| [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | Engineers choosing agent patterns | Starts with simple composable patterns and characterizes agents as models using tools in a feedback loop | Leaves the low-level dispatcher and replay behavior to implementations or frameworks | Official engineering guidance; December 2024 article carries a current-update note |

## Explanatory Architecture

| Resource | Opening and reader promise | How complexity is staged | Examples and visuals | Failures and trade-offs |
|---|---|---|---|---|
| Anthropic tool-use documentation | Starts with where client and server tools execute | Schema, model call, application execution, result, follow-up | Weather example plus complete message round trip | Links to error signaling and parallel-call variants |
| OpenAI function-calling guidance | Starts with connecting models to external systems | Function calls, structured outputs, JSON mode boundaries | Short use-case list and API behavior notes | Distinguishes valid JSON from schema conformance and calls out edge cases |
| MCP tools specification | Starts with protocol capability and user control | Discovery, invocation, results, safety responsibilities | Concrete JSON-RPC messages | Explicit validation, authorization, timeout, sanitization, and audit guidance |
| JSON Schema object documentation | Starts from object properties | Types, properties, required keys, extras, conditional structure | Valid and invalid JSON instances | Shows why declared properties alone do not make them required |
| Building Effective Agents | Starts by arguing for simple composable patterns | Single calls, workflows, augmented models, agents | Pattern diagrams and practical guidance | Notes latency/cost trade-offs and framework abstraction costs |

Transferable pattern: Show the complete round trip before adding abstractions,
then place validation and stopping at the boundary where they are enforced.
Keep provider message formats at the adapter edge and make failure results part
of the same trace as successful results.

## Original Contribution

Contribution selected: A reproducible implementation plus failure analysis.

The lesson provides a provider-neutral `ToolLoop` that can be tested without an
API key. A scripted adapter produces structured decisions; the host validates a
closed registry, checks JSON Schema arguments, converts exceptions into result
data, replays repeated call IDs without re-executing the handler, rejects call-ID
collisions, counts failures, and enforces a step budget. Six tests demonstrate
both accepted and rejected paths.

After the existing resources, a reader can recognize the standard tool-call
round trip. After this lesson, the reader can additionally point to the exact
line where authority changes hands, reproduce success and failure traces, and
test host policy independently from model quality or provider availability.

## Decision

Proceed. The provider-neutral execution harness, deterministic trace, replay
protection, and bounded failure fixtures add defensible implementation value
without copying another resource's voice, example, or section order.
