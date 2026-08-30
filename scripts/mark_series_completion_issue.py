#!/usr/bin/env python3
"""Mark the course-series state after the next-series issue is created."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-file", required=True, type=Path)
    args = parser.parse_args()
    state = json.loads(args.state_file.read_text(encoding="utf-8")) if args.state_file.exists() else {}
    state["completion_issue_created"] = True
    args.state_file.parent.mkdir(parents=True, exist_ok=True)
    args.state_file.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
