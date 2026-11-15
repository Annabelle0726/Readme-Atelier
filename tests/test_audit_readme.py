"""Observable CLI tests; no third-party dependencies or network access."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/readme-atelier/scripts/audit_readme.py"


class AuditReadmeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.readme = self.root / "README.md"

    def put(self, name, content=b"sample"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode() if isinstance(content, str) else content)
        return path

    def run_audit(self, text, *extra, readme=None):
        path = readme or self.readme
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(path), "--repo-root", str(self.root), *extra],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def codes(self, report, category="errors"):
        return {issue["code"] for issue in report[category]}

    def test_existing_local_links_and_images_pass_without_mutation(self):
        asset = self.put("assets/result.png", b"real fixture")
        original = "# Example\n\n![Result](assets/result.png)\n[Guide](guide.md)\n"
        self.put("guide.md", "# Guide")
        before = asset.read_bytes()
        code, report = self.run_audit(original)
        self.assertEqual(code, 0)
        self.assertEqual(report["errors"], [])
        self.assertEqual(self.readme.read_text(encoding="utf-8"), original)
        self.assertEqual(asset.read_bytes(), before)

    def test_missing_local_image_fails_with_line_number(self):
        code, report = self.run_audit("# Title\n\n![Demo](missing.png)")
        self.assertEqual(code, 1)
        issue = report["errors"][0]
        self.assertEqual(issue["code"], "missing_local_target")
        self.assertEqual(issue["line"], 3)

    def test_case_mismatch_is_an_error_even_on_windows(self):
        self.put("assets/Hero.svg", "<svg/>")
        code, report = self.run_audit("![Hero](assets/hero.svg)")
        self.assertEqual(code, 1)
        self.assertIn("case_mismatch", self.codes(report))

    def test_nested_readme_resolves_relative_and_repository_root_paths(self):
        self.put("assets/hero.svg", "<svg/>")
        code, report = self.run_audit(
            "![Hero](../assets/hero.svg)\n[Root](/assets/hero.svg)",
            readme=self.root / "docs/README.md",
        )
        self.assertEqual(code, 0, report)

    def test_percent_encoded_filename_query_and_fragment_resolve(self):
        self.put("assets/my hero.png")
        code, report = self.run_audit("![Demo](assets/my%20hero.png?raw=true#view)")
        self.assertEqual(code, 0, report)

    def test_parentheses_and_angle_delimited_paths_resolve(self):
        self.put("assets/scene(v2).png")
        self.put("assets/my hero.png")
        code, report = self.run_audit(
            '![Scene](assets/scene(v2).png "caption")\n![Hero](<assets/my hero.png>)'
        )
        self.assertEqual(code, 0, report)
        self.assertEqual(len(report["assets"]), 2)

    def test_fenced_and_inline_code_are_not_links(self):
        code, report = self.run_audit(
            '```md\n![fake](missing.png)\n```\n'
            '~~~text\n[Example](absent.md)\n~~~\n'
            '`![inline](gone.png)`\n<!-- ![comment](missing.png) -->'
        )
        self.assertEqual(code, 0, report)
        self.assertEqual(report["assets"], [])

    def test_reference_and_shortcut_images_resolve(self):
        self.put("assets/hero.png")
        code, report = self.run_audit(
            "![Example][hero]\n![hero][]\n![hero]\n[hero]: assets/hero.png\n"
        )
        self.assertEqual(code, 0, report)
        self.assertEqual(len(report["assets"]), 1)

    def test_missing_reference_definition_is_reported(self):
        code, report = self.run_audit("![Example][missing-ref]")
        self.assertEqual(code, 1)
        self.assertIn("undefined_reference", self.codes(report))

    def test_html_images_picture_sources_and_links_are_checked(self):
        self.put("assets/hero.png")
        self.put("assets/hero@2x.png")
        self.put("guide.md")
        code, report = self.run_audit(
            '<picture><source srcset="assets/hero.png 1x, assets/hero@2x.png 2x">'
            '<img src="assets/hero.png" alt="Real output"></picture>'
            '<a href="guide.md">Guide</a>'
        )
        self.assertEqual(code, 0, report)
        self.assertEqual(len(report["assets"]), 2)

    def test_empty_markdown_and_html_alt_text_warn(self):
        self.put("hero.png")
        code, report = self.run_audit('![](hero.png)\n<img src="hero.png">')
        self.assertEqual(code, 0)
        self.assertIn("empty_alt", self.codes(report, "warnings"))

    def test_asset_budget_warns_and_strict_fails(self):
        self.put("large.gif", b"x" * 2048)
        code, report = self.run_audit("![Demo](large.gif)", "--max-asset-mb", "0.001")
        self.assertEqual(code, 0)
        self.assertIn("large_asset", self.codes(report, "warnings"))
        code, _ = self.run_audit(
            "![Demo](large.gif)", "--max-asset-mb", "0.001", "--strict"
        )
        self.assertEqual(code, 1)

    def test_external_links_and_anchors_are_not_fetched(self):
        code, report = self.run_audit(
            "[Remote](https://invalid.invalid/never-fetch)\n"
            "![Remote](https://invalid.invalid/a.png)\n[Jump](#intro)\n"
            "[Mail](mailto:sample@example.invalid)"
        )
        self.assertEqual(code, 0, report)
        self.assertIn("https://invalid.invalid/never-fetch", report["external_links"])
        self.assertIn("external_link_availability", report["unchecked"])

    def test_path_outside_repository_is_rejected(self):
        code, report = self.run_audit("[Outside](../outside.md)")
        self.assertEqual(code, 1)
        self.assertIn("path_outside_repository", self.codes(report))

    def test_absolute_device_path_is_reported_as_nonportable(self):
        code, report = self.run_audit("[Local](file:///C:/private/example.md)")
        self.assertEqual(code, 1)
        self.assertIn("nonportable_target", self.codes(report))

    def test_missing_readme_returns_json_error(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.root / "absent.md")],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("readme_unreadable", self.codes(json.loads(result.stdout)))

    def test_negative_asset_budget_is_invalid(self):
        self.readme.write_text("# Title", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.readme), "--max-asset-mb", "-1"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("positive", result.stderr)

    def test_html_entity_encoded_path_resolves(self):
        self.put("a&b.png")
        code, report = self.run_audit('<img src="a&amp;b.png" alt="Example">')
        self.assertEqual(code, 0, report)


if __name__ == "__main__":
    unittest.main()
