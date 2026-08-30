# Outline

Title: What Actually Happens When an LLM Generates One Token?

Subtitle: A practical walkthrough of tokenization, prefill, KV cache, decode, streaming, and the production costs hiding inside a single response.

Reader: Developers, backend engineers, AI engineers, and serious learners.

Promise: Show the request path behind one token so the reader can reason about latency, memory, and cost in real systems.

## Opening

- Start with the observation that most people think in prompts and answers, but production systems have to care about the steps in between.
- Frame the article around one request, one token, and one serving path.
- State the practical payoff: once you understand the path, latency and cost stop feeling arbitrary.

## 1. The request enters a serving stack

- User request hits an API or gateway.
- The system may normalize the prompt, enforce limits, and queue the request.
- The model has not generated anything yet.

## 2. Tokenization turns text into model input

- Explain that the model reads token IDs, not raw text.
- Mention that tokenization changes prompt length in ways users do not always expect.
- Short example: one sentence can turn into many tokens.

## 3. Prefill processes the prompt

- The prompt is run through the model to build internal state.
- This is where the KV cache gets created.
- The prompt pass is the expensive setup step before generation starts.

## 4. Decode generates the next token

- The model predicts one token at a time.
- Each step reuses past keys and values.
- Sampling chooses the token that leaves the model next.

## 5. KV cache is the hidden memory bill

- Show why the cache grows with prompt length and output length.
- Explain why long-context requests crowd out batch size.
- Mention fragmentation and duplicated storage as serving problems.

## 6. Why streaming changes the user experience

- The user sees the first token before the whole answer is done.
- That is why TTFT matters.
- Steady-state token speed matters after the first token.

## 7. Production implications

- Long prompts are not free.
- More output tokens mean more decode work.
- Batch size, cache headroom, and max output length become cost controls.

## 8. Checklist

- What to watch before shipping an LLM feature.
- What metrics to log.
- What knobs to control.

## Closing

- Summarize the mental model in one paragraph.
- Encourage readers to look at inference as a pipeline, not a magic box.