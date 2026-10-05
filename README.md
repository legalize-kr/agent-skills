# Legalize-KR Agent Skills

[![skills.sh](https://skills.sh/b/legalize-kr/agent-skills)](https://skills.sh/legalize-kr/agent-skills)

Legalize-KR의 공개 한국 법률 데이터를 AI Agent가 활용하도록 돕는 스킬/플러그인 저장소입니다.

이 저장소는 법률 자문 도구가 아닙니다. AI Agent가 아래 공개 데이터에 더 정확히 접근하도록 돕는 안내와 설정을 제공합니다.

- 법령: `legalize-kr/legalize-kr`
- 판례: `legalize-kr/precedent-kr`
- 행정규칙: `legalize-kr/admrule-kr`
- 자치법규: `legalize-kr/ordinance-kr`

스킬 이름은 `legalize-kr`입니다.

## 먼저 고르기

현재 대화에 Legalize-KR MCP 조회 도구가 있다면 바로 사용하세요. Python이나 CLI를 설치하거나 개인 GitHub 계정을 연결할 필요가 없습니다. 스킬은 연결된 도구를 우선 선택하고, 검색한 문서 후보의 전문을 조회한 뒤 출처와 함께 답하도록 안내합니다.

OpenAI Sites의 `Legalize-KR MCP Server` 플러그인과 이 저장소의 스킬/로컬 MCP 패키지는 연결 방식이 다릅니다. [Sites 안내 페이지](https://legalize-kr-mcp.icy-bowl-0769.chatgpt.site)는 공개되어 있으며, 조회 도구는 앱에서 계정을 연결해 사용합니다. 사이트 공개와 플러그인 공개 목록 등록은 별개입니다. 이 저장소의 ZIP을 바꾸어도 Sites 플러그인이 갱신되지는 않습니다.

터미널이나 개발 도구가 익숙하지 않다면 **Claude Cowork에서 Release ZIP 업로드**를 권장합니다.

| 상황 | 권장 방법 |
|---|---|
| 현재 대화에 Legalize-KR MCP 도구가 이미 보임 | 플러그인을 선택하고 자연어로 조회 요청. 추가 로컬 설치 불필요 |
| Claude Cowork를 쓰고 있고 터미널을 피하고 싶음 | GitHub Releases에서 `legalize-kr-plugin.zip` 다운로드 후 Cowork에 업로드 |
| Claude Code를 씀 | `/plugin marketplace add legalize-kr/agent-skills` 후 플러그인 설치 |
| Cursor, Codex, Cline, GitHub Copilot, Warp 등을 씀 | `npx skills add legalize-kr/agent-skills --skill legalize-kr` |
| Agent가 실제 도구 호출로 법령/판례를 조회해야 함 | `legalize-mcp` MCP 서버 연결 |
| API나 자체 Agent에 넣고 싶음 | `SKILL.md`와 `references/` 문서를 프롬프트 컨텍스트에 포함 |

## 무엇이 설치되나요?

이 저장소는 두 계층을 제공합니다.

| 계층 | 역할 | 터미널 필요 여부 |
|---|---|---|
| 스킬/플러그인 | Agent가 Legalize-KR 데이터셋, 접근 방법, 출처 표기 방식을 이해하도록 안내 | 대부분 불필요 |
| 로컬 MCP 설정 | Agent가 `legalize-mcp`를 실행해 법령·판례·행정규칙·자치법규를 실제 도구로 조회 | 필요 |

비개발자는 먼저 스킬/플러그인만 설치해도 됩니다. 다만 Agent가 실제 도구 호출까지 수행하려면 사용 중인 앱이 로컬 MCP 서버를 실행할 수 있어야 하며, `uvx` 또는 `pipx`로 `legalize-cli[mcp]`를 실행할 수 있어야 합니다.

## 바로 써보기

설치 후 Agent에게 아래처럼 요청합니다.

```text
Legalize-KR로 민법 제750조를 조회해줘.
```

```text
점유취득시효 관련 판례를 찾아서 사건번호와 요지를 정리해줘.
```

```text
행정안전부 고시 목록을 5개 보여줘. 내가 선택한 문서의 전문과 출처를 불러와줘.
```

```text
서울특별시 조례 중 공공시설 사용료와 관련된 내용을 찾아줘.
```

```text
근로기준법이 2020년과 2024년 사이에 어떻게 바뀌었는지 비교해줘.
```

Agent가 단순 설명만 한다면 현재 대화에 조회 도구가 제공되는지 먼저 확인하세요. 플러그인 설치, 계정 연결, 현재 대화의 도구 선택은 서로 다를 수 있습니다. 이미 연결한 플러그인을 재설치하기보다 대화의 플러그인 선택 상태를 확인하세요. 로컬 MCP를 사용하는 환경에서만 `legalize-cli` 또는 `legalize-mcp` 실행 설정이 필요합니다.

스킬의 [MCP 조회 흐름](./skills/legalize-kr/references/mcp-workflows.md)은 네 자료 유형의 실제 도구 인수와 검색 후 전문 조회 절차를 설명합니다. 검색 결과를 본문으로 간주하지 않고, 시행일 기준과 출처, 검색 제한을 함께 확인합니다.

## 기준일 법령 조회

특정 날짜의 법령을 물을 때에는 공포된 버전과 시행 중인 파일 버전을 구분해야 합니다.
`legalize-cli`와 MCP `laws_get`, `laws_article`은 기본적으로 `공포일자`를 사용하므로,
시행 중인 파일을 찾는 요청에는 `시행일자`를 명시합니다.

```text
2024-10-01에 시행 중이던 민법 제1조를 조회해줘. 시행일자 기준을 사용하고, 조문별 부칙 시행일은 파일 단위 조회로 판정할 수 없다는 점도 밝혀줘.
```

응답의 `file_effective_date_only`가 `true`이면 조문별 시행일, 부칙의 적용례와 경과조치는
별도로 확인해야 합니다. 공포일자 기준 버전이 아직 시행 전이면 `warning`이 반환됩니다.
1970년 이전 기준일은 Git 보정 날짜 대신 frontmatter의 실제 공포일자 또는 시행일자를 사용합니다.

## 지원 방식 요약

| 대상 | 권장 설치 방식 | 상태 | 비고 |
|---|---|---|---|
| Claude Code | Claude plugin marketplace | 지원 | `/legalize-kr:legalize-kr`로 사용 |
| Claude Cowork | Release ZIP 업로드 또는 조직 Marketplace | 지원 | 비개발자에게 가장 쉬운 경로 |
| Claude Desktop | MCP 서버 설정 | 지원 | 도구 호출 기반 조회 |
| Cursor | Cursor plugin metadata, `skills.sh`, MCP 서버 설정 | 지원 | `.cursor-plugin/marketplace.json` 포함 |
| Codex | `skills.sh`, Codex plugin manifest | 지원 | `.codex-plugin/plugin.json` 포함 |
| Gemini CLI | Gemini extension 또는 `skills.sh` | 지원 | `gemini-extension.json` 포함 |
| GitHub Copilot, Cline, Warp 등 | `skills.sh` 또는 범용 `plugin.json` | 지원 | `skills` CLI의 agent sync 대상 |
| OpenAI/Claude API 직접 사용 | 프롬프트에 `SKILL.md`와 references 포함 | 수동 지원 | 네이티브 스킬 설치 개념이 없을 때 사용 |

별도 실행 바이너리는 제공하지 않습니다. 이 저장소는 Markdown 스킬, 플러그인 메타데이터, 보조 Python 스크립트만 포함합니다. 실제 데이터 조회 실행 도구는 `legalize-cli`와 `legalize-mcp`가 담당합니다.

## Claude Cowork

Cowork는 유료 플랜(Pro, Max, Team, Enterprise)에서 플러그인을 사용할 수 있습니다.

### 개인 사용자

1. GitHub Releases에서 `legalize-kr-plugin.zip`을 다운로드합니다.
2. Claude Desktop 앱에서 Cowork 탭을 엽니다.
3. 왼쪽 사이드바의 `Customize` 메뉴로 이동합니다.
4. `Browse plugins`에서 custom plugin file 업로드를 선택합니다.
5. 다운로드한 ZIP을 업로드합니다.
6. 대화에서 `/` 또는 `+` 버튼을 눌러 `legalize-kr` 스킬을 선택합니다.

### 조직 사용자

Team/Enterprise에서는 관리자가 이 저장소를 조직 plugin marketplace로 추가하는 방식이 적합합니다.

```text
/plugin marketplace add legalize-kr/agent-skills
/plugin install legalize-kr@legalize-kr-marketplace
```

조직 배포에서는 사용자가 ZIP을 직접 내려받지 않아도 되고, marketplace 업데이트로 새 버전을 받을 수 있습니다.

## Claude Code

GitHub 저장소를 Claude plugin marketplace로 추가한 뒤 플러그인을 설치합니다.

```bash
claude plugin marketplace add legalize-kr/agent-skills
claude plugin install legalize-kr@legalize-kr-marketplace
```

Claude Code 대화형 UI에서는 slash command로도 가능합니다.

```text
/plugin marketplace add legalize-kr/agent-skills
/plugin install legalize-kr@legalize-kr-marketplace
```

설치 후 스킬 호출:

```text
/legalize-kr:legalize-kr
```

업데이트:

```text
/plugin marketplace update legalize-kr-marketplace
/plugin update legalize-kr@legalize-kr-marketplace
```

로컬 테스트:

```bash
git clone https://github.com/legalize-kr/agent-skills.git
cd agent-skills
claude plugin validate .
claude --plugin-dir .
```

## Cursor

이 저장소는 Cursor plugin discovery를 위한 [.cursor-plugin/marketplace.json](./.cursor-plugin/marketplace.json)을 포함합니다. Cursor UI에서 plugin marketplace를 직접 추가할 수 있는 환경에서는 `legalize-kr/agent-skills`를 추가하고 `legalize-kr` 플러그인을 설치합니다.

스킬만 설치하려면:

```bash
npx skills add legalize-kr/agent-skills --skill legalize-kr --agent cursor
```

MCP 도구로 쓰려면 `.cursor/mcp.json`에 등록합니다.

```json
{
  "servers": {
    "legalize-kr": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "legalize-cli[mcp]", "legalize-mcp"]
    }
  }
}
```

## Codex

이 저장소는 Codex plugin manifest인 [.codex-plugin/plugin.json](./.codex-plugin/plugin.json)을 포함합니다. 현재 가장 호환성이 좋은 경로는 `skills.sh`로 스킬을 설치하는 방식입니다.

프로젝트에 스킬 설치:

```bash
npx skills add legalize-kr/agent-skills --skill legalize-kr --agent codex
```

전역 설치:

```bash
npx skills add legalize-kr/agent-skills --skill legalize-kr --agent codex --global
```

설치 후 Codex에 `legalize-kr 스킬을 사용해서 민법 제750조를 조회해줘`처럼 요청합니다.

## Gemini CLI

Gemini CLI extension metadata인 [gemini-extension.json](./gemini-extension.json)을 포함합니다.

```bash
gemini extensions install https://github.com/legalize-kr/agent-skills
```

스킬 파일만 설치하려면 `skills.sh`를 사용합니다.

```bash
npx skills add legalize-kr/agent-skills --skill legalize-kr --agent gemini-cli
```

## GitHub Copilot, Cline, Warp 등

`skills.sh`의 universal agent 설치를 사용합니다.

```bash
npx skills add legalize-kr/agent-skills --skill legalize-kr --agent '*'
```

특정 agent만 지정할 수도 있습니다.

```bash
npx skills add legalize-kr/agent-skills --skill legalize-kr --agent cline
npx skills add legalize-kr/agent-skills --skill legalize-kr --agent github-copilot
npx skills add legalize-kr/agent-skills --skill legalize-kr --agent warp
```

사용 가능한 agent 이름은 로컬 `skills` CLI 버전에 따라 달라질 수 있습니다.

```bash
npx skills add legalize-kr/agent-skills --skill legalize-kr --list
npx skills list --json
```

## MCP 도구 연결

이 저장소의 [.mcp.json](./.mcp.json)은 `uvx`로 `legalize-cli[mcp]`를 실행합니다. `uvx` 방식은 별도 가상환경을 만들지 않고 MCP 서버를 실행하므로, Claude Code, Cursor, Gemini CLI 같은 개발자 도구에서 가장 간단합니다.

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

`uvx`를 쓰지 않는 환경에서는 먼저 MCP extra를 한 번 설치한 뒤 `legalize-mcp`를 직접 실행하도록 바꿉니다.

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

Claude Desktop의 `claude_desktop_config.json`에도 같은 설정을 넣을 수 있습니다. Python 도구 설치가 익숙하지 않은 사용자는 이 단계에서 도움을 받을 가능성이 높습니다.

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

토큰 없이도 동작하지만 GitHub API 한도가 낮습니다. 반복 검색이나 코드 검색을 쓸 때는 Agent를 시작하는 환경에 `GITHUB_TOKEN` 또는 `LEGALIZE_GITHUB_TOKEN`을 설정하세요.

## 직접 API에 넣기

네이티브 스킬 설치 기능이 없는 환경에서는 아래 파일을 프롬프트 컨텍스트에 포함합니다.

```text
skills/legalize-kr/SKILL.md
skills/legalize-kr/references/access-options.md
skills/legalize-kr/references/data-layout.md
```

대량 조회나 자동화가 필요하면 모델에 `legalize-cli` 또는 `legalize-mcp` 사용을 지시하는 편이 낫습니다.

## 데이터 조회 CLI

스킬은 접근 전략을 안내하고, 실제 데이터 조회는 다음 도구를 사용합니다.

```bash
pipx install legalize-cli
pipx install 'legalize-cli[mcp]'
uvx legalize-cli laws list --json
```

예시:

```bash
legalize laws article 민법 제750조 --json
legalize precedents get "2022다12345" --json
legalize admrules list --agency 행정안전부 --type 고시 --json
legalize ordinances list --jurisdiction 서울특별시 --type 조례 --json
legalize search "부동산 점유취득시효" --in all --json
```

접근 방식 추천:

```bash
python3 skills/legalize-kr/scripts/select_access_mode.py --task search --scope all
```

## 설치 확인

스킬 레이어 확인:

```text
Legalize-KR에는 어떤 데이터셋이 있고, 법령과 판례는 어떻게 조회해야 해?
```

MCP 도구 확인:

```text
Legalize-KR MCP 도구로 민법 제750조를 JSON 기준으로 조회해줘.
```

검색 확인:

```text
Legalize-KR에서 "부동산 점유취득시효"를 전체 데이터셋 기준으로 검색해줘.
```

기대 결과는 “일반적인 법률 설명”이 아니라 Legalize-KR 데이터셋, 기준일, 경로, 사건번호, 조문 번호 같은 출처 단서가 포함된 답변입니다.

## 문제 해결

### 스킬이 보이지 않음

- Claude Code/Cowork는 플러그인을 설치한 뒤 새 대화에서 `/`를 눌러 확인합니다.
- `skills.sh` 사용자는 `npx skills list --json`으로 설치 여부를 확인합니다.
- Agent가 캐시를 쓰는 경우 앱 또는 세션을 재시작합니다.

### MCP 도구가 보이지 않음

- 원격 플러그인은 계정 연결과 현재 대화의 플러그인 선택을 확인합니다. 설치 완료만으로 모든 대화에서 도구를 사용할 수 있다고 단정하지 않습니다.
- Sites의 소유자 전용 서버는 다른 이용자가 설치해도 접근할 수 없습니다. 운영자가 허용한 대상과 앱의 설치 경로가 필요합니다.
- `uvx --version` 또는 `legalize-mcp`가 실행되는지 확인합니다.
- `uvx`를 사용한다면 `uvx --from legalize-cli[mcp] legalize-mcp`가 실행되는지 확인합니다.
- `pipx install 'legalize-cli[mcp]'`로 MCP extra가 설치되어 있는지 확인합니다.
- Claude/Cursor/Gemini 등 호스트 앱을 재시작합니다.

### GitHub rate limit 오류

반복 검색이나 code search에는 GitHub 토큰이 필요할 수 있습니다.

```bash
export GITHUB_TOKEN=$(gh auth token)
```

토큰은 공개 저장소 읽기 용도만 필요합니다.

### Cowork ZIP 업로드가 실패함

- GitHub Releases의 `legalize-kr-plugin.zip`을 그대로 업로드합니다.
- 저장소 전체 ZIP이 아니라 Release asset ZIP이어야 합니다.
- 직접 만든 ZIP은 아래 명령으로 검증합니다.

```bash
python3 scripts/package_claude_plugin.py
python3 scripts/validate_claude_plugin_package.py dist/legalize-kr-plugin.zip
```

## Release 산출물

Cowork 업로드용 ZIP만 Release asset으로 제공합니다.

- 파일명: `legalize-kr-plugin.zip`
- 내용: `.claude-plugin/plugin.json`, `.mcp.json`, `skills/legalize-kr/**`, `README.md`
- 제외: `.git`, `dist`, 캐시, 빌드 산출물

Git tag를 푸시하면 GitHub Actions가 ZIP을 만들고 Release에 첨부합니다.

```bash
git tag v0.1.0
git push origin v0.1.0
```

일반 AI Agent용 별도 바이너리는 제공하지 않습니다. 이유는 다음과 같습니다.

- 스킬은 Markdown 기반 지식/절차 패키지입니다.
- Claude Code와 Cowork는 플러그인/ZIP을 직접 소비합니다.
- Cursor, Codex, Gemini CLI, Cline 등은 `skills.sh`가 스킬 파일을 설치합니다.
- 데이터 조회 실행 파일은 이미 `legalize-cli` 패키지가 담당합니다.

## 저장소 구조

```text
.claude-plugin/
  marketplace.json
  plugin.json
.codex-plugin/
  plugin.json
.cursor-plugin/
  marketplace.json
.github/workflows/
  release.yml
.mcp.json
gemini-extension.json
plugin.json
scripts/
  package_claude_plugin.py
  validate_claude_plugin_package.py
skills/
  legalize-kr/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
```

## 참고

- Legalize-KR LLM 문맥: https://legalize.kr/llms.txt
- Legalize-KR GitHub: https://github.com/legalize-kr
- CLI/MCP 도구: https://github.com/legalize-kr/cli-tools
- skills.sh: https://skills.sh/
- Claude Code plugin marketplace 문서: https://code.claude.com/docs/ko/plugin-marketplaces
- Claude Cowork plugin 문서: https://support.claude.com/en/articles/13837440-use-plugins-in-claude-cowork
