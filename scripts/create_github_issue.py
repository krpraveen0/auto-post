#!/usr/bin/env python3
"""Create a GitHub issue from a workflow run."""

from __future__ import annotations

import argparse
import os
import sys

import requests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        print("GITHUB_TOKEN or GITHUB_REPOSITORY is missing; skipping issue creation.")
        return 0

    response = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={"title": args.title, "body": args.body},
        timeout=60,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"GitHub issue creation failed {response.status_code}: {response.text[:1000]}")
    print(response.json().get("html_url", "Issue created."))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
