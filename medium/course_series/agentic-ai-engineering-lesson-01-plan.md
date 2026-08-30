# Course Lesson Plan

Series: Agentic AI Engineering

Part number: 1

Lesson title: What Makes an AI Agent Different from a Chatbot?

Target reader: Software engineers and AI builders who have used LLM APIs but have not designed agent systems.

Reader state before this lesson: The reader knows prompts and chat completions, but may call any LLM workflow an agent.

Reader state after this lesson: The reader can explain the difference between a chatbot, workflow, and agent using autonomy, tools, state, and feedback loops.

Prerequisites: Basic familiarity with LLM prompts and API calls.

## Learning Outcomes

1. Define an AI agent in practical engineering terms.
2. Distinguish chatbots, scripted workflows, and agents.
3. Identify when agent behavior is useful and when a simpler workflow is safer.

## Lesson Shape

Hook: A support bot that answers one question is not the same system as an agent that investigates, calls tools, retries failures, and decides when to stop.

Core concept: An agent is not defined by hype words; it is defined by a loop that combines model reasoning, tool access, state, and goal-directed decisions.

Worked example: Compare three systems: a FAQ chatbot, a fixed invoice-processing workflow, and an incident triage agent that reads logs, queries metrics, opens a ticket, and asks for approval before remediation.

Common mistake: Treating every LLM wrapper as an agent.

Tradeoff: More autonomy can reduce manual work, but it also increases the need for observability, permissions, evals, and stop conditions.

Exercise: Review three product ideas and classify each as chatbot, workflow, or agent. For each one, list the tool access, state, risk, and required guardrail.

Expected exercise output: A small decision table with one recommended architecture per idea.

## Evidence & Visuals

Claims to validate: Definitions from official platform docs where available; safety claims around autonomy and tool permissions; examples of agent loops from primary documentation or papers.

Required diagram: Agent capability map contrasting chatbot, workflow, and agent.

Caption: Agents combine model reasoning with tools, state, and controlled autonomy.

Alt text: A comparison diagram showing a chatbot with prompt-response behavior, a workflow with fixed steps, and an agent with a reasoning and tool-use loop.

## Continuity

Previous lesson recap: None. This is the series opener.

Next lesson bridge: Now that the reader can identify an agent, the next lesson breaks down the six configuration surfaces that control its behavior.

Project milestone: Choose the final agent use case that the reader will build across the series.
