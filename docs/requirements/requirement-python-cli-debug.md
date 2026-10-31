**file**: docs/requirements/requirement-python-cli-debug.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-cli-debug`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns the debug switch and the four identity lines printed when debug mode is on.

It does not construct ChronicleLogger. `requirement-python-cli-logging` still writes `ChronicleLogger(...)` inside `def main`, still calls `logger.isDebug()` and `log_message`, and still requires the environment to be set before that constructor. This file is not a routed verb.

### 1.1 Human-facing

**In one sentence:** When `DEBUG` is already on, a run that does not open the text menu shows four status lines. When `DEBUG` is off, those four lines stay off.

| You | Another role | Not this |
|-----|--------------|----------|
| Set `DEBUG` before `agent-cli` | `logger.isDebug()` decides once | A `--debug` flag as this switch. That flag is the empty-argv menu overlay on `requirement-python-cli-interface` |

**Includes:** the environment switch and the four messages.  
**Excludes:** constructing ChronicleLogger, the `instantiated` line, temp / publish / discard lines, and thread lines.

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Ask for the debug lines | Before the process starts, `DEBUG` or `debug` is `1`, `true`, or `show`. `version` does not open the text screen, so the four lines can show on the console | `DEBUG=1 agent-cli version` |
| Leave debug off | Those four lines are not displayed | `agent-cli version` |

## 2. Core Rules

1. Debug status is an environment fact already set before `ChronicleLogger(...)`.
2. Accepted values are case-insensitive `show`, `true`, and `1`, read from `DEBUG`, then from `debug` when `DEBUG` is empty. That read belongs to `logger.isDebug()`. Product code **MUST NOT** read the environment again.
3. There is no `--debug` flag for this catalog. `--debug` with no verb stays the menu overlay on `requirement-python-cli-interface`.
4. The four lines below are the only debug identity messages. They run only inside `if logger.isDebug():`, before the argument parser, in this order. Component is `main`.
5. A library rotation header is not an extra product message. `ChronicleLogger.class_version()` supplies the library version. Product code **MUST NOT** type that version by hand.
6. `instantiated`, temp write, publish, discard, and any later thread line stay outside `if logger.isDebug():`.
7. A text-screen run keeps these four lines off the console. The daily file still receives them. `is_quiet` from `Cli.opens_text_screen` is the screen rule on `requirement-python-cli-logging`. It is not a second catalog.
8. **`TP-DBG-01`**, **`TP-DBG-02`**, and **`TP-DBG-03`** assert this catalog in `tests/test_debug.py`. They are **have**.

| Order | Message | Level | Component |
|-------|---------|-------|-----------|
| 1 | `{logName} v{package version} ({this file})` | default of `log_message` | `main` |
| 2 | `Using {ChronicleLogger.class_version()}` | default of `log_message` | `main` |
| 3 | `Base {baseDir}` | `DEBUG` | `main` |
| 4 | `debug mode` | default of `log_message` | `main` |

`logName`, `baseDir`, and `class_version()` are the values the logger instance already resolved. The package version is `__version__`.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | `main` calls `isDebug()` and does not read `DEBUG` itself |
| AC-2 | The four messages and only those four sit inside that gate, in the order above |
| AC-3 | `requirement-python-cli-logging` names this key and does not copy this table |

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-31 | Active 1.0.0 | Catalog from `cli.py` `main`. Switch is the environment, not `--debug` |
