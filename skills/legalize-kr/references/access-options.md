# Access Options

Use this reference when deciding how to retrieve or analyze Legalize-KR data.

## Decision Matrix

| Method | Use When | Strengths | Tradeoffs |
|---|---|---|---|
| `legalize-cli` | One-off lookup, JSON output, date-based law article retrieval, no local clone | Fast setup, agent-friendly `--json`, local cache, all four datasets, no manual path construction for common tasks | GitHub API rate limits; Python install or `uvx`; not ideal for very large local grep |
| Local MCP server | An MCP-capable agent can run local stdio tools | Conversational agent integration, structured tool calls, same package as CLI | Requires MCP client setup plus `uvx`, `pipx`, or `pip`; still subject to GitHub API limits |
| Git clone | Bulk grep, offline work, Git history/diff, reproducible snapshots | Full Markdown corpus, native `git log`/`git diff`, no API calls after clone | Larger local checkout; path knowledge required; data repos may be force-pushed |
| Direct GitHub/raw | Known path, tiny retrieval, no install desired | Minimal tooling, easy to cite URL | Brittle for search/disambiguation; rate limits for API; no helper parsing |
| `https://legalize.kr/llms.txt` | Prompt bootstrap or quick public overview | Compact LLM-friendly context | Summary only; verify detailed/current behavior against repo READMEs or `legalize-cli --help` |

## Recommended Defaults

- For user-facing answers about a single law, article, precedent, rule, or ordinance: start with `legalize-cli --json`.
- For agent product setup with local tool execution: configure `legalize-mcp`.
- For non-developer users who only need agent guidance: install the skill/plugin first, then add MCP only if actual tool calls are needed.
- For "find every occurrence", "compare many files", or "show history": clone the relevant repository and use `rg` plus Git.
- For exact current tool names: inspect the installed `legalize-cli` help or `cli-tools` README, because compact public summaries may not list every domain.

## CLI Patterns

```bash
# List and fetch laws.
legalize laws list --category 법률 --json
legalize laws get 민법 --date 2024-01-01 --json
legalize laws article 민법 제750조 --json

# Compare a law across dates.
legalize laws diff 근로기준법 근로기준법 \
  --date-a 2020-01-01 \
  --date-b 2024-01-01 \
  --mode article \
  --json

# Search all datasets.
legalize search "점유취득시효" --in all --json

# Administrative rules and local ordinances.
legalize admrules list --agency 행정안전부 --type 고시 --json
legalize ordinances list --jurisdiction 서울특별시 --type 조례 --json
```

## Rate Limits

GitHub REST API limits are usually:

- Unauthenticated: 60 requests/hour per IP.
- Authenticated: 5,000 requests/hour.

Set one of:

```bash
export GITHUB_TOKEN=$(gh auth token)
export GITHUB_TOKEN=ghp_xxxx
export LEGALIZE_GITHUB_TOKEN=ghp_xxxx
legalize --token ghp_xxxx ...
```

Use tree/metadata strategies or local clones when code search would exhaust quota.

## MCP Patterns

Register `legalize-mcp` as a local stdio MCP server. Ask the agent to call tools rather than scraping pages.

No permanent install:

```json
{
  "mcpServers": {
    "legalize-kr": {
      "command": "uvx",
      "args": ["--from", "legalize-cli[mcp]", "legalize-mcp"]
    }
  }
}
```

Installed command:

```bash
pipx install 'legalize-cli[mcp]'
```

```json
{
  "mcpServers": {
    "legalize-kr": {
      "command": "legalize-mcp"
    }
  }
}
```

Available tool categories:

- Laws: list, full text, article.
- Precedents: list, full text.
- Administrative rules: list, full text.
- Local ordinances: list, full text.
- Search: keyword search across scopes.

## Git Clone Patterns

```bash
git clone https://github.com/legalize-kr/legalize-kr.git
git clone https://github.com/legalize-kr/precedent-kr.git
git clone https://github.com/legalize-kr/admrule-kr.git
git clone https://github.com/legalize-kr/ordinance-kr.git

git -C legalize-kr log -- kr/민법/
git -C legalize-kr diff HEAD~1 -- kr/민법/법률.md
rg "개인정보" legalize-kr/kr
rg "사실혼" precedent-kr/가사
rg "공공데이터" admrule-kr
rg "공공시설" ordinance-kr
```

For durable references, prefer source URL, repository path, frontmatter identifiers, and dates over commit SHA alone.
