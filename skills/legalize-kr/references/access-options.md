# Access Options

Use this reference when deciding how to retrieve or analyze Legalize-KR data.

## Decision Matrix

| Method | Use When | Strengths | Tradeoffs |
|---|---|---|---|
| Connected MCP tools | Legalize-KR tools are available in the conversation | Direct retrieval without local installation | Host connection, Site audience, and server request limits apply |
| `legalize-cli` | One-off lookup, JSON output, date-based law article retrieval, no local clone | Fast setup, agent-friendly `--json`, local cache, all four datasets, no manual path construction for common tasks | GitHub API rate limits; Python install or `uvx`; not ideal for very large local grep |
| Local MCP server | An MCP-capable agent can run local stdio tools | Conversational agent integration, structured tool calls, same package as CLI | Requires MCP client setup plus `uvx`, `pipx`, or `pip`; still subject to GitHub API limits |
| Git clone | Bulk grep, offline work, Git history/diff, reproducible snapshots | Full Markdown corpus, native `git log`/`git diff`, no API calls after clone | Larger local checkout; path knowledge required; data repos may be force-pushed |
| Direct GitHub/raw | Known path, tiny retrieval, no install desired | Minimal tooling, easy to cite URL | Brittle for search/disambiguation; rate limits for API; no helper parsing |
| `https://legalize.kr/llms.txt` | Prompt bootstrap or quick public overview | Compact LLM-friendly context | Summary only; verify detailed/current behavior against repo READMEs or `legalize-cli --help` |

## Recommended Defaults

- For conversational retrieval, use connected Legalize-KR MCP tools first. Read `mcp-workflows.md` for the search-to-document workflow.
- If connected tools are unavailable and shell access is appropriate, use `legalize-cli --json`.
- For agent product setup with local tool execution: configure `legalize-mcp`.
- For non-developer users, use the host's plugin selection and connection controls. Installation alone does not prove tool availability in the current conversation.
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

## Law Date Semantics

`laws as-of`, `laws get`, `laws article`, `laws diff`, and MCP `laws_get` /
`laws_article` / `laws_diff` accept both `공포일자` and `시행일자`:

```bash
# Explicit compatibility behavior: latest file promulgated by the date.
legalize laws get 민법 --date 2024-10-01 --semantic 공포일자 --json

# File version in force by its frontmatter enforcement date.
legalize laws article 민법 제1조 --date 2024-10-01 --semantic 시행일자 --json
```

- The default is `공포일자`. If that version had not yet entered into force,
  the JSON response has `warning`.
- Use `시행일자` for a request about the file version in force on a date.
- The decision is file-level only. `file_effective_date_only: true` excludes
  article-specific effective dates, supplementary-rule application cases, and
  transitional measures. Report this limitation when it affects the answer.
- For a date before 1970, the selection uses the actual frontmatter date rather
  than the epoch-clamped Git author date.
- Cite `semantic`, `requested_date`, `resolved_version_date`, and the selected
  commit SHA in date-sensitive answers.

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

### Connected hosted MCP

The [Sites guide](https://legalize-kr-mcp.icy-bowl-0769.chatgpt.site) permits public visits.
Its document tools require the provisioned plugin and a Sites OAuth connection.
Public Site access does not establish public plugin directory distribution.
Personal GitHub key registration is optional. Without a key, retrieval limits or content search restrictions can apply.
A registered key serves only its owner and is not shared with other users.
Users can delete their key on the personal key page.
Other users need a supported installation path in their host app.
Do not change the audience or reuse the owner's credentials to resolve access failures.

For a separate Bearer-authenticated server, enter its access key through the host's secure connection controls.
Do not send access keys in conversation or as tool arguments. Read the connected tool schemas before use.

### Local stdio MCP

Register `legalize-mcp` as a local stdio MCP server. Ask the agent to call tools rather than scraping pages.

No permanent install:

```json
{
  "mcpServers": {
    "legalize-kr": {
      "command": "uvx",
      "args": ["--from", "legalize-cli[mcp]==0.5.1", "legalize-mcp"]
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

- Laws: list, full text, article, same-law structural diff. `laws_get`,
  `laws_article`, and `laws_diff` support the `semantic` argument. MCP 2.0
  uses `version.effective_date_scope: "file"`; CLI 1.0 keeps
  `file_effective_date_only: true`.
- Precedents: list, full text.
- Administrative rules: list, full text.
- Local ordinances: list, full text.
- Search: keyword search across scopes.

MCP 2.0 provides `structuredContent` plus equal JSON text. Inspect `version`,
`source`, `warnings`, and each search `outcomes` entry. `PATH_SEARCH_ONLY`
indicates path-only search, `PARTIAL_SEARCH` indicates missing datasets, and
`SEARCH_INDEX_NOT_SNAPSHOT` means GitHub body search is not a historical snapshot.
An error has `isError: true` and a JSON text `error.code`; `AMBIGUOUS_MATCH`
requires choosing a full public path. Do not supply token or arbitrary local
file paths as MCP arguments.

### Optional remote MCP

Worker 0.2.1 at `https://mcp.legalize.kr/mcp` adopts the same 11-tool MCP 2.0
contract. Configure `Authorization: Bearer <MCP_API_KEY>` through the host's
secure settings, never conversation or tool arguments. The endpoint is
access-key restricted, not an anonymous public service. An optional
`X-GitHub-Token` header overrides the server GitHub token for one request.
Remote HTTP does not change the local stdio installation or CLI 1.0 output.
Remote execution has additional CPU, input and diff-work limits; large requests
may require a narrower query or local execution. Inspect `tools/list` because
older remote deployments supplied only six tools and different results.

### Optional OpenAI Sites MCP

The workspace `sites-mcp/` implementation provides the same 11-tool MCP 2.0
contract through a Site-hosted `POST /mcp` endpoint. Publication and installation
must be verified before treating a registered Site as available.

Sites manages OAuth, access policy and its App/plugin. For a published instance,
install/connect its provisioned plugin under **Plugins → Personal → Created by
you**. Use Sites-reported connection details; do not reuse `MCP_API_KEY`, add a
local stdio server or run `codex mcp add` for this connection. The initial audience
is owner-private. Discovery is public-schema-only; data calls require the user
identity supplied by Sites after authentication and audience checks.

A personal GitHub key is optional. Register it through the Site’s personal key page.
Without a key, request limits or body search restrictions can apply.
If `auto` uses paths, report `PATH_SEARCH_ONLY`. If `code` requires authentication, report `AUTH_REQUIRED`. Check `warnings`, `outcomes` and `source`. The local CLI,
local stdio installation, and the separate Bearer-authenticated remote endpoint
retain their existing contracts.

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
