# Medium Writing Instructions

Apply these instructions to files under `medium/**`, article drafts, course-series plans, publishing packages, and visual briefs.

## Required workflow

1. Define reader promise.
2. Select angle/title/subtitle.
3. Complete the research dossier: question tree, prerequisites, misconceptions,
   evidence plan, unknowns, experiments, scope, and non-goals.
4. Benchmark strong existing resources and define a verifiable original contribution.
5. Create section contracts and an outline that satisfies them.
6. Build and verify the runnable companion artifact before relying on its results.
7. Draft substance to satisfy every section contract.
8. Run a gap and misconception review, then a reader-simulation pass.
9. Rewrite for human story.
10. Compress repetition only after the verified substance draft is complete.
11. Add and inspect explanatory draw.io visuals.
12. Run independent adversarial specialist reviews against the exact Markdown hash.
13. Pass structural, package, editorial, and named-human shipping gates.
14. After publication, collect reader-learning evidence and revise from observed gaps.

## Course-series workflow

For Medium course series, create the course map before drafting lessons:

1. Define the final learner outcome.
2. Set the reader's starting skill level.
3. Break modules into focused lessons.
4. Map prerequisites and dependencies.
5. Define one exercise or project milestone per lesson.
6. Plan a consistent visual system.
7. Design each lesson backward: outcomes, evidence of learning, then content.
8. Draft each lesson through the evidence-informed lesson arc below.
9. Review continuity across the full series.
10. Add previous/next navigation and a course index.

## Evidence-informed lesson arc

Use this sequence for developer and student readers. It combines backward
design, active learning, worked-example scaffolding, retrieval practice, and
accessible representation without claiming that one method fits every learner.

1. Open with a concrete problem or decision the reader recognizes.
2. State two to four observable learning outcomes.
3. Activate prior knowledge and identify prerequisites.
4. Introduce one mental model with a necessary explanatory visual.
5. Model the reasoning in a worked example, including a mistake or tradeoff.
6. Move from guided practice to a small independent task.
7. Give expected output and check-your-work criteria for timely feedback.
8. Add two to four retrieval questions and one transfer prompt.
9. Recap the durable model and connect the artifact to the next lesson.

Keep intrinsic technical difficulty; remove avoidable cognitive load. Present
code and its explanation together, disclose boundaries, and adapt scaffolding to
the reader's prior knowledge.

## Final article quality gate

The article must:

- deliver the title promise
- sound human and conversational
- include useful examples
- avoid unsupported claims
- avoid AI-generated structure smell
- include visuals that explain, not decorate
- include captions and alt text for visuals
- include a respectful ending or next-step prompt
- provide original implementation, experiment, framework, or analysis rather
  than a rewritten summary of existing sources
- document the tested environment, versions, expected output, and verification
  method for technical examples
- include an accurate byline and disclose material AI assistance according to
  the target platform's current policy
- use descriptive headings and links, equivalent alt text, and globally clear,
  inclusive language
- define a canonical-link strategy before cross-posting
- complete `medium/templates/competitive-content-benchmark.md`; stop or reframe
  when the article adds no defensible value beyond stronger existing resources
- complete `medium/templates/research-dossier.md` before outlining
- complete a `medium/templates/section-contract.md` for every major explanatory section
- satisfy `medium/templates/reproducible-example-contract.md` for technical artifacts
- run role-separated reviews using `medium/templates/adversarial-review.md`
- bind every approval and review to the exact canonical Markdown SHA-256

Use 3,000 reader-facing body words as the minimum depth gate and target an
approximately 18-minute technical read. Reach the floor through additional
evidence, implementation, failure analysis, comparison, examples, or practice;
never through repetition or generic background. Articles at or above 3,000 words
must include a short reading path.

The 3,000-word threshold is a minimum useful-depth gate, not a target to optimize.
For a typical deep dive, aim for 3,500–5,000 words when the coherent reader
promise requires it. A long article without original evidence, an inspectable
artifact, or a defensible synthesis still fails.

## Course lesson quality gate

Each lesson must:

- teach one primary concept
- state concrete learning outcomes
- use observable outcome verbs and fulfill them in the lesson
- activate relevant prior knowledge before adding new concepts
- respect prerequisites from earlier lessons
- include a worked example that exposes the reasoning process
- include guided or independent practice with expected output and self-checks
- include retrieval questions and a transfer prompt
- advance the course project thread
- end with a bridge to the next lesson
- avoid repeating full context from prior parts
- include at least one real explanatory visual, not a visual placeholder
- target 90+/100 and score at least 85/100 on
  `medium/templates/course-lesson-scorecard.md`
- have zero critical failures in `medium/templates/shipping-gate.md`

## Draft and publishing surfaces

- Notion may be the collaborative drafting and reader-preview surface.
- Markdown in the repository is the portable, reviewable canonical snapshot.
- A Notion page must not be treated as published until its content was read back,
  visually checked, and matched to the repository snapshot.
- Office-document formats are outside this workflow. Do not generate or validate
  DOCX artifacts.
- Create a small platform adapter for Medium, DEV, Hashnode, or an owned site;
  do not fork the article body into independently edited copies.

## Global platform contract

- Use publishing schema version 3 with title, subtitle, author, slug, status,
  tags, canonical strategy, AI-assistance note, and last-verified date.
- Keep the body in portable Markdown: descriptive headings, fenced code with
  language identifiers, descriptive links, and image alt text.
- Set the canonical URL when the first public version is known and reuse it on
  cross-posts where the platform supports canonical links.
- Preview the target platform on desktop and mobile where available.
- Follow the platform's current rules on AI disclosure, duplicate content,
  tagging, cover images, and distribution before the human presses Publish.

## Voice rules

- Prefer specific observation over generic introduction.
- Use first person when it clarifies real experience.
- Use second person when guiding the reader.
- Avoid academic filler.
- Avoid shallow motivational phrasing.
- Prefer concrete examples and small experiments.
- Avoid idioms, slang, culture-specific jokes, ambiguous dates, and unexplained
  acronyms that make the article harder to translate or understand globally.
