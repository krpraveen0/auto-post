import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import publish_medium_review as pmr


class MediumPublisherTests(unittest.TestCase):
    def test_payload_is_always_unlisted_and_silent(self):
        markdown = "---\ntags: ai, python, systems, ignored\n---\n# Title\n\nBody"
        payload = pmr.build_payload({"title": "Title"}, markdown)
        self.assertEqual(payload["publishStatus"], "unlisted")
        self.assertFalse(payload["notifyFollowers"])
        self.assertEqual(payload["tags"], ["ai", "python", "systems"])

    def test_relative_images_are_pinned_to_commit(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            article = Path(tmp) / "content" / "article.md"
            article.parent.mkdir()
            image = Path(tmp) / "visual.svg"
            image.write_text("svg", encoding="utf-8")
            rewritten = pmr.pin_relative_images(
                "![Useful diagram](../visual.svg)", article, "owner/repo", "abc123"
            )
        self.assertIn("raw.githubusercontent.com/owner/repo/abc123/", rewritten)
        self.assertIn("visual.svg", rewritten)

    def test_existing_matching_receipt_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            article = root / "article.md"
            article.write_text("body", encoding="utf-8")
            digest = hashlib.sha256(article.read_bytes()).hexdigest()
            manifest = root / "article.json"
            manifest.write_text(json.dumps({"markdown_sha256": digest}), encoding="utf-8")
            receipt = root / "receipt.json"
            receipt.write_text(json.dumps({"markdown_sha256": digest, "url": "https://medium.example/review"}), encoding="utf-8")
            with patch.object(pmr, "validate_manifest") as validate:
                validate.return_value.package_integrity_valid = True
                validate.return_value.editorial_gate_passed = True
                validate.return_value.critical_issues = []
                validate.return_value.release_blockers = []
                result = pmr.publish(manifest, receipt, "owner/repo", "abc", "token")
        self.assertEqual(result["url"], "https://medium.example/review")
