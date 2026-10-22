**file**: docs/requirements/requirement-python-packaging.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-packaging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Packaging SSOT for AgentCli. Version, name, and the console script live in `pyproject.toml`.

### 1.1 Human-facing

**In one sentence:** `pip install AgentCli` installs the command `agent-cli`.

| You | Another role | Not this |
|-----|--------------|----------|
| Install with pip | ChronicleLogger comes along | `sudo pip`, or `curl \| sh` as this package's installer |

## 2. Core Rules

1. `[project].name` **MUST** be `AgentCli`.
2. `[project].version` **MUST** equal `src/AgentCli/__init__.py` `__version__`. This tree is **1.2.0**.
3. The console script **MUST** be `agent-cli = AgentCli.cli:main`.
4. `requires-python` **MUST** allow 2.7 and 3.x except 3.0 through 3.4.
5. Dependency **MUST** include `ChronicleLogger>=1.3.1`.
6. `self-install` runs `python -m pip install AgentCli`. `self-update` runs `python -m pip install --upgrade AgentCli`. `version-check` runs `python -m pip index versions AgentCli`. `self-uninstall` runs `python -m pip uninstall -y AgentCli` and needs `--force` on the command line.
7. Those pip verbs **MUST NOT** use sudo.
8. Nothing in this tree uploads a release by itself.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | pyproject version equals `__version__` |
| AC-2 | README badge uses that version |
| AC-3 | README does not say `sudo pip` or `curl \| sh` |
