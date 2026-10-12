**file**: docs/requirements/requirement-shell-path-and-shell-support.md  
**Status**: Active (Version 1.2.1 – startup-file family points at requirement-shell-startup-files)  
**Area**: shell  
**Key**: `requirement-shell-path-and-shell-support`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the **topic-owner** for **shell-rc** edits on grok-cli: after a **user-bin** install, this login can run `grok-cli` by name, and an SSH login can reach that PATH.

It owns **path-ensure** (one shared `USER_BIN` line on interactive rc) and **profile-ensure** (create `~/.profile` if missing so a login shell sources `.bashrc`). It also owns **sibling unify** so another similar CLI does not, *by design*, make `.bashrc` non-compliant; **heal** on every user-bin `install` / channel ensure / `self-update` (including already-installed skip); **scoped uninstall**; and **detect** via a Type 0 `rc-test` (not a lock on the file).

**Scope:** Which rc files this product writes; the exact PATH line; create / append / no-op; profile create-if-absent; write-path env; sibling comments; uninstall of **this** product’s stickers; fixture tests; `rc-test`.  
**Out of scope (cited, not re-owned):** Placing or removing the binary (`requirement-shell-local-self-management` · `requirement-shell-online-install` · `requirement-shell-self-management`); peer grok vendor PATH block for `~/.grok/bin` (`requirement-grok-setup`); Termux host writing (`requirement-shell-termux-coding`); scratch/cache (`requirement-shell-cli-storage`); ash PATH on `.profile` (`requirement-shell-alpine`); the startup-file family and `.zprofile` (`requirement-shell-startup-files`).

**Not claimed:** login-review hook; Type 1 `setup` `chown` of another login’s rc; `/etc/environment`; crontab.

### 1.1 Human-facing

**In one sentence:** After `grok-cli install` (or the curl one-liner), this login’s desk note (`.bashrc`) gets “also look in `~/.local/bin`,” and if the door note (`.profile`) is missing the program hangs one that sources `.bashrc` — without wiping notes other programs already wrote.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person who ran install | `grok-cli install` |
| The other role | Tests that point `BASHRC` at a throw-away folder | `grok-cli rc-test --root "$tmpdir" --file bashrc --case create` |
| Not this file | Copying the program into `~/.local/bin`; installing peer grok | `requirement-shell-local-self-management.md` · `requirement-grok-setup.md` |

| Includes | Excludes |
|----------|----------|
| One shared PATH line; create `.bashrc` if missing; create `.profile` if missing | Login-review scrap; dest JSON owner; `/etc` PATH; vendor `# >>> grok installer >>>` for `~/.grok/bin` |
| Keep other apps’ comments; heal PATH if a sibling deleted the line | Locking `.bashrc` so nobody else can write; replacing the whole file |

| Surface | What you open | What for |
|---------|---------------|----------|
| `grok-cli install` | Command | Companion writes PATH + profile |
| `grok-cli rc-test` | Test-purpose command | Create / modify / no-op against a temp folder |
| `grok-cli help` | Command | Environment lists `BASHRC`; testers listed **apart** from operational verbs |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install for yourself | Program file goes in `USER_BIN`; PATH line is added once; missing `.profile` is created. A second install does not duplicate the PATH line. | `grok-cli install` |
| Prove PATH without touching this login’s real `.bashrc` | A temp folder is the scratch pad. Real home rc stays still. | `grok-cli rc-test --root "$tmpdir" --file bashrc --case create` |
| Remove this program while other tools remain in `~/.local/bin` | PATH line stays. Only this product’s installer comments may go. | `grok-cli uninstall --force` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Catalog (claimed vs unused)

| Feature | This product | Files |
|---------|--------------|-------|
| **path-ensure** | **Claimed (bash / Fish)** | `.bashrc` (`BASHRC`): create if missing. Fish `config.fish` (`FISH_CONFIG`): create the config dir if needed. **Not** `.profile`. **Zsh PATH is not this file** — `requirement-shell-zshenv` (`.zshenv`, not `.zshrc`) |
| **profile-ensure** | **Claimed** | `.profile` (`PROFILE`): create if absent with a sample that sources `.bashrc`; **never overwrite** an existing body |
| **login-hook** | **Unused** | Do **not** plant a review scrap in `.bashrc` or `.profile`. Do **not** strip another product’s `# BEGIN … login hook` block |
| **rc-owner** | **This-login writer** | After create/modify, mode readable (`0644`). No Type 1 `setup` `chown` of another login’s home. Writer **is** this login |

| File | path-ensure | profile-ensure | login-hook | rc-owner |
|------|-------------|----------------|------------|----------|
| `.bashrc` | Yes (create) | — | **Unused** | This login |
| `.zshrc` | **No** (do not write PATH) | — | Unused | — |
| `.zshenv` | **Not this file** — `requirement-shell-zshenv` | — | Unused | This login (that REQ) |
| `.profile` | **No** PATH line | **Yes** | Unused | This login |
| Fish `config.fish` | Yes (create dir) | — | Unused | This login |

**MUST NOT** treat `~/.ssh-*` vault dirs as this family. **MUST NOT** write another user’s rc.

### 2.2 Shared identity (measure 1)

Several similar CLIs **MAY** write the same login’s `.bashrc`. They **MUST** share **one** PATH identity.

| MUST | MUST NOT |
|------|----------|
| Use the exact bash/zsh line `export PATH="<USER_BIN>:$PATH"` (`USER_BIN` default `${HOME}/.local/bin`) | A second dialect (`$HOME` vs the expanded path, extra quotes, a different prefix) that would miss the exact-line check |
| Fish: exact `set -gx PATH <USER_BIN> $PATH` | A second Fish dialect |
| If that exact PATH line already exists (this product or a sibling), **do not** append a second `export PATH=` | Duplicate the exact export |
| **MAY** append **only** `# Added by grok-cli installer (<VERSION>)` when the shared PATH line is already present and this product’s comment is absent | Rewrite `# Added by <other-app> installer …` or any other product’s comment |
| Match the **exact** export line, not a `USER_BIN` substring | Treat a comment or unrelated line that contains `USER_BIN` as already-good |

The PATH line is **shared**. Compliance is “`USER_BIN` is on PATH,” not “only grok-cli’s sticker is on the note.”

Peer grok’s `# >>> grok installer >>>` / `# <<< grok installer <<<` block for `~/.grok/bin` is a **second** directory. This file **MUST NOT** treat that block as the shared `USER_BIN` line. Owner: `requirement-grok-setup`.

### 2.3 Append, never replace (measure 2)

| MUST | MUST NOT |
|------|----------|
| Create `BASHRC` if missing (header with `grok-cli` / `VERSION`, then PATH) | `printf … >` an **existing** `.bashrc` / Fish config. **MUST NOT** write PATH to `.zshrc` (zsh PATH: `requirement-shell-zshenv`) |
| Keep the prior body; append PATH if the exact line is absent | Truncate or rewrite the whole file to “ensure PATH” |
| Create `.profile` only when **absent** | Overwrite an existing `.profile` body (including one created by sshd-cli or another sibling) |
| No-op when this product’s `VERSION` comments **and** the exact export already match (file bytes unchanged) | Replace a dongle or user rc |

A sibling that “ensures PATH” by writing a fresh file is how the first app’s compliance dies. This product **MUST NOT** be that sibling. Today’s ship **MUST NOT** return because `.bashrc` is missing (Termux often has no file — **L-PATH-01**).

### 2.4 Scoped uninstall (measure 3)

PATH cleanup is `inst_self_uninstall_cleanup_path`. Dual mention: `requirement-shell-local-self-management` / `requirement-shell-self-management` (remove the binary) · this file (what may be edited in rc). Call after a **user-bin** remove (`uninstall` and `self-uninstall`).

| Situation | This product MAY remove | MUST NOT remove |
|-----------|-------------------------|-----------------|
| Other files still in `USER_BIN` | **Only** `# Added by grok-cli installer …` comments | The shared `export PATH=` line; other apps’ comments; `.profile`; vendor grok installer block; login-hook `BEGIN`/`END` scraps; unrelated user lines |
| `USER_BIN` empty or missing | This product’s comments **and** the shared PATH line | `.profile`; other apps’ comments; vendor grok installer block; login-hook scraps; unrelated user lines |

**MUST** match `# Added by grok-cli installer` (this `APP_NAME`) **always**.  
**MUST NOT** use `/# Added by .* installer/d` (that deletes sshd-cli / sudoer-cli / dns-cli stickers).  
**MUST NOT** delete `.profile`.  
**MUST NOT** delete `# >>> grok installer >>>` … `# <<< grok installer <<<`.  
Root/global uninstall **MUST NOT** edit this-login rc PATH (system `GLOBAL_BIN` is already on PATH).

There is **no** OS lock that stops a naive other program from rewriting `.bashrc`. This product **MUST** follow the table so *it* is not that program.

### 2.5 Heal on every user-bin ensure (measure 4)

`inst_ensure_companion` **MUST** run on user-bin success paths **including already-installed skip**:

| Call site | Owner of the call | This file owns |
|-----------|-------------------|----------------|
| Checkout `install` (place **and** already-installed no-op) | `requirement-shell-local-self-management` | What companion writes to rc |
| Channel place **and** Type O / `curl\|sh` already-installed skip | `requirement-shell-online-install` | same |
| `self-update` after place | `requirement-shell-self-management` | same (reuses channel place) |

What companion does to rc:

1. Missing `BASHRC` → create + PATH.  
2. Exact PATH line gone → append once (header comment + export).  
3. Exact PATH present, this product’s comment absent → **MAY** append only `# Added by grok-cli installer (<VERSION>)`.  
4. Exact PATH + this `VERSION` comments already match → no-op.  
5. Missing `.profile` → create source-bashrc sample. Existing `.profile` → leave the body.

User-bin install only. **MUST NOT** run path-ensure for a root/global place into `GLOBAL_BIN`.

Re-running `grok-cli install` (or the curl one-liner) **MUST** restore a missing exact PATH line without duplicating it. That is recovery after a bad sibling, not a file lock.

### 2.6 Detect, do not police (measure 5)

This product **MUST NOT** `chattr +i`, flock, or otherwise lock `.bashrc` against other writers. It **MUST** make non-compliance **visible** and **healable**.

| Detector | Role |
|----------|------|
| Type 0 **`rc-test`** | Test-purpose verb. Target = caller `--root` tmp/cache folder (or `mktemp -d`). **MUST NOT** write this login’s real `{{HOME}}/.bashrc`. Dual mention: `requirement-shell-cli-interface`. **MUST** be routed (not a named-only Gap). |
| Fixture suites | **TP-LC-20** create / **TP-LC-21** modify dongle / **TP-LC-22** VERSION+exact-PATH no-op with `BASHRC` in a random temp folder; real `{{HOME}}/.bashrc` untouched |
| `about` / `help` | Help Environment lists `BASHRC`. `about` **MUST NOT** claim rc is healthy without a check. `about` **MAY** report whether the exact PATH line is present |

**`rc-test` argv (normative sample):**

```text
grok-cli rc-test --root "$tmpdir" --file bashrc --case create
grok-cli rc-test --root "$tmpdir" --file bashrc --case modify
grok-cli rc-test --root "$tmpdir" --file bashrc --case noop
grok-cli rc-test --root "$tmpdir" --file profile --case create
```

| Flag | Meaning |
|------|---------|
| `--root` | Fixture directory (tmp/cache). Keep real `HOME`. |
| `--file` | `bashrc` \| `zshenv` \| `zprofile` \| `profile` (Fish when claimed) \| `ash`. **`zshrc` MUST fail closed** (Next: `--file zshenv`; zsh PATH is `.zshenv` and `.zprofile`; `.zprofile` owner `requirement-shell-startup-files`) |
| `--case` | `create` \| `modify` \| `noop` |
| `--feature` | Optional: `path-ensure` \| `profile-ensure` (default from `--file`) |

**MUST:** invoke the same `path_add_*` / `path_ensure_profile` helpers production uses; assert real home rc untouched; no `sudo` except wrapping chmod/chown of **that** folder (this product: skip sudo — this login owns the fixture).  
**MUST NOT:** call `install` / dest / `setup` as part of `rc-test`; set `HOME=/tmp/…` to “isolate.”  
Help **MUST** list `rc-test` under a heading **apart** from operational verbs (install, setup, …).

### 2.7 Write-path env

| Variable | Default | Tests |
|----------|---------|-------|
| `BASHRC` | `${HOME}/.bashrc` | Fixture file; **MUST** honor a non-empty override |
| `ZSHENV` | `${HOME}/.zshenv` | Fixture; honor override — **owner `requirement-shell-zshenv`** |
| `ZPROFILE` | `${HOME}/.zprofile` | Fixture; honor override — **owner `requirement-shell-startup-files`**. Do not default this before `path_add_zprofile` |
| `ZSHRC` | `${HOME}/.zshrc` | Uninstall may still strip leftover grok-cli comments. PATH ensure **MUST NOT** write this file |
| `FISH_CONFIG` | `${HOME}/.config/fish/config.fish` | Fixture; honor override when Fish PATH is claimed |
| `PROFILE` | `${HOME}/.profile` | Fixture; honor override when profile-ensure is claimed |

**MUST NOT** ignore a non-empty `BASHRC` (always write `${HOME}/.bashrc` instead). Same for `ZSHRC` / `FISH_CONFIG` / `PROFILE` when those helpers run.

Helpers: `path_add_shell` (orchestrator), `path_add_bashrc`, `path_add_zshenv` (body: `requirement-shell-zshenv`), `path_add_zprofile` (body: `requirement-shell-startup-files`), `path_add_fish`, `path_ensure_profile`, `path_rc_test`. Prefix ownership: `requirement-shell-modular-function-design`.

### 2.8 Implementation Notes (this project)

| Item | Value for grok-cli |
|------|------------------------|
| **Product / binary** | `grok-cli` (`APP_NAME`) |
| **Implementation** | `src/grok-cli` (`path_add_*`, `path_ensure_profile`, `path_rc_test`, `inst_ensure_companion`, `inst_self_uninstall_cleanup_path`) |
| **USER_BIN** | `${HOME}/.local/bin` |
| **Exact PATH line** | `export PATH="<USER_BIN>:$PATH"` |
| **Installer comment** | `# Added by grok-cli installer (<VERSION>)` |
| **Profile sample** | `# BEGIN grok-cli profile source-bashrc` … source `${HOME}/.bashrc` … `# END grok-cli profile source-bashrc` |
| **Companion call site** | `inst_ensure_companion` on user-bin `install` / channel place / already-installed skip / `self-update` |
| **Privilege** | Type 0 this-login only |
| **Vendor grok block** | `# >>> grok installer >>>` for `~/.grok/bin` — **not** this PATH line (`requirement-grok-setup`) |

#### Sibling-unify table (this host family)

| Shared token | Value |
|--------------|--------|
| PATH identity | `export PATH="${HOME}/.local/bin:$PATH"` (Fish: `set -gx PATH ${HOME}/.local/bin $PATH`) |
| This product’s sticker | `# Added by grok-cli installer ({{VERSION}})` |
| Other stickers | `# Added by <APP_NAME> installer …` (sshd-cli, sudoer-cli, dns-cli, nginx-cli, …) — do not rewrite |
| Profile | Create-if-absent source-bashrc; never overwrite; do not delete on uninstall. First writer’s `# BEGIN <APP_NAME> profile source-bashrc` stays |
| Login-hook | Unused here; do not plant; do not strip `# BEGIN <app> login hook` … `# END` |
| Vendor grok block | `# >>> grok installer >>>` … `# <<< grok installer <<<` — other REQ; not this PATH line |
| Proof | Fixture `--root`; real `{{HOME}}/.bashrc` untouched |

This chat **MUST NOT** edit those other project trees. Unify means grok-cli **behaves** as a good sibling.

#### Foreign-edit / heal

| What the other app did | grok-cli MUST | grok-cli MUST NOT |
|------------------------|---------------|-------------------|
| Sibling already wrote the exact PATH + its comment | No second `export PATH=`; **MAY** add only grok-cli’s comment | Rewrite their comment |
| Sibling created `.profile` | Leave the body | Replace with grok-cli BEGIN/END |
| Login-hook markers in `.bashrc` | Keep the block; append PATH if missing | Strip `BEGIN`/`END` |
| Sibling deleted the exact PATH line | Append it once on next ensure | Restore a canned full `.bashrc` |
| Vendor grok installer block present | Untouched by USER_BIN ensure **and** by uninstall | Treat it as the shared `USER_BIN` line |

#### Compliance notes (implementation status)

| Rule | Status |
|------|--------|
| Bash `BASHRC` create / exact-line append / VERSION+PATH no-op (**TP-LC-20..22**) | **Implemented** |
| Profile create-if-absent; never overwrite (**TP-LC-12** / **TP-LC-14**) | **Implemented** |
| Heal on every user-bin ensure including already-installed skip | **Implemented** |
| Empty-dir uninstall keeps shared PATH while `USER_BIN` has files | **Implemented** |
| Uninstall comment match **only** `grok-cli` (not `# Added by .* installer`) | **Implemented** |
| Exact-line match on Fish (not `USER_BIN` substring) | **Implemented** |
| Honor `BASHRC` / `FISH_CONFIG` / `PROFILE` env | **Implemented** |
| Zsh PATH (`.zshenv`, not `.zshrc`) | **Pointed** — `requirement-shell-zshenv` |
| Comment-only append when sibling already wrote the exact PATH | **Implemented** (MAY = do append the grok-cli sticker) |
| `rc-test` routed; help testers heading | **Implemented** |
| Login-hook | **Unused** (honest) |

### 2.9 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): Never replace an existing rc body; never strip a shared `USER_BIN` PATH while other tools remain.  
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): File vs feature vs fixture named; PATH line vs this product’s comment named.  
- **CIAO Principle 3 – Anti-fragile** (https://github.com/cloudgen/ciao): Second install heals a missing PATH line; sibling comments stay.  
- **CIAO Principle 5 – Single Source of Output** (https://github.com/cloudgen/ciao): User-visible PATH tips via `out_*`; file appends are class-C printf exceptions (`requirement-shell-output-requirements`).  
- **CIAO Principle 10 – Least-Privilege User** (https://github.com/cloudgen/ciao): This-login rc only; no in-tool `sudo` to edit another home.  
- **CIAO Principle 16 – Interactive vs Non-Interactive** (https://github.com/cloudgen/ciao): `rc-test` and install companion **MUST NOT** hang under `--json` / pipes.  
- **CIAO Principle 4 (O) / Principle 20** (https://github.com/cloudgen/ciao): Exact-line identity, scoped uninstall, and fixture tests are Protection Zone — not “simplify to echo PATH into `.bashrc`.”

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Assume another similar CLI will write the same files; assume `install` will be re-run.  
- **Intentional:** One exact PATH line; per-app comments; profile is the door note, not a second PATH file.  
- **Anti-fragile:** Heal on companion; no-op when already exact; keep sibling stickers.  
- **Over-protect:** Do not lock the file; do not police other writers; do not become the sibling that wipes the note.  
- **SSOT:** `path_*` bodies here; binary lifecycle on local/online/self-management; dispatcher on CLI-interface; vendor grok PATH on grok-setup.  
- **Respect old working logic:** Keep `path_add_*` as the family; surgical fixes for create-if-missing, exact-line, companion-on-skip, and APP_NAME-only uninstall.

---

## Under command line for normal user only

When the ship unit detects a **command line for normal user only** (Termux, Git Bash, Windows cmd, or the same class):

| MUST | MUST NOT |
|------|----------|
| Keep **normal user privilege** (Type 0) only | Implement or enable **admin privilege** (Type 1) or **dedicated system user privilege** (Type 2) |
| Write **this login’s** `BASHRC` / `USER_BIN` PATH | Rewrite another user’s rc; in-tool `sudo`; wrap `apt` |
| Termux: named `pkg` stays Type 0 (`requirement-shell-termux-coding`) | Recommend `sudo curl \| sh` so PATH ensure runs as root |
| Git Bash / Windows cmd: same privilege ceiling | Invoke Termux `pkg` because Git Bash or Windows cmd was detected |

**This requirement:** PATH / profile ensure stay Type 0 this-login file writes. Tests retarget `BASHRC` to a temp folder — they **MUST NOT** require `sudo` or the developer’s real home. Termux default PATH often has no `USER_BIN`; create-if-missing `.bashrc` is mandatory (**L-PATH-01**).

---

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

1. Replace an existing `.bashrc` / Fish config / `.profile` body to “ensure PATH.” Write PATH to `.zshrc` (zsh PATH is `.zshenv` — `requirement-shell-zshenv`).  
2. Append a second exact `export PATH="<USER_BIN>:$PATH"` or invent a private PATH dialect.  
3. Rewrite another product’s `# Added by … installer` comment.  
4. Strip the shared PATH line on uninstall while `USER_BIN` still contains files.  
5. Delete `.profile` on uninstall.  
6. Use `/# Added by .* installer/d` (wipes sibling stickers).  
7. Ignore a non-empty `BASHRC` env (always write `${HOME}/.bashrc` instead).  
8. Leave `BASHRC` missing when `install` can create it, or skip companion because the CLI binary is already placed.  
9. Plant a login-review hook in `.bashrc` or `.profile` (unused on this product), or strip another product’s hook markers.  
10. Lock `.bashrc` (`chattr`, flock, exclusive ownership of the whole file) as “sibling protection.”  
11. Prove PATH ensure by rewriting this login’s real `~/.bashrc`.  
12. Claim path-ensure without **TP-LC-20** / **TP-LC-21** / **TP-LC-22**, or without dual-mentioning Type 0 **`rc-test --root`**.  
13. Mix `rc-test` into operational help grouping, or treat `rc-test` as install.  
14. Strip the vendor `# >>> grok installer >>>` block, or tell the operator to add `USER_BIN` when peer grok lives under `~/.grok/bin`.  
15. Strip the **Under command line for normal user only** section, or wrap `sudo` / `apt` to write rc.  
16. Edit sshd-cli / sudoer-cli / dns-cli (or any other project tree) from a grok-cli session without this-turn named root.

**Violating this rule is a critical shell-rc regression.**

---

## 5. Definition of done (path and shell support)

Work claiming PATH / login-rc support for grok-cli is **not done** if any of the following fail:

1. User-bin `install` creates `BASHRC` if missing and appends the exact PATH line if absent.  
2. Existing rc body is kept.  
3. `.profile` is created only when absent; existing body is kept.  
4. Second install does not duplicate the exact PATH line; VERSION+exact-PATH is a no-op.  
5. Uninstall keeps the shared PATH line while `USER_BIN` has other files; does not delete `.profile`; matches **only** grok-cli comments.  
6. Already-installed skip (checkout `install` and channel ensure) still runs companion.  
7. **TP-LC-20** / **TP-LC-21** / **TP-LC-22** pass with `BASHRC` in a random temp folder; real `{{HOME}}/.bashrc` untouched. A HOME-isolated substring grep alone is **not** sufficient.  
8. `rc-test` is dual-mentioned here and on `requirement-shell-cli-interface` **and** routed.  
9. Implementation changes cite `requirement-shell-path-and-shell-support`.

---

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry SSOT |
| `docs/requirements/requirement-shell-cli-interface.md` | Dispatcher, `BASHRC` env, dual mention `install` / `rc-test` |
| `docs/requirements/requirement-shell-zshenv.md` | Independent zsh PATH (`.zshenv`, not `.zshrc`); `path_add_zshenv` |
| `docs/requirements/requirement-shell-startup-files.md` | Family matrix and `.zprofile` (`path_add_zprofile`); this file points |
| `docs/requirements/requirement-shell-local-self-management.md` | Checkout place/remove; companion **call site** |
| `docs/requirements/requirement-shell-online-install.md` | Channel place / already-installed skip **call site** |
| `docs/requirements/requirement-shell-self-management.md` | `self-update` / `self-uninstall` **call site** |
| `docs/requirements/requirement-shell-idempotency.md` | Re-run matrix for PATH / profile |
| `docs/requirements/requirement-shell-modular-function-design.md` | `path_` prefix |
| `docs/requirements/requirement-shell-output-requirements.md` | `out_*`; class-C file printf |
| `docs/requirements/requirement-grok-setup.md` | Vendor grok PATH block (`~/.grok/bin`) |
| `docs/requirements/requirement-shell-termux-coding.md` | Termux host writing (not rc bodies) |
| `./src/grok-cli` | Implementation under test |

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-LC-11** create `~/.bashrc` (HOME-isolated) | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-12** create `~/.profile` | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-13** no duplicate PATH | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-14** keep existing `.profile` | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-20** `BASHRC` env create-if-missing | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-21** `BASHRC` env modify dongle | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-22** `BASHRC` env VERSION+exact-PATH no-op | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-27** already-installed skip heals missing PATH | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-28** sibling comment + exact PATH, no grok-cli comment | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-29** grok-cli comment present, exact PATH removed | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-31** vendor grok installer block unchanged | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-32** uninstall while `USER_BIN` still has a file | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-33** sudoer-cli login-hook block kept | `tests/test_local_lifecycle.sh` | have |
| **TP-LC-23 / 24 / 34 / 35 / 36** zsh PATH | `tests/test_local_lifecycle.sh` | **pointed** — `requirement-shell-zshenv` |
| **TP-LC-43 / 44 / 45 / 46** `.zprofile` and `rc-test --file zprofile` | `tests/test_local_lifecycle.sh` | **pointed** — `requirement-shell-startup-files` |
| **TP-LC-25 / 26** `PROFILE` env create / keep-body | `tests/test_local_lifecycle.sh` | have |
| **`rc-test`** routed `--root` | `tests/test_local_lifecycle.sh` | have |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`

## Terminologies

### Shell startup files

**Definition:** Shell startup files are the family of files a POSIX-like shell reads at login or when a new session starts. The family includes `.bashrc`, `.zshenv`, `.zprofile`, `.zshrc`, `.profile`, and Fish `config.fish` when claimed. Windows cmd and PowerShell User PATH are not files in this family.

**Human daily-life explanation:** A shell startup file is one sticky note the kitchen reads at the door, when the light comes on, or at the desk. This file writes the bash desk note and hangs the door note. The zsh door note is another file’s job.

**Daily-life example:** A second install does not write the drawer line twice on the bash desk note.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-09-09 | Active (1.0.0) | Topic-owner: path-ensure + profile-ensure; sibling unify; scoped uninstall; heal on already-installed; routed `rc-test` |
| 2026-09-17 | Active (1.1.0) | Zsh PATH **points** at `requirement-shell-zshenv` (`.zshenv`, not `.zshrc`) |
| 2026-09-22 | Active (1.2.0) | Ash PATH **points** at `requirement-shell-alpine` (`.profile` when `$0` is ash) |
| 2026-10-12 | Active (1.2.1) | `.zprofile` and the startup-file family **point** at `requirement-shell-startup-files`; `ZPROFILE`; `rc-test --file zprofile` |

**Last Updated**: 2026-10-12  
**Owner**: grok-cli project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
