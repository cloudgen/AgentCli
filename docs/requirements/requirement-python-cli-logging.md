**file**: docs/requirements/requirement-python-cli-logging.md
**Status**: Active (Version 1.2.1)
**Area**: python
**Key**: `requirement-python-cli-logging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

One ChronicleLogger instance, constructed in `def main`.

### 1.1 Human-facing

**In one sentence:** The program writes its log through ChronicleLogger, and the text menu does not print that log on the console.

| You | Another role | Not this |
|-----|--------------|----------|
| Run `agent-cli` | `main` passes `is_quiet=True` when the screen will open | A second logger constructed at import time |

## 2. Core Rules

1. `def main` **MUST** contain the text `ChronicleLogger(`.
2. When the run opens the text screen, `is_quiet` **MUST** be true so directory-created lines stay off the console.
3. Other modules **MUST NOT** construct ChronicleLogger at import.
4. A missing ChronicleLogger **MUST** exit 1 and name `python -m pip install "ChronicleLogger>=1.3.1"`.
5. system-log views, clears, and shows that log folder. It does not invent a second log library.
6. `is_quiet` **MUST** be the return value of `Cli.opens_text_screen`. Identity lines **MUST** run only inside `isDebug()`. The switch and the message list are `requirement-python-cli-debug`. This file does not copy that list.
7. The environment is already set before `ChronicleLogger(...)`. Product code asks `logger.isDebug()` and then `log_message`. It does not read the environment again.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | `cli.py` `main` writes `ChronicleLogger(` |
| AC-2 | Import of `cli` does not require the constructor to have run |
| AC-3 | `is_quiet` is `opens_text_screen(argv)` |

## Terminologies

### Chronicle logger

**Definition:** Chronicle logger is the one process status logger, library ChronicleLogger, that `def main` instantiates by writing the statement `ChronicleLogger(...)` inside that function, before any product object. Debug identity lines run only inside `isDebug()`, and `log_message` carries them. The words of those lines are `requirement-python-cli-debug`. The environment is already set before the constructor.

**Human daily-life explanation:** A chronicle logger is the one kitchen notebook. When a new appliance arrives you write that it arrived. You do not start a second notebook. The guests in the dining room do not hear that line. The book still has it.

### Logger default quiet unless verbose

**Definition:** Logger-default-quiet-unless-verbose is the console-mirror rule for the one process status logger. The daily file still receives every line. This product sets `is_quiet` from `Cli.opens_text_screen`, so a text screen stays quiet. A run that does not open the screen leaves the mirror on. `--json` does not open the screen and does not draw the menu.

**Human daily-life explanation:** You still write “kettle arrived” in the book. You do not read that line out loud over the wall chart. When you are only talking at the counter, the notebook line can be heard.

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-22 | Active 1.2.0 | Quiet boolean is `opens_text_screen` |
| 2026-10-31 | Active 1.2.1 | Names `requirement-python-cli-debug`. The message list stays on that file |
