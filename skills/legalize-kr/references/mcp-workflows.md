# Connected MCP retrieval

Use these examples with the Legalize-KR tools available in the current conversation.
Read the connected schemas first. Older servers can expose fewer tools or different output fields.
The JSON blocks show tool names and arguments. They are not shell commands.

## Laws and articles

For “현재 민법 제750조를 알려줘”, retrieve the article with the effective-date basis:

```json
{"name":"laws_article","arguments":{"law_name":"민법","article_no":"제750조","semantic":"시행일자"}}
```

For “2024년 10월 1일에 시행 중이던 국경일에 관한 법률 전문을 보여줘”, use:

```json
{"name":"laws_get","arguments":{"law_name":"국경일에 관한 법률","date":"2024-10-01","semantic":"시행일자"}}
```

For “근로기준법 시행령 전문을 보여줘”, keep the category separate from the statute name:

```json
{"name":"laws_get","arguments":{"law_name":"근로기준법","category":"시행령","semantic":"시행일자"}}
```

These tools select a file version. They do not decide article-specific commencement dates or transitional rules.
Read `version`, `warnings`, and the source before describing legal effect.
Use `공포일자` for a request about promulgation. The tool default remains `공포일자` for compatibility.

For “2020년과 2024년의 근로기준법을 비교해줘”, use:

```json
{"name":"laws_diff","arguments":{"law_name":"근로기준법","date_a":"2020-01-01","date_b":"2024-01-01","semantic":"시행일자","mode":"article"}}
```

If the user needs different dates, use those dates. Report each resolved version and relevant warnings.
The comparison follows Markdown structure. A `renamed` result is a similarity estimate.

## Precedents

For “점유취득시효 관련 판례를 찾아 요지를 정리해줘”, search a short topic:

```json
{"name":"search","arguments":{"keyword":"점유취득시효","scope":"precedents","strategy":"auto","limit":5}}
```

Select relevant returned items. Call `precedents_get` with each selected `path` as `identifier`.
Read the body before summarizing case numbers, dates, courts, or holdings.
If the case number is known, `precedents_get` also accepts it directly.
On `AMBIGUOUS_MATCH`, use the user's court or case context to narrow the returned candidate paths.
If that context does not resolve the candidates, ask the user to choose.

## Administrative rules

For “행정안전부 고시를 찾아서 전문을 보여줘”, list a small filtered page:

```json
{"name":"admrules_list","arguments":{"agency":"행정안전부","type_":"고시","page_size":5}}
```

Use a document's returned `path` as `identifier` in `admrules_get`.
For a topic such as “공공데이터 지침”, use `search` with `scope="admrules"` and a short keyword.
If the user specifies an agency, select candidates from that agency.
Do not guess a complete document name or repository path.

## Local ordinances

For “서울특별시 강남구 조례를 찾아 전문을 보여줘”, use:

```json
{"name":"ordinances_list","arguments":{"jurisdiction":"서울특별시","subdivision":"강남구","type_":"조례","page_size":5}}
```

Use a document's returned `path` as `identifier` in `ordinances_get`.
For a topic such as “공공시설 사용료”, use `search` with `scope="ordinances"` and a short keyword.
Select candidates from the requested region. Do not substitute another region's same-name ordinance.
If more list results are necessary, use the returned `next_page`.
If `next_page` is null, the listing is complete for those filters.

## Sources and limits

Search results identify candidates. They do not supply document bodies.
For law search paths such as `kr/민법/법률.md`, use `law_name="민법"` and `category="법률"` with a law tool.
For other datasets, copy the returned `path` to the matching get tool's `identifier`.

Use sources from the fetched document. Cite its official `source.original_url` when available and its `source.github_url`.
The fetched source can differ from the search index. A code search result does not identify a historical snapshot.

Read every search `outcomes` entry and `warnings` before interpreting results.
`PATH_SEARCH_ONLY` means that the search covered paths rather than bodies.
`PARTIAL_SEARCH` means that some datasets failed. `truncated` means that further matches exist.
None of these results establish that a rule or precedent does not exist.

If the host does not expose tools, explain that this conversation cannot call them.
An installed or connected account alone does not prove tool availability here.
Use the host's plugin selection controls. Do not recommend reinstallation as the first response.
Sites controls access separately from installation. An owner-private Site is unavailable to other users.

The site owner configures `GITHUB_TOKEN` for shared content search and request limits.
Visitors do not need individual GitHub connections. Never request a token in chat or tool arguments.
For `AUTH_REQUIRED`, explain the missing server capability.
For `RATE_LIMITED`, explain the request limit and stop repeated identical calls.
For `RESPONSE_TOO_LARGE`, use `laws_article` if the request identifies a law article.
If the user needs the full document, provide the links from `error.source` instead of claiming full retrieval.
Ask which article the user needs when that choice remains unclear.
Do not raise `limit` or repeat the same full-document call. Those actions cannot reduce its response size.
Treat `isError: true` as a failed retrieval. Never invent source text after a failure.
