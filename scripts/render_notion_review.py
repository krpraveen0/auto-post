#!/usr/bin/env python3
"""Render canonical article Markdown for Notion and validate its read-back."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


FRONT_MATTER = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
DISPLAY_MATH = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)
INLINE_MATH = re.compile(r"\\\((.+?)\\\)")
IMAGE = re.compile(r"!\[([^\]]+)\]\(([^)]+)\)")
FENCE = re.compile(r"^```([^\s`]*)", re.MULTILINE)
HEADING = re.compile(r"^(#{1,4})\s+(.+?)\s*$", re.MULTILINE)


class RenderingError(ValueError):
    """The source cannot be converted into a reliable Notion review page."""


@dataclass(frozen=True)
class RenderReport:
    source_sha256: str
    display_equations: int
    inline_equations: int
    diagrams: int
    images: int
    headings: list[str]
    code_languages: list[str]


@dataclass(frozen=True)
class ReadbackReport:
    valid: bool
    issues: list[str]


def strip_front_matter_and_title(markdown: str, title: str | None) -> str:
    body = FRONT_MATTER.sub("", markdown, count=1)
    if title:
        body = re.sub(r"\A#\s+" + re.escape(title) + r"\s*\n+", "", body, count=1)
    return body.strip() + "\n"


def resolve_asset(article_path: Path, target: str) -> Path:
    clean_target = target.split("#", 1)[0].split("?", 1)[0]
    return (article_path.parent / clean_target).resolve()


def render_image(match: re.Match[str], article_path: Path) -> tuple[str, str]:
    alt, target = match.groups()
    if re.match(r"https?://", target):
        if target.lower().split("?", 1)[0].endswith(".svg"):
            raise RenderingError("remote SVG images are not reliable in Notion")
        return match.group(0), "image"

    asset = resolve_asset(article_path, target)
    if asset.suffix.lower() != ".svg":
        if not asset.is_file():
            raise RenderingError(f"image does not exist: {target}")
        return match.group(0), "image"

    mermaid = asset.with_suffix(".mermaid")
    png = asset.with_suffix(".png")
    if mermaid.is_file():
        source = mermaid.read_text(encoding="utf-8").strip()
        supported = ("flowchart", "sequenceDiagram", "graph ", "stateDiagram")
        if not source.startswith(supported):
            raise RenderingError(f"unsupported Mermaid source: {mermaid}")
        return f"```mermaid\n{source}\n```\n\n_{alt}_", "diagram"
    if png.is_file():
        relative = png.relative_to(article_path.parent).as_posix()
        return f"![{alt}]({relative})", "image"
    raise RenderingError(f"SVG requires a sibling .mermaid or .png Notion fallback: {target}")


def render(article_path: Path, title: str | None = None) -> tuple[str, RenderReport]:
    raw = article_path.read_bytes()
    body = strip_front_matter_and_title(raw.decode("utf-8"), title)
    counts = {"display": 0, "inline": 0, "diagram": 0, "image": 0}

    def display(match: re.Match[str]) -> str:
        counts["display"] += 1
        return f"$$\n{match.group(1).strip()}\n$$"

    def inline(match: re.Match[str]) -> str:
        counts["inline"] += 1
        return "$`" + match.group(1).strip() + "`$"

    def image(match: re.Match[str]) -> str:
        converted, kind = render_image(match, article_path)
        counts[kind] += 1
        return converted

    body = DISPLAY_MATH.sub(display, body)
    body = INLINE_MATH.sub(inline, body)
    body = IMAGE.sub(image, body)
    if DISPLAY_MATH.search(body) or INLINE_MATH.search(body):
        raise RenderingError("raw LaTeX delimiters remain after conversion")

    report = RenderReport(
        source_sha256=hashlib.sha256(raw).hexdigest(),
        display_equations=counts["display"],
        inline_equations=counts["inline"],
        diagrams=counts["diagram"],
        images=counts["image"],
        headings=[value.strip() for _, value in HEADING.findall(body)],
        code_languages=[language for language in FENCE.findall(body) if language],
    )
    return body, report


def validate_readback(text: str, expected: RenderReport) -> ReadbackReport:
    issues: list[str] = []
    if DISPLAY_MATH.search(text) or INLINE_MATH.search(text):
        issues.append("raw LaTeX bracket delimiters remain")
    if re.search(r"!\[[^\]]+\]\(https?://[^)]+\.svg(?:\?[^)]*)?\)", text, re.I):
        issues.append("remote SVG remains in the Notion page")

    equation_count = len(re.findall(r"(?m)^\$\$\s*$", text)) // 2
    inline_count = len(re.findall(r"\$`.+?`\$", text))
    diagram_count = len(re.findall(r"(?m)^```mermaid\s*$", text))
    if equation_count != expected.display_equations:
        issues.append(f"display equation count differs: expected {expected.display_equations}, got {equation_count}")
    if inline_count < expected.inline_equations:
        issues.append(f"inline equation count differs: expected at least {expected.inline_equations}, got {inline_count}")
    if diagram_count != expected.diagrams:
        issues.append(f"diagram count differs: expected {expected.diagrams}, got {diagram_count}")

    actual_headings = {value.strip() for _, value in HEADING.findall(text)}
    missing_headings = [value for value in expected.headings if value not in actual_headings]
    if missing_headings:
        issues.append("missing headings: " + ", ".join(missing_headings))
    actual_languages = set(FENCE.findall(text))
    missing_languages = sorted(set(expected.code_languages) - actual_languages)
    if missing_languages:
        issues.append("missing code languages: " + ", ".join(missing_languages))
    return ReadbackReport(valid=not issues, issues=issues)


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    render_command = commands.add_parser("render")
    render_command.add_argument("article", type=Path)
    render_command.add_argument("--title")
    render_command.add_argument("--output", type=Path, required=True)
    render_command.add_argument("--report", type=Path, required=True)
    validate_command = commands.add_parser("validate-readback")
    validate_command.add_argument("readback", type=Path)
    validate_command.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "render":
            rendered, report = render(args.article, args.title)
            args.output.write_text(rendered, encoding="utf-8")
            args.report.write_text(json.dumps(asdict(report), indent=2) + "\n", encoding="utf-8")
        else:
            expected = RenderReport(**json.loads(args.report.read_text(encoding="utf-8")))
            result = validate_readback(args.readback.read_text(encoding="utf-8"), expected)
            if not result.valid:
                for issue in result.issues:
                    print(f"Notion read-back failed: {issue}", file=sys.stderr)
                return 1
            print("Notion read-back passed")
        return 0
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RenderingError) as exc:
        print(f"Notion rendering failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
