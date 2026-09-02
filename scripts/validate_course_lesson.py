#!/usr/bin/env python3
"""Score portable, evidence-informed technical lessons before publishing.

The validator checks repository Markdown only. It has no office-document,
platform API, or third-party Python dependency. Schema 3 packages declare
``publishing_schema_version: 3`` in front matter or a sibling JSON manifest.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


CURRENT_SCHEMA = 3
PUBLISHING_THRESHOLD = 85
TARGET_SCORE = 90
MIN_BODY_WORDS = 3000
TECHNICAL_READING_WPM = 170
MEASURABLE_VERBS = {
    "apply", "build", "classify", "compare", "configure", "create", "debug",
    "define", "design", "diagnose", "distinguish", "evaluate", "explain",
    "implement", "justify", "measure", "refactor", "test", "trace",
}
REQUIRED_METADATA = {
    "title",
    "subtitle",
    "author",
    "slug",
    "status",
    "tags",
    "canonical_strategy",
    "ai_assistance",
    "last_verified",
}


@dataclass(frozen=True)
class Criterion:
    name: str
    score: int
    evidence: str


@dataclass(frozen=True)
class LessonReport:
    path: str
    publishing_schema_version: int | None
    word_count: int
    estimated_read_minutes: int
    total_score: int
    target_score: int
    threshold: int
    publishable: bool
    criteria: list[Criterion]
    critical_issues: list[str]
    recommendations: list[str]


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def front_matter(text: str) -> dict[str, str]:
    match = re.search(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([a-zA-Z][\w-]*):\s*(.*?)\s*$", line)
        if field:
            values[field.group(1)] = field.group(2).strip("'\"")
    return values


def article_body(text: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)


def headings(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"(?m)^#{2,3}\s+(.+?)\s*$", text)]


def has_heading(text: str, *names: str) -> bool:
    normalized = {heading.casefold() for heading in headings(text)}
    return any(name.casefold() in normalized for name in names)


def section_text(text: str, *names: str) -> str:
    wanted = {name.casefold() for name in names}
    capture: list[str] = []
    active = False
    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            if active:
                break
            active = match.group(1).strip().casefold() in wanted
            continue
        if active:
            capture.append(line)
    return "\n".join(capture).strip()


def schema_version(path: Path, text: str) -> int | None:
    metadata = front_matter(text)
    for key in ("publishing_schema_version", "teaching_schema_version"):
        if key in metadata:
            try:
                return int(metadata[key])
            except ValueError:
                return None

    manifest = path.with_suffix(".json")
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            version = data.get("publishing_schema_version", data.get("teaching_schema_version"))
            return int(version) if version is not None else None
        except (json.JSONDecodeError, TypeError, ValueError):
            return None
    return None


def count_questions(text: str) -> int:
    return text.count("?")


def visual_details(text: str) -> tuple[bool, bool, bool]:
    images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)
    actual = any(target.strip() and "placeholder" not in target.casefold() for _, target in images)
    useful_alt = any(len(alt.strip().split()) >= 5 for alt, _ in images)
    caption = bool(re.search(r"(?mi)^(?:\*\*)?(?:figure|diagram)\s*\d*[:.]", text))
    return actual, useful_alt, caption


def long_paragraphs(text: str, limit: int = 180) -> list[int]:
    prose = re.sub(r"```[^\n]*\n.*?\n```", "", text, flags=re.DOTALL)
    paragraphs = re.split(r"\n\s*\n", prose)
    return [word_count(paragraph) for paragraph in paragraphs if word_count(paragraph) > limit]


def code_fence_details(text: str) -> tuple[int, int]:
    fences = re.findall(r"(?m)^```([^\n`]*)$", text)
    language_tagged = sum(1 for value in fences if value.strip())
    return len(fences) // 2, language_tagged


def score_lesson(path: Path, require_schema: int | None = None) -> LessonReport:
    text = path.read_text(encoding="utf-8")
    lowered = text.casefold()
    metadata = front_matter(text)
    version = schema_version(path, text)
    critical: list[str] = []
    recommendations: list[str] = []
    scores: list[Criterion] = []

    if require_schema is not None and version != require_schema:
        critical.append(
            f"Publishing schema must be version {require_schema}; found {version or 'none'}."
        )

    missing_metadata = sorted(REQUIRED_METADATA - metadata.keys())
    if missing_metadata and require_schema == CURRENT_SCHEMA:
        critical.append("Add required front-matter metadata: " + ", ".join(missing_metadata) + ".")

    if version == CURRENT_SCHEMA or require_schema == CURRENT_SCHEMA:
        tags = [tag.strip() for tag in metadata.get("tags", "").strip("[]").split(",") if tag.strip()]
        if not 1 <= len(tags) <= 4:
            critical.append("Use one to four portable tags; platform adapters may narrow or extend them.")
        if metadata.get("status") not in {"draft", "reviewed-draft", "approved", "published", "corrected"}:
            critical.append("Use a supported publication status: draft, reviewed-draft, approved, published, or corrected.")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata.get("slug", "")):
            critical.append("Use a stable lowercase kebab-case slug.")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", metadata.get("last_verified", "")):
            critical.append("Record last_verified as an unambiguous YYYY-MM-DD date.")
        canonical = metadata.get("canonical_strategy", "")
        if canonical != "set-on-first-publication" and not canonical.startswith("https://"):
            critical.append("Set canonical_strategy to set-on-first-publication or an HTTPS canonical URL.")
        if len(metadata.get("ai_assistance", "").split()) < 5:
            critical.append("Describe material AI assistance and human verification in the metadata.")

    total_words = word_count(article_body(text))
    estimated_read_minutes = math.ceil(total_words / TECHNICAL_READING_WPM)
    title_present = bool(re.search(r"(?m)^#\s+\S", text))
    h1_match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    if metadata.get("title") and h1_match and metadata["title"].casefold() != h1_match.group(1).casefold():
        critical.append("Keep the front-matter title and canonical H1 identical.")
    clickbait = bool(re.search(r"(?i)\b(?:you won't believe|mind-blowing|ultimate guide|best ever|secret trick)\b", metadata.get("title", "")))
    if clickbait:
        critical.append("Replace clickbait or exaggerated title language with a descriptive promise.")
    intro = re.split(r"(?m)^##\s+", article_body(text), maxsplit=1)[0]
    authentic_hook = any(
        word in intro.casefold()
        for word in ("when", "you", "debug", "build", "production", "decision", "failure")
    )
    original_value = any(
        phrase in lowered
        for phrase in ("in this article", "you will build", "we will test", "what changes", "the key distinction")
    )
    focus_score = (4 if title_present else 0) + (3 if authentic_hook else 0) + (3 if original_value else 0)
    scores.append(Criterion("Reader promise and original value", focus_score, "Specific title, authentic problem, and explicit value beyond summary."))
    if total_words < MIN_BODY_WORDS:
        critical.append(
            f"Expand the reader-facing body from {total_words} to at least {MIN_BODY_WORDS} words "
            "with useful implementation, evidence, failure analysis, comparison, or practice."
        )
    if total_words >= MIN_BODY_WORDS and not has_heading(text, "In This Article", "Reading Path", "Contents"):
        critical.append("Add a short reading path for an article of 3,000 words or more.")

    outcomes = section_text(text, "Learning Outcomes")
    outcome_items = re.findall(r"(?m)^\s*(?:\d+\.|[-*])\s+(.+)$", outcomes)
    measurable = sum(
        1 for item in outcome_items
        if any(re.search(rf"\b{verb}\b", item, flags=re.IGNORECASE) for verb in MEASURABLE_VERBS)
    )
    outcomes_score = min(10, (3 if outcomes else 0) + min(3, len(outcome_items)) + min(4, measurable * 2))
    scores.append(Criterion("Observable outcomes and alignment", outcomes_score, f"{len(outcome_items)} outcomes; {measurable} use observable verbs."))
    if not outcomes or not (2 <= len(outcome_items) <= 4):
        critical.append("Include two to four observable learning outcomes.")

    prior = section_text(text, "Before You Start", "Prerequisites")
    prior_prompt = count_questions(prior) > 0 or "recall" in prior.casefold()
    mental_model = section_text(text, "Mental Model")
    scaffolding_score = (3 if prior else 0) + (3 if prior_prompt else 0) + (4 if mental_model else 0)
    scores.append(Criterion("Prior knowledge, scaffolding, and mental model", scaffolding_score, "Prerequisites, activation prompt, and one durable model."))
    if not prior or not mental_model:
        critical.append("Add Before You Start and Mental Model sections that match the reader's prior knowledge.")

    example = section_text(text, "Worked Example")
    code_blocks, language_tagged = code_fence_details(example)
    reasoning = any(term in example.casefold() for term in ("because", "tradeoff", "trade-off", "failure", "mistake", "choose"))
    tested = section_text(text, "Tested Environment", "Reproduce This", "Verification")
    version_context = bool(re.search(r"\b\d+(?:\.\d+){1,3}\b", tested))
    technical_score = (3 if example else 0) + (2 if code_blocks else 0) + (2 if language_tagged == code_blocks and code_blocks else 0) + (2 if reasoning else 0) + (1 if tested and version_context else 0)
    scores.append(Criterion("Technical depth and reproducibility", technical_score, f"Worked reasoning; {code_blocks} code fences; tested environment with versions={bool(tested and version_context)}."))
    if not example or not code_blocks:
        critical.append("Add a worked example with code, configuration, command, or explicitly labeled pseudocode.")
    if code_blocks and language_tagged != code_blocks:
        critical.append("Add a language identifier to every code fence for portable rendering and accessibility.")
    if not tested or not version_context:
        critical.append("Document the tested environment, dependency versions, and verification date or method.")

    practice = section_text(text, "Exercise", "Try It Yourself", "Independent Practice")
    expected_output = bool(re.search(r"(?i)expected output|deliverable|you should have", practice))
    feedback = section_text(text, "Check Your Work", "Self-Check")
    retrieval = section_text(text, "Retrieval Practice")
    retrieval_questions = count_questions(retrieval)
    transfer = bool(re.search(r"(?i)transfer prompt|apply this (?:to|in)|where else", text))
    learning_score = (2 if practice else 0) + (2 if expected_output else 0) + (2 if feedback else 0) + (2 if retrieval_questions >= 2 else 0) + (2 if transfer else 0)
    scores.append(Criterion("Practice, feedback, retrieval, and transfer", learning_score, f"Practice and self-check; {retrieval_questions} retrieval questions; transfer={transfer}."))
    if not practice or not expected_output:
        critical.append("Add an exercise with a concrete expected output.")
    if not feedback or retrieval_questions < 2 or not transfer:
        critical.append("Add self-check criteria, at least two retrieval questions, and a transfer prompt.")

    unresolved = len(re.findall(r"\[SOURCE NEEDED(?::[^\]]+)?\]", text, flags=re.IGNORECASE))
    sources = section_text(text, "Sources", "References", "Evidence")
    links = re.findall(r"https?://[^\s)>]+", sources)
    limitations = any(term in lowered for term in ("limitation", "tradeoff", "trade-off", "when not to", "boundary"))
    evidence_score = (4 if len(links) >= 2 else min(4, len(links) * 2)) + (3 if unresolved == 0 else 0) + (3 if limitations else 0)
    scores.append(Criterion("Evidence, trust, and limitations", evidence_score, f"{len(links)} source links; {unresolved} unresolved markers; limitations={limitations}."))
    if unresolved:
        critical.append(f"Resolve {unresolved} SOURCE NEEDED marker(s) before publishing.")
    if len(links) < 2:
        critical.append("Cite at least two direct primary or institutional sources for important claims.")

    actual_visual, useful_alt, caption = visual_details(text)
    oversized = long_paragraphs(text)
    descriptive_links = not bool(re.search(r"(?i)\[(?:click here|here|link)\]\(", text))
    accessibility_score = (3 if actual_visual else 0) + (2 if useful_alt else 0) + (2 if caption else 0) + (2 if not oversized else 0) + (1 if descriptive_links else 0)
    scores.append(Criterion("Visual explanation and accessibility", accessibility_score, f"Real visual, equivalent alt text, caption, descriptive links; {len(oversized)} oversized paragraphs."))
    if not actual_visual:
        critical.append("Embed a real explanatory visual; an authoring note is not publishable.")
    if actual_visual and not useful_alt:
        critical.append("Add equivalent alt text that communicates the visual's meaning.")
    if actual_visual and not caption:
        critical.append("Add a takeaway caption that explains why the visual matters.")
    if oversized:
        recommendations.append("Split paragraphs longer than 180 words unless the form genuinely benefits comprehension.")
    if not descriptive_links:
        critical.append("Replace vague link labels such as 'click here' with descriptive link text.")

    acronym_expanded = not bool(re.search(r"(?<![A-Z(])\b[A-Z]{3,}\b", intro))
    culturally_specific = any(term in lowered for term in ("piece of cake", "slam dunk", "ballpark", "hit it out of the park"))
    editorial_score = (4 if acronym_expanded else 2) + (3 if not culturally_specific else 0) + (3 if total_words >= 1000 else 1)
    scores.append(Criterion("Global editorial clarity", editorial_score, f"Consistent global English, defined terminology, and an estimated {estimated_read_minutes}-minute technical read."))
    if culturally_specific:
        recommendations.append("Replace culture-specific idioms with literal language that translates clearly.")

    ai_disclosure = "ai" in intro.casefold() and "assist" in intro.casefold()
    navigation = "previous" in lowered and "course index" in lowered and "next" in lowered
    recap = has_heading(text, "Recap")
    next_lesson = has_heading(text, "Next Lesson")
    canonical_strategy = bool(metadata.get("canonical_strategy", "").strip())
    platform_score = (4 if not missing_metadata else 0) + (3 if ai_disclosure else 0) + (3 if canonical_strategy else 0)
    scores.append(Criterion("Platform metadata and disclosure", platform_score, "Portable metadata, early AI disclosure, and canonical strategy."))
    if not ai_disclosure:
        critical.append("Disclose material AI assistance within the first two reader-facing paragraphs.")

    continuity_score = (4 if navigation else 0) + (3 if recap else 0) + (3 if next_lesson else 0)
    scores.append(Criterion("Series continuity and next action", continuity_score, "Previous/index/next navigation, recap, and next-lesson bridge."))
    if not navigation or not recap or not next_lesson:
        critical.append("Include previous/index/next navigation, a recap, and a next-lesson bridge.")

    if "visual guidance" in lowered or "create a diagram" in lowered:
        critical.append("Remove authoring instructions such as Visual Guidance from reader-facing copy.")
    if re.search(r"(?i)(?:sk-[a-z0-9]{20,}|AKIA[0-9A-Z]{16}|password\s*=\s*['\"][^'\"]+)", text):
        critical.append("Remove credentials or secret-like values from the article and examples.")
    if any(command in lowered for command in ("rm -rf", "curl | sh", "curl|sh")) and "safety" not in lowered:
        critical.append("Explain safety boundaries for destructive or pipe-to-shell commands.")

    total = sum(item.score for item in scores)
    publishable = total >= PUBLISHING_THRESHOLD and not critical
    if total < PUBLISHING_THRESHOLD:
        recommendations.append(f"Raise the reader-value score from {total} to at least {PUBLISHING_THRESHOLD}; target {TARGET_SCORE}+.")

    return LessonReport(
        path=str(path),
        publishing_schema_version=version,
        word_count=total_words,
        estimated_read_minutes=estimated_read_minutes,
        total_score=total,
        target_score=TARGET_SCORE,
        threshold=PUBLISHING_THRESHOLD,
        publishable=publishable,
        criteria=scores,
        critical_issues=critical,
        recommendations=recommendations,
    )


def discover_current(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.md")):
        if schema_version(path, path.read_text(encoding="utf-8")) == CURRENT_SCHEMA:
            yield path


def write_report(report: LessonReport, report_dir: Path | None) -> None:
    payload = asdict(report)
    if report_dir:
        report_dir.mkdir(parents=True, exist_ok=True)
        output = report_dir / f"{Path(report.path).stem}-reader-value.json"
        output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"{report.path}: {report.total_score}/100 — {'PUBLISH' if report.publishable else 'REVISE'}")
    for issue in report.critical_issues:
        print(f"  critical: {issue}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--discover-current", action="store_true")
    parser.add_argument("--require-schema", type=int)
    parser.add_argument("--report-dir", type=Path)
    args = parser.parse_args()

    paths = list(args.paths)
    if args.root:
        paths.extend(
            discover_current(args.root)
            if args.discover_current
            else sorted(args.root.rglob("*.md"))
        )
    paths = sorted(set(paths))
    if not paths:
        print("No matching course lessons found; nothing to validate.")
        return 0

    reports = [score_lesson(path, args.require_schema) for path in paths]
    for report in reports:
        write_report(report, args.report_dir)
    return 0 if all(report.publishable for report in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
