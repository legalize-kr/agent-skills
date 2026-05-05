# Data Layout

Use this reference when constructing paths, interpreting frontmatter, or explaining the Legalize-KR data model.

## Repositories

| Repository | Dataset | Notes |
|---|---|---|
| `legalize-kr/legalize-kr` | Laws | Markdown files under `kr/`; law revisions are Git commits dated by promulgation date |
| `legalize-kr/precedent-kr` | Court precedents | Markdown files grouped by case type and court level; commits are dated by decision date |
| `legalize-kr/admrule-kr` | Administrative rules | Markdown files grouped by agency path, rule type, and rule name |
| `legalize-kr/ordinance-kr` | Local ordinances | Markdown files grouped by jurisdiction, subdivision, ordinance type, and ordinance name |
| `legalize-kr/cli-tools` | CLI and MCP | `legalize-cli` package, including `legalize` CLI and `legalize-mcp` stdio server |

## Laws

Path pattern:

```text
kr/{law-name-without-spaces}/
  법률.md
  시행령.md
  시행규칙.md
  대통령령.md
```

Examples:

```text
kr/민법/법률.md
kr/민법/시행령.md
kr/친일반민족행위자재산의국가귀속에관한특별법/법률.md
```

Important frontmatter fields:

- `제목`
- `법령MST`
- `법령ID`
- `법령구분`
- `소관부처`
- `공포일자`
- `공포번호`
- `시행일자`
- `상태`
- `출처`

Use Git history for revision questions:

```bash
git -C legalize-kr log -- kr/민법/
git -C legalize-kr log --before="2025-01-01" -1 -- kr/민법/법률.md
```

## Court Precedents

Current path pattern:

```text
{case-type}/{court-level}/{court-name}_{decision-date}_{case-number}.md
{case-type}/{court-level}/{court-name}_{decision-date}_{case-number}_{precedent-id}.md
```

Examples:

```text
민사/대법원/대법원_2002-09-27_2000다10048.md
가사/대법원/대법원_2003-11-14_2000므1257_본소_1264_반소.md
```

Compact public summaries may show an older `{case-number}.md` pattern. When exact paths matter, use the current repository tree or `legalize precedents get` to avoid filename-version assumptions.

Case types include `민사`, `형사`, `일반행정`, `세무`, `가사`, `특허`, `선거·특별`, and `기타`.

Important frontmatter fields:

- `판례일련번호`
- `사건번호`
- `사건명`
- `법원명`
- `법원등급`
- `사건종류`
- `선고일자`
- `출처`

Common body sections:

- `판시사항`
- `판결요지`
- `참조조문`
- `참조판례`
- `판례내용`

## Administrative Rules

Path pattern:

```text
{agency-path...}/
  {rule-type}/
    {rule-name}/
      본문.md
    {rule-name}_{issue-number-or-rule-id}/
      본문.md
```

Examples:

```text
행정안전부/_본부/고시/공공데이터 관리지침/본문.md
국토교통부/제주지방항공청/훈령/제주지방항공청 사무분장 및 위임전결 사항 등에 관한 규정/본문.md
```

Important frontmatter fields:

- `행정규칙ID`
- `행정규칙일련번호`
- `행정규칙명`
- `행정규칙종류`
- `상위기관명`
- `소관부처명`
- `기관경로`
- `발령번호`
- `발령일자`
- `시행일자`
- `제개정구분`
- `본문출처`
- `출처`

`본문출처: parsing-failed` means the XML did not provide parsed body text, often because the source provides attachments or empty body fields.

## Local Ordinances

Path pattern:

```text
{jurisdiction}/
  {subdivision-or-_본청-or-_교육청}/
    {ordinance-type}/
      {ordinance-name}/
        본문.md
      {ordinance-name}_{promulgation-number-or-ordinance-id}/
        본문.md
```

Examples:

```text
서울특별시/_본청/조례/서울특별시 테스트 조례/본문.md
경기도/수원시/규칙/수원시 사무전결 처리 규칙/본문.md
부산광역시/_교육청/조례/부산광역시교육청 교육복지 조례/본문.md
```

Supported ordinance types include `조례`, `규칙`, `훈령`, `예규`, `고시`, and `의회규칙`.

Important frontmatter fields:

- `자치법규ID`
- `자치법규일련번호`
- `자치법규명`
- `자치법규종류`
- `지자체기관명`
- `지자체구분`
- `공포일자`
- `공포번호`
- `시행일자`
- `제개정구분`
- `자치법규분야`
- `담당부서`
- `본문출처`
- `출처`

## Known Caveats

- Data repositories may be force-pushed when collection or conversion pipelines are rebuilt.
- Git cannot represent pre-1970 dates directly; older law promulgation or precedent decision dates are preserved in frontmatter even if Git dates are pinned.
- Some old precedent dates from the source API use Dangi years and are normalized to CE.
- Some law image/formula/table markup may remain as source markup.
- Markdown renderers may hide angle-bracket annotations such as `<개정 2024.9.20>` if treated as HTML tags.

