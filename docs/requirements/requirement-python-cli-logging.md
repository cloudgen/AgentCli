**file**: docs/requirements/requirement-python-cli-logging.md
**Status**: Active (Version 1.3.0)
**Area**: python
**Key**: `requirement-python-cli-logging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

One ChronicleLogger instance, constructed in `def main`.

### 1.1 Human-facing

**In one sentence:** The program writes its log through ChronicleLogger, a caught exception is written there before it is replaced, and the text menu does not print that log on the console.

| You | Another role | Not this |
|-----|--------------|----------|
| Run `agent-cli` | `main` passes `is_quiet=True` when the screen will open | A second logger constructed at import time |
| The menu fails | The daily file already has the exception type, its text, and the traceback | A generic screen sentence with the exception dropped |

## 2. Core Rules

1. `def main` **MUST** contain the text `ChronicleLogger(`.
2. When the run opens the text screen, `is_quiet` **MUST** be true so directory-created lines stay off the console.
3. Other modules **MUST NOT** construct ChronicleLogger at import.
4. A missing ChronicleLogger **MUST** exit 1 and name `python -m pip install "ChronicleLogger>=1.3.1"`.
5. system-log views, clears, and shows that log folder. It does not invent a second log library.
6. `is_quiet` **MUST** be the return value of `Cli.opens_text_screen`. Identity lines **MUST** run only inside `isDebug()`. The switch and the message list are `requirement-python-cli-debug`. This file does not copy that list.
7. The environment is already set before `ChronicleLogger(...)`. Product code asks `logger.isDebug()` and then `log_message`. It does not read the environment again.
8. When that logger exists, a caught exception **MUST** be written with `log_message` at level `ERROR` **before** the handler returns, continues, uses `pass`, or replaces the exception with another sentence. The message **MUST** contain the exception type name, `str` of the exception, and the traceback text. A bare `except:` or `except Exception:` that does not bind the exception **MUST NOT** be the handler that drops it.
9. The operator sentence may stay short. The daily file **MUST** already hold rule 8. The menu sentence `The text menu could not open on this terminal.` is allowed only after that line. The console mirror stays quiet on the text screen. The file still receives the line.
10. An operator error that already has the logger (`Cli.report_error`) **MUST** write the same fact with `log_message` at level `ERROR` before the stderr `ERROR:` lines. A caller that holds the logger and then reports an error **MUST** write that line first. The missing-library path has no logger yet: it **MUST** stay the stderr install line `python -m pip install "ChronicleLogger>=1.3.1"`.
11. `KeyboardInterrupt` on a long child keeps its interrupt line. That line is the record, at `WARNING`. A handler that catches `KeyboardInterrupt` and returns with no log line **MUST** write one first. Every other caught exception is `ERROR`.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | `cli.py` `main` writes `ChronicleLogger(` |
| AC-2 | Import of `cli` does not require the constructor to have run |
| AC-3 | `is_quiet` is `opens_text_screen(argv)` |
| AC-4 | A caught exception is a `log_message` `ERROR` that names the type, the text, and the traceback, written before the handler returns or substitutes a generic sentence |
| AC-5 | `report_error` writes that `ERROR` log line when the logger exists |

## Terminologies

### Chronicle logger

**Definition:** Chronicle logger is the one process status logger, library ChronicleLogger, that `def main` instantiates by writing the statement `ChronicleLogger(...)` inside that function, before any product object. Debug identity lines run only inside `isDebug()`, and `log_message` carries them. The words of those lines are `requirement-python-cli-debug`. The environment is already set before the constructor.

**Human daily-life explanation:** A chronicle logger is the one kitchen notebook. When a new appliance arrives you write that it arrived. You do not start a second notebook. The guests in the dining room do not hear that line. The book still has it.

### Logger default quiet unless verbose

**Definition:** Logger-default-quiet-unless-verbose is the console-mirror rule for the one process status logger. The daily file still receives every line. This product sets `is_quiet` from `Cli.opens_text_screen`, so a text screen stays quiet. A run that does not open the screen leaves the mirror on. `--json` does not open the screen and does not draw the menu.

**Human daily-life explanation:** You still write “kettle arrived” in the book. You do not read that line out loud over the wall chart. When you are only talking at the counter, the notebook line can be heard.

### Exception record

**Definition:** An exception record is the `log_message` line at level `ERROR` written on the one ChronicleLogger before a handler returns, continues, passes, or replaces that exception. The message contains the exception type name, the exception text, and the traceback text. A short operator sentence may follow. It does not replace this line. `KeyboardInterrupt` on a long child may use the interrupt line at `WARNING` instead. The missing-library path has no logger and stays on stderr.

**Human daily-life explanation:** The pot boils over. You write what boiled, what it said, and the path you took, in the kitchen book, before you tell the dining room “the meal could not be served.” You do not throw the pot away and leave the book blank.

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-22 | Active 1.2.0 | Quiet boolean is `opens_text_screen` |
| 2026-10-31 | Active 1.2.1 | Names `requirement-python-cli-debug`. The message list stays on that file |
| 2026-11-01 | Active 1.3.0 | A caught exception is an `ERROR` log line (type, text, traceback) before a generic sentence. `report_error` logs when the logger exists |
