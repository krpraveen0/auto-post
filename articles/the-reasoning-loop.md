# The Reasoning Loop: How AI Agents Actually "Think"

**Moving beyond single-shot prompts to iterative execution without the "Infinite Loop" disaster.**

---

## 🎣 The Friday Afternoon Disaster: The Infinite Loop
Imagine you build an agent to "Research a company and summarize it." You give it a search tool and a summarizer tool. 

**The failure:** The agent searches for "Company X," finds a link, clicks it, finds another link, clicks it... and continues for 45 minutes, consuming $20 in tokens, only to tell you: *"I'm still searching for more details."*

**Why did this happen?** The agent had a goal, but no **reasoning loop** to evaluate if the goal was already met. It was "acting" without "reasoning."

---

## 🧠 The Core Concept: The Reasoning Loop
Most people think agents just "call tools." In reality, a production-grade agent runs a continuous cycle:
**Perceive $\rightarrow$ Think $\rightarrow$ Act $\rightarrow$ Observe $\rightarrow$ Repeat**

### 1. The ReAct Pattern (Reason + Act)
The gold standard for simple agents. Instead of going straight to a tool, the agent is forced to write a "Thought" first.

**The Internal Dialogue:**
- **Thought:** "I need to find the current price of NVDA to answer the user."
- **Action:** `get_stock_price("NVDA")`
- **Observation:** `$120.45`
- **Thought:** "I have the price. Now I can answer the user."
- **Final Answer:** "NVDA is currently trading at $120.45."

💡 **Grounded Truth:** Forcing the agent to write a "Thought" block acts as a "Chain-of-Thought" mechanism. It significantly reduces hallucinations because the agent commits to a plan *before* executing a tool.

---

## 🛠️ Deep Dive: Three Advanced Reasoning Patterns

### Pattern A: Plan-and-Execute
For complex tasks, ReAct is too short-sighted. It can get lost in the weeds. **Plan-and-Execute** separates the "Strategist" from the "Worker."

1. **The Planner:** Breaks the goal into a list of 5 discrete steps.
2. **The Executor:** Takes step 1, executes it, and returns the result.
3. **The Re-Planner:** Looks at the result of step 1 and decides if the remaining 4 steps are still valid.

**Best for:** Multi-step research, coding a full feature, or complex data analysis.

### Pattern B: The Self-Reflection Loop
The agent acts as its own critic. 
`Draft` $\rightarrow$ `Critique` $\rightarrow$ `Revise`

**The Loop:**
- **Agent:** Generates a Python script.
- **Critic:** "This script has a potential memory leak in the loop on line 12."
- **Agent:** Rewrites the script to fix the leak.

### Pattern C: State-Machine Routing
Instead of letting the LLM decide everything, you constrain the reasoning into a graph.
- **Node A:** Triage (Decide if this is a "Billing" or "Technical" query)
- **Node B:** Technical Path $\rightarrow$ Search Docs $\rightarrow$ Propose Solution.
- **Node C:** Billing Path $\rightarrow$ Check Invoice $\rightarrow$ Propose Refund.

---

## 💻 Hands-On: Building a "Self-Correcting Searcher"

Let's implement a mini-agent that doesn't just search, but **evaluates** if the search result is actually useful.

```python
import openai

class ReasoningAgent:
    def __init__(self, tools):
        self.tools = tools
        self.history = []

    def run(self, goal):
        print(f"🚀 Goal: {goal}")
        for i in range(5):  # Max 5 iterations to prevent infinite loops
            # 1. THINK & ACT
            prompt = f"Goal: {goal}\nHistory: {self.history}\nWhat is your Thought and Action?"
            response = self.call_llm(prompt)
            
            thought, action, params = self.parse_response(response)
            print(f"💭 Thought: {thought}")
            print(f"🛠️ Action: {action}({params})")

            # 2. OBSERVE
            observation = self.tools[action](params)
            print(f"👁️ Observation: {observation}")

            # 3. REFLECT (The Self-Correction Step)
            reflection_prompt = f"Goal: {goal}\nObservation: {observation}\nIs this enough to answer the goal? Answer YES or NO."
            is_enough = self.call_llm(reflection_prompt).strip().upper()

            if "YES" in is_enough:
                print("✅ Goal achieved!")
                return self.generate_final_answer(goal, self.history)
            
            self.history.append({"action": action, "obs": observation})
        
        return "❌ Failed to reach goal within iteration limit."

    def call_llm(self, prompt):
        # Mock LLM call for demonstration
        return "Thought: I need to check the price. Action: get_price, Params: 'BTC'"

    def parse_response(self, response):
        # Simplified parsing logic
        return "Searching...", "get_price", "BTC"

    def generate_final_answer(self, goal, history):
        return f"Final answer based on {len(history)} steps of reasoning."

# Mock Tools
tools = {"get_price": lambda x: f"The price of {x} is $60,000"}
agent = ReasoningAgent(tools)
agent.run("What is the price of Bitcoin?")
```

---

## 🔍 Under the Hood: The "Context Drift" Problem

As the reasoning loop continues, the `History` grows. 
`Thought 1` $\rightarrow$ `Obs 1` $\rightarrow$ `Thought 2` $\rightarrow$ `Obs 2` ...

**The Problem:** After 10 iterations, the LLM often forgets the original **Goal** because it's buried at the top of the prompt. This is called **Context Drift**.

**The Engineering Fix:**
1. **Goal Reinforcement:** Repeat the goal at the *bottom* of every prompt.
2. **Summary Memory:** Instead of passing the whole history, pass a summarized version of previous steps.
3. **Working Memory:** Maintain a "Scratchpad" where the agent explicitly writes down facts it has already confirmed.

---

## 🏁 Challenge: The "Fact-Checker" Agent

**The Task:** Build an agent that takes a claim (e.g., "The moon is made of green cheese") and must:
1. **Reason** why the claim might be false.
2. **Search** for a reputable source to disprove it.
3. **Reflect** on whether the source is actually a primary source.
4. **Finalize** a "Truth Score" (0-100%) with evidence.

**Success Criteria:**
- Must use at least 3 iterations of the loop.
- Must include a "Reflect" step that can reject a bad search result.
- Must handle the case where no information is found without looping infinitely.

---

**Your agent will drift. It will loop. It will hallucinate.** The difference between a demo and a product is the **reasoning loop** you build to catch those failures.

*Built something similar? Drop a comment—I'm exploring better ways to manage long-term agent memory and would love to hear your approach.*