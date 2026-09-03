# Visual Brief: Control Ownership

Figure number: 1

Article section: Visual Explanation

Purpose: Let readers distinguish three systems that can share the same chat
interface by tracing who selects the next action and which boundary constrains it.

Core idea: A chatbot produces language, a deterministic workflow follows a
predefined route, and a bounded agent chooses among allowed actions at runtime.

Diagram type: Three-lane control-flow comparison

Nodes: Chat interface, chatbot response, fixed workflow steps, bounded agent
loop, allowed tools, approval gate, stop conditions

Edges: Response arrow, fixed path, observe-decide-act loop, approval and stop
controls

Color palette: Slate background; blue for language; indigo for workflow; green
for permitted agent action; amber for approval; red for stop

Caption: The interface can look identical while control ownership changes from
response generation, to fixed code, to model-directed action inside explicit
approval and stopping boundaries.

Alt text: Three systems with the same chat interface but different control flow:
a chatbot produces text, a workflow follows fixed code, and a bounded agent
chooses actions inside approval and stop boundaries.

Credit: Original diagram for Agentic AI Engineering
