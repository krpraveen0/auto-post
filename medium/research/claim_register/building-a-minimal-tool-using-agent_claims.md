# Claim Register: Building a Minimal Tool-Using Agent

Verified: 2026-09-05

## Claim 1

Claim: For client-defined tools, the model returns a structured tool request and
the application executes the operation before sending a tool result back.

Source: [Anthropic: Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

Source type: Current official platform documentation

Confidence: High for the documented client-tool flow

Safe wording: In the documented client-tool flow, the model proposes a call; the
application executes it and returns a result for the next model turn.

Risk if overstated: Some providers also offer server-executed tools, so application
execution is not a universal description of every tool type.

Use in article: Establish the model-proposes, host-executes ownership boundary.

## Claim 2

Claim: Valid JSON is not the same as conformance to a specific tool schema.

Source: [OpenAI: Function Calling in the OpenAI API](https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api)

Source type: Current official platform documentation

Confidence: High for the documented distinction

Safe wording: JSON mode constrains syntax; a schema-aware mechanism or application
validator is still needed when arguments must match a particular shape.

Risk if overstated: Supported strict structured-output paths can provide schema
adherence for an accepted subset, but the application still owns authorization
and safe execution.

Use in article: Explain why parsing precedes, but does not replace, validation.

## Claim 3

Claim: JSON Schema can make properties required and reject additional object
properties when the schema declares the corresponding constraints.

Source: [JSON Schema: Object Validation](https://json-schema.org/understanding-json-schema/reference/object)

Source type: Primary specification documentation

Confidence: High

Safe wording: The example uses an object type, `required`, and
`additionalProperties: false` to reject a misspelled or unexpected argument.

Risk if overstated: Structural validity does not prove authorization, semantic
correctness, or harmless tool behavior.

Use in article: Support the failing `release` versus `release_id` trace.

## Claim 4

Claim: MCP's tool specification assigns validation, access control, rate limiting,
output sanitization, timeouts, result validation, auditing, and sensitive-action
confirmation responsibilities to servers and clients.

Source: [Model Context Protocol: Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

Source type: Primary protocol specification

Confidence: High for protocol revision 2025-06-18

Safe wording: The cited MCP revision lists these responsibilities as MUST or
SHOULD guidance; an application's exact enforcement design remains contextual.

Risk if overstated: Treating protocol guidance as proof that any particular MCP
client or server implements the controls correctly.

Use in article: Support the host-responsibility checklist and production boundary.

## Claim 5

Claim: The checked-in example validates arguments, limits steps and failures,
rejects unknown tools and call-ID collisions, and avoids re-executing an identical
repeated call ID.

Source: [Part 03 executable tests](../../examples/agentic-ai-engineering/part-03/test_tool_loop.py)

Source type: Original reproducible experiment

Confidence: High for the checked-in fixture and tested environment

Safe wording: Six deterministic tests passed with Python 3.12.13 and jsonschema
4.26.0 on macOS on 2026-09-05. The test does not measure model tool selection or
production authorization.

Risk if overstated: Confusing a local dispatcher test with end-to-end agent safety.

Use in article: Support the implementation, failure trace, and verification sections.
