---
name: legalize-kr
description: Use this skill when working with Legalize-KR public Korean legal data, including laws, court precedents, administrative rules, and local ordinances. It guides agents to choose between legalize-cli, the local stdio legalize MCP server, git clone workflows, and direct GitHub access for search, retrieval, article lookup, revision history, bulk analysis, offline work, and LLM context building.
---

# Legalize-KR Data

Use Legalize-KR as a public Markdown/Git mirror of Korean legal data. The core datasets are:

- Laws: `legalize-kr/legalize-kr`
- Court precedents: `legalize-kr/precedent-kr`
- Administrative rules: `legalize-kr/admrule-kr`
- Local ordinances: `legalize-kr/ordinance-kr`

Treat the data as legal source material, not legal advice. When answering a user, state the dataset, date basis, and access method used whenever those affect correctness.

## Workflow

1. Classify the request:
   - Dataset: laws, precedents, administrative rules, ordinances, or all.
   - Operation: list, search, fetch full text, fetch one law article, compare revisions, inspect history, bulk analyze, or configure agent access.
   - Freshness: current remote data, a specific date, a local clone, or cached/offline data.

2. Choose the access method:
   - Prefer `legalize-cli` for shell-based one-off lookup, JSON output, and no-clone workflows.
   - Prefer local stdio MCP tools when the user is configuring or using an MCP-capable agent that can run local commands.
   - Prefer `git clone` for large grep/search, history/diff work, reproducible offline analysis, or direct Markdown inspection.
   - Use direct GitHub/raw URLs only when the target path is already known and installing tools or cloning would be excessive.

   If the best path is unclear, run:

   ```bash
   python3 skills/legalize-kr/scripts/select_access_mode.py --task search --scope all
   ```

3. Use the selected method with a narrow query first, then broaden only if needed. Avoid dumping whole repositories into context.

4. If docs conflict, prefer the current target repository README or current tree over compact summaries. `https://legalize.kr/llms.txt` is useful LLM context, but it may be a summary and may lag detailed repo docs or newer CLI/MCP support.

## CLI Quick Reference

Install:

```bash
pipx install legalize-cli
pipx install 'legalize-cli[mcp]'
uvx legalize-cli laws list --json
uvx --from legalize-cli[mcp] legalize-mcp
```

Set a token for GitHub API rate limits when doing repeated or code-search work:

```bash
export GITHUB_TOKEN=$(gh auth token)
legalize auth status --json
```

Common commands:

```bash
legalize laws list --category 법률 --json
legalize laws get 민법 --date 2015-06-01 --json
legalize laws article 민법 제839조의2 --date 2015-06-01 --json
legalize laws diff 민법 민법 --date-a 2015-01-01 --date-b 2024-01-01 --mode article --json

legalize precedents list --court 대법원 --type 민사 --json
legalize precedents get "2022다12345" --json

legalize admrules list --agency 행정안전부 --type 고시 --json
legalize admrules get "공공데이터 관리지침" --agency 행정안전부 --type 고시 --json

legalize ordinances list --jurisdiction 서울특별시 --type 조례 --json
legalize ordinances get "서울특별시 테스트 조례" --jurisdiction 서울특별시 --type 조례 --json

legalize search "부동산 점유취득시효" --in all --json
```

Use `--json` for agent-readable output. Use `--offline` only when the needed data is already cached.

## MCP Quick Reference

Install MCP support:

```bash
pipx install 'legalize-cli[mcp]'
legalize-mcp
```

Register a local stdio server in MCP clients. Use `uvx` when the package should run without a permanent install:

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

Use an already installed `legalize-mcp` command when `legalize-cli[mcp]` was installed with `pipx` or `pip`:

```json
{
  "mcpServers": {
    "legalize-kr": {
      "command": "legalize-mcp",
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

Current tool surface in `legalize-cli` includes:

- `laws_list`, `laws_get`, `laws_article`
- `precedents_list`, `precedents_get`
- `admrules_list`, `admrules_get`
- `ordinances_list`, `ordinances_get`
- `search`

Prefer MCP when a user asks an agent to answer legal-data questions conversationally and the host can run local stdio MCP servers. If the host cannot run tools, use the skill as guidance and cite the GitHub dataset paths or direct URLs used.

## Git Clone Quick Reference

Clone only the dataset needed:

```bash
git clone https://github.com/legalize-kr/legalize-kr.git
git clone https://github.com/legalize-kr/precedent-kr.git
git clone https://github.com/legalize-kr/admrule-kr.git
git clone https://github.com/legalize-kr/ordinance-kr.git
```

Examples:

```bash
cat legalize-kr/kr/민법/법률.md
git -C legalize-kr log -- kr/민법/
rg "개인정보" legalize-kr/kr

rg "사실혼" precedent-kr/가사
rg "공공데이터" admrule-kr/행정안전부
rg "공공시설" ordinance-kr/서울특별시
```

The data repositories may be force-pushed after pipeline improvements. Do not rely on commit SHA stability for durable citations; cite repository path plus frontmatter dates or domain identifiers where possible.

## References

- Read `references/access-options.md` when choosing between CLI, MCP, git clone, and direct GitHub access.
- Read `references/data-layout.md` when constructing repository paths, interpreting frontmatter, or explaining data model details.
