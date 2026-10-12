**file**: docs/requirements/requirement-shell-startup-files.md  
**Status**: Active (Version 1.0.0)  
**Area**: shell  
**Key**: `requirement-shell-startup-files`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the **topic-owner** for the **shell startup file** family on grok-cli: which file each operating environment reads, where the shared `USER_BIN` PATH line goes, and what happens when a startup file is missing.

It owns the **missing-file matrix** and **zsh login PATH on `.zprofile`** (`path_add_zprofile`, env `ZPROFILE`, `rc-test --file zprofile`). Bash PATH on `.bashrc`, Fish PATH, and the bash/zsh/fish profile-ensure body stay on `requirement-shell-path-and-shell-support`. Always-on zsh PATH on `.zshenv` stays on `requirement-shell-zshenv`. Ash PATH on an existing or new `.profile` stays on `requirement-shell-alpine`. Peers **point** here for the family; they do not re-own `.zprofile`.

**Scope:** OS and shell matrix; missing `.profile`, missing `.zshenv`, missing `.zprofile`; append-never-replace; `rc-test --file zprofile`; uninstall stickers on `.zprofile`.  
**Out of scope (cited, not re-owned):** Placing the binary; the vendor grok `# >>> grok installer >>>` block (stays on `.bashrc` or `.zshenv` per `requirement-grok-setup`); writing PATH to `.zshrc`.

**Not claimed:** `.zlogin` for PATH; `/etc/zprofile`; Windows User `Path` as a file this product creates; another login’s home.

### 1.1 Human-facing

**In one sentence:** After install, this login’s shell startup files say “also look in `~/.local/bin`,” and a missing note is hung before the next login — a bash kitchen does not invent the zsh notes.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person who ran install | `grok-cli install` or the curl one-liner |
| The other role | A test that points the write at a throw-away folder | `grok-cli rc-test --root "$tmpdir" --file zprofile --case create` |
| Not this file | The always-on zsh line alone; the ash-only profile line; copying the program | `requirement-shell-zshenv` · `requirement-shell-alpine` · `requirement-shell-local-self-management` |

| Includes | Excludes |
|----------|----------|
| One shared PATH line on `.zshenv` and, for zsh login, again on `.zprofile`; hang a missing `.profile`; create a missing `.zshenv` or `.zprofile` only when that shell applies | Writing PATH to `.zshrc`; inventing `.zprofile` because `ZSHENV` was set; replacing an existing note; a Windows User `Path` file |

| Surface | What you open | What for |
|---------|---------------|----------|
| `grok-cli install` | Command | Companion writes the PATH line on the files this shell reads |
| `grok-cli rc-test --file zprofile` | Test-purpose command | Create / modify / no-op against a temp folder |
| `grok-cli help` | Command | Environment lists `ZPROFILE` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install on zsh | The program file goes in `USER_BIN`. The always-on note and the zsh login note each get the PATH line once. A second install does not duplicate it. `.zshrc` is left alone. | `grok-cli install` |
| Prove a missing `.zprofile` without touching this login’s real note | A temp folder is the scratch pad. Real home startup files stay still. | `grok-cli rc-test --root "$tmpdir" --file zprofile --case create` |
| Install on bash only | `.profile` may be created so login sources `.bashrc`. `.zshenv` and `.zprofile` are not invented. | `grok-cli install` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Operating environments

| Environment | Shell | Startup files that matter | PATH file this product writes |
|-------------|-------|---------------------------|-------------------------------|
| Linux login | bash | `.bash_profile` if present, else `.profile`; interactive also `.bashrc` | `.bashrc` (owner: `requirement-shell-path-and-shell-support`) |
| Alpine | ash (`$0` is `ash`, or `sh` when `/etc/alpine-release` exists) | `.profile` | `.profile` (owner: `requirement-shell-alpine`) |
| macOS and Linux | zsh | `.zshenv` always; `.zprofile` on login (after `path_helper`); `.zshrc` interactive | `.zshenv` and `.zprofile`. **Not** `.zshrc` |
| Fish | fish | `config.fish` | `config.fish` |
| Termux | bash | `.bashrc`, `.profile` | `.bashrc` |
| Git Bash / MSYS / Cygwin | bash | `.bashrc`, `.profile` | `.bashrc` |
| Windows cmd / PowerShell | cmd or PowerShell | User `Path` is **not** a file in this family | Do **not** invent `.profile`, `.zshenv`, or `.zprofile` |

Zsh login order is `.zshenv`, then `/etc/zprofile` (`path_helper` on macOS can reorder PATH), then user `.zprofile`, then `.zshrc`. The same `USER_BIN` export on `.zprofile` restores `USER_BIN` at the front after `path_helper`.

### 2.2 Missing shell startup file

| Missing file | What to do |
|--------------|------------|
| `.profile` | **Generate** the login note that sources `.bashrc` for bash, zsh, and fish. Those shells do **not** put the PATH export on that new file. Ash generates the same note **and** adds the shared PATH line. An existing file is kept; only ash appends PATH. Owner of the generate step: `requirement-shell-path-and-shell-support`. Owner of the ash append: `requirement-shell-alpine`. |
| `.zshenv` | **Create** with the shared PATH line when this login’s shell basename is `zsh` **or** `ZSHENV` is set **or** the file already exists. A bash-only login with no override does **not** invent the file. Owner: `requirement-shell-zshenv`. |
| `.zprofile` | **Create** with the shared PATH line when this login’s shell basename is `zsh` **or** `ZPROFILE` is set. Setting `ZSHENV` alone does **not** create it. A bash-only login with no override does **not** invent it. An existing file is kept and the line is appended if absent, even when `$SHELL` is bash. **This file owns this row.** |
| `.zshrc` | **Do not** create it for PATH. `path_add_zshrc` returns without writing. |
| `.bashrc` | **Create** if missing, then append the shared PATH line. Owner: `requirement-shell-path-and-shell-support`. |
| Fish `config.fish` | **Create** the config directory if needed, then append the Fish PATH line. |

**Shared line (every PATH file this product writes):** `export PATH="<USER_BIN>:$PATH"` with `USER_BIN` default `${HOME}/.local/bin`. Comment `# Added by grok-cli installer (<VERSION>)`. Append. Never replace an existing body.

**Create permission for a missing `.zprofile`** (either one):

1. `basename "${SHELL:-}"` is `zsh`.  
2. The caller set `ZPROFILE` before the helper’s default assignment (`[ -n "${ZPROFILE+x}" ]`).

**MUST NOT** treat a set `ZSHENV` as permission to create `.zprofile`.  
**MUST NOT** invent `${HOME}/.zprofile` for a bash-only login when `ZPROFILE` was not set and the file is missing.  
**MUST** append the exact line when the file already exists, even if `$SHELL` is not zsh.

### 2.3 `.zprofile` create / append / no-op

| MUST | MUST NOT |
|------|----------|
| Header on create: `# Zsh login rc created by grok-cli installer (<VERSION>)` | `printf … >` an **existing** `.zprofile` |
| Message on create: `→ Created ${ZPROFILE}` | Delete the file on uninstall |
| Message when the line is added: `→ Added ${USER_BIN} to PATH for zsh (.zprofile)` | Put the vendor grok `# >>> grok installer >>>` block on `.zprofile` |
| Mode `0644` after create | Write PATH to `.zshrc` “because zsh login” |
| No-op when this product’s comment **and** the exact export already match | Duplicate the exact export on a second install |
| If create fails, warn with a next step and return failure | Silent success when the file could not be created |

`path_add_shell` **MUST** call `path_add_zprofile` after `path_add_zshenv`. It **MUST NOT** assign a default `ZPROFILE` before that call.

### 2.4 `rc-test --file zprofile`

`rc-test` is Type 0 **test-purpose**. Allowed `--file`: `bashrc|zshenv|zprofile|profile|fish|ash`. `--file zshrc` **MUST** fail closed. Next step names `--file zshenv` and states that zsh PATH is `.zshenv` and `.zprofile`.

| MUST | MUST NOT |
|------|----------|
| Export `ZPROFILE` under `--root` so the case is explicit | Write this login’s real `${HOME}/.zprofile` |
| Snapshot real `${HOME}/.bashrc`, `.profile`, `.zshenv`, and `.zprofile` and refuse if any change | Call `install` / `setup` as part of `rc-test` |
| Dual-mention on `requirement-shell-cli-interface` and on this file | Treat help text as the second mention |

Sample:

```text
grok-cli rc-test --root "$tmpdir" --file zprofile --case create
grok-cli rc-test --root "$tmpdir" --file profile --case create
grok-cli rc-test --root "$tmpdir" --file zshenv --case create
```

### 2.5 Uninstall

`inst_self_uninstall_cleanup_path` **MUST** include `ZPROFILE` (default `${HOME}/.zprofile`) with `BASHRC`, `ZSHENV`, `ZSHRC`, `FISH_CONFIG`, and `PROFILE`. It **MAY** strip this product’s `# Added by grok-cli installer` stickers. It **MUST NOT** delete the files. Root uninstall **MUST NOT** edit this-login startup files.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| App | `grok-cli` |
| Helper | `path_add_zprofile` in `src/grok-cli` |
| Env | `ZPROFILE` default `${HOME}/.zprofile`; `USER_BIN` default `${HOME}/.local/bin` |
| Orchestrator | `path_add_shell` calls `path_add_zprofile` and does not pre-assign `ZPROFILE` |
| Proof | **TP-LC-43** create when `SHELL` is zsh; **TP-LC-44** bash-only does not invent; **TP-LC-45** existing file appends and keeps the body; **TP-LC-46** `rc-test --file zprofile` |
| Workspace | ram-drive-first `/dev/shm/grok-cli` when present, else `{{HOME}}/prjs/grok-cli` |

### 2.7 Why this requirement exists

- **CIAO Principle 2 – Intentional**: Each missing file has one written action.  
- **CIAO Principle 5 – SSOT**: One family owner; peers point.  
- **CIAO Principle 3 – Anti-fragile**: An existing note is appended. A bash login does not grow zsh files.

## Under command line for normal user only

When the product detects Termux, Git Bash, Windows cmd, or the same class, admin privilege and a dedicated system user stay unused. This requirement does not enable `sudo`, wrap `apt`, or create a system account.

**This requirement:** shell startup files are this-login notes. Git Bash uses bash `.bashrc`. Termux uses bash `.bashrc` plus profile-ensure. Windows cmd and PowerShell User `Path` are not files this product creates. None of those classes get a new `.zprofile`.

| Do | Do not |
|----|--------|
| Write this login’s startup files | `sudo` to edit another login’s notes |
| Leave Windows User `Path` to that environment | Invent `.zprofile` because the host is Windows |

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution** (Principle 1): Create fails with a next step. `ZSHENV` alone does not create `.zprofile`.  
- **Intentional** (Principle 2): The matrix names every missing file in the family.  
- **Anti-fragile** (Principle 3): Existing bodies stay. A second install does not duplicate the export.  
- **Over-protect** (Principle 4): `rc-test` snapshots real home `.zprofile` as well as `.bashrc`, `.profile`, and `.zshenv`.  
- **Least privilege** (Principle 10): This-login writer. Mode `0644`. No other user’s home.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Write PATH to `.zshrc`, or move the vendor grok installer block onto `.zprofile`.  
2. Create `.zprofile` because `ZSHENV` is set, or because `$SHELL` is bash and the file is missing.  
3. Replace an existing `.profile`, `.zshenv`, or `.zprofile` body.  
4. Put the PATH export on a `.profile` generated for bash, zsh, or fish.  
5. Delete startup files on uninstall.  
6. Let `rc-test` change this login’s real home notes.  
7. Treat `--file zshrc` as success.  
8. Strip the **Under command line for normal user only** section, or enable admin privilege on Termux / Git Bash / Windows cmd for these writes.  
9. Re-own `.zshenv` or ash `.profile` in this file’s helpers.

## 5. Definition of done

1. Zsh login creates a missing `.zprofile` with the shared PATH line and also keeps `.zshenv` (**TP-LC-43**).  
2. Bash-only does not invent `.zprofile` or `.zshenv` (**TP-LC-44**).  
3. An existing `.zprofile` keeps its body and gains the PATH line once (**TP-LC-45**).  
4. `rc-test --file zprofile --case create` writes only the fixture (**TP-LC-46**) and is named here and on `requirement-shell-cli-interface`.  
5. A second install does not duplicate the exact export.

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry SSOT |
| `docs/requirements/requirement-shell-path-and-shell-support.md` | Bash / Fish / profile-ensure; orchestrator |
| `docs/requirements/requirement-shell-zshenv.md` | `.zshenv`; does not write `.zprofile` |
| `docs/requirements/requirement-shell-alpine.md` | Ash PATH on `.profile` |
| `docs/requirements/requirement-shell-cli-interface.md` | Dual mention `rc-test --file zprofile` |
| `docs/requirements/requirement-shell-modular-function-design.md` | `path_add_zprofile` prefix |
| `docs/requirements/requirement-class-software-dev.md` | Leftover pointer |
| `./src/grok-cli` | Implementation under test |

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-LC-43** create missing `.zprofile` when `SHELL` is zsh | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-44** bash-only does not invent `.zprofile` or `.zshenv` | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-45** existing `.zprofile` appends PATH and keeps the body | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-46** `rc-test --file zprofile --case create` | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-41** missing `.profile` for bash/zsh/fish has no PATH export | `tests/test_local_lifecycle.sh` | **pointed** — `requirement-shell-alpine` |
| **TP-LC-34 / 35** `.zshenv` create / do-not-invent | `tests/test_local_lifecycle.sh` | **pointed** — `requirement-shell-zshenv` |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`

## Terminologies

### Shell startup files

**Definition:** Shell startup files are the family of files a POSIX-like shell reads at login or when a new session starts. One member is a shell rc-file. The family includes `.bashrc`, `.zshenv`, `.zprofile`, `.zshrc`, `.profile` (and `.bash_profile` when that file wins first), plus Fish `config.fish` when claimed. Windows cmd and PowerShell User PATH are not files in this family. It is the file. A named edit of that file (PATH ensure, profile-ensure, login-hook plant, owner align) is a separate feature. Tests write a throw-away copy, never this login’s real home notes.

**Human daily-life explanation:** A shell startup file is one sticky note the kitchen reads when you unlock the door (login `.profile` / `.zprofile`), when the light comes on (`.zshenv`), or when you sit down (`.bashrc` / `.zshrc`). Putting `{{HOME}}/.local/bin` on PATH writes that line on the always-on light (`.zshenv`) and, for a zsh login, again on the zsh door note (`.zprofile`) so a later building list cannot hide the side drawer. A missing door note is hung before you leave. A bash-only kitchen does not invent the zsh notes.

**Daily-life example:** The side drawer is `{{HOME}}/.local/bin`. The always-on light note and the zsh door note both say to look there first. Ash writes that line on the door note. Bash hangs the door note so morning unlock also reads the desk note, and keeps the drawer line on the desk note.

### Command line for normal user only

**Definition:** Termux, Git Bash, Windows cmd, and the same class have a privilege ceiling of ordinary this-login work. On detect, admin privilege and a dedicated system account stay unused.

**Human daily-life explanation:** On a phone or a Git Bash window you work as yourself. You do not borrow the building keys, and you do not invent a staff account, to hang a kitchen note.

**Daily-life example:** Termux and Git Bash get the bash desk note. They do not get a new zsh door note.

## 7. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-12 | Active 1.0.0 | Family owner: missing `.profile` / `.zshenv` / `.zprofile`; `.zprofile` PATH; `rc-test --file zprofile` (**TP-LC-43..46**) |

**Last Updated**: 2026-10-12  
**Owner**: grok-cli project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
