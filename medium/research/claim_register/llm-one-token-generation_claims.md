# Claim Register

Article: What Actually Happens When an LLM Generates One Token?

Slug: llm-one-token-generation

## Claim 1

Claim: The Transformer replaced recurrence and convolution with attention, which made the architecture more parallelizable.

Source: Attention Is All You Need, arXiv:1706.03762.

Source type: Research paper.

Confidence: High.

Safe wording: The Transformer architecture is based solely on attention mechanisms and is more parallelizable than earlier recurrent approaches.

Risk if overstated: It can sound like every step of inference is parallel, which is not true during autoregressive generation.

Use in article: Introduce why the prompt can be processed differently from token-by-token decoding.

---

## Claim 2

Claim: High-throughput LLM serving systems must manage KV cache memory carefully because it grows and shrinks dynamically with each request.

Source: Efficient Memory Management for Large Language Model Serving with PagedAttention, arXiv:2309.06180.

Source type: Research paper.

Confidence: High.

Safe wording: KV cache memory changes over the life of a request, so serving systems have to manage it dynamically.

Risk if overstated: It can sound like only the cache matters; compute scheduling and batching still matter too.

Use in article: Explain why memory pressure is a first-class production concern.

---

## Claim 3

Claim: Inefficient KV cache management wastes memory through fragmentation and redundant duplication.

Source: Efficient Memory Management for Large Language Model Serving with PagedAttention, arXiv:2309.06180.

Source type: Research paper.

Confidence: High.

Safe wording: Poor KV cache management can waste memory through fragmentation and duplicated storage.

Risk if overstated: It may sound universal; the exact waste depends on the serving stack.

Use in article: Support the production checklist and the memory-growth diagram.

---

## Claim 4

Claim: PagedAttention and vLLM reported 2-4x throughput improvements with similar latency compared with systems like FasterTransformer and Orca in their evaluated settings.

Source: Efficient Memory Management for Large Language Model Serving with PagedAttention, arXiv:2309.06180.

Source type: Research paper.

Confidence: Medium-high.

Safe wording: In the paper’s evaluated settings, PagedAttention-based serving improved throughput substantially while keeping latency comparable.

Risk if overstated: Benchmark numbers can be misread as universal product guarantees.

Use in article: Add one concrete example of why memory-efficient serving matters.

---

## Claim 5

Claim: In autoregressive generation, the model consumes the prompt first and then generates subsequent tokens one at a time.

Source: Synthesized from Transformer autoregressive generation behavior and PagedAttention serving design.

Source type: Research synthesis.

Confidence: High.

Safe wording: The prompt is handled as an initial pass, and then each new token is produced in sequence.

Risk if overstated: None major, as long as the article does not imply the model runs all generation steps in parallel.

Use in article: Define the prefill-vs-decode split.

---

## Claim 6

Claim: TTFT and tokens per second measure different parts of the serving path, so they can move in opposite directions.

Source: Serving-system synthesis based on the prefill/decode split and production inference behavior.

Source type: Original synthesis.

Confidence: Medium.

Safe wording: Time to first token and steady-state token throughput are related but distinct serving metrics.

Risk if overstated: It can sound like a formal benchmark definition when it is really an operational framing.

Use in article: Explain the latency visual and the user experience tradeoff.

---

## Claim 7

Claim: KV cache stores information from earlier tokens so the model does not have to recompute all prior attention work from scratch on every new token.

Source: PagedAttention paper and Transformer attention mechanics.

Source type: Research paper.

Confidence: High.

Safe wording: The cache preserves prior attention state so decoding can reuse past computation.

Risk if overstated: It can sound like the whole model is cached; only the attention state is cached.

Use in article: Explain why decoding is cheaper than the initial prompt pass but still not free.