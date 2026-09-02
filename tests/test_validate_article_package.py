import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_article_package as vap


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ValidateArticlePackageTests(unittest.TestCase):
    def make_package(self, root: Path, approved: bool = False):
        for name in ("lesson.md", "platform.json", "example.py", "figure.drawio", "figure.svg", "benchmark.md", "claims.md"):
            (root / name).write_text(f"content for {name}\n", encoding="utf-8")
        (root / "structural.json").write_text('{"structurally_valid": true}\n', encoding="utf-8")
        review = {
            "review_schema_version": 2,
            "reviewer": "Technical editor",
            "reviewed_at_utc": "2026-09-03T12:00:00Z",
            "reader_value_score": 90,
            "critical_issues": [],
            "decision": "ready_for_human_review",
            "categories": [
                {"name": f"Category {index}", "score": score, "maximum": maximum, "evidence": "Concrete evidence from an inspected artifact."}
                for index, (score, maximum) in enumerate(
                    [(11, 12), (16, 18), (14, 16), (14, 16), (11, 12), (9, 10), (7, 8), (8, 8)],
                    start=1,
                )
            ],
        }
        (root / "editorial.json").write_text(json.dumps(review), encoding="utf-8")
        data = {
            "publishing_schema_version": 3,
            "series": "series",
            "part": 1,
            "title": "Title",
            "markdown": "lesson.md",
            "markdown_sha256": digest(root / "lesson.md"),
            "canonical_strategy": "set-on-first-publication",
            "platform_adapter": "platform.json",
            "platform_adapter_sha256": digest(root / "platform.json"),
            "target_platforms": ["medium", "notion"],
            "tested_environment": {"python": "3.12.13", "verified_at": "2026-09-03"},
            "examples": [{
                "path": "example.py",
                "sha256": digest(root / "example.py"),
                "verification_command": "python example.py",
            }],
            "research": {
                "benchmark": "benchmark.md",
                "benchmark_sha256": digest(root / "benchmark.md"),
                "claim_register": "claims.md",
                "claim_register_sha256": digest(root / "claims.md"),
            },
            "visuals": {
                "drawio": "figure.drawio", "drawio_sha256": digest(root / "figure.drawio"),
                "svg": "figure.svg", "svg_sha256": digest(root / "figure.svg"),
            },
            "quality": {
                "structural_report": "structural.json",
                "structural_report_sha256": digest(root / "structural.json"),
                "editorial_report": "editorial.json",
                "editorial_report_sha256": digest(root / "editorial.json"),
            },
            "notion": {"sync_status": "pending", "page_id": None, "url": None, "content_sha256": None},
            "human_approval": {
                "approved": approved,
                "reviewer": "Human" if approved else None,
                "approved_at_utc": "2026-09-03T12:00:00Z" if approved else None,
            },
            "validation_time_utc": "2026-09-03T12:00:00Z",
        }
        manifest = root / "lesson.json"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        return manifest

    def test_complete_unapproved_package_passes_integrity_but_not_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = vap.validate_manifest(self.make_package(root), root)
        self.assertTrue(report.package_integrity_valid)
        self.assertTrue(report.editorial_gate_passed)
        self.assertFalse(report.release_ready)
        self.assertIn("human publication approval is pending", report.release_blockers)

    def test_stale_hash_fails_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_package(root)
            (root / "lesson.md").write_text("changed\n", encoding="utf-8")
            report = vap.validate_manifest(manifest, root)
        self.assertFalse(report.package_integrity_valid)
        self.assertTrue(any("hash is stale" in issue for issue in report.critical_issues))

    def test_stale_research_hash_fails_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_package(root)
            (root / "claims.md").write_text("changed claim\n", encoding="utf-8")
            report = vap.validate_manifest(manifest, root)
        self.assertFalse(report.package_integrity_valid)
        self.assertTrue(any("research claim_register hash is stale" in issue for issue in report.critical_issues))

    def test_verified_notion_requires_identity_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_package(root)
            data = json.loads(manifest.read_text())
            data["notion"]["sync_status"] = "verified"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            report = vap.validate_manifest(manifest, root)
        self.assertFalse(report.package_integrity_valid)
        self.assertTrue(any("verified Notion sync" in issue for issue in report.critical_issues))


if __name__ == "__main__":
    unittest.main()
