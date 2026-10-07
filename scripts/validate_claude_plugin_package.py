#!/usr/bin/env python3
"""Validate the Claude Cowork plugin ZIP shape."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import PurePosixPath

CLI_PIN = "legalize-cli[mcp]==0.5.0"
PLUGIN_VERSION = "0.2.0"


REQUIRED_FILES = {
    ".claude-plugin/plugin.json",
    ".mcp.json",
    "skills/legalize-kr/SKILL.md",
    "README.md",
    "skills/legalize-kr/references/access-options.md",
    "skills/legalize-kr/references/data-layout.md",
}


def validate(path: str, expected_version: str = PLUGIN_VERSION) -> None:
    with zipfile.ZipFile(path) as zip_file:
        names = set(zip_file.namelist())

        missing = REQUIRED_FILES - names
        if missing:
            raise SystemExit(f"missing required files: {', '.join(sorted(missing))}")

        disallowed = [
            name
            for name in names
            if ".git" in PurePosixPath(name).parts
            or "__pycache__" in PurePosixPath(name).parts
            or name.startswith("dist/")
            or name.endswith(".pyc")
        ]
        if disallowed:
            raise SystemExit(f"disallowed files in package: {', '.join(sorted(disallowed))}")

        plugin_json = json.loads(zip_file.read(".claude-plugin/plugin.json"))
        if plugin_json.get("name") != "legalize-kr":
            raise SystemExit("plugin name must be legalize-kr")
        if plugin_json.get("version") != expected_version:
            raise SystemExit("plugin version does not match the prepared release")
        if plugin_json.get("mcpServers") != "./.mcp.json":
            raise SystemExit("plugin.json must reference ./.mcp.json")

        mcp_json = json.loads(zip_file.read(".mcp.json"))
        server = mcp_json.get("mcpServers", {}).get("legalize-kr")
        if not server:
            raise SystemExit(".mcp.json must include legalize-kr MCP server")
        if server.get("args") != ["--from", CLI_PIN, "legalize-mcp"]:
            raise SystemExit("MCP executable does not pin the tested CLI version")

        skill = zip_file.read("skills/legalize-kr/SKILL.md").decode("utf-8")
        if "name: legalize-kr" not in skill:
            raise SystemExit("SKILL.md must declare name: legalize-kr")
        for contract in ("laws_diff", 'schema_version: "2.0"', "PARTIAL_SEARCH", "AMBIGUOUS_MATCH", CLI_PIN):
            if contract not in skill:
                raise SystemExit(f"SKILL.md missing MCP contract marker: {contract}")
        readme = zip_file.read("README.md").decode("utf-8")
        if CLI_PIN not in readme or "laws_diff" not in readme:
            raise SystemExit("README.md does not describe the pinned MCP contract")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path")
    parser.add_argument("--expected-version", default=PLUGIN_VERSION)
    args = parser.parse_args()
    validate(args.zip_path, args.expected_version)
    print(f"valid: {args.zip_path}")


if __name__ == "__main__":
    main()
