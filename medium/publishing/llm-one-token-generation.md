# Publishing Package

Article: What Actually Happens When an LLM Generates One Token?

## Medium

Title: What Actually Happens When an LLM Generates One Token?

Subtitle: A practical walkthrough of tokenization, prefill, KV cache, decode, streaming, and the production costs hiding inside a single response.

Meta preview: A single LLM token is the visible part of a longer serving pipeline. Here is the request path, the cache, the latency split, and the production checklist that actually matter.

Topics: AI engineering, LLM inference, system design, machine learning infrastructure, backend engineering

Featured image: medium/visuals/exported/llm-one-token-generation-hero.svg

Image caption: One token is the output of a pipeline: tokenize, prefill, cache, decode, stream.

Image alt text: A request path diagram showing prompt tokenization, prefill, KV cache reuse, decode, and streamed output tokens.

Disclosure note: Written with AI assistance and reviewed for technical accuracy.

## Additional visual assets

- Hero image: medium/visuals/exported/llm-one-token-generation-hero.svg
- LLM request path diagram: medium/visuals/exported/llm-one-token-generation-request-path.svg
- Prefill-vs-decode diagram: medium/visuals/exported/llm-one-token-generation-prefill-vs-decode.svg
- KV cache growth diagram: medium/visuals/exported/llm-one-token-generation-kv-cache-growth.svg
- TTFT vs tokens-per-second visual: medium/visuals/exported/llm-one-token-generation-ttft-vs-tps.svg
- Production inference checklist: medium/visuals/exported/llm-one-token-generation-production-checklist.svg

## Visual captions and alt text

1. Hero image
Caption: One token is the output of a pipeline, not a single step.
Alt text: A clean pipeline showing request entry, tokenization, prefill, KV cache, decode, and streaming.

2. LLM request path diagram
Caption: The request path from API ingress to the token stream.
Alt text: A horizontal serving pipeline showing gateway, tokenizer, scheduler, model forward pass, sampler, and streaming output.

3. Prefill-vs-decode diagram
Caption: Prefill processes the prompt; decode generates the next token one step at a time.
Alt text: Two-lane diagram contrasting a parallel prompt pass with a sequential token generation loop.

4. KV cache growth diagram
Caption: KV cache grows as the prompt and generation length increase.
Alt text: A chart showing memory usage rising with context length and batch size.

5. TTFT vs tokens-per-second visual
Caption: Time to first token and tokens per second measure different parts of the serving path.
Alt text: A timeline and throughput comparison that separates startup latency from steady-state generation speed.

6. Production inference checklist
Caption: Production LLM inference needs cache headroom, output caps, and serving metrics.
Alt text: A checklist of the operational items that keep an LLM serving system fast and affordable.

## Publication submission note

Hi [Publication Editor],

I’d like to submit this article for consideration:

What Actually Happens When an LLM Generates One Token?

It walks through the request path behind LLM inference, from tokenization and prefill to KV cache behavior, decode, streaming, and the production metrics that shape latency and cost. I wrote it for developers, backend engineers, AI engineers, and curious readers who want a practical mental model they can use in production.

Thanks for taking a look.

## LinkedIn post

I keep seeing teams treat LLMs like a prompt goes in and an answer comes out.

That model is fine for a demo, but it falls apart fast once you care about latency, memory, and cost.

I wrote a new piece on what actually happens when an LLM generates one token: tokenization, prefill, KV cache growth, decode, streaming, TTFT, and why long prompts quietly make everything more expensive.

If you build with LLMs, the request path matters more than the demo path.

## X/Twitter thread

1/8 Most people think an LLM does one thing: prompt in, answer out.

That’s a fine mental model for using an API.
It breaks down once you’re shipping production inference.

2/8 The request usually hits a serving layer first.
Before the model sees anything, the prompt may be normalized, queued, batched, or limited.

3/8 The model does not read text.
It reads tokens.
That’s why prompt length, not just character count, drives cost and latency.

4/8 Before generation starts, the model runs prefill.
That’s where it processes the prompt and builds internal state.

5/8 Then comes decode: one token at a time.
The server streams output, but under the hood it’s a repeated next-token loop.

6/8 The KV cache is the hidden memory bill.
It lets the model reuse prior attention state, but it also grows with context length and batch size.

7/8 Time to first token and tokens per second are different metrics.
One measures startup latency.
The other measures steady-state generation speed.

8/8 I wrote the full walkthrough with diagrams for the request path, prefill vs decode, KV cache growth, and a production inference checklist.

If you work on LLM apps, this is the mental model that matters.