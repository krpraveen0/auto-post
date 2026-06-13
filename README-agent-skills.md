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

medium/
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

The orchestrator should call specialized skills in order:

1. Angle strategist
2. Evidence validator
3. Technical architect reviewer
4. Human story editor
5. Compression editor
6. Visual draw.io designer
7. Publishing package

## Core rule

A Medium article is ready when it is:

- useful
- honest
- human
- technically safe
- visually supported
- ready to publish without endless polishing
