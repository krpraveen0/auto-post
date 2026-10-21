# Course Lesson Plan

Series: Agentic AI Engineering

Part number: 3

Lesson title: Building a Minimal Tool-Using Agent

Target reader: Software engineers and AI builders who completed Parts 1 and 2
and can read Python and JSON.

Reader state before this lesson: The reader has an agent boundary and a versioned
configuration but has not implemented the host-side tool-call loop.

Reader state after this lesson: The reader can build and test a bounded loop that
normalizes model decisions, validates tool arguments, executes allow-listed local
functions, returns structured results, and stops visibly.

Prerequisites: Parts 1 and 2; Python 3.12; basic JSON Schema familiarity.

## Backward Design

| Observable outcome | Evidence of learning |
|---|---|
| Trace the five transitions in a tool-call loop | Annotated success transcript |
| Implement a provider-neutral tool registry and dispatcher | Runnable `ToolLoop` with three local tools |
| Reject malformed, unknown, duplicated, and excessive calls | Six deterministic tests plus visible failure trace |
| Explain which responsibilities belong to the model versus the host | Exercise design note and transfer prompt |

## Angle Strategy

Central promise: Replace the vague instruction “let the model use tools” with an
inspectable host loop whose decisions, validations, results, and stop reasons can
be reproduced without a model API.

Recommended angle: The model proposes actions; the host owns authority. Teach the
boundary by building and testing the loop rather than starting from a framework.

What this article is not: A comparison of agent frameworks or a claim that one
provider's function-calling format is universal.

### Title Options

| Title | Clarity | Curiosity | Specificity | Promise | Honesty | Fit | Total / 60 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Building a Minimal Tool-Using Agent | 10 | 7 | 9 | 9 | 10 | 10 | 55 |
| The Five Transitions Behind Every Tool Call | 9 | 9 | 9 | 9 | 9 | 9 | 54 |
| Your Model Does Not Execute Tools—Your Application Does | 10 | 9 | 9 | 9 | 10 | 9 | 56 |
| Build the Smallest Tool Loop You Can Actually Test | 9 | 9 | 10 | 10 | 10 | 9 | 57 |
| From Tool Schema to Tool Result in Python | 9 | 7 | 10 | 9 | 10 | 9 | 54 |
| A Provider-Neutral Tool Loop with Visible Failures | 9 | 8 | 10 | 10 | 10 | 9 | 56 |
| Stop Hiding Tool Calls Inside a Framework | 8 | 9 | 8 | 8 | 8 | 8 | 49 |
| The Host-Side Contract of an AI Agent | 8 | 8 | 8 | 8 | 10 | 9 | 51 |
| How an Agent Turns a Model Decision into an Action | 10 | 8 | 9 | 9 | 10 | 9 | 55 |
| Build, Validate, Execute, Observe, Repeat | 8 | 8 | 7 | 8 | 10 | 8 | 49 |

Course continuity selects the map title, “Building a Minimal Tool-Using Agent.”
The subtitle and opening carry the sharper host-authority angle.

Subtitle options:

1. Implement the host loop that turns structured model requests into bounded, observable local actions.
2. Give a model three local tools without giving it direct execution authority.
3. Validate every proposed action, record every result, and stop on explicit budgets.
4. Learn the agent loop by replacing a provider call with a deterministic script.
5. Build the tool boundary you will extend with retries and reasoning state.

Opening hooks:

1. A model returned perfect JSON, yet the application still executed the wrong operation.
2. “The model called the function” is convenient shorthand that hides the most important owner in the system.
3. The first useful agent loop can fit on one screen; the dangerous assumptions around it usually do not.

## Lesson Shape

Primary concept: A tool-using agent is a controlled protocol loop. The model
proposes a structured decision; the host validates, authorizes, executes, records,
and decides whether another model turn is allowed.

Worked example: A release analyst reads release notes and a test summary from an
in-memory data source. A scripted model adapter makes the exact decisions so the
host loop can be tested without network or provider variance.

Common mistake: Dispatching by dynamically resolving an arbitrary model-provided
name or passing unvalidated arguments directly to a handler.

Tradeoff: A small explicit dispatcher contains more visible ceremony than a
framework helper, but it reveals authority, trace shape, replay behavior, and
stop policy before abstraction is added.

Exercise: Add `read_risk_register(release_id)` and make the scripted model use it
before answering. Add one valid-path test and one malformed-argument test.

Expected output: A four-step completed trace containing three successful,
non-replayed tool results and a final answer that includes the risk count.

## Evidence and Visuals

Claims to validate: Client tool execution occurs in the application; tool
descriptions include input schemas; JSON Schema can require and reject fields;
MCP guidance assigns validation, access control, timeout, result validation, and
audit responsibilities outside the model.

Required diagram: Tool-call sequence separating model proposals from host-owned
validation, execution, trace append, failure accounting, and stopping.

Caption: The model proposes the next move; the host controls whether and how it executes.

Alt text: Sequence diagram showing a task sent to a model, a structured tool call
returned to the host, schema and allow-list validation, local tool execution,
the tool result appended to the trace, and either another model turn or a stop.

## Continuity

Previous lesson recap: Part 2 defined a versioned allow-list, schemas, and bounded
policies. Part 3 makes the tool surface executable.

Next lesson bridge: Part 4 will replace the fixed scripted decisions with explicit
reasoning-loop state and compare react-style and plan-execute transitions.

Project milestone: A minimal local agent with three read-only tools, a validated
dispatcher, an inspectable trace, replay protection, and explicit stop budgets.
