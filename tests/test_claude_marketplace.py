import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


class ClaudeMarketplaceTest(unittest.TestCase):
    def setUp(self) -> None:
        marketplace = load_json(".claude-plugin/marketplace.json")
        self.marketplace_plugin = next(
            plugin
            for plugin in marketplace["plugins"]
            if plugin["name"] == "legalize-kr"
        )
        self.plugin_manifest = load_json(".claude-plugin/plugin.json")

    def test_marketplace_delegates_components_to_plugin_manifest(self) -> None:
        self.assertEqual(self.marketplace_plugin["source"], "./")
        for component in ("skills", "mcpServers"):
            with self.subTest(component=component):
                self.assertNotIn(component, self.marketplace_plugin)

    def test_plugin_manifest_keeps_component_declarations(self) -> None:
        self.assertEqual(self.plugin_manifest["skills"], "./skills/")
        self.assertEqual(self.plugin_manifest["mcpServers"], "./.mcp.json")


if __name__ == "__main__":
    unittest.main()
