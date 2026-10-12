**file**: docs/requirements/requirement-shell-cli-interface.md  
**Status**: Active (Version 2.15.7)  
**Area**: shell  
**Key**: `requirement-shell-cli-interface`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **project Single Source of Truth** for the **POSIX shell CLI interface** of grok-cli: command surface, privilege typing, global flags, dispatcher behavior, help/about contracts, and mode rules.

It defines a **Type 0 shell CLI** with **dual-mode install** (channel `curl|sh` plus checkout `install`), **domain grok-auth** commands, **`setup`** (peer `grok` via the studied xAI procedure, not `install.sh`), and a **narrow elevated deposit** path. Empty argv: TTY menu; off-TTY Type O ensure. Full domain semantics live in `requirement-domain-grok-cli.md`. Peer grok install lives in `requirement-grok-setup.md`. Channel place lives in `requirement-shell-online-install.md`. PATH / profile / `rc-test` live in `requirement-shell-path-and-shell-support.md`. Zsh PATH (`.zshenv`, not `.zshrc`) lives in `requirement-shell-zshenv.md`.

---

### 1.1 Human-facing

This file lists the grok-cli commands you can type after install — names the program actually runs, not names that only appear in a plan.

| You | Another role | Not this |
|-----|--------------|----------|
| Type `grok-cli help` to see live commands | Domain law owns backup/sync meaning | Typing a name that was never wired |

**Includes:** dispatch table, flags. **Excludes:** auth.json parse rules.

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start at a prompt | Numbered list on a real terminal; install-ensure in a script / pipe | `grok-cli` |


## 2. Core Rules / Requirements (Mandatory)

### 2.1 Command surface (portable shape)

Every command **MUST** map to exactly one privilege type. Unclassified commands are incomplete design.

| Category | Privilege | Meaning |
|----------|-----------|---------|
| **Type 0 – CLI lifecycle + diagnostics** | Invoking user | `install`, `uninstall`, `where-is-me`, `version`, `about`, `help`, `menu` (`main` alias), `version-check`, `self-update`, `self-uninstall` |
| **Type 0 – Domain (user work)** | Invoking user | `setup` (peer grok channel + artifact), `update-grok` (refresh peer grok from xAI), `reinstall` (force place peer grok), `run` (start grok without auto-update), session/sync, sudoers fragment **print** |
| **Type 1 – Narrow elevated deposit** | Controlled sudo (allowlisted only) | Copy `~/.grok/auth.*` into `/var/grok-cli` only |
| **Type 2 – Dedicated system user app ops** | Dedicated app user | **Not in scope** for this product |

### 2.2 Global flags (portable)

| Flag | Env / state | Behavior |
|------|-------------|----------|
| `--quiet`, `-q` | `QUIET=1` | Suppress non-error human output; errors still visible |
| `--json` | `JSON=1` (implies quiet) | Machine-readable structured output |
| `--debug` | `DEBUG=1` | Extra diagnostics on stderr; must not break JSON purity on stdout. Numbered-menu paint elapsed is `requirement-shell-internal-volatile-timer` |
| `--force` | `FORCE=1` / force policy | Skip safe confirms or force reinstall only where documented |

Additional flags **MAY** be added only when documented here (or a superseding requirement) and wired in the dispatcher.

### 2.3 Dispatcher and entry rules

1. **Single entry:** `app_main` **MUST** parse global flags and route commands.  
2. **Unknown command:** **MUST** fail loudly with pointer to `help` (via output SSOT).  
3. **Empty argv:** `requirement-shell-cli-zero-arguments.md`: **no command token** after flag parse (overlay switches such as `--debug` **do not** disqualify). TTY → numbered start list (same handler as `menu` / `main`); off-TTY → Type O install-ensure (**MUST NOT** help). `--json` with no command **is** empty argv; **special case** = JSON help on TTY **and** off-TTY (not the list, not ensure).  
4. **No raw user I/O:** User-facing messages **MUST** go through `out_*`.  
5. Script end **MUST** call `app_main "$@"` (no basename gate that blocks dispatch).

### 2.4 Help surface

`help` **MUST** list:

- Usage line  
- Every supported command with one-line purpose  
- Privilege category (Type 0 vs elevated deposit)  
- Global flags  
- Honest note that deposit requires admin-installed sudoers fragment  
- **Test-purpose** verbs (when any exist, including `rc-test`) under a heading **apart** from operational verbs  

In JSON mode, help **MUST NOT** dump long human text; return a short structured success/note object.

### 2.5 Implementation Notes (this project)

| Item | Value for grok-cli |
|------|-------------------------|
| **Product / binary name** | `grok-cli` (`APP_NAME`) |
| **Primary executable** | `src/grok-cli` (POSIX `/bin/sh`, single-file ship unit) |
| **Dispatcher** | `app_main` |
| **Output SSOT** | `out_text` + wrappers (`out_info`, `out_success`, `out_warn`, `out_error`, `out_die`, `out_plain`, `out_json`, …) |
| **Version SSOT** | ship unit `VERSION=` in `src/grok-cli` (do not pin a stale number here) |
| **Install paths** | Global: `GLOBAL_BIN` default `/usr/local/bin`; User: `USER_BIN` default `${HOME}/.local/bin` |
| **Primary install story** | User bin: `~/.local/bin/grok-cli` |
| **Interactive rc write path** | `BASHRC` default `${HOME}/.bashrc`. User-bin PATH ensure creates/modifies this file. Tests/CI **MAY** set `BASHRC` to a file in a temp folder. Dual mention: `requirement-shell-path-and-shell-support`. |
| **Zsh always-on rc write path** | `ZSHENV` default `${HOME}/.zshenv`. User-bin zsh PATH ensure writes this file (not `.zshrc`). Tests/CI **MAY** set `ZSHENV` to a file in a temp folder. Dual mention: `requirement-shell-zshenv`. |
| **Online channel env** | `SCRIPT_URL` default `https://raw.githubusercontent.com/cloudgen/grok-cli/main/src/grok-cli` |
| **Type 2 commands** | None |
| **Dedicated system user** | Not required |

#### Supported commands (normative for this project)

| Command | Type | Handler family | Required behavior |
|---------|------|----------------|-------------------|
| *(no command token — empty argv; overlay flags such as `--debug` allowed)* | Type 0 | TTY → `app_default`; off-TTY → `inst_channel_ensure` | TTY numbered menu; off-TTY Type O ensure (**MUST NOT** help). `--json` no-command is 0-argv **special case** → JSON help (TTY and off-TTY) |
| `install` | Type 0 | `inst_local_install` | Checkout copy of the running ship unit; idempotent unless `--force`. User-bin: **always** `inst_ensure_companion` (PATH + profile), including already-installed skip. Dual mention: `requirement-shell-local-self-management` · `requirement-shell-path-and-shell-support` |
| `uninstall` | Type 0 | `inst_local_uninstall` | Remove managed binary; confirm unless `--force`. User-bin: PATH cleanup per `requirement-shell-path-and-shell-support` |
| `rc-test` | Type 0 **test-purpose** | `path_rc_test` | Fixture create / modify / no-op against `--root` tmp/cache. **MUST NOT** write this login’s real `{{HOME}}/.bashrc` or `{{HOME}}/.zshenv`. Help lists this **apart** from operational verbs. Dual mention: `requirement-shell-path-and-shell-support` · `requirement-shell-zshenv` · `requirement-shell-alpine`. Samples: `grok-cli rc-test --root "$tmpdir" --file bashrc --case create` · `grok-cli rc-test --root "$tmpdir" --file zshenv --case create` · `grok-cli rc-test --root "$tmpdir" --file ash --case create`. `--file zshrc` **MUST** fail closed (Next: `--file zshenv`) |
| `version-check` | Type 0 | `ver_check` | Compare local vs remote VERSION on `SCRIPT_URL` |
| `self-update` | Type 0 | `inst_self_update` | Re-download from `SCRIPT_URL` when remote is newer (or `--force`). Proceeding first INFO: `Starting the self-update of {{APP_NAME}}({{local}}) to new version:{{remote}}...` |
| `self-uninstall` | Type 0 | `inst_self_uninstall` | Remove managed binary (channel name; same dest as `uninstall`). User-bin PATH cleanup: `requirement-shell-path-and-shell-support` |
| `where-is-me` | Type 0 | `app_where_is_me` | Running + install paths + installed flag |
| `version` | Type 0 | `app_version` | Local `VERSION` only; no network |
| `about` | Type 0 | `app_about` | Diagnostics: install presence, paths, user, shell, TTY; **Cache folder used**, **Cache folder (preferred)**, **Cache folder (1st fallback)**, **Cache folder (2nd fallback)** when that host has one (`requirement-shell-cli-storage`); **Persistence storage** `${HOME}/.local/${APP_NAME}`; grok home, session, deposit dir; **no** channel one-liner. Human labels follow the menu language. JSON stays English |
| `help` | Type 0 | `app_help` | Full usage in human mode; short JSON note in JSON mode. Human text follows the menu language. JSON stays English |
| `menu` | Type 0 | `app_default` | Numbered list (`requirement-shell-cli-default-interaction`). Front **7** sets the menu language (`requirement-shell-cli-language` **1.2.0**: assigned **80–92**). Front **8** is not a row. `language` is **not** an argv verb. `GROK_CLI_LANG` overrides this process and does not write the file. Interactive: **ignore `--json`**. Non-interactive: help, following `--json`. |
| `main` | Type 0 | `app_default` (alias) | Same as `menu` |
| `setup` | Type 0 | `gc_setup` (domain) | Perform the studied xAI grok procedure (platform, channel pointer, artifact, `~/.grok` place) so peer `grok` is installed; **MUST NOT** fetch or exec `install.sh`; skip if grok already **runs on this host** unless `--force` **or** a TTY reinstall pick. On a TTY, already-installed grok **MUST** offer keep / reinstall / Exit (`requirement-grok-setup` 9b). `--json` / off-TTY **MUST NOT** prompt. Stale session PATH is not an error. **MUST NOT** install grok-cli |
| `update-grok` | Type 0 | `gc_update_grok` (domain) | Refresh peer `grok` from the xAI channel + artifact (same place path as `setup --force`). **MUST NOT** exec grok auto-update. **MUST NOT** update grok-cli (`self-update` stays that). Missing grok → Next `{{APP_NAME}} setup`. Dual mention `requirement-grok-setup` · `requirement-domain-grok-cli`. **INC-20260910-002** |
| `reinstall` | Type 0 | `gc_reinstall` (domain) | Remove existing grok and install again (same place path as `setup --force`). **MUST** appear on the TTY numbered main menu. Missing grok **MUST** still fetch (install). **MUST NOT** delete `auth.*` or wipe `{{GROK_HOME}}`. **MUST NOT** exec grok auto-update. **MUST NOT** update grok-cli. JSON type **MUST** be `reinstall` with `status=reinstalled` on success. Dual mention `requirement-grok-setup` · `requirement-domain-grok-cli` · `requirement-shell-cli-default-interaction` |
| `run` | Type 0 | `gc_run_grok` (domain) | Start peer grok with `--no-auto-update` (unless already in argv) then remaining grok args. Missing grok → Next `{{APP_NAME}} setup`. `--json` **MUST NOT** exec grok. Dual mention `requirement-grok-setup` · `requirement-domain-grok-cli` |
| `check-session` | Type 0 | `gc_check_session` (domain) | Confirm grok is logged in by running `grok -p hello` first (not `auth.json` parse alone) |
| `backup` | Type 0 (+ Type 1 deposit step) | `gc_backup` (domain) | Session gate; elevated copy of `~/.grok/auth.*` into `/var/grok-cli` |
| `sync-auth` | Type 0 | `gc_sync_auth` (domain) | Copy `/var/grok-cli/auth.*` into `~/.grok` without sudo; **skip** when grok is already logged in |
| `sync-auth-from-remote` | Type 0 | `gc_sync_auth_from_remote` (domain) | `scp` remote `/var/grok-cli/auth.*` into `~/.grok`; SPEC is `user@IPv4`, IPv4, domain, or `user@domain`; **does not** use sudo; **skip** when grok is already logged in |
| `sync-auth-to-remote` | Type 0 | `gc_sync_auth_to_remote` (domain) | `ssh` + `scp` this login’s `~/.grok/auth.*` onto the remote login’s `~/.grok`; same SPEC forms; **does not** use sudo; **still runs** when grok is already logged in; remote `auth.json` mode `0600` |
| `add-crontab` | Type 0 | `gc_add_crontab` (domain) | Install this login’s crontab jobs (backup every 30 min; sync-auth at :45) after **this** login’s backup grant exists — **does not** write `/etc` |
| `print-sudoers` | Type 0 | `gc_print_sudoers` (domain) | Emit sudoers fragment for admin to install under `/etc/sudoers.d/` — **does not** write `/etc` itself |
| `print-sudoers-install-script` | Type 0 | `gc_print_sudoers_install_script` (domain) | Write admin handoff script (no `/etc` write) |
| `remove-project-sudoers` | Type 0 | `gc_remove_project_sudoers` (domain) | Delete draft only; never `/etc` |
| `generate-sudoer-request` | Type 0 | `gc_generate_sudoer_request` (domain) | **Independent** generate: write JSON grant to a dest tests/review can read without sudo (compact; backup verb; sibling convert when present) — **does not** write `/etc` or inbound |
| `submit-sudoer-request` | Type 0 | `gc_submit_sudoer_request` (domain) | Detect sudoer-cli + sudoer-adm + public inbound; **update** if this user’s `/etc/sudoers.d` fragment exists else **add**; `--add`/`--update` override — **does not** write `/etc` or `mkdir` inbound |

#### Global flags (normative wiring)

| Flag | Required wiring |
|------|-----------------|
| `--quiet`, `-q` | `QUIET=1` in `app_main` |
| `--json` | `JSON=1` and `QUIET=1` in `app_main` |
| `--debug` | `DEBUG=1` in `app_main`; TTY `menu` elapsed of each paint step (`requirement-shell-internal-volatile-timer`) |
| `--force` | `FORCE=1` (and install reinstall policy when applicable) |
| `--update` | `SUBMIT_ACTION=update` + explicit (submit only) |
| `--add` | `SUBMIT_ACTION=add` + explicit (submit only) |

#### Dispatcher acceptance criteria

1. Unknown token after flag parse → `out_die` with pointer to `grok-cli help`.  
2. Zero-arg (no command token, including overlay `--debug` / `--quiet`) → TTY numbered menu; off-TTY Type O ensure (never help, never `setup`). `--json` with no command is 0-argv special case → JSON help (TTY and off-TTY).  
3. Command routing table in `app_main` **must** include every **Supported commands** row above. **`rc-test`** is routed; help **MUST** list it under a heading **apart** from operational verbs (`requirement-shell-path-and-shell-support`).  
4. Help text **must** stay aligned with that table.  
5. Domain catalog detail is owned by `requirement-domain-grok-cli.md` — this file owns the **listed verbs** and routing. Auth ops detail is `requirement-grok-auth-backup.md`. Peer grok install is `requirement-grok-setup.md`.

#### Explicitly out of scope

- Type O-P payload installer  
- Type 1 host bootstrap beyond **narrow deposit** and **sudoers fragment generation**  
- Creating the sibling inbound (`sudo sudoer-cli setup` is not this CLI)  
- Type 2 app runtime under a dedicated system user  

### 2.6 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 1 – Caution**: Unknown commands fail loud; force gates destructive ops.  
- **CIAO Principle 2 – Intentional**: Every command has one privilege type and one handler family.  
- **CIAO Principle 5 – Single Source of Output**: Central `out_*`.  
- **CIAO Principle 6 – Single Point of Entry**: `app_main` is the dispatcher SSOT.  
- **CIAO Principle 9 – Three Types of Commands**: Type 0 lifecycle/domain; Type 1 narrow deposit only.  
- **CIAO Principle 10 – Least-Privilege User**: No invented system-user requirement for binary lifecycle.  
- **CIAO Principle 16 – Interactive vs Non-Interactive**: No hang in non-interactive mode.  
- **CIAO Principle 4 / 20 – Over-protect**: Protection Rule blocks privilege and UX regressions.

---

## Under command line for normal user only

When grok-cli runs on Termux, Git Bash, Windows cmd, or the same class (this login only — no root, no dedicated system account):

| MUST | MUST NOT |
|------|----------|
| Keep **normal user privilege** only | Enable **admin privilege** (`sudo`, write `/etc`) or a **dedicated system user** |
| Treat admin-privilege and dedicated-account work as **unused** | Wrap `apt` / `dnf` / `yum`; `useradd`; recommend `sudo curl \| sh` |
| Termux: `pkg` as this login stays ordinary-user work | Recommend `sudo curl \| sh` as the install path |
| Git Bash and Windows cmd: same ceiling | Invoke Termux `pkg` because those hosts were detected |

Detect: Termux — `uname` contains Android, or `PREFIX` / `TERMUX_VERSION` is set. Git Bash — `MSYSTEM` or `uname -s` is MINGW*/MSYS*. Windows cmd — `OS=Windows_NT` after excluding Git Bash, Cygwin, and WSL.

**This requirement:** the Type 1 backup/sudoers rows stay **unused** on detect. The main menu **MUST NOT** list `backup`, `sync-auth`, or `sudoers` on detect (host not-available line: `requirement-shell-cli-default-interaction` **2.27.0**). Auth **11** `backup` and auth **13** `sync-auth` stay off this class. When **logged in**, that REQ also omits auth **12** `sync-auth-from-remote` and **appends** the logged-in not-available line. When **logged out**, that REQ lists auth **12** and **appends** the logged-out not-available line. `sync-auth-to-remote` is not a numbered row. Do not add sudo verbs because Linux has them.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Fail loud on bad input; never silent wrong privilege context.  
- **Intentional:** Command table + help + dispatcher stay synchronized.  
- **Anti-fragile:** Works under TTY, quiet, JSON, offline local install.  
- **Over-protect:** Do not collapse Type 0/1, reintroduce online verbs, or raw output for user messages.  
- **SSOT:** `APP_NAME` / `VERSION` / flags at config defaults; output via `out_*`; dispatch via `app_main`.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Drop channel lifecycle commands without updating this file and the dual-mode matrix.  
2. Route off-TTY empty argv to help, or hang off-TTY empty argv on the numbered menu.  
3. List commands in help that are not routed (or route commands not listed).  
4. Bypass `out_*` for product user messages.  
5. Run the entire CLI as root by default instead of narrow deposit elevation.  
6. Put full domain archive semantics only here and omit the domain SSOT.  
7. Add a second submit verb (`submit-sudoer`) without routing + help, or invent inbound `mkdir` as this CLI’s job.

8. Strip the **Under command line for normal user only** section, or enable admin privilege / a dedicated system user on Termux / Git Bash / Windows cmd.  
9. Drop `rc-test` from the dual-mention table without updating `requirement-shell-path-and-shell-support`, mix it into operational help grouping, or treat it as install.  
10. Drop `reinstall` from routing or help, or treat it as grok-cli `self-update` / grok auto-update.  

**Violating this rule is a critical CLI interface regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | All commands in the table are routed and listed in help |
| AC-2 | Global flags wire QUIET/JSON/DEBUG/FORCE as specified |
| AC-3 | Empty argv (no command token, including `--debug`): TTY numbered menu; off-TTY Type O ensure; never help on the pipe; `--json` no-command is 0-argv special case → JSON help (TTY and off-TTY) |
| AC-4 | `version-check` / `self-update` / `self-uninstall` routed and listed |
| AC-5 | Domain verbs point to domain requirement for deep semantics |
| AC-6 | `submit-sudoer-request` is Type 0, routed, listed in help; does not write `/etc` or create inbound |
| AC-7 | `generate-sudoer-request` is Type 0, routed, listed in help; independent of submit; dest is invoking-user readable; does not write `/etc` or inbound |
| AC-8 | `menu` / `main` routed; match `requirement-shell-cli-default-interaction` |
| AC-9 | `add-crontab` is Type 0, routed, listed in help; does not write `/etc`; dual mention `requirement-grok-crontab` |
| AC-10 | `sync-auth-from-remote` is Type 0, routed, listed in help; dual mention `requirement-grok-auth-backup` |
| AC-10b | `sync-auth-to-remote` is Type 0, routed, listed in help, and not a numbered row; direct CLI still runs when logged in; dual mention `requirement-grok-auth-backup` · `requirement-shell-cli-default-interaction` |
| AC-11 | `setup` is Type 0, routed, listed in help; dual mention `requirement-grok-setup`; **MUST NOT** fetch or exec `install.sh` |
| AC-11b | `update-grok` is Type 0, routed, listed in help (distinct from `self-update`); dual mention `requirement-grok-setup` |
| AC-11c | `reinstall` is Type 0, routed, listed in help and on the TTY numbered main menu; dual mention `requirement-grok-setup` · `requirement-shell-cli-default-interaction` |
| AC-12 | `--debug` listed in help; TTY `menu` elapsed owned by `requirement-shell-internal-volatile-timer` |
| AC-13 | `run` is Type 0, routed, listed in help; starts grok with `--no-auto-update`; dual mention `requirement-grok-setup` · `requirement-domain-grok-cli` |
| AC-14 | `rc-test` is Type 0 test-purpose, routed, listed **apart** from operational verbs; dual mention `requirement-shell-path-and-shell-support` |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-shell-cli-zero-arguments` | Empty argv = no command token (overlay `--debug` follows); TTY menu; off-TTY Type O ensure |
| `requirement-shell-online-install` | Dual mention of channel pipe / `SCRIPT_URL` |
| `requirement-shell-self-management` | Dual mention of `version-check` / `self-update` / `self-uninstall` |
| `requirement-shell-cli-default-interaction` | Numbered list body; TTY empty argv and `menu`/`main` |
| `requirement-shell-internal-volatile-timer` | Dual mention of `--debug` menu elapsed (helpers, not domain verbs) |
| `requirement-shell-local-self-management` | install/uninstall/where-is-me |
| `requirement-shell-path-and-shell-support` | PATH / profile; `BASHRC`; dual mention `rc-test` |
| `requirement-shell-zshenv` | Zsh PATH on `.zshenv`; dual mention `rc-test --file zshenv` |
| `requirement-shell-alpine` | Ash PATH on `.profile`; dual mention `rc-test --file ash` |
| `requirement-shell-output-requirements` | `out_*` catalog |
| `requirement-domain-grok-cli` | Domain four pillars |
| `requirement-grok-setup` | Dual mention of `setup`, `update-grok`, `reinstall`, and `run` |
| `requirement-grok-crontab` | Dual mention of `add-crontab` |
| `requirement-three-layer-privilege-model` | Elevation model |
| `docs/requirements/index.md` | Registry |

---

## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-01..13** | `tests/test_cli.sh` | have |
| **TP-CLI-29** | `tests/test_cli.sh` | have (overlay flags-only `--debug` / `--quiet` follow empty argv) |
| **TP-CLI-25..28** | `tests/test_cli.sh` | have (`--debug` menu elapsed; dual mention `requirement-shell-internal-volatile-timer`) |
| **TP-VCLI-01..09**, **11**–**18** | `tests/test_grok_setup.sh` | have |
| **TP-VCLI-33**–**35** | `tests/test_grok_setup.sh` | have |
| **TP-VCLI-37**–**39** | `tests/test_grok_setup.sh` | have |
| **TP-VCLI-40**–**42** | `tests/test_grok_setup.sh` | have — `reinstall` |
| **TP-CLI-31** | `tests/test_cli.sh` | have — grok-auth **15** `setup` and **16** `reinstall` |
| **TP-GROK-CLI-46** | `tests/test_domain_grok_cli.sh` | have — `run` `--no-auto-update` |
| **TP-GROK-CLI-50** | `tests/test_domain_grok_cli.sh` | have — `sync-auth-to-remote` |
| **TP-CLI-04**, **TP-CLI-13**, **TP-CLI-19**, **TP-CLI-20** | `tests/test_cli.sh` | have — help lists `sync-auth-to-remote`; the numbered menu does not |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-03 | Active 1.0.0 | CLI surface for local-only folder-backup + domain backup |
| 2026-08-15 | Active 1.1.0 | `submit-sudoer-request` listed as Type 0 JSON submit into sibling public inbound |
| 2026-08-17 | Active 1.2.0 | `--add` / `--update`; default submit action from host `/etc/sudoers.d` probe |
| 2026-08-17 | Active 1.3.0 | `generate-sudoer-request` Type 0; AC-7 |
| 2026-08-17 | Active 1.3.1 | Generate dest must be readable for tests/review; independent of submit |
| 2026-08-23 | Active 2.1.0 | Intended Gap `menu`/`main`; empty argv stays Type N help (not the numbered list) |
| 2026-08-23 | Active 2.2.0 | `menu`/`main` routed to `app_default`; TTY empty argv numbered list |
| 2026-08-25 | Active 2.3.0 | `setup` Type 0 — curl xAI grok installer (peer CLI; not grok-cli install) |
| 2026-08-30 | Active 2.3.1 | About **Cache folder (preferred)/(fallback)** |
| 2026-08-30 | Active 2.3.2 | About **Persistence storage** `${HOME}/.local/${APP_NAME}` |
| 2026-09-02 | Active 2.4.0 | `add-crontab` Type 0 — per-login backup/sync-auth crontab jobs |
| 2026-09-02 | Active 2.5.0 | `sync-auth-from-remote` Type 0 — four SPEC forms |
| 2026-09-02 | Active 2.6.0 | `setup` inlines studied xAI procedure; **MUST NOT** fetch or exec `install.sh` |
| 2026-09-02 | Active 2.7.0 | Dual-mode channel; off-TTY empty argv Type O; `version-check` / `self-update` / `self-uninstall` |
| 2026-09-04 | Active 2.7.1 | `setup` skip only if grok already runs on this host (dual mention `requirement-grok-setup` 2.2.0) |
| 2026-09-04 | Active 2.7.2 | `setup` Android ET_EXEC wrapper (dual mention `requirement-grok-setup` 2.3.0) |
| 2026-09-04 | Active 2.7.3 | `setup` Termux `pkg install -y proot` when needed (dual mention `requirement-grok-setup` 2.4.0) |
| 2026-09-04 | Active 2.7.4 | `setup` HTTP status on curl fail (dual mention `requirement-grok-setup` 2.5.0) |
| 2026-09-04 | Active 2.7.5 | `setup` Android proot resolv bind (dual mention `requirement-grok-setup` 2.6.0) |
| 2026-09-05 | Active 2.7.6 | `check-session` live `grok -p hello` (dual mention `requirement-grok-auth-backup` 1.2.0) |
| 2026-09-07 | Active 2.7.7 | `--debug` dual mention of menu paint elapsed (`requirement-shell-internal-volatile-timer`) |
| 2026-09-07 | Active 2.7.8 | Empty argv = no command token; overlay `--debug` follows 0-argv (`requirement-shell-cli-zero-arguments` 2.1.0) |
| 2026-09-07 | Active 2.7.9 | `--json` no-command is 0-argv special case: JSON help even on a TTY (`requirement-shell-cli-zero-arguments` 2.2.0) |
| 2026-09-07 | Active 2.8.0 | `run` Type 0 — start peer grok without auto-update (Termux hang) |
| 2026-09-07 | Active 2.8.1 | `self-update` first INFO names local and remote VERSION (dual mention) |
| 2026-09-09 | Active 2.9.0 | `rc-test` dual mention + routed; PATH owner `requirement-shell-path-and-shell-support` |
| 2026-09-10 | Active 2.10.0 | `update-grok` Type 0 — refresh peer grok from xAI (dual mention `requirement-grok-setup` 2.12.0; **INC-20260910-002**) |
| 2026-09-12 | Active 2.11.0 | TTY `setup` already-installed keep / reinstall / Exit (dual mention `requirement-grok-setup` 2.14.0) |
| 2026-09-14 | Active 2.12.0 | `reinstall` Type 0 — force place peer grok; listed on the TTY main menu (dual mention `requirement-grok-setup` 2.15.0) |
| 2026-09-17 | Active 2.13.0 | `rc-test --file zshenv`; `ZSHENV` env; dual mention `requirement-shell-zshenv` |
| 2026-09-22 | Active 2.14.0 | `sync-auth-to-remote` Type 0 — push `~/.grok/auth.*` onto a remote login (dual mention `requirement-grok-auth-backup` 1.10.0) |
| 2026-09-22 | Active 2.15.0 | `rc-test --file ash`; ash PATH on `.profile` (dual mention `requirement-shell-alpine` 1.0.0) |
| 2026-09-27 | Active 2.15.1 | `about` cache lines follow `requirement-shell-cli-storage` 1.4.0 (used / preferred / 1st / 2nd) |
| 2026-09-28 | Active 2.15.2 | `language` is menu-only (front **6**), not an argv verb. Human `help` and human `about` follow `requirement-shell-cli-language`. JSON stays English |
| 2026-10-02 | Active 2.15.3 | Menu language is front **5** / block **50–69** assigned **51–63** (dual mention `requirement-shell-cli-language` 1.1.0). 2.15.2 was front **6** / **61–68**. |
| 2026-10-10 | Active 2.15.4 | This-login-only menu dual mention follows `requirement-shell-cli-default-interaction` **2.24.0** (logged-out not-available line; auth **11** omitted; auth **13** only when logged in) |
| 2026-10-10 | Active 2.15.5 | This-login-only menu follows default-interaction **2.25.0** (auth **11** and **13** omitted; auth **12** when logged out; `sync-auth-to-remote` is not a row) |
| 2026-10-10 | Active 2.15.6 | Logged-out not-available line follows default-interaction **2.26.0** (`backup features are not available for logged-out environment.`) |
| 2026-10-12 | Active 2.15.7 | Menu language is front **7** / assigned **80–92** (dual mention `requirement-shell-cli-language` **1.2.0**). Front **8** is not a row. |

---

**Last Updated**: 2026-10-12 (2.15.7 — menu language is front **7** / assigned **80–92**; front **8** is not a row. 2.15.6 followed default-interaction **2.26.0**.)  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
