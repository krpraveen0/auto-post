# Human Rewrite

## What actually happens when an LLM generates one token?

The first time I watched a real LLM serving path break down on a long prompt, I realized how misleading the usual prompt-to-answer mental model is.

If you are only calling an API, that model is fine. You send text in, you get text back, and you move on.

If you are shipping the system, it is not fine.

The useful question is not “what did the model answer?” It is “what had to happen before the first visible token, and what has to repeat for every token after that?” Once you can answer that, latency and cost stop feeling like magic.

## The request path starts before the model

In production, the request usually passes through a gateway or serving layer first. The system may normalize the prompt, enforce limits, queue it, or batch it with other requests. Only after that does it hit the model.

That is the first reason LLM apps behave differently from ordinary request/response APIs. The model is not alone. It is sharing compute and memory with other requests, and both of those are scarce.

## The model reads tokens, not text

This sounds obvious until you look at a prompt that feels short and discover that it turns into far more tokens than you expected.

Tokenization is where the user’s text becomes model input. The serving system thinks in token counts, not sentence length. So if you are not watching tokens, you are not really watching the cost.

That is one of the easiest places for LLM products to surprise teams. The prompt a person sees and the workload the GPU sees are not the same thing.

## Prefill is the setup step

Before the model can generate anything, it has to process the full prompt. That initial pass is usually called prefill.

Prefill is where the model builds the internal state it will reuse while generating. In transformer-based serving, that includes the KV cache. The cache keeps past keys and values around so the model does not have to rebuild all of its attention work from scratch for every new token.

I think this is the single most useful sentence in the whole article: the first pass prepares the request, but it is not yet the response.

## Decode is where the answer appears one token at a time

After prefill, the model enters the decode loop. Now it predicts one token, the sampler picks one token, the token is appended to the context, and the next step begins.

The user sees a stream. The server sees a loop.

That difference matters because every extra output token adds work, and every active request keeps memory alive. Decode is cheap enough to feel interactive, but it is never free.

## The KV cache is the invisible bill

The cache is what makes decoding practical. It lets the model reuse earlier attention state instead of recomputing everything.

It is also what makes long-context serving hard.

As the prompt grows, the cache grows. As the output grows, the cache grows again. When a server manages that memory poorly, it wastes space through fragmentation and duplication. That directly caps how many requests you can fit on a GPU.

So yes, the weights are expensive. But the moving per-request cache is often the part that turns a pleasant demo into an operational headache.

## TTFT and tokens per second tell different stories

You will usually see two metrics in a real LLM system: time to first token and tokens per second.

They are related, but they are not the same.

Time to first token is about everything the user waits through before the stream starts: queueing, prompt processing, prefill, and the first decode step. Tokens per second is the pace after the stream is already flowing.

That is why a system can feel slow to start and still be decent once it begins talking, or feel snappy at first and then crawl on long answers. Those are different tuning problems.

## Why production teams obsess over batch size and context length

Once you trace one token through the system, the knobs make sense.

Long prompts eat cache. Long answers increase decode work. Bigger batches help throughput, but only until memory pressure starts pushing back. That is why serving teams care so much about max context length, output caps, batching policy, and cache headroom.

These are not cosmetic infra settings. They decide whether your LLM feature stays fast and affordable after real users get their hands on it.

## The shortest useful mental model

I like to reduce the whole thing to this:

1. Request arrives.
2. Text becomes tokens.
3. The prompt is prefetched.
4. The KV cache is created and reused.
5. The model decodes one token.
6. The server streams it.
7. The loop repeats until stop.

That is enough to reason about almost every production issue people hit with LLMs.

## Checklist before you ship

- Track prompt tokens, output tokens, TTFT, and tokens per second.
- Cap output length so one request cannot run away with cost.
- Watch cache headroom, not just GPU utilization.
- Expect long prompts to hurt latency even when the answer is short.
- Treat batching as a memory scheduling problem.
- Use streaming when users benefit from early feedback.
- Test long-context behavior before traffic finds it for you.

## Closing thought

An LLM response is not one action. It is a pipeline.

If you can trace one token through that pipeline, you can usually explain why the system feels fast or slow, cheap or expensive, safe or fragile. That is the real production skill.