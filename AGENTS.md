# Repository Guidelines

## Project Structure & Module Organization

This repository is a content and workflow workspace for Medium-style technical articles. Core article work lives under `medium/`: `ideas/` for topic seeds, `research/claim_register/` for evidence tracking, `drafts/00_raw` through `drafts/04_final` for staged writing, `visuals/drawio/` for editable diagrams, `visuals/exported/` for rendered assets, `publishing/` for final platform copy, and `reviews/scorecards/` for editorial review. Reusable prompts and editorial forms live in `medium/templates/`. Agent skill definitions are under `.github/skills/`, with global writing instructions in `.github/instructions/`. Top-level `articles/`, `courses/`, `personas/`, `social-posts/`, and `diagrams/` contain standalone content assets.

## Build, Test, and Development Commands

There is no application build system or package manager in this repo. Use simple inspection commands before submitting changes:

- `rg "term" medium/` searches drafts, templates, and publishing assets.
- `find medium -maxdepth 3 -type f` reviews the content inventory.
- `git diff --check` catches trailing whitespace and patch formatting issues.
- `git status --short` confirms exactly which files changed.

For visual work, keep both editable `.drawio` files and exported `.svg` files in sync.

## Coding Style & Naming Conventions

Use Markdown for prose and templates. Prefer short paragraphs, descriptive headings, and direct language. Follow the existing article workflow and voice rules: avoid generic AI phrasing, unsupported claims, and decorative visuals. Name article-related files with lowercase kebab-case, for example `llm-one-token-generation.md`, and keep related drafts, claims, visuals, and scorecards under matching slugs.

## Testing Guidelines

Testing is editorial rather than automated. For Medium article changes, verify the title promise, evidence quality, human tone, technical safety, captions, alt text, and visual usefulness. Use `medium/templates/shipping-gate.md` before moving work to `medium/publishing/`. Validate technical claims against primary sources where possible and record important claims in `medium/research/claim_register/`.

## Commit & Pull Request Guidelines

Recent commits use concise imperative messages such as `Add publishing workspace README` and `Add review scorecards workspace placeholder`. Keep commits focused on one content asset, template, or workflow update. Pull requests should summarize the changed content, list affected paths, note any claim-validation work, and include screenshots or exported SVG references when diagrams changed.

## Agent-Specific Instructions

For Medium article tasks, use the skills in `.github/skills/` in the staged workflow described by `README-agent-skills.md`. Do not skip human review gates for final publishing packages.
