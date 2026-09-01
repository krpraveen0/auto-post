# The Six Configuration Surfaces of an Agent

*Part 2 of Agentic AI Engineering: turn an agent boundary into configuration you can review, test, and version.*

**Series navigation:** Previous: Part 1 — What Makes an AI Agent Different from a Chatbot? | Course index: Agentic AI Engineering | Next: Part 3 — Building a Minimal Tool-Using Agent

The first agent configuration I reviewed looked reassuringly small. It had a system prompt, a model name, and a list of tools. The team could explain every line.

Then we tried to answer a simple release question: “What changed, and is it safe to deploy?”

The agent searched the wrong documents, remembered a decision from another project, called a write-capable tool before approval, and produced different answers after a model update. None of those failures lived in the prompt. The system’s behavior was spread across code, environment variables, database settings, and defaults that no reviewer could see in one place.

This is why an agent needs more than a prompt file. It needs a **configuration contract**: a versioned description of the six surfaces that shape its behavior—prompts, tools, model, retrieval, guardrails, and memory.

The six surfaces are not six independent knobs. They are six places where behavior can change. If you cannot point to the versioned value for each one, you cannot reliably explain which agent you tested or what changed between two releases.

## Learning Outcomes

By the end of this lesson, you will be able to:

1. Explain how prompts, tools, model settings, retrieval, guardrails, and memory each influence agent behavior.
2. Separate policy from implementation defaults so reviewers can see the agent’s real operating contract.
3. Draft a versioned configuration manifest that Part 3 can turn into a minimal tool-using agent.

## Start with the Boundary Card

Part 1 ended with a boundary card: what the agent may observe, which actions it may take, what it may retain, when approval is required, and how it stops. That card describes intent. Configuration makes the intent executable and reviewable.

Suppose the boundary says, “The agent may read release notes and test results, but it must not promote a build without approval.” That sentence touches several surfaces at once:

- The prompt must tell the agent to distinguish analysis from authorization.
- The tool list must expose read operations and either omit promotion or place it behind an approval mechanism.
- Retrieval must restrict evidence to the correct project and release.
- Guardrails must reject an unapproved promotion request even if the model asks for it.
- Memory must not carry approval from a previous release.

If the restriction exists only in prose, the rest of the system can quietly disagree with it. A configuration contract forces the agreement into view.

## Surface 1: Prompts Define the Task Policy

Prompts describe the agent’s role, priorities, definitions, and response rules. They should answer questions such as: What does “done” mean? When should the agent ask for clarification? How should it report uncertainty? Which evidence belongs in the final answer?

Prompts are good at expressing judgment. They are a poor substitute for permissions. “Never deploy without approval” is useful instruction, but it is not an access-control system. Keep that instruction because it helps the model choose correctly; enforce the same rule outside the model because instructions can be misread, displaced by context, or contradicted by untrusted content. [SOURCE NEEDED: primary guidance on prompt injection and enforcing authorization outside model instructions.]

Store prompts as named, versioned assets rather than long strings embedded in application code. A reviewer should be able to compare `release-analyst-v2` with `release-analyst-v3` without searching through a request handler.

## Surface 2: Tools Define the Action Space

A tool is not merely a function the model can call. Its schema, credentials, validation, timeout, and side effects define what an agent can actually do.

The tool surface should record:

- a stable tool name and purpose;
- its input schema and validation rules;
- whether it is read-only or mutating;
- the credential scope used by the surrounding application;
- timeout, retry, and idempotency behavior;
- approval requirements and audit expectations.

Prefer narrow tools over general ones. `read_test_summary(release_id)` gives the agent less room to make a dangerous mistake than `run_shell(command)`. The narrower tool also produces a clearer trace: you know what operation was intended and which identifier controlled it.

In Part 3, we will implement the tool-call loop. For now, the important move is to treat the allowed tool set as a release artifact, not an incidental list assembled at runtime.

## Surface 3: The Model Defines a Behavior Envelope

The model surface includes the model identifier plus settings that affect generation, such as temperature, token limits, reasoning mode, and structured-output requirements when the provider supports them.

This surface is best understood as a **behavior envelope**, not a personality switch. A model change can alter tool selection, instruction following, latency, cost, context capacity, or output shape. Exact effects depend on the model and evaluated task, so test them rather than assuming that a newer model is a drop-in replacement. [SOURCE NEEDED: primary model documentation for versioning, snapshots, and parameter behavior used by the chosen provider.]

Record the exact identifier accepted by your provider, not a team nickname such as `smart-model`. Also record the fallback policy. An invisible fallback can make an incident hard to reproduce because the configured model and the model that handled the request are different facts.

## Surface 4: Retrieval Defines the Evidence Window

Retrieval determines which external knowledge enters the agent’s working context. Its configuration includes source collections, filters, query strategy, result count, ranking or reranking, freshness rules, and citation requirements.

This surface is easy to hide behind one boolean: `rag_enabled: true`. That tells a reviewer almost nothing. Which repository? Which tenant? Which release? How old may a document be? What happens when results conflict or nothing relevant is found?

For our release analyst, retrieval should filter by project and release ID before semantic ranking. A semantically similar postmortem from another project may look relevant while being operationally wrong. Retrieval controls the evidence window; it does not guarantee that the evidence is true or sufficient.

Keep “no supporting evidence found” as a valid result. An agent that must always answer will often turn a retrieval miss into confident prose.

## Surface 5: Guardrails Enforce Runtime Policy

Guardrails are checks around the model and tools. They can validate inputs, reject unsafe tool arguments, limit budgets, require approval, inspect outputs, or stop a run after repeated failures.

Some guardrails are deterministic: a release ID must match a known pattern; a promotion tool requires an approval token; the agent may take no more than eight steps. Others may use classifiers or models and therefore need their own evaluation and failure policy.

Keep hard authorization rules deterministic whenever possible. The model may recommend an action, but application code should decide whether the caller and the current task are allowed to perform it. A denied action should become an observation the agent can report, not an invitation to find a less visible path.

## Surface 6: Memory Defines What Survives

Memory is the information that persists beyond the immediate model call. It may include structured task state, a short session summary, user preferences, or durable facts approved for later reuse.

The useful question is not “Does the agent have memory?” It is “Which facts survive, for how long, under which identity and scope?”

Separate at least three lifetimes:

1. **Step state** lasts inside one tool-use loop, such as the current release ID and remaining budget.
2. **Session state** lasts for the current task, such as documents already inspected and unresolved checks.
3. **Durable memory** survives across tasks, such as an approved preference or a stable project convention.

Do not place approvals, temporary permissions, or unverified retrieved claims in durable memory. For the release analyst, “release 2.4 was approved” must not become authority for release 2.5.

## Worked Example

We will configure a bounded release analyst. Its job is to inspect a release candidate, summarize changes and test evidence, and prepare a recommendation. It may not deploy anything.

Here is a compact manifest:

```yaml
schema_version: 1
agent_id: release-analyst
config_version: 0.2.0

prompt:
  id: release-analyst-v2
  success_definition: evidence-backed recommendation produced

model:
  id: provider-model-snapshot
  temperature: 0
  max_output_tokens: 1800
  fallback: none

tools:
  allow:
    - read_release_notes
    - read_test_summary
    - request_clarification
  deny:
    - promote_release

retrieval:
  collections: [release-notes, test-reports]
  required_filters: [project_id, release_id]
  max_results: 8
  require_evidence_for_claims: true

guardrails:
  max_steps: 8
  max_tool_failures: 2
  mutation_policy: deny
  on_missing_evidence: report_unknown

memory:
  step: [project_id, release_id, remaining_steps]
  session: [documents_read, open_questions]
  durable: []
```

Trace one request through the surfaces: “Review release 2.5 for Project North.” The prompt defines a recommendation—not deployment—as success. The model may choose which read tool to call first. The tool allow-list gives it only three possible actions. Retrieval filters prevent Project South documents from entering the evidence set. Guardrails stop the run after eight steps or two tool failures. Memory keeps the release ID during the task but preserves nothing afterward.

Now imagine changing only `mutation_policy` from `deny` to `approval_required` and adding `promote_release` to the tool list. That is not a minor configuration cleanup. It expands the action boundary and should trigger security review, new tests, and a deliberate version change.

A readable diff is the point. When behavior is separated into surfaces, reviewers can ask the right question for each change instead of re-reading one enormous prompt and hoping the important behavior is inside it.

## Treat Configuration Changes Like Code Changes

Use a stable schema and validate it before the agent starts. Reject unknown fields rather than silently ignoring a misspelled guardrail. Record the resolved configuration with each run so a trace can answer, “Which prompt, model, tool set, retrieval policy, guardrails, and memory policy produced this result?”

Version numbers do not remove the need for judgment, but they make judgment visible. A wording correction may be a patch. Adding a read-only tool may be a minor change. Adding a mutating tool or widening memory scope may deserve a major version and a fresh risk review. Your exact policy can differ; consistency matters more than copying a numbering convention.

Secrets do not belong in the manifest. Store credential references, not credential values. The manifest should say which identity or secret binding a tool expects while the deployment environment supplies the secret.

## Visual Guidance

Create a **configuration surface diagram** with a bounded agent loop in the center and six surrounding panels: Prompt Policy, Tool Action Space, Model Envelope, Retrieval Evidence Window, Runtime Guardrails, and Memory Lifetimes. Connect each panel to the loop. Add a version tag around the complete configuration and show a run trace recording the resolved value from every surface.

**Caption:** An agent release is the combined, versioned state of six behavior surfaces—not just a prompt and model name.

**Alt text:** Diagram of an agent loop surrounded by six configuration panels for prompts, tools, model, retrieval, guardrails, and memory, all enclosed by one version boundary and recorded in a run trace.

## Exercise

Take the boundary card you created in Part 1 and convert it into `agent-config.yaml`. Use the worked example as a shape, but replace its values with your agent’s actual goal and limits.

Your manifest must include:

1. one prompt identifier and a one-line success definition;
2. one exact model identifier plus explicit generation settings;
3. an allow-list of two or three narrow tools, marking any mutating tool;
4. retrieval sources, filters, result limits, and missing-evidence behavior;
5. at least three deterministic guardrails, including a step limit;
6. separate step, session, and durable memory fields;
7. a schema version and configuration version.

Then write a five-line change note for one hypothetical update. Name the surface changed, the old value, the new value, the risk introduced, and the validation required.

**Expected output:** one valid YAML file and one Markdown change note. A strong submission makes every Part 1 boundary visible, contains no secrets, denies or gates mutating actions, scopes retrieval by task identity, keeps temporary approval out of durable memory, and identifies which tests must run before the changed configuration is released.

Keep both files. Part 3 will load this manifest, expose three local tools, and implement the smallest useful tool-call loop around it.

## Recap

An agent’s behavior comes from six configuration surfaces: prompts define task policy, tools define possible actions, the model defines a behavior envelope, retrieval defines the evidence window, guardrails enforce runtime policy, and memory defines what survives.

Treat the six surfaces as one versioned contract. Validate its schema, record the resolved configuration with each run, and review boundary-expanding changes with the seriousness you would apply to code that receives new permissions.

The prompt still matters. It simply stops carrying responsibilities it cannot safely enforce.

## Next Lesson

Part 3, **Building a Minimal Tool-Using Agent**, turns this manifest into code. We will define three narrow tool schemas, execute a tool-call loop, feed results back into state, and stop without hiding failures.

**Series navigation:** Previous: Part 1 — What Makes an AI Agent Different from a Chatbot? | Course index: Agentic AI Engineering | Next: Part 3 — Building a Minimal Tool-Using Agent
