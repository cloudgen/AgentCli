**file**: docs/requirements/requirement-python-idempotency.md
**Status**: Active (Version 1.0.0)
**Area**: python
**Key**: `requirement-python-idempotency`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Re-run safety for the Python package. A second run of an ensure-style operation reaches the same desired outcome. Logs and timestamps may differ.

The POSIX reference matrix, including dated archive numbering, stays on `requirement-shell-idempotency`. This file does not copy that matrix. Python `backup` follows `requirement-grok-auth-backup`: the same `auth.*` basenames are replaced. It does not allocate a dated tar slot.

### 1.1 Human-facing

**In one sentence:** Running backup again replaces the same auth names. Running an install that is already in place succeeds.

| You | Another role | Not this |
|-----|--------------|----------|
| Run `agent-cli backup` twice | The same basenames in the shared host store are replaced | A second dated archive, or a failure that says the files already exist |

## 2. Core Rules

1. A state-changing ensure **MUST** detect whether the desired state already holds, skip unsafe duplicate work, and succeed when the state is already achieved.
2. **MUST NOT** fail solely because the desired file or package is already present.
3. `backup` **MUST** overwrite the same `auth.*` basenames. The session gate, modes, and ownership stay on `requirement-grok-auth-backup`. This file does not restate that procedure.
4. `sync-auth` and `sync-auth-from-remote` **MUST** succeed without copying when the session is already valid. That skip stays on `requirement-grok-auth-backup`.
5. `self-install`, `self-update`, and `self-uninstall` **MUST** be safe to repeat. Already installed is success. `self-uninstall` on the command line still requires `--force`, as `requirement-python-cli-interface` states.
6. `add-crontab` **MUST NOT** append a second copy of the same command line. The crontab text stays on `requirement-grok-crontab`.
7. Scratch files **MUST** go through `Storage.mktemp`. **MUST NOT** reuse a predictable `$$` template as the file name. Cache leaves themselves stay per process on `requirement-python-cli-storage`.
8. Read-only verbs (`help`, `version`, `about`, `hello`, `where-is-me`) **MUST** stay safe to repeat.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | A second `backup` replaces the same `auth.*` basenames and does not create a dated tar name |
| AC-2 | A second `self-install` when the console script is already present returns success |
| AC-3 | `Storage.mktemp` refuses a suffix that contains `$$` |

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-31 | Active 1.0.0 | Language peer of the shell idempotency key. Python backup overwrites the same names |
