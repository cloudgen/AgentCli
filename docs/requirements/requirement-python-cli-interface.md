**file**: docs/requirements/requirement-python-cli-interface.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-cli-interface`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the command-line entry, empty-argv behavior, and typed verbs for the AgentCli Python package.

The text-menu picture is `requirement-python-tui`. Domain verbs are `requirement-domain-grok-cli`. The about page is `requirement-python-about`. The logger construct is `requirement-python-cli-logging`.

### 1.1 Human-facing

**In one sentence:** `agent-cli` with no words opens the text menu on a terminal, and with no terminal it prints help and returns 0.

| You | Another role | Not this |
|-----|--------------|----------|
| Type `agent-cli`, `agent-cli hello`, or a domain verb | The menu draws the same verbs | `join`, `list-videos`, `restore`, or a vendor `install.sh` |

**Includes:** console script, module entry, typed verbs, empty-argv menu or help.  
**Excludes:** a second shell installer as the package install story.

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on a terminal | The front board opens. Pip does not run. grok is not downloaded | `agent-cli` |
| Start with no terminal | Help prints and the process returns 0 | `agent-cli` |
| See the welcome line | One line, no menu | `agent-cli hello` |
| Do the domain work | The same verb the menu runs | `agent-cli setup` |

## 2. Core Rules

1. Console script **MUST** be `agent-cli`. Module entry **MUST** be `python -m AgentCli`. Both call `cli.main`.
2. `def main` **MUST** construct `ChronicleLogger(...)` before `Cli`.
3. On a terminal, empty argv **MUST** open the front board and **MUST NOT** run pip and **MUST NOT** download grok.
4. With no terminal and no verb, the program **MUST** print help and return 0.
5. `--json` with no verb **MUST** print JSON help and **MUST NOT** open the menu.
6. Typed verbs **MUST** be: `help`, `version`, `about`, `hello`, `menu`, `main`, `ensure`, `install`, `uninstall`, `rc-test`, `where-is-me`, `self-install`, `version-check`, `self-update`, `self-uninstall`, `setup`, `update-grok`, `reinstall`, `run`, `check-session`, `backup`, `sync-auth`, `sync-auth-from-remote`, `sync-auth-to-remote`, `add-crontab`, `print-sudoers`, `print-sudoers-install-script`, `remove-project-sudoers`, `generate-sudoer-request`, `submit-sudoer-request`.
7. `language` and `Exit` are menu-only. **MUST NOT** add `join`, `list-videos`, or `restore`.
8. `hello` **MUST** print `Welcome to AgentCli <version>.` and **MUST NOT** draw the menu.
9. `self-uninstall` on the command line **MUST** require `--force`.
10. `run` **MUST** refuse `--json`. It **MUST** pass `--no-auto-update` unless the operator already passed that flag.
11. `update-grok` **MUST** fail closed when grok is not installed, with next step `agent-cli setup`.
12. Unknown verbs **MUST** exit non-zero and name the unknown token.
13. Domain behavior for the grok verbs stays on `requirement-domain-grok-cli`, `requirement-grok-setup`, `requirement-grok-auth-backup`, and `requirement-grok-crontab`. This file names the entry. It does not restate those procedures.
14. `main` **MUST** accept `argv`, `basedir`, and `logdir`. It **MUST** set `is_quiet` from `Cli.opens_text_screen(argv)`, construct `Cli(logger)`, and call `run(argv)`.
15. `--quiet` or `--debug` with no verb on a terminal **MUST** open the menu. With no terminal, that same argv **MUST** print help and return 0. `--json` with no verb stays JSON help.

## Sample code

`cli.py` writes this entry. `opens_text_screen` is the quiet decision. The parser stays inside `Cli.run`.

```python
def main(argv=None, basedir="", logdir=""):
    """This function instantiates ChronicleLogger. The statement below is the construct."""
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        sys.stderr.write(
            'ChronicleLogger is required. Next step: python -m pip install "ChronicleLogger>=1.3.1"\n'
        )
        return 1

    from AgentCli import __version__

    screen = Cli.opens_text_screen(argv)
    logger = ChronicleLogger(
        logname=Cli.APP_NAME,
        is_quiet=screen,
        basedir=basedir,
        logdir=logdir,
    )
    appname = logger.logName()
    resolved_base = logger.baseDir()
    logger.logDir()
    if logger.isDebug():
        logger.log_message(
            "{0} v{1} ({2})".format(appname, __version__, __file__),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(resolved_base),
            level="DEBUG",
            component="main",
        )
        logger.log_message("debug mode", component="main")
    app = Cli(logger)
    return app.run(argv)
```

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | Empty argv on a terminal opens the menu and does not run pip |
| AC-2 | Empty argv with no terminal prints help and returns 0 |
| AC-3 | `hello` prints the welcome line and does not draw the menu |
| AC-4 | `join`, `list-videos`, and `restore` are unknown |
| AC-5 | `run` inserts `--no-auto-update` |
| AC-6 | `main(argv, basedir, logdir)` uses `opens_text_screen` as `is_quiet` and calls `Cli(logger).run(argv)` |

## Terminologies

### Major TUI entry point

**Definition:** Major TUI entry point is the rule that the major entry of a claimed text screen is interactive mode with no positional command token. Flags that are not a command (`--debug`, `--quiet`, `--force` with no command, and peers of that kind) stay on that entry. `--json` with no command stays JSON help, not the text screen. Creating or keeping a text screen does not attach every CLI verb to that screen. A verb opens the screen only when a specialized requirement explicitly names that verb as using the text screen.

**Human daily-life explanation:** A major TUI entry point is the walk-up board at a shop. You see that board when you name no dish. Naming a dish sends you to a different counter. A light switch that is not a dish (`--debug` and the same kind of flag) still leaves you at the walk-up board. Asking for the paper list with no dish (`--json` alone) is the paper list, not the board.

### Chronicle logger

**Definition:** Chronicle logger is the one process status logger, library ChronicleLogger, that `def main` instantiates by writing the statement `ChronicleLogger(...)` inside that function, before any product object. It records the resolved application name, the version, this file's path, `ChronicleLogger.class_version()`, the base folder, and a line whose message is `debug mode`, and those identity lines run only inside `isDebug()`.

**Human daily-life explanation:** A chronicle logger is the one kitchen notebook. When a new appliance arrives you write that it arrived. You do not start a second notebook. The guests in the dining room do not hear that line. The book still has it.

### Avoid-factory-create-class

**Definition:** Avoid-factory-create-class is the rule that an object is created by writing `ClassName(...)` at the site that needs that object. A factory is a function or a method whose job is to instantiate a class. The class can be created without that factory.

**Human daily-life explanation:** You pick up the thing itself. You do not hand the job to a clerk whose only task is to pick it up and hand it back. Writing `Cli(logger)` is that step.

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-22 | Active 1.2.0 | Sample `main` matches `cli.py`. `opens_text_screen` is `is_quiet`. Overlay `--quiet` stays on the menu |
| 2026-10-22 | Active 1.2.0 | Python entry for AgentCli |
