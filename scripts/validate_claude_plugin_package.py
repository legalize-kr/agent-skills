#!/usr/bin/env python3
"""Validate the Claude Cowork plugin ZIP shape."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import PurePosixPath


REQUIRED_FILES = {
    ".claude-plugin/plugin.json",
    ".mcp.json",
    "skills/legalize-kr/SKILL.md",
    "README.md",
}


def validate(path: str) -> None:
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
        if plugin_json.get("mcpServers") != "./.mcp.json":
            raise SystemExit("plugin.json must reference ./.mcp.json")

        mcp_json = json.loads(zip_file.read(".mcp.json"))
        server = mcp_json.get("mcpServers", {}).get("legalize-kr")
        if not server:
            raise SystemExit(".mcp.json must include legalize-kr MCP server")

        skill = zip_file.read("skills/legalize-kr/SKILL.md").decode("utf-8")
        if "name: legalize-kr" not in skill:
            raise SystemExit("SKILL.md must declare name: legalize-kr")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path")
    args = parser.parse_args()
    validate(args.zip_path)
    print(f"valid: {args.zip_path}")


if __name__ == "__main__":
    main()
