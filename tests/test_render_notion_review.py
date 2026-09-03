import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import render_notion_review as notion


class RenderNotionReviewTests(unittest.TestCase):
    def make_article(self, root: Path) -> Path:
        article = root / "generated" / "article.md"
        article.parent.mkdir(parents=True)
        visual = root / "visual.svg"
        visual.write_text("<svg/>", encoding="utf-8")
        visual.with_suffix(".mermaid").write_text(
            'flowchart TD\n    A["Input"] --> B["Output"]\n', encoding="utf-8"
        )
        article.write_text(
            "---\ntitle: Example\n---\n# Example\n\n## Mental Model\n\n"
            "\\[x = y + 1\\]\n\nInline \\(x\\).\n\n"
            "![Useful flow](../visual.svg)\n\n```python\nprint(1)\n```\n",
            encoding="utf-8",
        )
        return article

    def test_render_converts_math_and_svg_to_native_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            rendered, report = notion.render(self.make_article(Path(tmp)), "Example")
        self.assertNotIn("# Example\n", rendered)
        self.assertIn("$$\nx = y + 1\n$$", rendered)
        self.assertIn("$`x`$", rendered)
        self.assertIn("```mermaid", rendered)
        self.assertNotIn(".svg)", rendered)
        self.assertEqual((report.display_equations, report.inline_equations, report.diagrams), (1, 1, 1))

    def test_svg_without_fallback_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            article = self.make_article(root)
            (root / "visual.mermaid").unlink()
            with self.assertRaisesRegex(notion.RenderingError, "Notion fallback"):
                notion.render(article, "Example")

    def test_readback_detects_missing_equation_and_diagram(self):
        with tempfile.TemporaryDirectory() as tmp:
            rendered, expected = notion.render(self.make_article(Path(tmp)), "Example")
            broken = rendered.replace("$$\nx = y + 1\n$$", "x = y + 1").replace("```mermaid", "```text")
            result = notion.validate_readback(broken, expected)
        self.assertFalse(result.valid)
        self.assertTrue(any("equation count" in issue for issue in result.issues))
        self.assertTrue(any("diagram count" in issue for issue in result.issues))

    def test_valid_readback_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            rendered, expected = notion.render(self.make_article(Path(tmp)), "Example")
            result = notion.validate_readback(rendered, expected)
        self.assertTrue(result.valid, result.issues)


if __name__ == "__main__":
    unittest.main()
