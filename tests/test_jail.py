"""Unit tests for FileJail."""
import unittest
import os
import tempfile
from agent_file_jail.jail import FileJail

class TestFileJail(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.jail = FileJail(root_dir=self.temp_dir)

    def test_safe_path(self):
        ok, path = self.jail.resolve_safe_path("app/utils.py")
        self.assertTrue(ok)
        self.assertTrue(path.startswith(os.path.abspath(self.temp_dir)))

    def test_path_traversal_blocked(self):
        ok, msg = self.jail.resolve_safe_path("../../windows/system32")
        self.assertFalse(ok)
        self.assertIn("escapes sandbox", msg)

    def test_blocked_extension(self):
        ok, msg = self.jail.resolve_safe_path("config.env")
        self.assertFalse(ok)
        self.assertIn("forbidden in sandbox", msg)

if __name__ == "__main__":
    unittest.main()
