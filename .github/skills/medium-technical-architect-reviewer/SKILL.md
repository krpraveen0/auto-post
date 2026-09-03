# Medium Technical Architect Reviewer Skill

## Purpose

Review technical correctness, architecture quality, and production realism.

## Checks

- Are explanations accurate?
- Are tradeoffs explained?
- Are simplified explanations still safe?
- Are metrics used correctly?
- Are examples realistic?
- Are diagrams architecturally meaningful?
- Would a senior engineer trust this?
- Is the review bound to the exact canonical Markdown SHA-256?
- Can empirical results be regenerated from committed raw data?
- Have happy-path assumptions been challenged with failure fixtures?
- Does the simplification state where it stops being accurate?

## Output

Provide:

```text
Accuracy issues:
Missing nuance:
Overclaims:
Suggested examples:
Diagram improvements:
Publication risk:
Final score:
```

For every score of 8/10 or higher, cite exact evidence from the reviewed artifact.
A score of 10/10 must state why no material improvement is currently known.
Missing evidence, runnable artifacts, or required visuals cannot be averaged away.

## Scoring

Score 1–10:

- technical correctness
- production realism
- terminology precision
- tradeoff quality
- reader trust
