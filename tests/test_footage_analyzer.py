from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest


def load_analyzer_module():
    module_path = Path(__file__).resolve().parents[1] / "apps" / "footage-analyzer" / "footage_analyzer.py"
    spec = importlib.util.spec_from_file_location("footage_analyzer", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FootageAnalyzerTests(unittest.TestCase):
    def test_build_footage_index_contains_file_and_video_metadata(self):
        analyzer = load_analyzer_module()
        settings = analyzer.AnalyzerSettings(
            input_dir=Path("assets/raw"),
            output_dir=Path("knowledge/footage/test"),
            keyframes_root=Path("assets/keyframes"),
            project_id="test-project",
            project_title="Test Project",
            episode="episode-01",
            prefix="TP",
            country="unknown",
            region="unknown",
            destination="unknown",
            skip_keyframes=True,
            narration_path=None,
        )
        memory = analyzer.ClipMemory(
            clip_id="TP-0001",
            original_filename="opening.MP4",
            asset_path="opening.MP4",
            project={"series": "test-project", "title": "Test Project"},
            location={},
            camera={},
            visual_context={},
            emotion_tags=[],
            story_tags=[],
            best_usage=[],
            scores={},
            flags={},
            technical_metadata={"duration_seconds": 3.5, "width": 1920, "height": 1080, "fps": 30.0, "codec": "h264"},
            keyframes={},
            director_notes="",
        )
        file_sizes = {"TP-0001": 123456}

        index = analyzer.build_footage_index([memory], settings, file_sizes)

        self.assertEqual(index["schema"], "turvis.footage.index.v0.1")
        self.assertEqual(index["clips"][0]["filename"], "opening.MP4")
        self.assertEqual(index["clips"][0]["extension"], ".mp4")
        self.assertEqual(index["clips"][0]["size_bytes"], 123456)
        self.assertEqual(index["clips"][0]["duration_seconds"], 3.5)
        self.assertEqual(index["clips"][0]["width"], 1920)
        self.assertEqual(index["clips"][0]["height"], 1080)

    def test_build_shot_list_links_narration_lines_to_footage_candidates(self):
        analyzer = load_analyzer_module()
        index = {
            "clips": [
                {"clip_id": "TP-0001", "filename": "opening.mp4", "duration_seconds": 3.5, "width": 1920, "height": 1080},
                {"clip_id": "TP-0002", "filename": "arrival.mp4", "duration_seconds": 4.0, "width": 1920, "height": 1080},
            ]
        }
        narration_lines = ["Opening narration.", "Arrival narration."]

        shot_list = analyzer.build_shot_list("Test Project", narration_lines, index)

        self.assertIn("# Shot List — Test Project", shot_list)
        self.assertIn("Opening narration.", shot_list)
        self.assertIn("TP-0001", shot_list)
        self.assertIn("Arrival narration.", shot_list)
        self.assertIn("TP-0002", shot_list)

    def test_build_shot_list_prefers_filename_keywords_over_sequence_order(self):
        analyzer = load_analyzer_module()
        index = {
            "clips": [
                {"clip_id": "TP-0001", "filename": "가는길.MOV", "duration_seconds": 12.0, "width": 1920, "height": 1080},
                {"clip_id": "TP-0002", "filename": "보즈지라 드래곤 크레스트 회전.MP4", "duration_seconds": 90.0, "width": 1920, "height": 1080},
                {"clip_id": "TP-0003", "filename": "화성 드론 파노라마.MP4", "duration_seconds": 60.0, "width": 1920, "height": 1080},
            ]
        }

        shot_list = analyzer.build_shot_list("Test Project", ["드래곤 크레스트 능선을 따라 걷는다."], index)

        self.assertIn("TP-0002", shot_list)
        self.assertIn("보즈지라 드래곤 크레스트 회전.MP4", shot_list)
    def test_write_scan_outputs_creates_footage_index_and_shot_list_files(self):
        analyzer = load_analyzer_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            narration = root / "narration.md"
            narration.write_text("# Narration\n\nPaste narration text for the current project here.\n\n```text\nOpening narration.\n```\n", encoding="utf-8-sig")
            settings = analyzer.AnalyzerSettings(
                input_dir=root / "raw",
                output_dir=root / "memory",
                keyframes_root=root / "keyframes",
                project_id="test-project",
                project_title="Test Project",
                episode="episode-01",
                prefix="TP",
                country="unknown",
                region="unknown",
                destination="unknown",
                skip_keyframes=True,
                narration_path=narration,
            )
            memory = analyzer.ClipMemory(
                clip_id="TP-0001",
                original_filename="opening.mp4",
                asset_path="opening.mp4",
                project={"series": "test-project", "title": "Test Project"},
                location={},
                camera={},
                visual_context={},
                emotion_tags=[],
                story_tags=[],
                best_usage=[],
                scores={},
                flags={},
                technical_metadata={"duration_seconds": 3.5, "width": 1920, "height": 1080, "fps": 30.0, "codec": "h264"},
                keyframes={},
                director_notes="",
            )
            settings.output_dir.mkdir(parents=True)

            analyzer.write_scan_outputs([memory], settings, {"TP-0001": 123456})

            self.assertTrue((settings.output_dir / "footage-index.json").exists())
            self.assertTrue((settings.output_dir / "shot-list.md").exists())
            shot_list = (settings.output_dir / "shot-list.md").read_text(encoding="utf-8")
            self.assertIn("Opening narration.", shot_list)
            self.assertNotIn("# Narration", shot_list)


if __name__ == "__main__":
    unittest.main()
