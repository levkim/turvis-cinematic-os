from pathlib import Path
import importlib.util
import unittest


def load_render_runner_module():
    module_path = Path(__file__).resolve().parents[1] / "apps" / "render-runner" / "render_project.py"
    spec = importlib.util.spec_from_file_location("render_project", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RenderRunnerTests(unittest.TestCase):
    def test_npm_executable_uses_cmd_shim_on_windows(self):
        runner = load_render_runner_module()

        self.assertEqual(runner.npm_executable("nt"), "npm.cmd")

    def test_npm_executable_uses_npm_on_posix(self):
        runner = load_render_runner_module()

        self.assertEqual(runner.npm_executable("posix"), "npm")


if __name__ == "__main__":
    unittest.main()
