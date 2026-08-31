# What Makes an AI Agent Different from a Chatbot?

*Part 1 of Agentic AI Engineering: define the control boundary before you add tools, memory, or autonomy.*

**Series navigation:** Previous: Course index (this is the first lesson) | Course index: Agentic AI Engineering | Next: Part 2 — The Six Configuration Surfaces of an Agent

A demo once told me it had “resolved” a customer’s delivery problem. The response was polished. It summarized the complaint, apologized, and said a replacement had been arranged.

Nothing had actually happened.

The system had no order lookup, no replacement tool, and no durable record of the conversation. It was a chatbot performing the language of action. The failure was not that its prose was weak. The failure was that we had confused a convincing response with an executed task.

That distinction is the foundation of this course. An agent is not a chatbot with a more ambitious system prompt. It is a system allowed to choose and perform actions inside an explicit boundary, while carrying enough state to decide what should happen next.

The useful engineering question is therefore not, “Does this feel agentic?” It is: **What can this system observe, decide, change, remember, and stop?**

## Learning Outcomes

By the end of this lesson, you will be able to:

1. Distinguish a chatbot, a deterministic workflow, and an agent by their control flow rather than their interface.
2. Describe an agent as a bounded loop of observation, decision, action, state update, and stopping.
3. Write a one-page boundary specification that makes autonomy reviewable before implementation.

## A Chat Interface Tells You Almost Nothing

Three systems can share the same chat window and still have completely different architectures.

A **chatbot** primarily turns conversation history into a response. It may answer questions, transform text, or suggest a next step. If it cannot affect another system, its output remains advice or language.

A **workflow** performs actions, but its route is mostly decided in advance. A rule might say: if an invoice is overdue, send a reminder; after seven days, create a collection task. The workflow acts, yet the designer—not a model at runtime—selected the sequence.

An **agent** uses a model or another policy component to choose among permitted actions based on the current situation. It observes a task, selects a tool, reads the result, updates its working state, and decides whether to act again or stop.

These are not prestige levels. A workflow is often the better design when the rules are stable and the cost of improvisation is high. A chatbot is often sufficient when the user only needs explanation. Calling everything an agent hides the exact control decision that deserves review.

There is no single universally accepted industry definition that cleanly separates every agent from every workflow. [SOURCE NEEDED: compare primary definitions of AI agents across standards or major platform documentation.] For this course, we will use an operational definition that can be tested in code:

> An agent is a bounded software system that chooses its next action from an allowed set, observes the result, updates task state, and repeats until a stop condition is met.

The word **bounded** does most of the safety work in that sentence.

## The Five-Part Agent Loop

You can recognize an agent by tracing five responsibilities.

### 1. Observe

The system receives a goal plus relevant context. Later observations may include tool results, validation errors, approval decisions, or time and budget remaining. Observation is broader than reading the user’s last message.

### 2. Decide

The system chooses the next permitted move. That could be calling a search tool, asking the user for missing information, validating a draft, or finishing. The model is not merely composing text; it is influencing control flow.

### 3. Act

The chosen action crosses a boundary. A read-only action might fetch a file. A mutating action might create a ticket or update a record. The tool—not the model’s prose—performs the operation and returns a result.

### 4. Update state

The system records what matters for the next decision: completed steps, tool results, failed attempts, approvals, unresolved questions, or a compact task summary. Conversation history can be part of state, but state can also live in structured fields, files, or a database.

### 5. Stop

The loop ends because the goal is satisfied, the user must decide, an error is not recoverable, or a limit has been reached. A production agent needs stop conditions just as much as it needs tools. “Keep trying” is not a stop policy.

If one of these responsibilities is missing, name the missing piece instead of stretching the word agent. A model that proposes tool calls but never executes them is an assistant with action suggestions. A fixed sequence that cannot choose a different next step is a workflow. A loop with no bounded action set or stop rule is an incident waiting to happen.

## Boundaries Matter More Than Personality

Teams often start an agent design by polishing its role: “You are an expert operations analyst.” That may influence responses, but it does not establish the system’s authority.

A useful boundary specification answers five concrete questions:

- **Observation boundary:** What inputs and tool results may the agent see?
- **Action boundary:** Which tools may it call, with which parameter constraints?
- **State boundary:** What may persist across steps, sessions, or users?
- **Approval boundary:** Which actions require a human decision before execution?
- **Termination boundary:** What counts as success, failure, timeout, or escalation?

This turns “autonomy” from a mood into a contract. The agent may have freedom inside the contract, but the surrounding software owns authentication, authorization, validation, budgets, and audit records.

Treat tool output as input, not as authority. A web page, document, ticket, or tool error can contain misleading instructions or malformed data. [SOURCE NEEDED: primary security guidance on prompt injection and untrusted tool or retrieval content.] The agent can reason about that content, but application controls must still decide what the tool is allowed to do.

## Worked Example

Imagine an internal support system that handles laptop-access requests. The user writes: “My laptop was replaced and I can’t access the analytics dashboard. Please fix it before the morning report.”

### Version A: the chatbot

The chatbot explains the usual access steps and drafts a message to IT. It may be helpful, but it cannot inspect identity records or change permissions. Its completion condition is “a useful response was produced.”

If it says, “Your access has been restored,” it is making an unsupported claim. The architecture gives it no evidence that the action occurred.

### Version B: the deterministic workflow

The workflow extracts the employee ID, checks whether the request matches a known access bundle, creates a ticket, and sends a confirmation. Each step is useful and real. However, the route was fixed by code. An exception such as a contractor account or a missing manager mapping follows a predefined error branch.

This may be exactly what the organization needs. Predictability is a feature.

### Version C: the bounded agent

The agent receives a goal and a set of tools:

1. `lookup_employee` — read-only identity and employment status.
2. `inspect_access` — read-only current entitlements.
3. `create_access_ticket` — creates a proposed access request.
4. `request_approval` — asks an authorized manager to approve the proposal.

The agent first looks up the employee. It notices that the replacement laptop is registered but the dashboard entitlement is missing. It inspects the standard bundle for that role, prepares a ticket, and requests approval. It does **not** grant access directly because that action is outside its boundary.

After approval, a separate access-management service performs the grant. The agent reads the service result and reports either verified success or an explicit failure. If the employee record is ambiguous, it stops and asks for clarification. If a tool fails twice, it stops retrying and exposes the failure.

The chat window did not make Version C an agent. Runtime choice did: the system selected its next action after each observation. The boundary made that choice acceptable: read operations were allowed, the write operation created a proposal rather than a privilege grant, approval was mandatory, and retries were limited.

Here is the minimal state we would want to inspect during a run:

```yaml
goal: restore analytics access for employee E-1042
status: waiting_for_approval
completed_steps:
  - employee_verified
  - current_access_inspected
  - access_ticket_created
pending:
  - manager_approval
attempts:
  inspect_access: 1
stop_reason: null
```

Notice what is absent: hidden claims of success. The state says what the system has evidence for and what still blocks completion.

## Visual Guidance

Create an **agent capability map** with three left-to-right lanes: Chatbot, Deterministic Workflow, and Bounded Agent. Use five columns labeled Observe, Decide, Act, Update State, and Stop. Show the chatbot producing a response without an external action; show the workflow following a fixed route; show the agent looping from tool result back to decision. Draw a visible boundary around the agent’s allowed tools, with an approval gate before any permission-changing action.

**Caption:** The interface may look identical, but control flow separates a chatbot, a workflow, and an agent.

**Alt text:** Comparison diagram showing a chatbot generating text, a workflow following fixed steps, and a bounded agent choosing tools in an observe-decide-act-state loop with approval and stop conditions.

## Exercise

Classify each system below as a chatbot, deterministic workflow, or bounded agent. Do not classify by marketing name; trace who chooses the next action.

1. A writing assistant rewrites an email and suggests three subject lines. It cannot send the email.
2. A scheduled job reads a CSV, applies a fixed validation rule, and uploads valid rows to a database.
3. A research system chooses among local document search, metadata lookup, and “ask the user,” then stops when every answer statement is supported or a search budget is exhausted.

For each system, write one sentence explaining your classification. Then create a boundary card for system 3 with these fields:

```yaml
goal:
allowed_observations:
allowed_actions:
persistent_state:
approval_required_for:
success_condition:
failure_condition:
maximum_steps:
```

**Expected output:** a Markdown file containing three classifications and one completed boundary card. A strong answer classifies the systems as chatbot, deterministic workflow, and bounded agent, respectively. The boundary card should permit read-only research tools, require clarification when the question is underspecified, stop when claims are supported or the budget is exhausted, and prohibit unsanctioned writes or publication.

Keep this file. In Part 2, you will turn the same boundary into a versioned configuration that separates prompts, tools, model choice, retrieval, guardrails, and memory.

## Recap

An agent is not defined by a chat interface, a dramatic system prompt, or the ability to produce convincing prose. It is defined by runtime control: it observes, chooses a permitted action, reads the result, updates state, and stops under explicit conditions.

The safest place to begin is the boundary, not the prompt. Write down what the system can see, change, retain, require approval for, and treat as done. Once those decisions are visible, you can decide whether you need an agent at all. A chatbot or deterministic workflow may be simpler and more trustworthy.

That is not a downgrade. It is good engineering.

## Next Lesson

Part 2, **The Six Configuration Surfaces of an Agent**, turns today’s boundary card into a versioned agent configuration. We will separate behavior that teams often bury in one prompt: instructions, tools, model settings, retrieval, guardrails, and memory.

**Series navigation:** Previous: Course index | Course index: Agentic AI Engineering | Next: Part 2 — The Six Configuration Surfaces of an Agent
