**file**: docs/requirements/requirement-python-coding-style.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-coding-style`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Python style for AgentCli. Fail closed. Do not hide an error.

### 1.1 Human-facing

**In one sentence:** When a step cannot finish, the program says what happened and the next command.

| You | Another role | Not this |
|-----|--------------|----------|
| Read an ERROR line and a Next line | Domain procedures stay in their requirement files | A media publish path |

## 2. Core Rules

1. Expected failures **MUST** return a non-zero status and an operator-readable message with a next step.
2. **MUST NOT** claim success after a failed copy, download, or crontab install.
3. Scratch files **MUST** go through `Storage.mktemp`. A `$$` template **MUST** be refused.
4. A missed cache tier **MUST** be silent. The next tier is tried.
5. **MUST NOT** pipe a downloaded script into a shell. `setup` **MUST NOT** execute a vendor `install.sh`.
6. Source **MUST NOT** contain unfinished markers (`TODO`, `FIXME`, `NotImplementedError` as delivery).
7. Product paths come from `Storage`, `Host`, and `GrokDomain` attributes. Do not scatter a second deposit path.
8. `def main` **MUST** write `ChronicleLogger(...)` and `Cli(logger)`. It **MUST NOT** publish a file. A missing ChronicleLogger **MUST** name `python -m pip install "ChronicleLogger>=1.3.1"` on stderr and return 1.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | `grok_domain.py` does not contain `install.sh` |
| AC-2 | `mktemp` refuses a `$$` template |
| AC-3 | `main` constructs `Cli(logger)` and does not call `shutil.move` |

## Terminologies

### Avoid-factory-create-class

**Definition:** Avoid-factory-create-class is the rule that an object is created by writing `ClassName(...)` at the site that needs that object. A factory is a function or a method whose job is to instantiate a class. The class can be created without that factory.

**Human daily-life explanation:** You pick up the thing itself. You do not hand the job to a clerk whose only task is to pick it up and hand it back.

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-22 | Active 1.2.0 | Entry construct matches `cli.py`. Publish stays out of `main` |
