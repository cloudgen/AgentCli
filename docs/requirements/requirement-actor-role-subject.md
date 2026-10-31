**file**: docs/requirements/requirement-actor-role-subject.md
**Status**: Active (Version 1.0.0)
**Area**: architecture
**Key**: `requirement-actor-role-subject`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Who runs AgentCli. This product has no dest approval machine. The catalog is three columns.

Specialized from **`LM-ACTOR-ROLE-SUBJECT`**. There is no Approver column and no Submitter column.

### 1.1 Human-facing

**In one sentence:** The person at this login runs the verbs. Nobody else has to approve them first.

| You | Another role | Not this |
|-----|--------------|----------|
| Run `agent-cli` | The verb family in the table | An approver account, a dest review queue, or a second who-table |

## 2. Core Rules

1. Columns **MUST** be Actor, Role, and Subject only.
2. **MUST NOT** add Approver or Submitter. **MUST NOT** invent an approver account. **MUST NOT** invent a `*-adm` file.
3. The class file points here. It does not replace this table.
4. The help family and the menu family have Subject **None**. `install` is on the placed-files row.
5. Routed-verb wording stays on `requirement-python-cli-interface` and `requirement-domain-grok-cli`. This file does not restate those procedures.
6. **`TP-ARS-01`**, **`TP-ARS-02`**, and **`TP-ARS-03`** assert this table in `tests/test_actor.py`. They are **have**.

| Actor | Role | Subject |
|-------|------|---------|
| This login | `help`, `version`, `about`, `hello` | None |
| This login | `menu`, `main`, menu-only `language`, menu-only Exit | None |
| This login | `ensure`, `install`, `uninstall`, `where-is-me`, `rc-test` | This login's placed files |
| This login | `self-install`, `version-check`, `self-update`, `self-uninstall` | This login's package |
| This login | `setup`, `update-grok`, `reinstall`, `run`, `check-session` | Peer `grok` for this login |
| This login | `backup`, `sync-auth`, `sync-auth-from-remote`, `sync-auth-to-remote`, `add-crontab` | This login's grok auth files |
| This login | `print-sudoers`, `print-sudoers-install-script`, `remove-project-sudoers`, `generate-sudoer-request`, `submit-sudoer-request` | This login's sudoer draft |

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | The table has Actor, Role, and Subject only |
| AC-2 | The help family uses Subject None. `install` is on the placed-files row |
| AC-3 | No requirement file in this tree adds an Approver column for this catalog |

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-31 | Active 1.0.0 | Light catalog. No dest approver. Class file points here |
