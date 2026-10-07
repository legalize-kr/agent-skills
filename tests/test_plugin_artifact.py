import tempfile
import unittest
from pathlib import Path

from scripts.package_claude_plugin import package
from scripts.validate_claude_plugin_package import validate

ROOT = Path(__file__).resolve().parents[1]


class PluginArtifactTest(unittest.TestCase):
    def test_packaged_zip_has_pinned_contract(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "plugin.zip"
            package(ROOT, output)
            validate(str(output))
