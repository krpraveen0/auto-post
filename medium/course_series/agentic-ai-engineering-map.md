# Agentic AI Engineering Course Series Map

Course title: Agentic AI Engineering

Series promise: Help engineers move from prompt experiments to reliable, evaluated, versioned agent systems.

Target reader: Software engineers and AI builders who have used LLM APIs but have not shipped production agent systems.

Starting skill level: Comfortable with APIs, JSON, basic backend code, and command-line workflows.

Final learner outcome: Build a versioned agent with tools, retrieval, eval gates, deployment promotion, and rollback.

## Module Map

| Module | Purpose | Lessons | Project milestone |
|---|---|---:|---|
| 1. Agent foundations | Define what an agent is and how configuration shapes behavior | 3 | Basic tool-using agent |
| 2. Reasoning loop | Show how state, planning, retries, and correction work | 3 | Self-correcting task runner |
| 3. Retrieval and grounding | Add knowledge integration with defensible citations | 3 | Document-grounded assistant |
| 4. Evaluation | Replace intuition with repeatable quality checks | 3 | Eval suite with golden cases |
| 5. Production release | Ship, monitor, promote, and roll back safely | 3 | Versioned production agent |

## Lesson Sequence

| Part | Lesson title | Reader learns | Prerequisite | Exercise | Visual |
|---:|---|---|---|---|---|
| 1 | What Makes an AI Agent Different from a Chatbot? | Agent boundaries, autonomy, tools, and state | None | Identify agent vs chatbot behavior in three examples | Agent capability map |
| 2 | The Six Configuration Surfaces of an Agent | Prompts, tools, models, retrieval, guardrails, memory | Part 1 | Draft a versioned agent config | Config surface diagram |
| 3 | Building a Minimal Tool-Using Agent | Tool schemas and the tool-call loop | Part 2 | Build an agent with three local tools | Tool-use sequence |
| 4 | Inside the Reasoning Loop | ReAct, plan-execute, and state transitions | Part 3 | Trace one task through a loop | Reasoning loop diagram |
| 5 | Handling Tool Failures Without Hiding Them | Retries, fallbacks, stop conditions, and user-visible errors | Part 4 | Add retry and failure reporting | Failure handling flow |
| 6 | Designing a Self-Correcting Research Agent | Reflection, query revision, and result sufficiency checks | Part 5 | Build a re-query loop | Research loop diagram |
| 7 | RAG Is Not a Magic Truth Layer | Retrieval limits, embeddings, hybrid search, and citations | Part 6 | Compare weak and strong retrieval results | RAG pipeline |
| 8 | Managing Context Before It Manages You | Chunking, reranking, compression, and truncation tradeoffs | Part 7 | Add context budgeting rules | Context budget map |
| 9 | Building a Document-Grounded Agent | Source-backed answers and refusal behavior | Part 8 | Answer questions over a small document set | Grounded answer path |
| 10 | Why LLM Evals Are Different from Unit Tests | Deterministic checks, judges, humans, and edge cases | Part 9 | Write 10 golden cases | Eval taxonomy |
| 11 | Building an Eval Gate for an Agent | Scoring, thresholds, regressions, and release blocking | Part 10 | Create a release gate | Eval gate flow |
| 12 | Reading Eval Results Like an Engineer | False passes, false fails, drift, and reviewer calibration | Part 11 | Review failed eval examples | Eval review dashboard |
| 13 | Agent-as-Code: Versioning Behavior, Not Just Code | Config versions, model pinning, prompts, and tools | Part 12 | Create a version manifest | Version manifest diagram |
| 14 | Promotion Pipelines for Agents | Staging, canary, production, metrics, and rollback triggers | Part 13 | Define a promotion checklist | Promotion pipeline |
| 15 | Capstone: Ship and Roll Back a Production Agent | Tie together config, evals, release, and rollback | Part 14 | Demo broken deploy to rollback | Capstone architecture |

## Project Thread

Final artifact: A production-style agent repository with versioned configuration, tool schemas, retrieval, eval gates, promotion rules, and rollback instructions.

Milestones:

1. Minimal tool-user.
2. Stateful reasoning loop.
3. Grounded retrieval layer.
4. Golden eval suite.
5. Release gate.
6. Promotion and rollback flow.

## Series Navigation

Index slug: `agentic-ai-engineering-course-index`

Previous/next link pattern: Each lesson should include “Previous,” “Course index,” and “Next” links after the intro and at the end.

Recommended publishing cadence: Publish one lesson every 3-5 days. Group module recaps after parts 3, 6, 9, 12, and 15 if reader feedback shows confusion.

## Risks

Concepts that may be too broad: RAG, evals, and production deployment each need multiple lessons and should not be compressed.

Terms that need early definition: agent, tool call, state, guardrail, memory, retrieval, eval, canary, rollback.

Lessons likely to need code or diagrams: Parts 3, 5, 6, 8, 9, 11, 13, 14, and 15.
