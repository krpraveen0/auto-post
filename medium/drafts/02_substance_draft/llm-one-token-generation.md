# Substance Draft

## What actually happens when an LLM generates one token?

When most people talk about an LLM response, they picture a prompt going in and an answer coming out. That is the right mental model if you are just trying to use the API.

It is the wrong mental model if you are trying to ship the thing in production.

The interesting part is not the full answer. It is the path from prompt to first token, and then from first token to the next one, and the next one after that. Once you see that path clearly, a lot of the weird behavior around latency, cost, and memory stops looking mysterious.

## The request does not go straight to the model

A real request usually hits a gateway or serving layer first. The prompt may be normalized, safety-checked, truncated, queued, or batched with other requests. Only then does it enter the model path.

That matters because the model is not just answering a question. It is sharing compute and memory with other requests, often under tight latency targets.

## The model does not read text

The model reads tokens.

Tokenization turns your text into IDs that the model can process. That is why a short-looking prompt can still be expensive, and why two prompts that look similar to a person can behave differently once they are broken into tokens.

This is also where the first production surprise shows up: the user thinks in characters and words, but the serving system thinks in tokens. If you are not watching token counts, you are already missing part of the bill.

## Prefill: the prompt gets processed first

Before the model can generate anything, it has to process the entire prompt. This initial pass is usually called prefill.

Prefill is where the model builds its internal state for the request. In transformer-based models, that state includes the key-value cache. The cache stores information from earlier tokens so the model does not have to rebuild all prior attention work from scratch for every new token.

You can think of prefill as setup work. It is not the answer yet, but it creates the conditions for the answer.

## Decode: the model generates one token at a time

After prefill, the model enters the decode loop.

Decode is sequential. The model predicts one token, the sampler picks one token, that token is appended to the context, and the next step starts. The output feels continuous to the user because the server streams it, but under the hood it is still a loop of repeated next-token decisions.

This is the moment where the system becomes a production problem instead of a demo problem. Every extra output token adds more work. Every active request needs memory. Every batch needs scheduling.

## The KV cache is the hidden memory bill

The key-value cache is why decoding can be fast enough to feel interactive. It lets the model reuse prior attention state instead of recomputing everything from the beginning.

But the cache is also why long prompts and long outputs hurt.

As the sequence grows, the cache grows. As batch size grows, memory pressure grows. If the serving system manages that memory poorly, you get wasted space from fragmentation and duplication. That directly limits how many requests you can pack onto a GPU.

This is one of the reasons LLM serving feels expensive even when the model is already loaded. The cost is not only model weights. It is also the moving, per-request memory footprint of the context you are asking the model to carry around.

## Why first token latency and tokens per second are not the same thing

If you have shipped an LLM feature, you have probably seen two metrics that behave differently: time to first token and tokens per second.

They measure different parts of the path.

Time to first token is dominated by everything that happens before the user sees output: queueing, prompt processing, prefill, and the first decode step. Tokens per second is what happens after the stream is already flowing.

That difference matters in product work. A system can feel slow to start but fast once it begins. It can also start quickly and then crawl on long answers. Those are not the same failure mode, and they should not be tuned the same way.

## Why production systems care about batch size and context length

Once you understand the path, the operational knobs make sense.

Longer prompts consume more cache. More output tokens mean more decode steps. Larger batches improve throughput, but only if the memory footprint leaves enough room for everyone.

That is why LLM serving teams care so much about max context length, output caps, batching policy, cache headroom, and request scheduling. These are not abstract infra choices. They are the difference between a system that looks fine in a notebook and a system that stays alive under load.

## A simple mental model

I like to think about one token like this:

1. The request arrives.
2. The prompt is tokenized.
3. The prompt is prefetched into model state.
4. The KV cache is built and reused.
5. The model decodes one token.
6. The server streams that token.
7. The loop repeats until the stop condition is hit.

That is the whole story, but it is also the part most people never see.

## Production inference checklist

- Track prompt token count, output token count, TTFT, and tokens per second.
- Set sane max output limits before users can accidentally create runaway decode cost.
- Watch KV cache headroom, not just GPU utilization.
- Expect long prompts to hurt latency even if the answer itself is short.
- Treat batching as a memory scheduling problem, not just a throughput trick.
- Use streaming when the user experience benefits from earlier feedback.
- Review serving behavior under long-context load, not only happy-path prompts.

## Closing

The main shift here is simple: an LLM response is not one atomic action. It is a pipeline.

If you can trace one token through that pipeline, you can usually explain the cost, the latency, and the failure modes of the whole system. That is the real skill behind building with LLMs in production.