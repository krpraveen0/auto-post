# Codex Daily World-Class Technical Article Automation

This runbook creates one evidence-informed technical course article per run.
Codex and Notion support research and collaborative review; Markdown, JSON, and
versioned visual assets are the complete portable publishing package. No office
document is generated.

## Automation Settings

Name: `Daily World-Class Technical Lesson`

Schedule: `06:00 Asia/Kolkata`, every day

Repository: `krpraveen0/auto-post`

Branch policy: create `feature/daily-medium-course-part-XX`; never push directly
to `master`.

Notion parent: `Agentic AI`

Notion workflow page:
[Cloud-Agnostic Medium Course Automation](https://app.notion.com/p/3cdc633ae23a81d7ae49d3624aeb7d16?pvs=204)

## Automation Prompt

```text
You are working in krpraveen0/auto-post.

Your job is to create one deeply useful technical course article for developers
and students. Do not generate DOCX or any office-document artifact. Do not call
api.openai.com or require OPENAI_API_KEY. Use the Codex session for research,
authoring, review, and Notion interaction.

The repository Markdown is the canonical portable article. Notion is the
collaborative reading and review surface. Platform copies are generated from the
same reviewed Markdown and must not become independent drafts.

Every run:
1. Read AGENTS.md, README-agent-skills.md if present, .github/instructions/, and
   every Medium skill required by the repository's staged workflow.
2. Read the course map, state, previous lesson, lesson plan, scorecard, shipping
   gate, competitive-content benchmark, global publishing standard, and relevant
   claim register.
3. Select exactly one lesson from next_part. Never advance the state merely
   because a draft exists.
4. Complete `medium/templates/research-dossier.md`: define the reader question
   tree, prerequisites, misconceptions, evidence obligations, unknowns requiring
   experiments, scope, non-goals, and two to four observable outcomes. Stop
   before outlining if the original contribution is not concrete and verifiable.
5. Find at least three strong existing explanations plus the primary sources
   needed for factual claims. Record transferable patterns in opening, staging,
   examples, visuals, trade-offs, failures, and evaluation. Do not imitate their
   voice, wording, examples, or section order. Identify what they omit,
   oversimplify, or fail to make reproducible. State the article's original
   contribution: an experiment, implementation, failure analysis, decision
   framework, or tested synthesis.
6. Create a section contract for every major explanatory section. Build and
   verify the companion implementation or experiment before using its results.
   The companion directory must satisfy
   `medium/templates/reproducible-example-contract.md`, including tests, a
   failure fixture, raw data, expected output, and regeneration commands.
7. Draft using this learning arc:
   concrete problem; Learning Outcomes; Before You Start; Mental Model; Worked
   Example; Tested Environment; Exercise; Check Your Work; Retrieval Practice;
   Recap; Next Lesson; Sources. Include at least one transfer prompt.
8. Produce at least 3,000 reader-facing body words and target an approximately
   18-minute technical read. Expand through evidence, implementation detail,
   failure modes, comparisons, or practice; remove repetition and filler. Add a
   short reading path. Split into multiple lessons only when the outcomes stop
   forming one coherent learning unit.
9. Verify every important technical claim against primary documentation or a
   reproducible experiment. Run code and commands where the repository permits.
   Record versions, operating environment, expected output, failure output, and
   the verification date. Label pseudocode explicitly. Never invent citations,
   measurements, quotations, URLs, or product behavior.
10. Create at least one necessary explanatory visual. Keep the editable .drawio
   and exported SVG/PNG synchronized. Embed the real asset with equivalent alt
   text and a caption that states the takeaway. Never ship visual instructions.
11. Write globally clear English: define acronyms, use consistent terminology,
    avoid slang and culture-specific idioms, use unambiguous dates and units, and
    make headings and links descriptive. Do not put essential code or text only
    inside an image.
12. Save the Markdown with publishing_schema_version: 3 and complete front matter:
    title, subtitle, author, slug, status, tags, canonical_strategy,
    ai_assistance, and last_verified. Disclose material AI assistance within the
    first two reader-facing paragraphs. Keep the human author responsible for
    every claim.
13. Create a sibling JSON manifest containing the schema version, Markdown and
    visual hashes, evidence register, tested environment, quality report path,
    Notion page ID/URL, target platforms, canonical strategy, and validation time.
14. Run the repository, lesson-example, structural, and package checks:
    python -m unittest discover -s tests
    python -m unittest discover
      -s medium/examples/agentic-ai-engineering/part-XX -v
    python scripts/validate_course_lesson.py --require-schema 3
      --report-dir medium/reviews/scorecards <lesson.md>
    python scripts/validate_article_package.py <lesson.json>
    The first validator reports structural coverage only. It cannot award a
    reader-value score or approve publication.
15. Run separate adversarial technical, evidence, pedagogy, reproducibility,
    accessibility, global-English, originality, and platform-policy reviews.
    Every review must attempt to falsify its quality claim, cite exact artifact
    evidence, and record the canonical Markdown SHA-256. Scores of 8/10 or above
    require concrete evidence; 10/10 requires an explanation of why no material
    improvement is currently known.
    Target 90+/100. Publishing requires at least 85/100, zero critical issues,
    and named human approval. The deterministic score cannot approve its own
    technical correctness.
16. Create or update one child page below Agentic AI in Notion. Preserve the
    Markdown hierarchy, code, visual, caption, practice, self-check, retrieval,
    disclosure, and sources. Read the page back and compare it with Markdown.
    Record the page ID, URL, and canonical Markdown SHA-256 in the manifest.
17. Prepare platform adapters without changing the article body:
    - Medium: title/subtitle, five or fewer suitable topics, disclosure, visual
      captions, and canonical link when cross-posted. Do not create a duplicate
      Medium story.
    - DEV: Markdown/front matter, no more than four tags, disclosure, series, cover
      image if used, and canonical_url when cross-posted.
    - Hashnode: title/subtitle, series, cover, SEO title/description, preview, and
      Original URL when republishing.
    - Owned site: semantic headings, descriptive links, equivalent alt text,
      canonical metadata, author information, and responsive preview.
18. Return the Notion URL as the review result. The human reads the rendered page
    and decides to approve, request revision, or stop.
19. Never call a Medium publishing API or automate browser publication. After
    approval, the author manually copy-pastes the Notion article to Medium.
20. Update next_part only after Markdown, visuals, evidence, report, manifest,
    specialist reviews, and verified Notion read-back exist. Commit only related
    files to a review branch.

Never claim that the article or teaching method is objectively superior to every
other resource. Demonstrate quality with originality, reproducible evidence,
clarity, accessibility, reader outcomes, and a visible correction process.
```

## Portable Package

```text
lesson.md                         canonical article and metadata
lesson.json                       manifest, hashes, evidence, platform state
visual.drawio                     editable explanatory visual
visual.svg or visual.png          portable rendered visual
reader-value.json                 deterministic gate evidence
claim-register.md                 verified claims and source decisions
Notion page                       primary human reading and decision surface
platform adapter metadata         Medium / DEV / Hashnode / owned site
```

## State and Failure Rules

- Failed research, code verification, visual, validation, policy review, or
  Notion verification leaves the same part ready to retry.
- Re-running a part updates the Notion page stored in the manifest and never
  creates a duplicate.
- The publishing score is a checklist, not a claim of learning effectiveness or
  popularity.
- After public release, record completion, saves, exercise attempts, reader questions,
  corrections, and meaningful discussion. Use the evidence to revise the lesson.
- New or substantively revised lessons must use publishing schema version 3.
- After publication, complete `medium/templates/reader-learning-feedback.md`
  with exercise attempts, successful reproductions, retrieval and transfer
  results, confusion points, and corrections. Views alone are not learning evidence.

## Cloud Validation

`Daily Medium Course Quality Audit` runs on Ubuntu with read-only permissions and
pinned Python dependencies. `Validate Medium Output` enforces schema 3 on changed
lessons during pull requests. Neither workflow generates prose, writes state,
publishes externally, or requires a model API key.

The complete deterministic quality pipeline is also packaged in
`Containerfile.quality`. Any Linux container runner can execute:

```bash
docker build -f Containerfile.quality -t medium-course-quality .
docker run --rm medium-course-quality
```

Remote authoring remains a separate capability. It requires an explicitly
configured hosted model or Codex runtime plus repository and Notion credentials;
the validation container deliberately does not infer or embed those credentials.

## Notion Review Handoff

The authoring pipeline uses the configured Notion connection to create or update
the manifest's page below `Agentic AI`. A rerun updates the same page instead of
creating a duplicate. It then reads the page back, records the source Markdown
SHA-256, and returns the page URL for human review.

Medium remains a manual destination. Do not configure a Medium token, call a
Medium publishing API, or automate browser publication.
