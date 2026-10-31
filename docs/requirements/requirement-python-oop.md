**file**: docs/requirements/requirement-python-oop.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-oop`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

One class in each module. The class that owns a job is the only place that job is written.

### 1.1 Human-facing

**In one sentence:** Menu drawing, grok work, and the about page are three classes, not one long function.

| You | Another role | Not this |
|-----|--------------|----------|
| Change a menu row | Edit `MenuPainter` | A class named `Join` |

## 2. Core Rules

1. `Cli` owns parse and dispatch. `Tui` owns the screen. `MenuPainter` owns rows and the frame. `MenuModel` owns keystrokes. `MenuSession` owns the loop. `MenuLanguage` owns the saved language.
2. `GrokDomain` owns setup, session, backup, sync, crontab, and sudoer JSON.
3. `Host` owns this-login-only detect. `Storage` owns cache tiers. The tier law is `requirement-python-cli-storage`. `Output` owns human lines and JSON. `ShellStartup` owns rc files. `SelfManage` owns pip. `SystemLog` owns log files. `AboutPage` and `CheckSystem` own the about page.
4. **MUST NOT** add class `Join`.
5. `def main` constructs `ChronicleLogger`. Other modules **MUST NOT** construct it at import time.
6. `main` **MUST** write `Cli(logger)` at the site. `Cli.run` **MUST NOT** take a logger argument.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | `GrokDomain` is the only class in `grok_domain.py` |
| AC-2 | There is no `Join` class |
| AC-3 | `main` writes `Cli(logger)` and calls `run(argv)` |

## Terminologies

### Avoid-factory-create-class

**Definition:** Avoid-factory-create-class is the rule that an object is created by writing `ClassName(...)` at the site that needs that object. A factory is a function or a method whose job is to instantiate a class. The class can be created without that factory.

**Human daily-life explanation:** You pick up the thing itself. You do not hand the job to a clerk whose only task is to pick it up and hand it back. Writing `Cli(logger)` in `main` is that step.

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-22 | Active 1.2.0 | Construct is `Cli(logger)` then `run(argv)` |
