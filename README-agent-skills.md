# Medium Article Agent Skills for `auto-post`

This repository stores modular agent skills and templates for creating high-quality Medium articles with a human-in-the-loop editorial workflow.

The system is designed for technical writing, especially:

- AI engineering
- LLM inference
- MLOps
- software architecture
- production engineering
- project-based tutorials
- technical essays with original diagrams

## What this repository contains

```text
.github/
  copilot-instructions.md
  instructions/
    medium-writing.instructions.md
  skills/
    medium-orchestrator/
    medium-angle-strategist/
    medium-evidence-validator/
    medium-human-story-editor/
    medium-technical-architect-reviewer/
    medium-compression-editor/
    medium-visual-drawio-designer/
    medium-publishing-package/
    medium-course-orchestrator/

medium/
  course_series/
  templates/
  ideas/
  research/
  drafts/
  visuals/
  publishing/
  reviews/
```

## How to use

Ask Copilot or agent mode:

```text
Use the medium-orchestrator skill to create a Medium article package for:
Topic: [topic]
Target reader: [reader]
Available experience: [your notes]
Required visuals: draw.io
```

For a course series, ask:

```text
Use the medium-course-orchestrator skill to convert this curriculum into a Medium course series:
Course: [course name]
Target reader: [reader]
Starting skill level: [baseline]
Final learner outcome: [outcome]
Preferred number of lessons: [count]
```

The orchestrator should call specialized skills in order:

1. Angle strategist
2. Evidence validator
3. Technical architect reviewer
4. Human story editor
5. Compression editor
6. Visual draw.io designer
7. Publishing package

The course orchestrator should first create a course map, lesson sequence, project thread, and continuity checks. Then each lesson should pass through the normal article workflow.

Structural automation and reader-value review are separate gates. Run
`bash scripts/run_quality_pipeline.sh` to test executable examples, validate
schema-3 lesson structure, and verify the hashes in every article manifest. A
lesson can move to human review only after an evidence-backed editorial score of
at least 85/100 with no critical issues. It is publishable only after a named
human approves it and its Notion mirror is read back and verified.

Before outlining, complete `medium/templates/research-dossier.md`. Before the
substance draft, create a section contract for each major explanatory section
and verify the companion example contract. Reviews must use the adversarial
review template and name the canonical Markdown SHA-256. After publication,
record reader-learning evidence instead of treating views as proof of teaching.

## Core rule

A Medium article is ready when it is:

- useful
- honest
- human
- technically safe
- visually supported
- backed by reproducible examples and traceable evidence
- explicitly approved by a human for publication

A Medium course series is ready when each lesson is individually useful and the full sequence has clear progression, exercises, previous/next navigation, and a concrete learner outcome.
