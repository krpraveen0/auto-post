# Global Technical Publishing Standard

This standard defines the common package for Medium, DEV Community, Hashnode,
Notion, and an owned website. Platform rules change, so the release reviewer must
check current official guidance before publication.

## Common Quality Standard

Every article must provide:

- a descriptive, non-clickbait title and a specific reader promise;
- an original implementation, experiment, framework, comparison, or failure
  analysis beyond summarizing existing pages;
- accurate authorship and a transparent explanation of material AI assistance;
- reproducible code or explicitly labeled pseudocode, with versions and expected
  output;
- primary-source evidence, boundaries, trade-offs, and correction readiness;
- semantic headings, descriptive links, equivalent image alt text, and no
  essential code embedded only as an image;
- globally clear language, consistent terminology, expanded acronyms, and
  unambiguous dates, times, and units;
- one canonical-source strategy before cross-posting;
- a desktop and mobile preview where the platform supplies those previews.

## Length Policy

The editorial depth floor is 3,000 reader-facing body words, which is roughly an
18-minute technical read at 170 words per minute. This is an internal learning-
depth standard, not a claim that search engines reward a particular length.
Google explicitly warns against writing to a word count believed to be preferred
by search engines.

- Treat fewer than 3,000 body words as a critical publishing failure.
- Target 3,400–3,800 words when code, diagrams, or exercises materially slow the
  reader; do not pad an article to reach that range.
- Add depth for evidence, implementation, comparison, failure modes, or practice.
- Remove repetition, filler, generic motivation, and duplicated background.
- Add a short reading path to every article at or above 3,000 words.
- Split the article only when it contains multiple independent outcome sets.

## Benchmark-Informed Depth

Before drafting, review at least three strong resources selected for the topic,
including experienced practitioners, primary technical sources, or institutional
engineering publications. A curated directory can help discover candidates, but
the directory itself is not evidence for a technical claim.

Learn from successful explanatory patterns without copying another author's
voice, wording, or section order. Strong long-form technical writing commonly:

- starts with a precise observation, problem, or architecture decision;
- builds from a small system to a more complete one;
- explains why components exist and when they are unnecessary;
- pairs abstractions with traces, code, diagrams, or measured examples;
- makes uncertainty and scope explicit;
- treats failure modes, trade-offs, evaluation, and observability as core
  content rather than closing disclaimers;
- provides navigation so readers can skip background without losing the main
  argument.

Every article must still make a defensible original contribution. Benchmarking
is for quality calibration, not imitation.

## Platform Adapters

### Medium

- Follow Medium Rules and current distribution guidance.
- Disclose material AI-generated or AI-assisted text within the first two
  paragraphs; caption AI-generated images accordingly.
- Do not publish duplicate copies of one story inside Medium.
- Set a canonical link when republishing from another public source.
- Use an honest title, subtitle, visual, and topics; avoid clickbait and low-value
  mass-produced content.

### DEV Community

- Use supported Markdown and Jekyll-style front matter.
- Use at most four relevant tags and a canonical_url for a cross-post.
- Put related lessons in a series.
- Disclose AI assistance and ensure the human author already understands and has
  checked the educational material.

### Hashnode

- Add title, subtitle, cover where useful, series, SEO title, and description.
- Use Original URL when republishing.
- Check the web, mobile, and email previews provided by the editor.

### Owned Website

- Use one H1, descriptive hierarchical headings, crawlable descriptive links,
  equivalent text alternatives, canonical metadata, and clear author information.
- Preserve portable code fences and responsive visual assets.
- Optimize for helpful, reliable, people-first content, not search manipulation.

## Official References

- [Medium distribution guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution)
- [Medium AI content policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy)
- [Medium canonical-link guidance](https://help.medium.com/hc/en-us/articles/360033930293-Set-a-canonical-link)
- [DEV writing, editing, series, and cross-posting](https://dev.to/help/writing-editing-scheduling)
- [DEV AI-assisted article guidelines](https://dev.to/guidelines-for-ai-assisted-articles-on-dev/)
- [Hashnode: Writing a Blog Post](https://docs.hashnode.com/blogs/editor/writing-a-blog-post)
- [Google: Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google developer documentation style guide](https://developers.google.com/style)
- [Google: Write for a global audience](https://developers.google.com/style/translation)
- [W3C WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/)
