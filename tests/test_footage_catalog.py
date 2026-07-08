from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest


def load_catalog_module():
    module_path = Path(__file__).resolve().parents[1] / "apps" / "footage-analyzer" / "build_catalog.py"
    spec = importlib.util.spec_from_file_location("build_catalog", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FootageCatalogTests(unittest.TestCase):
    def test_build_catalog_creates_markdown_and_html_review_files(self):
        catalog = load_catalog_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            memory = root / "memory"
            memory.mkdir()
            index = {
                "project": {"title": "Test Project"},
                "footage_root": str(root / "raw"),
                "clips": [
                    {
                        "clip_id": "TP-0001",
                        "filename": "dragon-crest.mp4",
                        "extension": ".mp4",
                        "size_bytes": 1234,
                        "duration_seconds": 42.5,
                        "width": 1920,
                        "height": 1080,
                        "fps": 30.0,
                        "codec": "h264",
                    }
                ],
            }

            catalog.write_catalog_outputs(index, memory)

            markdown = (memory / "footage-catalog.md").read_text(encoding="utf-8")
            html = (memory / "footage-catalog.html").read_text(encoding="utf-8")
            self.assertIn("# Footage Catalog - Test Project", markdown)
            self.assertIn("TP-0001", markdown)
            self.assertIn("dragon-crest.mp4", markdown)
            self.assertIn("42.50s", markdown)
            self.assertIn("<video", html)
            self.assertIn("dragon-crest.mp4", html)
            self.assertIn("review-note", html)


if __name__ == "__main__":
    unittest.main()