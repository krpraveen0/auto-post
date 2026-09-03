# Publishing Metadata Schema 3

Place this front matter at the beginning of every new or substantially revised
course lesson. Replace every placeholder with truthful, reviewed information.

```yaml
---
publishing_schema_version: 3
title: A specific, descriptive title
subtitle: The concrete outcome or decision the reader will gain
author: Human author responsible for the article
slug: lowercase-kebab-case-slug
status: reviewed-draft
tags: tag-one, tag-two, tag-three, tag-four
canonical_strategy: set-on-first-publication
ai_assistance: Accurate description of material AI assistance and human review
last_verified: YYYY-MM-DD
---
```

## Field Rules

- `title` and `subtitle` must describe the content without clickbait.
- `author` names the human who reviewed and stands behind every claim.
- `slug` remains stable after the first public release.
- `status` is `draft`, `reviewed-draft`, `approved`, `published`, or `corrected`.
- `tags` contains no more than four portable tags; a Medium adapter may add a
  fifth topic after review.
- `canonical_strategy` is `set-on-first-publication` until the first public URL
  exists, then becomes that canonical URL in the manifest and platform adapters.
- `ai_assistance` accurately describes generated text, images, research support,
  and the human verification performed. The reader-facing disclosure must also
  appear within the first two paragraphs when required by the platform.
- `last_verified` changes only after technical claims and examples are checked.

Keep platform-specific fields such as DEV `published`, Hashnode SEO description,
or Medium topics in adapter metadata rather than altering the canonical body.
