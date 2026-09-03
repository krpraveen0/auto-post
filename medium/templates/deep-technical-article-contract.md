# Deep Technical Article Contract

Use this contract to produce original, evidence-backed teaching at the standard
of respected long-form engineering essays. It is a quality floor, not permission
to imitate another writer's voice, wording, examples, or section order.

## Progressive construction

- Start with the smallest useful system or mental model.
- Introduce each component in response to a concrete limitation, failure, risk,
  cost, or scale requirement.
- Show the architecture after meaningful transitions so the reader can see what
  changed and why.
- State what can be skipped and under which conditions.

## Explanatory depth

- Define the boundary and explicitly state what is outside the article's scope.
- Pair every abstraction with a realistic example, runnable experiment, measured
  observation, or operational scenario.
- Separate mechanism, implementation choice, and product consequence.
- Explain a credible alternative and the trade-off that decides between it and
  the recommended approach.
- Include failure behavior, observability, recovery, and cost or latency effects
  where they materially affect the design.

## Reader trust

- Distinguish sourced facts, experimental results, estimates, and author judgment.
- Link primary evidence near the claim it supports.
- State assumptions and tested boundaries; do not turn one benchmark into a
  universal promise.
- Prefer falsifiable claims and reproducible artifacts over confident adjectives.

## Teaching quality

- Give the reader a map before detail and preserve consistent terminology.
- Use diagrams to explain changing state, boundaries, or data flow—not decoration.
- Use examples that build on one another instead of unrelated snippets.
- End each major section with the decision or mental model the reader should retain.
- Meet the 3,000-word floor through evidence, mechanisms, trade-offs, failures,
  and practice rather than generic background or repetition.

## Final review questions

1. Can the reader explain why every major component exists?
2. Can the reader reproduce at least one important result?
3. Can the reader identify when the proposed design should not be used?
4. Does each diagram answer a question that prose alone would make harder?
5. Is the article useful even if the reader never adopts the exact implementation?
