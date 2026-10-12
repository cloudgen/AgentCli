**file**: docs/requirements/requirement-shell-zshenv.md  
**Status**: Active (Version 1.0.1)  
**Area**: shell  
**Key**: `requirement-shell-zshenv`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the **topic-owner** for **zsh PATH** on grok-cli. After a **user-bin** install, a zsh login (macOS default, SSH `%` prompt, `zsh -c`) can run `grok-cli` and a `USER_BIN` grok symlink by name because `~/.zshenv` carries the shared `USER_BIN` line.

It owns **zshenv path-ensure**: one shared `USER_BIN` export on `.zshenv` (`ZSHENV`). It does **not** write PATH to `.zshrc` and it does **not** write `.zprofile`. Login `.zprofile` is owned by `requirement-shell-startup-files`. Bash PATH, Fish PATH, and profile-ensure stay on `requirement-shell-path-and-shell-support`. Peer grok’s `# >>> grok installer >>>` block for `~/.grok/bin` is a **second** directory; when `$SHELL` is zsh, that block **MUST** land on `.zshenv` too (dual mention `requirement-grok-setup`).

**Scope:** Which zsh file this product writes for PATH; create / append / no-op; `ZSHENV` env; `rc-test --file zshenv`; uninstall of this product’s stickers on `.zshenv` (and leftover `.zshrc` stickers).  
**Out of scope (cited, not re-owned):** Bash / Fish / `.profile` (`requirement-shell-path-and-shell-support`); placing the binary (`requirement-shell-local-self-management` · `requirement-shell-online-install`); peer grok fetch (`requirement-grok-setup`).

**Not claimed:** login-review hook in `.zshenv` or `.zshrc`; Type 1 `chown` of another login’s home; `/etc/environment`.

### 1.1 Human-facing

**In one sentence:** After `grok-cli install` (or the curl one-liner) on a zsh login, this login’s always-on zsh note (`.zshenv`) gets “also look in `~/.local/bin`” — not the interactive desk note (`.zshrc`).

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person who ran install at a zsh prompt | `curl … \| sh` then SSH again |
| The other role | Tests that point `ZSHENV` at a throw-away folder | `grok-cli rc-test --root "$tmpdir" --file zshenv --case create` |
| Not this file | Bash PATH; hanging `.profile`; copying the program | `requirement-shell-path-and-shell-support` · `requirement-shell-local-self-management` |

| Includes | Excludes |
|----------|----------|
| One shared PATH line on `.zshenv`; create `.zshenv` when this is a zsh environment or `ZSHENV` is set | Writing PATH to `.zshrc`; inventing `.zshenv` for a bash-only login with no override |
| Keep other apps’ comments; heal PATH if a sibling deleted the line | Locking `.zshenv`; replacing the whole file; a private `path+=` dialect as the line this product writes |

| Surface | What you open | What for |
|---------|---------------|----------|
| `grok-cli install` | Command | Companion writes PATH on `.zshenv` when zsh |
| `grok-cli rc-test --file zshenv` | Test-purpose command | Create / modify / no-op against a temp folder |
| `grok-cli help` | Command | Environment lists `ZSHENV` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install for yourself on macOS zsh | Program file goes in `USER_BIN`; PATH line is added once to `.zshenv`. A second install does not duplicate it. `.zshrc` is left alone. | `grok-cli install` |
| Prove zsh PATH without touching this login’s real `.zshenv` | A temp folder is the scratch pad. Real home rc stays still. | `grok-cli rc-test --root "$tmpdir" --file zshenv --case create` |
| Remove this program while other tools remain in `~/.local/bin` | PATH line stays. Only this product’s installer comments on `.zshenv` (and leftover `.zshrc` stickers) may go. | `grok-cli uninstall --force` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Catalog (claimed vs unused)

| Feature | This product | Files |
|---------|--------------|-------|
| **zshenv path-ensure** | **Claimed** | `.zshenv` (`ZSHENV`): create if missing **when zsh environment or `ZSHENV` is set**; modify if the file exists. **Not** `.zshrc` |
| **zshrc path-ensure** | **Unused** | **MUST NOT** append `USER_BIN` PATH to `.zshrc` |
| **profile-ensure / bash / fish** | **Unused here** | Owner: `requirement-shell-path-and-shell-support` |
| **login-hook** | **Unused** | Do **not** plant a review scrap in `.zshenv` or `.zshrc` |
| **rc-owner** | **This-login writer** | After create/modify, mode readable (`0644`). Writer **is** this login |

| File | path-ensure | login-hook | rc-owner |
|------|-------------|------------|----------|
| `.zshenv` | **Yes** (create when zsh environment or `ZSHENV` set; always modify if present) | Unused | This login |
| `.zshrc` | **No** | Unused | Do not write PATH |

**Zsh environment** (any one is enough):

1. `basename "${SHELL:-}"` is `zsh`.  
2. The caller set `ZSHENV` (tests/CI retarget).  
3. The target `ZSHENV` file already exists.

**MUST NOT** invent `${HOME}/.zshenv` when `$SHELL` is not zsh, `ZSHENV` was not set, and the default file is missing.

**MUST NOT** treat `~/.ssh-*` vault dirs as this family. **MUST NOT** write another user’s rc.

### 2.2 Shared identity (measure 1)

Zsh **MUST** use the **same** PATH identity as bash (sibling unify).

| MUST | MUST NOT |
|------|----------|
| Use the exact line `export PATH="<USER_BIN>:$PATH"` (`USER_BIN` default `${HOME}/.local/bin`) | A second dialect as **the line this product writes** (`path+=('…')`, `$HOME` vs the expanded path, extra quotes) |
| If that exact PATH line already exists in `ZSHENV` (this product or a sibling), **do not** append a second `export PATH=` | Duplicate the exact export |
| **MAY** append **only** `# Added by grok-cli installer (<VERSION>)` when the shared PATH line is already present and this product’s comment is absent | Rewrite `# Added by <other-app> installer …` |
| Match the **exact** export line, not a `USER_BIN` substring | Treat a comment, a `path+=` line, or an unrelated line that contains `USER_BIN` as the exact export (a `path+=` line **MAY** coexist; this product still writes the shared export once if it is absent) |

Peer grok’s `# >>> grok installer >>>` / `# <<< grok installer <<<` block for `~/.grok/bin` is a **second** directory. This file **MUST NOT** treat that block as the shared `USER_BIN` line. When `$SHELL` is zsh, `requirement-grok-setup` **MUST** append that vendor block to `.zshenv` (not `.zshrc`). Owner of the vendor block: `requirement-grok-setup`.

### 2.3 Append, never replace (measure 2)

| MUST | MUST NOT |
|------|----------|
| Create `ZSHENV` if missing **and** zsh environment / `ZSHENV` set (header with `grok-cli` / `VERSION`, then PATH) | `printf … >` an **existing** `.zshenv` |
| Keep the prior body; append PATH if the exact line is absent | Truncate or rewrite the whole file to “ensure PATH” |
| No-op when this product’s `VERSION` comments **and** the exact export already match (file bytes unchanged) | Replace a dongle or user `.zshenv` |
| Leave `.zshrc` bytes unchanged for PATH | Append PATH to `.zshrc` “because zsh” |

### 2.4 Scoped uninstall (measure 3)

PATH cleanup is `inst_self_uninstall_cleanup_path` (same helper as bash). Dual mention: `requirement-shell-path-and-shell-support` (orchestrator) · this file (what may be edited in `.zshenv` / leftover `.zshrc`).

| Situation | This product MAY remove | MUST NOT remove |
|-----------|-------------------------|-----------------|
| Other files still in `USER_BIN` | **Only** `# Added by grok-cli installer …` comments on `ZSHENV` and on leftover `ZSHRC` | The shared `export PATH=` line; other apps’ comments; vendor grok installer block; unrelated user lines (`path+=`, maven, cargo, …) |
| `USER_BIN` empty or missing | This product’s comments **and** the shared PATH line on those files | Other apps’ comments; vendor grok installer block; unrelated user lines |

**MUST** match `# Added by grok-cli installer` (this `APP_NAME`) **always**.  
**MUST NOT** use `/# Added by .* installer/d`.  
**MUST NOT** delete `.zshenv` or `.zshrc`.  
Root/global uninstall **MUST NOT** edit this-login rc PATH.

### 2.5 Heal on every user-bin ensure (measure 4)

`inst_ensure_companion` → `path_add_shell` → `path_add_zshenv` **MUST** run on user-bin success paths **including already-installed skip** (call site: `requirement-shell-path-and-shell-support`). Global/`GLOBAL_BIN` place **MUST NOT** run this helper.

What `path_add_zshenv` does:

1. Missing `ZSHENV` + (zsh environment or `ZSHENV` set) → create + PATH.  
2. Missing `ZSHENV` + not zsh environment + `ZSHENV` unset → no-op (do not invent).  
3. Exact PATH line gone on an existing file → append once (header comment + export).  
4. Exact PATH present, this product’s comment absent → **MAY** append only `# Added by grok-cli installer (<VERSION>)`.  
5. Exact PATH + this `VERSION` comments already match → no-op.  
6. **MUST NOT** write PATH to `.zshrc`.

Re-running `grok-cli install` (or the curl one-liner) **MUST** restore a missing exact PATH line on `.zshenv` without duplicating it.

### 2.6 Detect, do not police (measure 5)

This product **MUST NOT** lock `.zshenv`. It **MUST** make non-compliance **visible** and **healable**.

| Detector | Role |
|----------|------|
| Type 0 **`rc-test --file zshenv`** | Test-purpose. Target = caller `--root` tmp/cache folder. **MUST NOT** write this login’s real `{{HOME}}/.zshenv`. Dual mention: `requirement-shell-cli-interface`. Sample: `grok-cli rc-test --root "$tmpdir" --file zshenv --case create` |
| Fixture suites | **TP-LC-23** modify dongle · **TP-LC-24** VERSION+exact-PATH no-op · **TP-LC-34** create-if-missing when `ZSHENV` set · **TP-LC-35** do not invent default `.zshenv` for bash-only · **TP-LC-36** `.zshrc` unchanged |
| `rc-test --file zshrc` | **MUST** fail closed: zsh PATH is `.zshenv`. Next: `--file zshenv` |

### 2.7 Write-path env

| Variable | Default | Tests |
|----------|---------|-------|
| `ZSHENV` | `${HOME}/.zshenv` | Fixture file; **MUST** honor a non-empty override (setting it **is** zsh environment for create) |
| `ZSHRC` | `${HOME}/.zshrc` | Uninstall may still strip leftover grok-cli comments. PATH ensure **MUST NOT** write this file |

**MUST NOT** ignore a non-empty `ZSHENV` (always write `${HOME}/.zshenv` instead).

Helpers: `path_add_zshenv` (body here), `path_add_shell` (orchestrator on `requirement-shell-path-and-shell-support`), `path_rc_test` (`--file zshenv`). Prefix ownership: `requirement-shell-modular-function-design`.

### 2.8 Implementation Notes (this project)

| Item | Value for grok-cli |
|------|------------------------|
| **Product / binary** | `grok-cli` (`APP_NAME`) |
| **Implementation** | `src/grok-cli` (`path_add_zshenv`, `path_add_shell`, `path_rc_test`, `inst_self_uninstall_cleanup_path`, `gc_setup_maybe_bashrc` zsh branch) |
| **USER_BIN** | `${HOME}/.local/bin` |
| **Exact PATH line** | `export PATH="<USER_BIN>:$PATH"` |
| **Installer comment** | `# Added by grok-cli installer (<VERSION>)` |
| **Zsh PATH file** | `.zshenv` (`ZSHENV`) |
| **Not the zsh PATH file** | `.zshrc` |
| **Companion call site** | `inst_ensure_companion` → `path_add_shell` → `path_add_zshenv` |
| **Privilege** | Type 0 this-login only |
| **Vendor grok block** | `# >>> grok installer >>>` for `~/.grok/bin` on `.zshenv` when `$SHELL` is zsh (`requirement-grok-setup`) |

#### Sibling-unify table (zsh slice)

| Shared token | Value |
|--------------|--------|
| PATH identity | `export PATH="${HOME}/.local/bin:$PATH"` (same as bash) |
| This product’s sticker | `# Added by grok-cli installer ({{VERSION}})` |
| Zsh file | `.zshenv` — not `.zshrc` |
| Vendor grok block | `# >>> grok installer >>>` … `# <<< grok installer <<<` on `.zshenv` when `$SHELL` is zsh |
| Proof | Fixture `--root`; real `{{HOME}}/.zshenv` untouched |

#### Compliance notes (implementation status)

| Rule | Status |
|------|--------|
| `ZSHENV` create when override set / `$SHELL` is zsh (**TP-LC-34**) | **Implemented** |
| Do not invent default `.zshenv` for bash-only (**TP-LC-35**) | **Implemented** |
| Existing `.zshenv` exact-line append / VERSION+PATH no-op (**TP-LC-23** / **TP-LC-24**) | **Implemented** |
| `.zshrc` not written for PATH (**TP-LC-36**) | **Implemented** |
| `rc-test --file zshenv` routed; `--file zshrc` fails closed | **Implemented** |
| Honor `ZSHENV` env | **Implemented** |
| Vendor grok block on `.zshenv` when `$SHELL` is zsh | **Implemented** |
| Login-hook | **Unused** (honest) |

### 2.9 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): Never replace an existing `.zshenv` body; never write PATH to `.zshrc` “because the prompt is `%`.”  
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): Zsh always-on file (`.zshenv`) named separately from interactive `.zshrc` and from bash `.bashrc`.  
- **CIAO Principle 3 – Anti-fragile** (https://github.com/cloudgen/ciao): Second install heals a missing PATH line on `.zshenv`; sibling comments stay.  
- **CIAO Principle 5 – Single Source of Output** (https://github.com/cloudgen/ciao): User-visible PATH tips via `out_*`; file appends are class-C printf exceptions (`requirement-shell-output-requirements`).  
- **CIAO Principle 10 – Least-Privilege User** (https://github.com/cloudgen/ciao): This-login rc only.  
- **CIAO Principle 16 – Interactive vs Non-Interactive** (https://github.com/cloudgen/ciao): `.zshenv` applies to login, interactive, and `zsh -c`; `rc-test` **MUST NOT** hang under `--json` / pipes.  
- **CIAO Principle 4 (O) / Principle 20** (https://github.com/cloudgen/ciao): Independent zsh law so bash PATH helpers cannot silently skip macOS zsh.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Assume another similar CLI will write the same `.zshenv`; assume the operator already uses `path+=`.  
- **Intentional:** One exact PATH line; `.zshenv` not `.zshrc`.  
- **Anti-fragile:** Heal on companion; no-op when already exact.  
- **Over-protect:** Do not invent `.zshenv` for bash-only people; do not become the sibling that wipes the note.  
- **SSOT:** zsh PATH bodies here; bash/profile on `requirement-shell-path-and-shell-support`; vendor grok PATH on `requirement-grok-setup`.

---

## Under command line for normal user only

When the ship unit detects a **command line for normal user only** (Termux, Git Bash, Windows cmd, or the same class):

| MUST | MUST NOT |
|------|----------|
| Keep **normal user privilege** (Type 0) only | Implement or enable **admin privilege** (Type 1) or **dedicated system user privilege** (Type 2) |
| Write **this login’s** `ZSHENV` PATH when zsh environment | Rewrite another user’s rc; in-tool `sudo`; wrap `apt` |
| Termux: named `pkg` stays Type 0 (`requirement-shell-termux-coding`) | Recommend `sudo curl \| sh` so PATH ensure runs as root |
| Git Bash / Windows cmd: same privilege ceiling | Invent `.zshenv` because Git Bash was detected |

**This requirement:** zshenv PATH ensure stays Type 0 this-login file writes. Tests retarget `ZSHENV` to a temp folder — they **MUST NOT** require `sudo` or the developer’s real home.

---

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Write grok-cli `USER_BIN` PATH to `.zshrc` “because zsh.”  
2. Replace an existing `.zshenv` body to “ensure PATH.”  
3. Append a second exact `export PATH="<USER_BIN>:$PATH"` or invent a private PATH dialect as the line this product writes.  
4. Invent `${HOME}/.zshenv` when `$SHELL` is not zsh, `ZSHENV` was not set, and the file is missing.  
5. Ignore a non-empty `ZSHENV` env.  
6. Strip the shared PATH line on uninstall while `USER_BIN` still contains files.  
7. Use `/# Added by .* installer/d`.  
8. Delete `.zshenv` or `.zshrc` on uninstall.  
9. Plant a login-review hook in `.zshenv` or `.zshrc`.  
10. Lock `.zshenv` (`chattr`, flock).  
11. Prove zsh PATH by rewriting this login’s real `~/.zshenv`.  
12. Claim zshenv path-ensure without **TP-LC-23** / **TP-LC-24** / **TP-LC-34** / **TP-LC-35** / **TP-LC-36**, or without dual-mentioning Type 0 **`rc-test --file zshenv`**.  
13. Treat `rc-test --file zshrc` as success.  
14. Put the vendor `# >>> grok installer >>>` block on `.zshrc` when `$SHELL` is zsh.  
15. Strip the **Under command line for normal user only** section.  
16. Fold this file back into `requirement-shell-path-and-shell-support` as a silent `.zshrc` row.

**Violating this rule is a critical zsh PATH regression.**

---

## 5. Definition of done (zshenv path)

Work claiming zsh PATH support for grok-cli is **not done** if any of the following fail:

1. User-bin `install` writes the exact PATH line to `ZSHENV` when the file exists or zsh environment / `ZSHENV` is set.  
2. Existing `.zshenv` body is kept.  
3. `.zshrc` is not given a `USER_BIN` PATH line.  
4. Second install does not duplicate the exact PATH line; VERSION+exact-PATH is a no-op.  
5. Bash-only (no `ZSHENV` override, `$SHELL` not zsh, file missing) does not invent `.zshenv`.  
6. `rc-test --file zshenv` is dual-mentioned here and on `requirement-shell-cli-interface` **and** routed.  
7. Implementation changes cite `requirement-shell-zshenv`.

---

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry SSOT |
| `docs/requirements/requirement-shell-path-and-shell-support.md` | Bash / Fish / profile; `path_add_shell` orchestrator; companion call site |
| `docs/requirements/requirement-shell-cli-interface.md` | Dispatcher, `ZSHENV` env, dual mention `rc-test --file zshenv` |
| `docs/requirements/requirement-shell-local-self-management.md` | Checkout place; companion **call site** |
| `docs/requirements/requirement-shell-online-install.md` | Channel place / already-installed skip **call site** |
| `docs/requirements/requirement-shell-self-management.md` | `self-update` / `self-uninstall` **call site** |
| `docs/requirements/requirement-shell-modular-function-design.md` | `path_add_zshenv` prefix |
| `docs/requirements/requirement-grok-setup.md` | Vendor grok PATH block on `.zshenv` when `$SHELL` is zsh |
| `docs/requirements/requirement-class-software-dev.md` | Leftover pointer |
| `docs/requirements/requirement-shell-startup-files.md` | `.zprofile` PATH; this file does not write `.zprofile` |
| `./src/grok-cli` | Implementation under test |

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-LC-23** `ZSHENV` env modify dongle | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-24** `ZSHENV` env VERSION+exact-PATH no-op | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-34** `ZSHENV` env create-if-missing | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-35** bash-only does not invent default `.zshenv` | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-36** `.zshrc` unchanged for PATH | `tests/test_local_lifecycle.sh` | have |
| **`rc-test --file zshenv`** routed `--root` | `tests/test_local_lifecycle.sh` | have |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`

## Terminologies

### Shell startup files

**Definition:** Shell startup files are the family of files a POSIX-like shell reads at login or when a new session starts. `.zshenv` is the always-on member. `.zprofile` is the zsh login member and is not written by this file.

**Human daily-life explanation:** The always-on light note is this file’s note. The zsh door note is hung by the family owner. This file does not invent that door note.

**Daily-life example:** A zsh login gets “look in the side drawer” on the light. The door note is a sibling file.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-09-17 | Active (1.0.0) | Independent zsh PATH owner: `.zshenv` instead of `.zshrc` |
| 2026-10-12 | Active (1.0.1) | `.zprofile` **points** at `requirement-shell-startup-files`; this file still does not write `.zprofile` |

**Last Updated**: 2026-10-12  
**Owner**: grok-cli project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
