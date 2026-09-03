#!/usr/bin/env python3
"""Concurrency-safe eligibility and advancement checks for a course series."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from validate_article_package import validate_manifest


class StateBlocked(RuntimeError):
    pass


def load_state(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("course state must be a JSON object")
    return value


def assert_generation_eligible(state: dict[str, Any]) -> int:
    if state.get("generation_enabled") is not True:
        raise StateBlocked(f"generation is disabled: {state.get('workflow_status', 'no reason recorded')}")
    unresolved = state.get("unresolved_revisions", [])
    pending = state.get("pending_human_review", [])
    if unresolved:
        raise StateBlocked(f"lessons require revision: {unresolved}")
    if pending:
        raise StateBlocked(f"lessons await human review: {pending}")
    next_part = state.get("next_part")
    if not isinstance(next_part, int) or next_part < 1:
        raise ValueError("next_part must be a positive integer")
    return next_part


def write_atomic(path: Path, value: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def advance(
    state_path: Path,
    manifest_path: Path,
    repository_root: Path,
    expected_next_part: int,
) -> dict[str, Any]:
    state = load_state(state_path)
    current = assert_generation_eligible(state)
    if current != expected_next_part:
        raise StateBlocked(f"compare-and-swap failed: expected {expected_next_part}, found {current}")
    package = validate_manifest(manifest_path, repository_root)
    if not package.release_ready:
        reasons = package.critical_issues + package.release_blockers
        raise StateBlocked("article package is not release ready: " + "; ".join(reasons))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("part") != current:
        raise StateBlocked(f"manifest part {manifest.get('part')} does not match next_part {current}")
    state["next_part"] = current + 1
    state.setdefault("generated", []).append({
        "part": current,
        "title": manifest["title"],
        "markdown": manifest["markdown"],
        "manifest": str(manifest_path),
        "publishable": True,
        "reader_value_score": manifest["quality"]["reader_value_score"],
        "approved_at_utc": manifest["human_approval"]["approved_at_utc"],
    })
    write_atomic(state_path, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check")
    check.add_argument("state", type=Path)
    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("state", type=Path)
    advance_parser.add_argument("manifest", type=Path)
    advance_parser.add_argument("--expected-next-part", type=int, required=True)
    advance_parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        if args.command == "check":
            print(assert_generation_eligible(load_state(args.state)))
        else:
            updated = advance(
                args.state,
                args.manifest,
                args.repository_root.resolve(),
                args.expected_next_part,
            )
            print(updated["next_part"])
    except StateBlocked as exc:
        print(f"blocked: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
