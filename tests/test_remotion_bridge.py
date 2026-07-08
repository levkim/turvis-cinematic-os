from pathlib import Path
import importlib.util
import tempfile
import unittest


def load_bridge_module():
    module_path = Path(__file__).resolve().parents[1] / "apps" / "remotion-bridge" / "build_remotion_timeline.py"
    spec = importlib.util.spec_from_file_location("build_remotion_timeline", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RemotionBridgeTests(unittest.TestCase):
    def test_build_remotion_timeline_derives_width_and_height_from_resolution(self):
        bridge = load_bridge_module()
        config = {
            "output": {
                "aspect_ratio": "16:9",
                "resolution": "3840x2160",
                "language": "ko",
            },
            "rules": {
                "generate_audio": False,
                "generate_music": False,
                "generate_sound_effects": False,
            },
        }
        draft = {
            "project": {"id": "test-video", "title": "test video"},
            "output": {"fps": 30},
            "clips": [
                {
                    "id": "beat-01",
                    "start_seconds": 0,
                    "duration_seconds": 5,
                    "beat": "Opening",
                    "footage": "TBD",
                    "subtitle": "Opening line",
                }
            ],
        }

        timeline = bridge.build_remotion_timeline(config, draft)

        self.assertEqual(timeline["composition"]["width"], 3840)
        self.assertEqual(timeline["composition"]["height"], 2160)

    def test_build_remotion_timeline_uses_footage_index_video_sources(self):
        bridge = load_bridge_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            footage = root / "raw"
            memory = root / "memory"
            footage.mkdir()
            memory.mkdir()
            video = footage / "opening.mp4"
            video.write_bytes(b"fake")
            (memory / "footage-index.json").write_text(
                '{"footage_root":"' + str(footage).replace('\\', '\\\\') + '","clips":[{"clip_id":"TP-0001","filename":"opening.mp4","asset_path":"opening.mp4"}]}',
                encoding="utf-8",
            )
            (memory / "shot-list.md").write_text(
                """# Shot List

| Beat | Narration | Candidate Clip | Filename | Duration | Resolution |
|---:|---|---|---|---:|---|
| 1 | Opening line | TP-0001 | opening.mp4 | 1.00s | 1920x1080 |
""",
                encoding="utf-8",
            )
            config = {
                "paths": {"memory": str(memory)},
                "output": {"resolution": "1920x1080"},
                "rules": {},
            }
            draft = {
                "project": {"id": "test-video", "title": "test video"},
                "output": {"fps": 30},
                "clips": [{"id": "beat-01", "start_seconds": 0, "duration_seconds": 5, "beat": "Opening", "footage": "TBD", "subtitle": "Opening line"}],
            }

            timeline = bridge.build_remotion_timeline(config, draft)

            self.assertEqual(timeline["clips"][0]["type"], "video")
            self.assertTrue(timeline["clips"][0]["src"].startswith("http://127.0.0.1:37678/"))
            self.assertIn("opening.mp4", timeline["clips"][0]["src"])
    def test_remotion_root_registers_root_component_for_cli_entrypoint(self):
        root_path = Path(__file__).resolve().parents[1] / "remotion" / "src" / "Root.tsx"
        source = root_path.read_text(encoding="utf-8")

        self.assertIn("registerRoot", source)
        self.assertIn("registerRoot(RemotionRoot)", source)

    def test_documentary_composition_uses_clip_type_before_rendering_video(self):
        composition_path = Path(__file__).resolve().parents[1] / "remotion" / "src" / "compositions" / "DocumentaryComposition.tsx"
        source = composition_path.read_text(encoding="utf-8")

        self.assertIn("clip.type", source)
        self.assertIn("clip.type === 'video'", source)


if __name__ == "__main__":
    unittest.main()
