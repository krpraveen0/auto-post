# Research Dossier: What Happens When an LLM Generates One Token?

Target reader: application or backend engineer who calls an LLM API but has not operated an inference server.

Reader capability after: trace request, prefill, sampling, decode, cache growth, and streaming; run a cache experiment; choose the right metric for a latency symptom.

Central question: what work happens before and after the first visible token?

Scope: decoder-style causal Transformer inference and serving concepts.

Non-goals: training, distributed GPU kernels, speculative decoding implementation, model-quality evaluation, or vendor benchmarking.

## Question Tree

1. How does text become a next-token decision?
2. Which work belongs to prefill and which repeats during decode?
3. What is cached, why is it valid, and how can we test it?
4. How does cache memory scale?
5. Which measurements distinguish queueing, prompt processing, and decoding?
6. Where does the toy model stop matching production?

## Misconceptions

| Misconception | Correction |
|---|---|
| Streaming makes model computation faster | Streaming changes when output becomes visible; it does not inherently reduce compute |
| KV cache stores previous tokens | It stores projected key/value tensors derived from token representations |
| One token has one fixed cost | Cost depends on context, batching, architecture, hardware, scheduling, and implementation |
| High GPU utilization proves healthy serving | User latency, queueing, throughput, cache headroom, and tail distributions still matter |
| Toy CPU timing predicts production throughput | It demonstrates algorithmic direction only |

## Original Contribution

Reproducible implementation, corrupted-cache failure fixture, raw benchmark,
memory worksheet, diagnostic framework, and progressive visual explanation.

Draft readiness: Proceed.
