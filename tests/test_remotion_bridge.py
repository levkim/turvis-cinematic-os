from pathlib import Path
import importlib.util
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
