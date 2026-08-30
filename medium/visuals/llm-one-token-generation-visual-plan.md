# Visual Plan

## Figure 1
Figure number: 1
Article section: Opening / hero image
Purpose: Give the reader an immediate mental model of the one-token request path.
Core idea: One token is the output of a pipeline, not a single step.
Diagram type: Flow diagram
Nodes: User prompt, gateway, tokenization, prefill, KV cache, decode, streamed token
Edges: Left-to-right request path
Color palette: Blue, indigo, slate, amber highlight for the output token
Caption: One token is the output of a pipeline, not a single model call.
Alt text: A request path showing prompt entry, tokenization, prefill, cache reuse, decode, and streamed output.
Credit: Original
Export format: PNG and SVG
Placement notes: Use as the hero image near the title.

## Figure 2
Figure number: 2
Article section: Request path
Purpose: Show the end-to-end serving path from API ingress to the token stream.
Core idea: Request handling includes serving, scheduling, model execution, sampling, and streaming.
Diagram type: Architecture flow
Nodes: Client, API gateway, tokenizer, scheduler, model forward pass, sampler, stream
Edges: Sequential processing path with a stream output
Color palette: Slate, blue, teal, green
Caption: The request path from API ingress to streamed token output.
Alt text: A horizontal serving pipeline from client request through model execution to output streaming.
Credit: Original
Export format: PNG and SVG
Placement notes: Use early in the article, after the request-path explanation.

## Figure 3
Figure number: 3
Article section: Prefill vs decode
Purpose: Contrast prompt processing with token-by-token generation.
Core idea: Prefill is parallel over the prompt; decode is sequential over generated tokens.
Diagram type: Comparison diagram
Nodes: Prompt tokens, prefill lane, decode lane, next token, next token
Edges: Parallel block for prefill, looping block for decode
Color palette: Blue for prefill, amber for decode
Caption: Prefill processes the prompt; decode generates one token at a time.
Alt text: Two lanes showing a prompt pass and a sequential generation loop.
Credit: Original
Export format: PNG and SVG
Placement notes: Put immediately after the prefill explanation.

## Figure 4
Figure number: 4
Article section: KV cache section
Purpose: Explain why memory pressure grows with sequence length and batch size.
Core idea: KV cache size rises as requests get longer and as more requests share the GPU.
Diagram type: Growth chart
Nodes: Prompt length axis, KV cache memory axis, sample request curves
Edges: Rising line/area curves
Color palette: Slate, blue, red warning zone, amber headroom band
Caption: KV cache memory grows as the prompt and output grow.
Alt text: A chart showing cache memory increasing with context length and batch pressure.
Credit: Original
Export format: PNG and SVG
Placement notes: Use with the section on memory pressure and fragmentation.

## Figure 5
Figure number: 5
Article section: Latency metrics
Purpose: Separate time to first token from steady-state token speed.
Core idea: Startup latency and throughput are different user experiences.
Diagram type: Metric comparison timeline
Nodes: Request start, prefill, first token, stream, token stream rate
Edges: Timeline plus throughput bars
Color palette: Blue, green, amber
Caption: Time to first token and tokens per second measure different parts of serving.
Alt text: A timeline showing first-token latency and a separate token-throughput measure.
Credit: Original
Export format: PNG and SVG
Placement notes: Place before the production implications section.

## Figure 6
Figure number: 6
Article section: Production checklist
Purpose: Give readers a practical shipping checklist for LLM inference.
Core idea: Production quality depends on token metrics, cache headroom, output caps, and long-context testing.
Diagram type: Checklist board
Nodes: TTFT, tokens per second, cache headroom, max output length, batching policy, long-context tests
Edges: Checklist rows grouped by operational area
Color palette: Slate, blue, green, amber
Caption: The operational checklist that keeps LLM inference fast and affordable.
Alt text: A production checklist covering latency, memory headroom, output limits, and serving behavior.
Credit: Original
Export format: PNG and SVG
Placement notes: Use as the closing visual before the checklist section.