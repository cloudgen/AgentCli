**file**: docs/requirements/requirement-python-cli-storage.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-cli-storage`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Cache and persistence for the Python package. Class `Storage` is the only resolver.

The POSIX reference for the same tier shapes is `requirement-shell-cli-storage`. This file does not copy that shell procedure. Deposit of `auth.*` into the shared host store stays on `requirement-grok-auth-backup`.

### 1.1 Human-facing

**In one sentence:** Scratch files go in a per-login per-process cache folder. Durable notes for this login go under the home persistence directory.

| You | Another role | Not this |
|-----|--------------|----------|
| Let `agent-cli about` show the cache and persistence lines | `Storage` picks the first writable tier | The shared host deposit, or the install directory |

**Includes:** tier shapes, silent fallback, about fields, scratch files.  
**Excludes:** chown of the deposit, pip install paths, and a ram-drive project tree.

## 2. Core Rules

1. `Storage` in `storage.py` is the only cache and persistence resolver. Other modules **MUST** call that class. **MUST NOT** add module-level path helpers.
2. The leaf name uses the package app name `agent-cli`, this login, and this process id. Home leaves omit the login segment. **MUST NOT** hardcode a person's login.
3. A missed tier is silent. An error is allowed only when every tier for this host failed.
4. Leaf mode is `0700`. Shared parents `/dev/shm/cache` and `/tmp/cache` are created `01777` when this process creates them.
5. Persistence is `${HOME}/.local/agent-cli`, mode `0700`. It **MUST NOT** be the install bin directory.
6. `mktemp` **MUST** refuse a suffix that contains `$$`. The scratch file is created with `tempfile` under the chosen cache root.
7. `about` **MUST** show cache used, preferred, first fallback, second fallback when this host has one, and persistence. A skipped tier prints nothing.
8. The preferred cache is **not** `/dev/shm/agent-cli` and **not** a per-login ram-drive project folder.

| Host | Preferred | 1st fallback | 2nd fallback |
|------|-----------|--------------|--------------|
| Linux, including Termux | `/dev/shm/cache/cache-agent-cli-${login}-${pid}` | `/tmp/cache/cache-agent-cli-${login}-${pid}` | `${HOME}/.cache/cache-agent-cli-${pid}` |
| Git Bash (`MSYSTEM`, or a `MINGW` / `MSYS` system name) | `/tmp/cache/cache-agent-cli-${login}-${pid}` | `${HOME}/AppData/Local/Temp/cache-agent-cli-${pid}` | none |
| Mac (`Darwin`) | `/tmp/cache/cache-agent-cli-${login}-${pid}` | `${HOME}/Library/Caches/cache-agent-cli-${pid}` | `${HOME}/cache/cache-agent-cli-${pid}` |

| Class | Method |
|-------|--------|
| Preferred cache | `preferred_dir` |
| 1st fallback | `fallback_dir` |
| 2nd fallback | `fallback2_dir` (empty on Git Bash) |
| Chosen cache | `resolve` |
| Persistence path | `persistent_dir` |
| Persistence create | `resolve_persistent` |
| Scratch file | `mktemp` |

Host kind **MAY** be forced with `AGENT_CLI_CACHE_HOST` set to `linux`, `gitbash`, or `mac`. `AGENT_CLI_CACHE_SKIP=preferred` skips the preferred tier. Those two names are test controls. They are not a second resolver.

| Forbidden as this package's storage | Why |
|-------------------------------------|-----|
| `${HOME}/.local/bin` | Install directory |
| The shared host deposit named by `requirement-grok-auth-backup` | Privilege law, not scratch |
| `/dev/shm/agent-cli` | Looks like a ram-drive project folder |

On Termux the chosen cache **MAY** be `noexec`. Scratch stays scratch. Downloaded binaries are not executed from the cache root.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | `storage.py` defines class `Storage` and no second resolver |
| AC-2 | Linux preferred path contains `/dev/shm/cache/cache-agent-cli-` |
| AC-3 | `about` prints the cache used line and the persistence line |

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-31 | Active 1.0.0 | Language peer of the shell storage key. Law is class `Storage` |
