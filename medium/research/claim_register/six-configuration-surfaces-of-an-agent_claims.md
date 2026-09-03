# Claim Register: The Six Configuration Surfaces of an Agent

Verified: 2026-09-03

## Claim 1

Claim: Prompting behavior can change across model snapshots; pinned versions and
evals improve reproducibility.

Source: [OpenAI API: Backward Compatibility](https://platform.openai.com/docs/api-reference/backward-compatibility)

Source type: Official API documentation

Confidence: High for OpenAI API models

Safe wording: OpenAI states that prompting behavior may differ between snapshots
and recommends pinned model versions with evals for consistency.

Risk if overstated: Assuming pinning removes inherent output variability

Use in article: Support the model behavior-envelope explanation

## Claim 2

Claim: Runtime checks may apply at agent input/output boundaries and around each
custom function-tool invocation.

Source: [OpenAI Agents SDK: Guardrails](https://openai.github.io/openai-agents-python/guardrails/)

Source type: Official SDK documentation

Confidence: High for the documented SDK

Safe wording: The SDK distinguishes input, output, and tool guardrails, with
documented workflow-boundary limitations.

Risk if overstated: Implying the same pipeline covers every hosted tool or handoff

Use in article: Explain why runtime guardrails are a separate surface

## Claim 3

Claim: JSON Schema can require object properties and reject unrecognized fields
with `additionalProperties: false`.

Source: [JSON Schema: Object Validation](https://json-schema.org/understanding-json-schema/reference/object)

Source type: Primary specification documentation

Confidence: High

Safe wording: A schema can require named properties and reject additional fields;
the schema must also declare expected types to constrain the instance correctly.

Risk if overstated: Confusing structural validity with safe agent behavior

Use in article: Support configuration validation and the tested example

## Claim 4

Claim: Semantic Versioning applies to software with a declared public API.

Source: [Semantic Versioning 2.0.0](https://semver.org/)

Source type: Primary specification

Confidence: High

Safe wording: Define an agent configuration compatibility contract before
adapting major/minor/patch semantics.

Risk if overstated: Treating every prompt edit as a SemVer-compatible API change

Use in article: Add nuance to the configuration-versioning recommendation

## Claim 5

Claim: Production generative-AI systems should treat evaluation and
observability as continuous architectural concerns rather than late additions.

Sources: [Chip Huyen: Building a Generative AI Platform](https://huyenchip.com/2024/07/25/genai-platform.html)
and [Eugene Yan: Patterns for Building LLM-based Systems and Products](https://eugeneyan.com/writing/llm-patterns/)

Source type: Experienced-practitioner synthesis grounded in research and
production examples

Confidence: High as engineering guidance, not as a universal implementation law

Safe wording: Use staged evaluation and observability to make behavior-changing
configuration releases inspectable; adapt the exact ladder to the application.

Risk if overstated: Claiming one rollout sequence fits every risk level or that
offline evaluation guarantees production behavior

Use in article: Support the release-evidence ladder and the separation of static,
component, behavioral, shadow, and canary evidence

## Claim 6

Claim: The checked-in resolver rejects unauthorized production overrides,
invalid collection and memory element types, unknown schema fields, and a
mutating allowed tool under a deny policy; it also produces a stable resolved
configuration hash.

Source: [Part 02 executable tests](../../examples/agentic-ai-engineering/part-02/test_resolve_config.py)

Source type: Original reproducible experiment

Confidence: High for the checked-in fixtures and dependency versions

Safe wording: Six tests passed with Python 3.12.13, PyYAML 6.0.3, and jsonschema
4.26.0 on 2026-09-03. The example verifies resolution mechanics, not model
quality or production permission enforcement.

Risk if overstated: Treating configuration validation as behavioral evaluation
or security proof

Use in article: Support the strict-merge, schema, cross-field policy, exact
version binding, and tested-environment sections
