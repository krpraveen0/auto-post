#!/usr/bin/env python3
"""Publish a validated article as an unlisted Medium review story.

Medium's legacy API is unsupported, so every network failure is terminal and
explicit. The script never falls back to public publication.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_article_package import validate_manifest


API_ROOT = "https://api.medium.com/v1"


def request_json(url: str, token: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method="POST" if payload is not None else "GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Charset": "utf-8",
            "User-Agent": "auto-post-medium-review/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Medium API returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Medium API could not be reached: {exc.reason}") from exc


def read_front_matter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([\w-]+):\s*(.*?)\s*$", line)
        if field:
            result[field.group(1)] = field.group(2).strip("'\"")
    return result


def article_body(text: str) -> str:
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)


def pin_relative_images(markdown: str, article_path: Path, repository: str, commit_sha: str) -> str:
    def replace(match: re.Match[str]) -> str:
        alt, target = match.group(1), match.group(2)
        if re.match(r"^(?:https?:|data:)", target):
            return match.group(0)
        resolved = (article_path.parent / target).resolve()
        root = Path.cwd().resolve()
        try:
            relative = resolved.relative_to(root).as_posix()
        except ValueError as exc:
            raise ValueError(f"Image escapes repository root: {target}") from exc
        url = f"https://raw.githubusercontent.com/{repository}/{commit_sha}/{relative}"
        return f"![{alt}]({url})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace, markdown)


def build_payload(manifest: dict[str, Any], markdown: str) -> dict[str, Any]:
    metadata = read_front_matter(markdown)
    tags = metadata.get("tags", "").strip("[]")
    parsed_tags = [item.strip().strip("'\"") for item in tags.split(",") if item.strip()][:3]
    return {
        "title": manifest["title"][:100],
        "contentFormat": "markdown",
        "content": article_body(markdown),
        "tags": parsed_tags,
        "publishStatus": "unlisted",
        "notifyFollowers": False,
        "license": "all-rights-reserved",
    }


def publish(manifest_path: Path, receipt_path: Path, repository: str, commit_sha: str, token: str) -> dict[str, Any]:
    root = Path.cwd().resolve()
    report = validate_manifest(manifest_path, root)
    if not report.package_integrity_valid or not report.editorial_gate_passed:
        details = "; ".join(report.critical_issues + report.release_blockers)
        raise RuntimeError(f"Article is not eligible for unlisted review publication: {details}")
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt.get("markdown_sha256") == json.loads(manifest_path.read_text())["markdown_sha256"]:
            print(f"Already published for review: {receipt['url']}")
            return receipt
        raise RuntimeError("A receipt exists for a different article hash; use a new receipt path")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    article_path = root / manifest["markdown"]
    markdown = article_path.read_text(encoding="utf-8")
    actual_hash = hashlib.sha256(article_path.read_bytes()).hexdigest()
    if actual_hash != manifest["markdown_sha256"]:
        raise RuntimeError("Canonical Markdown changed after manifest validation")

    prepared = pin_relative_images(markdown, article_path, repository, commit_sha)
    profile = request_json(f"{API_ROOT}/me", token)["data"]
    response = request_json(f"{API_ROOT}/users/{profile['id']}/posts", token, build_payload(manifest, prepared))
    post = response["data"]
    if post.get("publishStatus") != "unlisted":
        raise RuntimeError(f"Medium returned unexpected publish status: {post.get('publishStatus')}")
    receipt = {
        "receipt_schema_version": 1,
        "manifest": manifest_path.as_posix(),
        "markdown_sha256": actual_hash,
        "medium_post_id": post["id"],
        "url": post["url"],
        "publish_status": "unlisted",
        "published_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "review_status": "awaiting_post_publish_review",
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"Published unlisted Medium review story: {receipt['url']}")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--repository", default=os.getenv("GITHUB_REPOSITORY", ""))
    parser.add_argument("--commit-sha", default=os.getenv("GITHUB_SHA", ""))
    args = parser.parse_args()
    token = os.getenv("MEDIUM_INTEGRATION_TOKEN", "")
    if not token:
        print("MEDIUM_INTEGRATION_TOKEN is required", file=sys.stderr)
        return 2
    if not args.repository or not args.commit_sha:
        print("Repository and commit SHA are required to pin article images", file=sys.stderr)
        return 2
    try:
        publish(args.manifest, args.receipt, args.repository, args.commit_sha, token)
    except (KeyError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Medium review publication failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
