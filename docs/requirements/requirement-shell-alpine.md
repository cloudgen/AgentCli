**file**: docs/requirements/requirement-shell-alpine.md  
**Status**: Active (Version 1.0.1)  
**Area**: shell  
**Key**: `requirement-shell-alpine`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the **topic-owner** for **ash PATH** on grok-cli. Alpine’s login shell is ash (`$0` is `-ash`). A user-bin install must put the shared `USER_BIN` line on `~/.profile`, which that login actually reads. The bash-only block that sources `~/.bashrc` when `BASH_VERSION` is set does not do that.

It owns **ash profile path-ensure**: when this run’s command name is ash, append one shared `export PATH="$USER_BIN:$PATH"` line to `.profile` (`PROFILE`). Alpine’s `/bin/sh` is ash, so `curl | sh` (`$0` is `sh`) on a host with `/etc/alpine-release` is the same case. Bash PATH, Fish PATH, zsh `.zshenv`, and the create-if-missing bash source block stay on their owners.

**Scope:** When to treat this run as ash; the PATH line on `.profile`; create / append / no-op; `GROK_CLI_ARGV0` and `GROK_CLI_ALPINE_RELEASE` for tests; `rc-test --file ash`.  
**Out of scope (cited, not re-owned):** Bash / Fish / zsh rc (`requirement-shell-path-and-shell-support` · `requirement-shell-zshenv`); placing the binary; peer grok’s `~/.grok/bin` block.

**Not claimed:** `/etc/profile`; changing the login’s shell; a separate `~/.ashrc` (ash does not read it unless `ENV` is set).

### 1.1 Human-facing

**In one sentence:** On an ash login, including Alpine, install writes “also look in `~/.local/bin`” into the login note (`.profile`) so the next ash login can run `grok-cli` by name.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person whose shell is ash | `echo $0` prints `-ash` |
| The other role | Tests that set the invoking name without being ash | `GROK_CLI_ARGV0=-ash` |
| Not this file | The bash desk note; copying the program | `requirement-shell-path-and-shell-support` |

| Includes | Excludes |
|----------|----------|
| PATH line on `.profile` when `$0` is ash (leading `-` ignored), or when `$0` is `sh` and Alpine’s release file exists | Writing that PATH line for a bash-only run; replacing the whole `.profile`; inventing `~/.ashrc` |
| Keep the bash “source `.bashrc`” block already on `.profile` | Deleting `.profile` on uninstall |

| Surface | What you open | What for |
|---------|---------------|----------|
| `grok-cli install` or the curl one-liner | Command | Companion writes `.profile` when this run is ash |
| `grok-cli rc-test --file ash` | Test-purpose command | Create / modify / no-op in a temp folder |
| `~/.profile` | Login note | Ash reads this; bash reads it only as a login shell |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install on Alpine ash | The program sees ash (or Alpine `sh`) and adds the PATH line to `.profile`. A new login can run `grok-cli`. The same shell still needs `source ~/.profile` or a new login. | `curl -fsSL …/src/grok-cli \| sh` |
| Install on bash | `.profile` may be created so bash login sources `.bashrc`. The ash PATH line is not added. | `grok-cli install` |

## 2. Core Rules

1. **Detect ash from the invoking name.** Take `$0` unless `GROK_CLI_ARGV0` is set (tests). Strip one leading `-`, then the basename. If that name is `ash`, this run **is** ash (`-ash`, `ash`, `/bin/ash`).  
2. **Alpine `sh` is ash.** If that name is `sh` and the alpine-release file exists, this run **is** ash. Default file: `/etc/alpine-release`. Tests may point `GROK_CLI_ALPINE_RELEASE` at another file. An empty override or a missing file means “not Alpine.” A `sh` run without that file **is not** ash.  
3. **Missing `.profile` is one step** (`path_ensure_profile`), shared with bash, zsh, and fish.  
   - **Not ash** (bash, zsh, fish, and any other non-ash run): **generate** `.profile` that sources `~/.bashrc` when `BASH_VERSION` is set. **MUST NOT** put the `USER_BIN` PATH export in that new file.  
   - **Ash / Alpine:** **generate** that same file, then **in the same step** add `export PATH="${USER_BIN}:$PATH"` (default `USER_BIN` is `${HOME}/.local/bin`).  
4. **Existing `.profile`:** **MUST NOT** replace it. **Ash / Alpine** **MUST** modify it by appending the PATH line when that line is absent. Bash, zsh, and fish **MUST** leave an existing file unchanged.  
5. **Keep** the bash source-bashrc block (`requirement-shell-path-and-shell-support`). The ash PATH line is additional. A non-ash run **MUST NOT** append that PATH export.  
6. Idempotent: a second install does not duplicate the line.  
7. The restart hint **MUST** name `.profile` when the ash line was written, so the operator is not told only to source `.bashrc`.  
8. Uninstall may remove this product’s `# Added by ${APP_NAME} installer` sticker and, when `USER_BIN` is empty, the exact PATH line. **MUST NOT** delete `.profile` or the source-bashrc block.  
9. `rc-test --file ash` is Type 0 test-purpose. It **MUST** force the ash path against `--root` and **MUST NOT** write this login’s real `${HOME}/.profile`. Dual mention: `requirement-shell-cli-interface`. Sample: `grok-cli rc-test --root "$tmpdir" --file ash --case create`.

### 2.1 Implementation Notes (this project)

| Item | Value |
|------|--------|
| Product | grok-cli |
| Ship unit | `src/grok-cli` |
| Helpers | `path_invoking_is_ash`, `path_add_profile_ash` (called from `path_add_shell` after `path_ensure_profile`) |
| PATH line | `export PATH="${HOME}/.local/bin:$PATH"` |
| Profile | `${HOME}/.profile` (`PROFILE`) |
| Ash names | basename of `$0` or `GROK_CLI_ARGV0`, one leading `-` removed, equals `ash` |
| Alpine pipe | `$0` basename `sh` and `/etc/alpine-release` exists |
| Message | `→ Added ${USER_BIN} to PATH for ash (.profile)` |

## Under command line for normal user only

When grok-cli runs on Termux, Git Bash, Windows cmd, or the same class (this login only — no root, no dedicated system account):

**This requirement:** ash profile PATH is this-login file writing. It does not use sudo and does not create a dedicated system user. Git Bash and Windows cmd are not ash; they do not get this `.profile` PATH line unless `$0` is ash.

| Do | Do not |
|----|--------|
| Write this login’s `.profile` when the invoking name is ash | `sudo` to edit another login’s profile |
| Alpine `sh` counts as ash | Treat every `sh` on every host as ash |

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution** (Principle 1): A missing `.profile` write fails with a next step. A non-ash run does not invent an ash PATH line.  
- **Intentional** (Principle 2): Ash is detected from the invoking name, not from a guessed distro list, except the Alpine fact that `sh` is ash.  
- **Anti-fragile** (Principle 3): An existing `.profile` is appended, not replaced. The bash source block stays.  
- **Over-protect** (Principle 4): Tests inject the invoking name and the release file so the suite never needs a real Alpine host. `rc-test` cannot touch the real home profile.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Leave Alpine ash with only the bash `BASH_VERSION` source block and no `USER_BIN` export on `.profile`.  
2. Treat every `sh` as ash. Only `ash` (leading `-` allowed) or Alpine `sh` (release file present).  
3. Replace `.profile` wholesale, delete it on uninstall, or drop the source-bashrc block.  
4. Write the ash PATH line when this run is not ash.  
5. Tell an ash operator to source only `.bashrc` after the ash line was written.

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Missing `.profile` and `$0` `-ash`: generate the source-bashrc block and add the PATH line in that same step (TP-LC-37). Existing `.profile` and ash: modify by appending PATH; keep the old body (TP-LC-42) |
| AC-2 | `$0` `sh` without an alpine-release file does not add that PATH line (TP-LC-38) |
| AC-3 | `$0` `sh` with an alpine-release file adds the PATH line (TP-LC-39) |
| AC-4 | `rc-test --file ash` writes the fixture profile only (TP-LC-40) |
| AC-5 | Missing `.profile` and invoking name bash, zsh, or fish: generate the source-bashrc file and do not add the PATH export (TP-LC-41) |

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `requirement-shell-path-and-shell-support.md` | Orchestrator; bash source-bashrc block; not the ash PATH line |
| `requirement-shell-cli-interface.md` | `rc-test --file ash` dual mention |
| `requirement-shell-zshenv.md` | Zsh peer; does not own `.profile` |
| `requirement-shell-startup-files.md` | Family matrix names this file’s missing-`.profile` row; ash PATH stays here |
| `src/grok-cli` | `path_invoking_is_ash`, `path_add_profile_ash` |

## Terminologies

### Shell startup files

**Definition:** Shell startup files are the family a shell reads at login or session start. On Alpine ash the file is `.profile`.

**Human daily-life explanation:** Ash hangs the door note and writes the drawer line on it. Bash hangs the same kind of note without that line.

**Daily-life example:** A missing `.profile` on Alpine gets both the source note and `~/.local/bin`. A missing `.profile` on bash gets the source note only.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-09-22 | Active (1.0.0) | Ash `$0` (and Alpine `sh`) writes `USER_BIN` PATH into `.profile` |
| 2026-10-12 | Active (1.0.1) | Family matrix **points** at `requirement-shell-startup-files`; ash PATH stays here |

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-LC-37** | `tests/test_local_lifecycle.sh` | have (`-ash` writes PATH on `PROFILE`) |
| **TP-LC-38** | `tests/test_local_lifecycle.sh` | have (`sh` without release file does not) |
| **TP-LC-39** | `tests/test_local_lifecycle.sh` | have (Alpine `sh` does) |
| **TP-LC-40** | `tests/test_local_lifecycle.sh` | have (`rc-test --file ash`) |
| **TP-LC-41** | `tests/test_local_lifecycle.sh` | have (bash / zsh / fish missing `.profile` is generated, no PATH export) |
| **TP-LC-42** | `tests/test_local_lifecycle.sh` | have (existing `.profile` + ash appends PATH, body kept) |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`.

**Last Updated**: 2026-10-12 (1.0.1 — family pointer; ash PATH unchanged)  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
