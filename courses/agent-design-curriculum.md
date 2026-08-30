# Course Curriculum: Agentic AI Engineering
**Tagline:** "From Prompting to Production: Building Reliable, Versioned, and Scalable AI Agents"
**Persona Alignment:** Research-Driven, Grounded Truth, Project-Based

**Medium series map:** `medium/course_series/agentic-ai-engineering-map.md`

---

## 🎯 Course Objective
Move students from "writing prompts" to "engineering systems." By the end of this course, students will build a production-ready agentic system with a full CI/CD pipeline, automated evaluation gates, and a versioned deployment strategy.

## 🛠️ Learning Path: The 5 Pillars

### Module 1: The Anatomy of an Agent (The Foundation)
*Focus: Understanding the 6 dimensions of agent configuration.*
- **The Conceptual Shift:** LLM as a Reasoning Engine vs. LLM as a Chatbot.
- **The 6 Dimensions:**
  - System Prompts: Structuring instructions for reliability.
  - Tool Definitions: JSON schemas and the "Tool-Use" loop.
  - Model Selection: Throughput, Context Window, and Parameter tuning.
  - RAG & Retrieval: Indexing, top-k, and score thresholds.
  - Guardrails: Hard constraints and safety filters.
  - Memory: Short-term (context) vs. Long-term (persistence).
- **🛠️ Mini-Project:** "The Basic Tool-User" — Build an agent that can call 3 custom local tools to solve a multi-step task.

### Module 2: The Reasoning Loop (The Internals)
*Focus: How agents actually "think" and execute.*
- **Agentic Patterns:** 
  - ReAct (Reason + Act)
  - Plan-and-Execute
  - Self-Reflection/Self-Correction loops.
- **Managing State:** Transitioning from stateless requests to stateful sessions.
- **Handling Tool Failures:** Retries, fallback prompts, and error recovery.
- **🛠️ Mini-Project:** "The Self-Correcting Researcher" — An agent that searches the web, evaluates the result, and re-queries if the information is insufficient.

### Module 3: RAG & Knowledge Integration (The Brain)
*Focus: Grounding agents in truth.*
- **Vector DB Internals:** Embeddings, Cosine Similarity, and Hybrid Search.
- **Advanced Retrieval:** Query Expansion, Re-ranking, and Context Compression.
- **The "Context Window" Problem:** Strategies for managing token limits (Summarization vs. Truncation).
- **🛠️ Mini-Project:** "The Doc-Expert Agent" — Build a RAG system that can answer complex questions across 100+ PDF documents with source citations.

### Module 4: Evaluation & Testing (The Truth)
*Focus: Moving from "it feels right" to "it is right."*
- **The Eval Crisis:** Why traditional unit tests fail for LLMs.
- **Building Evaluation Sets:** Golden Datasets and Synthetic Data generation.
- **The 3 Pillars of Eval:**
  - Deterministic Tests (JSON structure, tool calls).
  - LLM-as-a-Judge (using GPT-4 to grade a smaller model).
  - Human-in-the-loop (HITL) feedback loops.
- **🛠️ Mini-Project:** "The Eval Suite" — Create a test suite that automatically scores an agent's performance on 50 edge cases.

### Module 5: Productionalizing Agents (The Engineering)
*Focus: Deployment, Rollbacks, and Safe Promotion.*
- **Agent-as-Code:** Treating configuration as versioned artifacts.
- **The Promotion Pipeline:** Staging $\rightarrow$ Canary $\rightarrow$ Production.
- **Automated Gates:** Implementing Quality, Performance, and Safety checks.
- **Model Pinning:** Avoiding the "Silent Update" disaster.
- **🛠️ Final Capstone Project:** "The Enterprise Agent" — Build a fully versioned agent with a deployment manager, automated eval gates, and a 1-click rollback system.

---

## 📈 Pedagogy: The "Grounded Truth" Method

Each lesson follows this structure:
1. **The Curiosity Hook:** A real-world failure case (e.g., "Why this agent spent $500 in a loop").
2. **The Deep Dive:** Breaking the concept into simple units + a `.drawio` architecture diagram.
3. **The Proof:** A small, runnable code snippet demonstrating the "Internal" behavior.
4. **The Build:** A mini-project that reinforces the concept.
5. **The Trade-off:** A "Grounded Truth" callout explaining when *not* to use this pattern.

## 🏁 Final Certification Requirement
To pass, students must submit their **Capstone Project** including:
- A GitHub repo with a versioned config.
- An Evaluation Report showing $\ge 90\%$ accuracy on the golden set.
- A recorded demo of a "Broken Deploy $\rightarrow$ Instant Rollback" scenario.
