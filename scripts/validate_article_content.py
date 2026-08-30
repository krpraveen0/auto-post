#!/usr/bin/env python3
"""Validate generated lesson evidence, Mermaid, and executable Python examples."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import requests


SAFE_IMPORTS = {
    "collections",
    "dataclasses",
    "datetime",
    "enum",
    "functools",
    "hashlib",
    "itertools",
    "json",
    "math",
    "re",
    "statistics",
    "typing",
}
FORBIDDEN_CALLS = {"compile", "eval", "exec", "open", "__import__"}


def fenced_blocks(article: str, language: str) -> list[str]:
    return re.findall(rf"(?ims)^```{re.escape(language)}\s*\n(.*?)^```\s*$", article)


def evidence_urls(article: str) -> list[str]:
    match = re.search(r"(?ims)^## Evidence\s*$\n(.*?)(?=^## |\Z)", article)
    if not match:
        return []
    return list(dict.fromkeys(re.findall(r"https://[^\s)>\]]+", match.group(1))))


def check_python_safety(code: str) -> None:
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
            if any(name not in SAFE_IMPORTS for name in names):
                raise ValueError(f"unsafe import in Python example: {', '.join(names)}")
        elif isinstance(node, ast.ImportFrom):
            name = (node.module or "").split(".")[0]
            if name not in SAFE_IMPORTS:
                raise ValueError(f"unsafe import in Python example: {name}")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_CALLS:
                raise ValueError(f"forbidden call in Python example: {node.func.id}")


def run_python(code: str) -> dict[str, str | int]:
    check_python_safety(code)
    with tempfile.TemporaryDirectory() as directory:
        script = Path(directory) / "example.py"
        script.write_text(code, encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, "-I", str(script)],
            cwd=directory,
            env={"PATH": os.environ.get("PATH", "")},
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    if completed.returncode:
        raise ValueError(
            f"Python example failed with exit code {completed.returncode}: "
            f"{completed.stderr[-600:]}"
        )
    return {"exit_code": completed.returncode, "stdout": completed.stdout[-600:]}


def validate_url(url: str) -> dict[str, str | int]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"evidence URL must be absolute HTTPS: {url}")
    response = requests.get(
        url,
        timeout=20,
        allow_redirects=True,
        headers={"User-Agent": "auto-post-evidence-validator/1.0"},
        stream=True,
    )
    try:
        if response.status_code >= 400:
            raise ValueError(f"evidence URL returned HTTP {response.status_code}: {url}")
        return {
            "url": url,
            "resolved_url": response.url,
            "status": response.status_code,
        }
    finally:
        response.close()


def validate_article(article: str, check_urls: bool = True) -> dict[str, object]:
    mermaid = fenced_blocks(article, "mermaid")
    python = fenced_blocks(article, "python")
    urls = evidence_urls(article)
    if len(mermaid) != 1:
        raise ValueError(f"expected exactly one Mermaid infographic; found {len(mermaid)}")
    if len(python) < 1:
        raise ValueError("expected at least one executable Python example")
    if len(urls) < 2:
        raise ValueError("expected at least two distinct evidence URLs")
    if "caption:" not in article.lower() or "alt text:" not in article.lower():
        raise ValueError("infographic requires both caption and alt text")
    code_results = [run_python(block) for block in python]
    source_results = [validate_url(url) for url in urls] if check_urls else []
    return {
        "validated_python_blocks": len(code_results),
        "python_results": code_results,
        "evidence_urls": source_results,
        "mermaid_blocks": len(mermaid),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("article", type=Path)
    parser.add_argument("--mermaid-output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--skip-url-check", action="store_true")
    args = parser.parse_args()

    article = args.article.read_text(encoding="utf-8")
    result = validate_article(article, check_urls=not args.skip_url_check)
    args.mermaid_output.parent.mkdir(parents=True, exist_ok=True)
    args.mermaid_output.write_text(fenced_blocks(article, "mermaid")[0].strip() + "\n", encoding="utf-8")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"validated {args.article}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
