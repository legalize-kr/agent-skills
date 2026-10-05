import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/legalize-kr/scripts/select_access_mode.py"
SPEC = importlib.util.spec_from_file_location("select_access_mode", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AccessModeTest(unittest.TestCase):
    @patch.object(MODULE, "detect_tools", return_value={})
    def test_connected_tools_work_without_local_commands(self, _detect) -> None:
        for task in ("single", "article", "search", "compare", "list", "agent"):
            for scope in ("laws", "precedents", "admrules", "ordinances", "all"):
                with self.subTest(task=task, scope=scope):
                    result = MODULE.recommend(task, scope, mcp_connected=True)
                    self.assertEqual(result.primary, "mcp")
                    self.assertEqual(result.example_commands, [])

    @patch.object(MODULE, "detect_tools", return_value={})
    def test_connected_tools_do_not_replace_bulk_or_offline_access(self, _detect) -> None:
        for task in ("bulk", "history", "offline"):
            with self.subTest(task=task):
                result = MODULE.recommend(task, "ordinances", mcp_connected=True)
                self.assertEqual(result.primary, "git-clone")
                self.assertIn("ordinance-kr.git", result.example_commands[0])

    @patch.object(MODULE, "detect_tools", return_value={})
    def test_default_preserves_shell_access(self, _detect) -> None:
        self.assertEqual(MODULE.recommend("article", "laws").primary, "legalize-cli")
        self.assertEqual(MODULE.recommend("agent", "laws").primary, "mcp")
