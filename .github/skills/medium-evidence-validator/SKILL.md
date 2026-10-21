# Medium Evidence Validator Skill

## Purpose

Validate factual and technical claims before they enter a Medium article.

## Source priority

1. Official documentation
2. Research papers
3. Official engineering blogs
4. GitHub repositories
5. Reputable publications
6. Original experiments
7. Personal experience

## Claim register format

For every important claim, record:

```markdown
## Claim
Claim:
Source:
Source type:
Confidence:
Safe wording:
Risk if overstated:
Use in article:
Exact supporting location:
Contradicting or qualifying evidence:
Experiment or reproduction:
Last verified:
```

## Rules

- Do not overclaim benchmarks.
- Distinguish vendor claims from independent results.
- Prefer “in the evaluated setting” for benchmark claims.
- Do not cite weak blogs for technical facts.
- Do not include a claim if it cannot be defended.
- Separate observation, interpretation, hypothesis, and recommendation.
- Require committed raw data and a regeneration command for empirical claims.
- Record uncertainty and credible conflicting evidence instead of forcing consensus.

## Output

Create or update a claim register in:

```text
medium/research/claim_register/[article_slug]_claims.md
```
