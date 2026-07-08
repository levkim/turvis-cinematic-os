from pathlib import Path
import importlib.util
import unittest


def load_timeline_module():
    module_path = Path(__file__).resolve().parents[1] / "apps" / "timeline-builder" / "build_timeline.py"
    spec = importlib.util.spec_from_file_location("build_timeline", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TimelineBuilderTests(unittest.TestCase):
    def test_allocate_durations_respects_short_target_duration(self):
        timeline = load_timeline_module()
        beats = [
            {"emotion": "neutral-cinematic", "rhythm": "measured", "silence_need": "low"},
            {"emotion": "neutral-cinematic", "rhythm": "measured", "silence_need": "low"},
        ]

        durations = timeline.allocate_durations(6, beats)

        self.assertEqual(sum(durations), 6)
        self.assertEqual(len(durations), 2)
        self.assertTrue(all(duration > 0 for duration in durations))


if __name__ == "__main__":
    unittest.main()
