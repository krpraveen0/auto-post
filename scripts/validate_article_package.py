#!/usr/bin/env python3
"""Validate a complete article package without claiming human publication approval."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "publishing_schema_version",
    "series",
    "part",
    "title",
    "markdown",
    "markdown_sha256",
    "canonical_strategy",
    "platform_adapter",
    "platform_adapter_sha256",
    "target_platforms",
    "tested_environment",
    "examples",
    "research",
    "visuals",
    "quality",
    "notion",
    "human_approval",
    "validation_time_utc",
}
SUPPORTED_PLATFORMS = {"medium", "dev", "hashnode", "owned-site", "notion"}


@dataclass(frozen=True)
class PackageReport:
    manifest: str
    package_integrity_valid: bool
    editorial_gate_passed: bool
    release_ready: bool
    critical_issues: list[str]
    release_blockers: list[str]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_path(repository_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repository_root / path


def validate_hash(
    repository_root: Path,
    path_value: Any,
    expected: Any,
    label: str,
    issues: list[str],
) -> None:
    if not isinstance(path_value, str) or not path_value:
        issues.append(f"{label} path is missing")
        return
    path = resolve_path(repository_root, path_value)
    if not path.is_file():
        issues.append(f"{label} file does not exist: {path_value}")
        return
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        issues.append(f"{label} SHA-256 is missing or malformed")
        return
    actual = sha256(path)
    if actual != expected:
        issues.append(f"{label} hash is stale: expected {expected}, got {actual}")


def load_json(path: Path, label: str, issues: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"cannot read {label}: {exc}")
        return {}
    if not isinstance(value, dict):
        issues.append(f"{label} must contain one JSON object")
        return {}
    return value


def validate_manifest(path: Path, repository_root: Path) -> PackageReport:
    issues: list[str] = []
    blockers: list[str] = []
    data = load_json(path, "manifest", issues)
    missing = sorted(REQUIRED_TOP_LEVEL - data.keys())
    if missing:
        issues.append("manifest is missing fields: " + ", ".join(missing))
    if data.get("publishing_schema_version") != 3:
        issues.append("publishing_schema_version must be 3")

    validate_hash(
        repository_root,
        data.get("markdown"),
        data.get("markdown_sha256"),
        "canonical Markdown",
        issues,
    )
    validate_hash(
        repository_root,
        data.get("platform_adapter"),
        data.get("platform_adapter_sha256"),
        "platform adapter",
        issues,
    )

    platforms = data.get("target_platforms")
    if not isinstance(platforms, list) or not platforms:
        issues.append("target_platforms must be a non-empty list")
    elif unknown := sorted(set(platforms) - SUPPORTED_PLATFORMS):
        issues.append("unsupported target platforms: " + ", ".join(unknown))

    environment = data.get("tested_environment")
    if not isinstance(environment, dict) or not environment.get("python") or not environment.get("verified_at"):
        issues.append("tested_environment must record Python and verified_at")

    examples = data.get("examples")
    if not isinstance(examples, list) or not examples:
        issues.append("examples must contain at least one verified artifact")
    else:
        for index, item in enumerate(examples):
            if not isinstance(item, dict):
                issues.append(f"example {index} must be an object")
                continue
            validate_hash(
                repository_root,
                item.get("path"),
                item.get("sha256"),
                f"example {index}",
                issues,
            )
            if not item.get("verification_command"):
                issues.append(f"example {index} has no verification_command")

    visuals = data.get("visuals")
    if not isinstance(visuals, dict) or not visuals:
        issues.append("visuals must contain editable and exported assets")
    else:
        path_keys = [key for key in visuals if not key.endswith("_sha256")]
        for key in path_keys:
            validate_hash(
                repository_root,
                visuals.get(key),
                visuals.get(f"{key}_sha256"),
                f"visual {key}",
                issues,
            )

    research = data.get("research")
    if not isinstance(research, dict):
        issues.append("research must identify benchmark and claim register")
    else:
        for key in ("benchmark", "claim_register"):
            validate_hash(
                repository_root,
                research.get(key),
                research.get(f"{key}_sha256"),
                f"research {key}",
                issues,
            )

    quality = data.get("quality") if isinstance(data.get("quality"), dict) else {}
    structural_path = quality.get("structural_report")
    editorial_path = quality.get("editorial_report")
    editorial_gate = False
    validate_hash(
        repository_root,
        structural_path,
        quality.get("structural_report_sha256"),
        "quality structural report",
        issues,
    )
    validate_hash(
        repository_root,
        editorial_path,
        quality.get("editorial_report_sha256"),
        "quality editorial report",
        issues,
    )
    if editorial_path and resolve_path(repository_root, editorial_path).is_file():
        review = load_json(resolve_path(repository_root, editorial_path), "editorial review", issues)
        categories = review.get("categories")
        review_version = review.get("review_schema_version")
        if review_version not in {2, 3}:
            issues.append("editorial review must use review_schema_version 2 or 3")
        if not review.get("reviewer") or not review.get("reviewed_at_utc"):
            issues.append("editorial review must identify its reviewer and review time")
        if review_version == 3:
            if review.get("canonical_markdown_sha256") != data.get("markdown_sha256"):
                issues.append("editorial review must match the canonical Markdown SHA-256")
            required_roles = {
                "technical", "evidence", "pedagogy", "reproducibility",
                "originality", "accessibility", "global-English",
            }
            completed_roles = set(review.get("review_roles", []))
            if missing_roles := sorted(required_roles - completed_roles):
                issues.append("editorial review is missing adversarial roles: " + ", ".join(missing_roles))
        elif review_version == 2:
            blockers.append("legacy editorial review schema 2 must be migrated before release")
        if not isinstance(categories, list) or len(categories) < 8:
            issues.append("editorial review must contain at least eight evidence-backed categories")
        else:
            scored = sum(item.get("score", 0) for item in categories if isinstance(item, dict))
            maximum = sum(item.get("maximum", 0) for item in categories if isinstance(item, dict))
            if scored != review.get("reader_value_score") or maximum != 100:
                issues.append("editorial category totals must equal reader_value_score out of 100")
            if any(len(str(item.get("evidence", ""))) < 20 for item in categories if isinstance(item, dict)):
                issues.append("every editorial category requires concrete evidence")
        editorial_gate = (
            review_version == 3
            and review.get("canonical_markdown_sha256") == data.get("markdown_sha256")
            and isinstance(review.get("reader_value_score"), int)
            and review["reader_value_score"] >= 85
            and review.get("critical_issues") == []
            and review.get("decision") in {"ready_for_human_review", "approved"}
        )
        if review_version == 3 and not editorial_gate:
            issues.append("editorial review must score at least 85 with zero critical issues")

    notion = data.get("notion") if isinstance(data.get("notion"), dict) else {}
    if notion.get("sync_status") != "verified":
        blockers.append("Notion synchronization is not release-verified")
    for key in ("page_id", "url", "content_sha256"):
        if notion.get("sync_status") == "verified" and not notion.get(key):
            issues.append(f"verified Notion sync is missing {key}")

    approval = data.get("human_approval") if isinstance(data.get("human_approval"), dict) else {}
    if approval.get("approved") is not True:
        blockers.append("human publication approval is pending")
    elif not approval.get("reviewer") or not approval.get("approved_at_utc"):
        issues.append("approved human review must identify reviewer and approval time")
    elif approval.get("canonical_markdown_sha256") != data.get("markdown_sha256"):
        issues.append("human approval must match the canonical Markdown SHA-256")

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(data.get("validation_time_utc", ""))):
        issues.append("validation_time_utc must use YYYY-MM-DDTHH:MM:SSZ")

    integrity = not issues
    release_ready = integrity and editorial_gate and not blockers
    return PackageReport(
        manifest=str(path),
        package_integrity_valid=integrity,
        editorial_gate_passed=editorial_gate,
        release_ready=release_ready,
        critical_issues=issues,
        release_blockers=blockers,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifests", nargs="+", type=Path)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--require-release-ready", action="store_true")
    args = parser.parse_args()

    reports = [validate_manifest(path, args.repository_root.resolve()) for path in args.manifests]
    for report in reports:
        state = "RELEASE READY" if report.release_ready else (
            "PACKAGE PASS" if report.package_integrity_valid else "PACKAGE FAIL"
        )
        print(f"{report.manifest}: {state}")
        for issue in report.critical_issues:
            print(f"  critical: {issue}")
        for blocker in report.release_blockers:
            print(f"  release blocker: {blocker}")

    if args.require_release_ready:
        return 0 if all(report.release_ready for report in reports) else 1
    return 0 if all(report.package_integrity_valid for report in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
