#!/usr/bin/env python3
"""Recommend an access method for Legalize-KR data."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import asdict, dataclass


@dataclass
class Recommendation:
    primary: str
    fallbacks: list[str]
    reasons: list[str]
    example_commands: list[str]
    token_present: bool
    detected_tools: dict[str, bool]


def detect_tools() -> dict[str, bool]:
    return {
        "legalize": shutil.which("legalize") is not None,
        "legalize-mcp": shutil.which("legalize-mcp") is not None,
        "uvx": shutil.which("uvx") is not None,
        "pipx": shutil.which("pipx") is not None,
        "git": shutil.which("git") is not None,
        "rg": shutil.which("rg") is not None,
    }


def recommend(task: str, scope: str) -> Recommendation:
    token_present = bool(os.environ.get("GITHUB_TOKEN") or os.environ.get("LEGALIZE_GITHUB_TOKEN"))
    tools = detect_tools()

    if task == "agent":
        return Recommendation(
            primary="mcp",
            fallbacks=["legalize-cli", "direct-github"],
            reasons=[
                "Local stdio MCP exposes Legalize-KR as structured tools for agent workflows.",
                "Use legalize-cli or direct GitHub access if the current client cannot run local MCP commands.",
            ],
            example_commands=[
                "uvx --from legalize-cli[mcp] legalize-mcp",
                "pipx install 'legalize-cli[mcp]'",
                "legalize-mcp",
            ],
            token_present=token_present,
            detected_tools=tools,
        )

    if task in {"history", "bulk", "offline"}:
        repo = {
            "laws": "legalize-kr",
            "precedents": "precedent-kr",
            "admrules": "admrule-kr",
            "ordinances": "ordinance-kr",
        }.get(scope, "legalize-kr")
        return Recommendation(
            primary="git-clone",
            fallbacks=["legalize-cli", "direct-github"],
            reasons=[
                "Git clone is best for bulk search, offline work, and native git history/diff.",
                "Clone only the dataset repository needed for the task.",
            ],
            example_commands=[
                f"git clone https://github.com/legalize-kr/{repo}.git",
                f"rg '검색어' {repo}",
            ],
            token_present=token_present,
            detected_tools=tools,
        )

    if task in {"single", "article", "search", "compare", "list"}:
        commands = {
            "laws": "legalize laws get 민법 --json",
            "precedents": "legalize precedents get '2022다12345' --json",
            "admrules": "legalize admrules list --agency 행정안전부 --json",
            "ordinances": "legalize ordinances list --jurisdiction 서울특별시 --json",
            "all": "legalize search '검색어' --in all --json",
        }
        if task == "article":
            commands["laws"] = "legalize laws article 민법 제750조 --json"
        if task == "compare":
            commands["laws"] = "legalize laws diff 민법 민법 --date-a 2020-01-01 --date-b 2024-01-01 --mode article --json"

        return Recommendation(
            primary="legalize-cli",
            fallbacks=["mcp", "git-clone", "direct-github"],
            reasons=[
                "legalize-cli gives stable JSON and avoids manual path construction.",
                "Set GITHUB_TOKEN for repeated API calls or code-search-backed queries.",
            ],
            example_commands=[commands.get(scope, commands["all"])],
            token_present=token_present,
            detected_tools=tools,
        )

    raise ValueError(f"unsupported task: {task}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--task",
        choices=["single", "article", "search", "compare", "list", "history", "bulk", "offline", "agent"],
        required=True,
    )
    parser.add_argument(
        "--scope",
        choices=["laws", "precedents", "admrules", "ordinances", "all"],
        default="all",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    rec = recommend(args.task, args.scope)
    if args.json:
        print(json.dumps(asdict(rec), ensure_ascii=False, indent=2))
        return

    print(f"primary: {rec.primary}")
    print(f"fallbacks: {', '.join(rec.fallbacks)}")
    print(f"token_present: {str(rec.token_present).lower()}")
    print("reasons:")
    for reason in rec.reasons:
        print(f"- {reason}")
    print("example_commands:")
    for command in rec.example_commands:
        print(f"- {command}")


if __name__ == "__main__":
    main()
