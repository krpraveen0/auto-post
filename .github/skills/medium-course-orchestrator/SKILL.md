# Medium Course Orchestrator Skill

## Purpose

Use this skill to turn a course idea or curriculum into a coherent Medium course series.

## When to use

Use when the user asks to:

- create a Medium course series
- convert a curriculum into Medium articles
- plan lessons, modules, projects, or a capstone
- improve continuity across multiple technical posts

## Workflow

Run these stages in order:

1. Course intake
2. Reader and skill baseline
3. Series promise and scope
4. Module-to-lesson breakdown
5. Lesson dependency map
6. Backward lesson design: observable outcomes and evidence of learning
7. Prior-knowledge and cognitive-load plan
8. Worked example, guided practice, independent exercise, and feedback design
9. Retrieval and transfer prompts
10. Evidence and claim plan
11. Competitive-content benchmark and original contribution
12. Visual system plan
13. Draft each lesson through `medium-orchestrator`
14. Verify runnable artifacts, raw data, failure fixtures, and derived visuals
15. Run independent adversarial reviews against the canonical Markdown hash
16. Reader-value score and critical shipping gate
17. Course continuity review
18. Notion preview plus canonical Markdown snapshot
19. Cross-platform metadata, disclosure, and canonical-link review
20. Lesson publishing packages
21. Series index and navigation copy
22. Collect reader-learning and transfer evidence for revision

## Required specialist skills

Use these article skills for each lesson:

- `medium-angle-strategist`
- `medium-evidence-validator`
- `medium-technical-architect-reviewer`
- `medium-human-story-editor`
- `medium-compression-editor`
- `medium-visual-drawio-designer`
- `medium-publishing-package`

## Output format

For every course series, produce:

```text
Course title:
Target reader:
Starting skill level:
Final learner outcome:
Series promise:
Module map:
Lesson sequence:
Prerequisites by lesson:
Project thread:
Evidence plan:
Visual system:
Publishing cadence:
Series index:
Continuity review:
```

For every lesson, produce:

```text
Series:
Part number:
Lesson title:
Reader state before lesson:
Learning outcomes:
Prerequisites:
Prior-knowledge prompt:
Core concept:
Mental model:
Worked example:
Tested environment and versions:
Verification method:
Guided practice:
Independent exercise:
Expected output:
Check-your-work criteria:
Retrieval questions:
Transfer prompt:
Evidence notes:
Strong existing resources and their gaps:
Original contribution:
Visuals:
Recap:
Next lesson bridge:
Reader-value score:
Notion draft URL:
Author and AI disclosure:
Canonical-link strategy:
Publishing package:
```

## Quality rules

- Each lesson teaches one primary concept.
- Outcomes must use observable verbs and align with practice and assessment.
- Every lesson must activate relevant prior knowledge.
- Every lesson must include a concrete worked example and an exercise.
- Scaffolding must move from modeled reasoning toward independent work.
- Practice must include expected output and check-your-work criteria.
- Every lesson must include retrieval questions and a transfer prompt.
- Do not introduce unexplained terms from future lessons.
- Do not repeat full setup context in every lesson; link back to earlier parts.
- Every lesson must move the reader closer to the final project.
- The series must include previous/next navigation and a course index.
- Visuals must explain a relationship, decision, or sequence; decorative or
  placeholder visuals do not satisfy the gate.
- Target 90+/100 evidence-backed reader-value points. Publishing requires at
  least 85/100, zero critical failures, and explicit human approval. The
  deterministic Markdown validator measures structural coverage only and must
  never create or approve the reader-value score.
- Every lesson contains at least 3,000 reader-facing body words and targets an
  approximately 18-minute technical read. Additional length must provide
  evidence, implementation, failure analysis, comparison, or practice—not
  padding—and every qualifying lesson includes a short reading path.
- Every technical example must record the tested environment, versions, expected
  behavior, and verification method.
- Use publishing schema version 3 and keep the canonical article body in portable
  Markdown. Do not generate DOCX.
- Include accurate authorship, material AI-assistance disclosure, canonical-link
  strategy, global-English review, and platform previews.
- Do not claim the article or method is universally superior. Demonstrate value
  through originality, reproducible evidence, reader outcomes, and corrections.
