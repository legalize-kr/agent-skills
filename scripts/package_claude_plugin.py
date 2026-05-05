#!/usr/bin/env python3
"""Package the root Legalize-KR Claude plugin as a ZIP for Cowork upload."""

from __future__ import annotations

import argparse
import os
import zipfile
from pathlib import Path


DEFAULT_INCLUDES = (
    ".claude-plugin/plugin.json",
    ".mcp.json",
    "skills",
    "README.md",
)


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(
        parts & {
            ".git",
            "__pycache__",
            "dist",
        }
    ) or path.name.endswith(".pyc")


def add_path(zip_file: zipfile.ZipFile, root: Path, path: Path) -> None:
    if path.is_file():
        zip_file.write(path, path.relative_to(root).as_posix())
        return

    for child in sorted(path.rglob("*")):
        if child.is_file() and not should_skip(child.relative_to(root)):
            zip_file.write(child, child.relative_to(root).as_posix())


def package(root: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for include in DEFAULT_INCLUDES:
            path = root / include
            if not path.exists():
                raise FileNotFoundError(path)
            add_path(zip_file, root, path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="dist/legalize-kr-plugin.zip",
        help="Output ZIP path relative to the repository root.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output

    package(root, output)
    print(os.fspath(output))


if __name__ == "__main__":
    main()
