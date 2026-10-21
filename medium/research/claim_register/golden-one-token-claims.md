# Claim Register: What Happens When an LLM Generates One Token?

Verified: 2026-09-03

## Claim 1

Claim: A causal Transformer converts the current hidden state into logits over a vocabulary, then a decoding strategy selects the next token.

Source: Attention Is All You Need; Hugging Face Generation Strategies.

Source type: Primary paper and official documentation.

Confidence: High.

Safe wording: Autoregressive Transformer implementations commonly produce next-token logits and apply a decoding strategy; exact internals vary by architecture and serving engine.

Exact supporting location: Transformer decoder and output softmax; Hugging Face generation strategy overview.

Risk if overstated: Not every generative model is a Transformer or uses identical sampling code.

## Claim 2

Claim: Reusing previously computed keys and values avoids recomputing them for every decode step.

Source: Hugging Face cache explanation and committed `one_token.py` experiment.

Source type: Official documentation and original reproduction.

Confidence: High.

Experiment: Cached and full-recomputation logits agree within 2.776e-17 in the tested toy model.

Risk if overstated: This equality test does not measure production GPU speed or model quality.

## Claim 3

Claim: KV-cache storage grows with layers, cached tokens, KV heads, head dimension, and bytes per stored value.

Source: Tensor shapes implied by cached attention; verified formula in unit test.

Safe wording: For a conventional cache, approximate bytes are `2 × layers × tokens × kv_heads × head_dim × bytes_per_value`; implementations may add metadata, padding, quantization, paging, or sharing.

Confidence: High for the stated model.

## Claim 4

Claim: Poor KV-cache memory management can waste capacity through fragmentation and duplication, restricting batching.

Source: Kwon et al., Efficient Memory Management for Large Language Model Serving with PagedAttention.

Source type: Peer-reviewed systems paper.

Confidence: High within evaluated systems.

Safe wording: The PagedAttention authors observed these problems and reported improvements in their evaluated workloads; do not generalize their throughput numbers to every stack.

## Claim 5

Claim: Prompt processing and iterative decoding create different latency regimes.

Source: Algorithmic structure plus committed CPU experiment.

Confidence: High for the distinction; quantitative results are environment-specific.

Experiment: On the recorded environment, median toy prefill time rose from 0.0410 ms at 16 tokens to 24.1330 ms at 1,024 tokens; cached generation with a 128-token prompt rose from 0.3595 ms for one decode step to 2.4019 ms for 64 steps.

Risk if overstated: NumPy CPU timings must not be presented as production LLM serving benchmarks.
