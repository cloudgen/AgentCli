**file**: docs/requirements/requirement-runtime-prerequisites.md
**Status**: Active (Version 1.2.0)
**Area**: runtime
**Key**: `requirement-runtime-prerequisites`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

What must be present before AgentCli can run, and what it refuses to install for you.

### 1.1 Human-facing

**In one sentence:** Pip installs ChronicleLogger with AgentCli. `setup` needs curl when it downloads grok. The program does not install packages as root.

| You | Another role | Not this |
|-----|--------------|----------|
| Have Python and ChronicleLogger | curl, scp, and crontab when you use those verbs | An automatic `sudo apt` or `pkg` from this package |

## 2. Core Rules

1. ChronicleLogger **MUST** be at least 1.3.1. A missing import **MUST** name the pip install line and return 1.
2. `setup` **MUST** require `curl` on PATH when it downloads, unless a test runner supplies the bytes.
3. `sync-auth-from-remote` **MUST** require `scp`. `sync-auth-to-remote` **MUST** require `scp` and `ssh`. Tests may set `AGENT_CLI_SCP` and `AGENT_CLI_SSH`.
4. `add-crontab` **MUST** require a crontab program. Tests may set `AGENT_CLI_CRONTAB`.
5. The package **MUST NOT** run `sudo` to install itself, **MUST NOT** run `apt`, and **MUST NOT** run Termux `pkg` by itself.
6. No FFmpeg prerequisite. This product does not join media.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | Missing ChronicleLogger returns 1 with the pip line |
| AC-2 | setup source does not execute `install.sh` |
