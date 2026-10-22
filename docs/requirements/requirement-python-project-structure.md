**file**: docs/requirements/requirement-python-project-structure.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-project-structure`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The Python package lives under `src/AgentCli/`. One class in each module.

### 1.1 Human-facing

**In one sentence:** The program you run is the `AgentCli` package, not a second copy of HelloTui.

| You | Another role | Not this |
|-----|--------------|----------|
| Import `AgentCli` | `src/grok-cli` is the shell reference | A `join.py` module |

## 2. Core Rules

1. The package **MUST** contain `__init__.py`, `__main__.py`, `cli.py`, `tui.py`, `menu_painter.py`, `menu_model.py`, `menu_session.py`, `menu_language.py`, `system_log.py`, `self_management.py`, `about_page.py`, `check_system.py`, `grok_domain.py`, `host.py`, `output.py`, `storage.py`, and `shell_startup.py`.
2. **MUST NOT** add `join.py` or an encoder module.
3. `__main__.py` **MUST** call `cli.main`.
4. `src/grok-cli` may remain as the POSIX behavior reference. It is not the pip ship unit.
5. `__main__.py` **MUST** import `main` from `cli` and call `sys.exit(main())`.

## Sample code

```python
import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
```

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | `python -m AgentCli` reaches `cli.main` |
| AC-2 | No `join.py` is in the package |
| AC-3 | `__main__.py` calls `sys.exit(main())` |

## Terminologies

### Python PyPI CLI

**Definition:** A Python PyPI CLI is a software-development product whose primary operator surface is a short-lived console script installed from Python packaging. `pyproject.toml` is the packaging SSOT, ship source lives under `src/AgentCli/`, and the operator runs the declared console entry `agent-cli`. It is not a long-running HTTP process. `requirement-python-oop` leaves StateLogic unordered. The classes in this package stay ordinary classes.

**Human daily-life explanation:** A Python PyPI CLI is a short-lived console command installed from Python packaging: `pyproject.toml`, source under `src/`, and a declared entry. It is not a backend and frontend diner.

**Daily-life example:** A mixer you install from a catalog listing, with a named on switch. It is not a café that stays open with a dining room.

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-22 | Active 1.2.0 | Sample `__main__.py` matches the package |
