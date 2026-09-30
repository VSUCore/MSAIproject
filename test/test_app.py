"""Tests for the repository checker command-line app."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repository = Path(self.temporary_directory.name)
        (self.repository / "README.md").write_text("Sample project\n", encoding="utf-8")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def run_app(self, repository):
        return subprocess.run(
            [sys.executable, str(APP_PATH), str(repository)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_passes_when_all_required_items_exist(self):
        (self.repository / "test").mkdir()
        (self.repository / "requirements.txt").write_text("", encoding="utf-8")

        result = self.run_app(self.repository)

        self.assertEqual(result.returncode, 0)
        self.assertIn("All required items are present.", result.stdout)

    def test_fails_and_names_missing_items(self):
        result = self.run_app(self.repository)

        self.assertEqual(result.returncode, 1)
        self.assertIn("[MISSING] test folder", result.stdout)
        self.assertIn("[MISSING] requirements.txt", result.stdout)

    def test_fails_when_repository_folder_does_not_exist(self):
        missing_folder = self.repository / "not-a-repository"

        result = self.run_app(missing_folder)

        self.assertEqual(result.returncode, 1)
        self.assertIn("Folder not found:", result.stdout)


if __name__ == "__main__":
    unittest.main()