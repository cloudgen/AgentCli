**file**: docs/requirements/requirement-python-cli-language.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-cli-language`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Menu language for AgentCli. Thirteen languages. Front row **7**. Codes **80**–**92**.

### 1.1 Human-facing

**In one sentence:** Row **7** picks the menu language and saves it for the next run.

| You | Another role | Not this |
|-----|--------------|----------|
| Pick **80** English through **92** Greek | Leaf tokens such as `grok-auth` stay English | An argv verb named `language` |

## 2. Core Rules

1. Codes **MUST** be `en`, `zh-Hans`, `zh-Hant`, `es`, `ar`, `fr`, `pt`, `ru`, `de`, `ja`, `ko`, `nl`, `el` on rows **80**–**92**.
2. **70**–**79** and **93**–**98** **MUST NOT** be printed.
3. The saved leaf **MUST** be `${HOME}/.local/agent-cli/language`, mode 0600.
4. `AGENT_CLI_LANG` **MUST** override one process and **MUST NOT** write the file.
5. **0** Back **MUST NOT** write.
6. A failed write **MUST** keep the previous code.
7. The welcome line stays English. The about page stays English.
8. `language` is not an argv verb.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | Row 7 lists 80–92 and not the reserved numbers |
| AC-2 | Save writes mode 0600. Back does not write |
| AC-3 | `AGENT_CLI_LANG` wins and does not write |
