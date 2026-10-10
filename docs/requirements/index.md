# Requirements index

**Product:** grok-cli (POSIX `/bin/sh` CLI — grok auth backup to `/var/grok-cli` with narrow sudo deposit + unprivileged sync-auth; dual-mode install)  
**Workspace state:** Specialized product law (left genesis); **software-development** class; bootstrap **cli-template → folder-backup → grok-cli** (domain) **plus** selfmanaged online package specialized onto grok-cli (channel `curl\|sh`).  
**Updated:** 2026-10-10 (29 Active + 4 superseded; auth **11** backup when logged in; **12** sync-auth-from-remote and **13** sync-auth when logged out; logged-out line names `backup`; `sync-auth-to-remote` is not a row)

| ID / key | Title | Area | Status | Path | Updated |
|----------|-------|------|--------|------|---------|
| requirement-class-software-dev | Software-development class law + leftover stack (posix-sh, dual-mode); no dest approver / no dest fence; leftover PATH/profile → path-and-shell-support; leftover zsh PATH → zshenv; leftover ash PATH → alpine | class | Active (1.3.6) | `requirement-class-software-dev.md` | 2026-09-22 |
| requirement-bootstrap-chain | Bootstrap: cli-template → folder-backup → grok-cli (domain) + selfmanaged online package | architecture | Active (4.0.0) | `requirement-bootstrap-chain.md` | 2026-09-02 |
| requirement-project-folder | Project layout (`src/`), install bins, `/var/grok-cli` deposit; Termux `PREFIX` / `~/.grok` classes; cache leaves point at `requirement-shell-cli-storage`; persistence `${HOME}/.local/${APP_NAME}` | architecture | Active (1.2.1) | `requirement-project-folder.md` | 2026-09-27 |
| requirement-three-layer-privilege-model | Type 0 + narrow Type 1 `grok-cli backup`; sudoers emit + install-script; per-user fragments; grant is backup only; samples use `id -un`; staging cache points at storage 1.4.0 | architecture | Active (2.0.2) | `requirement-three-layer-privilege-model.md` | 2026-09-27 |
| requirement-sudoer-json-file | JSON sudoer file SSOT: `{{PRJ_NAME}}` only; args `["backup"]` only; independent generate dest readable; samples use `id -un` | architecture | Active (2.0.0) | `requirement-sudoer-json-file.md` | 2026-09-06 |
| requirement-grok-auth-backup | **Auth ops SSOT**: session gate — PRoot/Termux local `auth.json` cookies (no live `grok -p hello`); other hosts live `grok -p hello` (bounded, default 14s; timeout is not logged-out; live probe code protected) + deposit `auth.*` to `/var/grok-cli` (root:root 0644) + unprivileged `sync-auth` / `sync-auth-from-remote` (skip when already logged in; preferred SPEC in persistence) + `sync-auth-to-remote` (push `~/.grok/auth.*` onto a remote login; still runs when logged in; not a numbered row; grok-auth **11** `backup` when logged in, **12** `sync-auth-from-remote` and **13** `sync-auth` when logged out); elevated probe uses `SUDO_USER` home | backup | Active (1.10.3) | `requirement-grok-auth-backup.md` | 2026-10-10 |
| requirement-grok-setup | Type 0 `setup` + `update-grok` + `reinstall` + `run`: studied xAI channel + artifact so peer `grok` is installed or refreshed; TTY already-installed keep / reinstall / Exit; named `reinstall` on the TTY main menu; Git Bash/MSYS/Cygwin `windows-*` PE; `run` starts grok without auto-update; Android wrapper `--kill-on-exit` / `proot-exit-reaper` / `start-services.sh` no-op bind; heal stale wrapper on skip **and** `self-update`; zsh vendor PATH → `.zshenv` | domain | Active (2.16.0) | `requirement-grok-setup.md` | 2026-09-17 |
| requirement-grok-crontab | Cron-job law: Type 0 `add-crontab` — this login’s crontab jobs (backup every 30 min; sync-auth at :45) after **this** login’s backup grant | domain | Active (1.1.0) | `requirement-grok-crontab.md` | 2026-09-06 |
| requirement-shell-cli-interface | Shell CLI interface; `setup` (TTY reinstall list); `update-grok`; `reinstall`; `run` (start grok without auto-update); auth verbs including `sync-auth-to-remote`; `version-check` / `self-update` / `self-uninstall` (start line names local and remote VERSION); empty argv TTY menu / off-TTY ensure; overlay `--debug` follows 0-argv; `--json` no-command is 0-argv special case (JSON help even TTY); `--debug` menu elapsed dual mention; `rc-test` dual mention (`zshenv`, `ash`); `about` cache lines point at storage 1.4.1; `language` is menu-only (front **5** / **51–63**, not an argv verb); this-login-only menu follows default-interaction **2.26.0** | shell | Active (2.15.6) | `requirement-shell-cli-interface.md` | 2026-10-10 |
| requirement-shell-cli-zero-arguments | Empty argv = no command token (overlay `--debug` / `--quiet` follow); TTY numbered menu; off-TTY Type O install-ensure (not help); `--json` no-command is 0-argv special case → JSON help (TTY and off-TTY) | shell | Active (2.2.0) | `requirement-shell-cli-zero-arguments.md` | 2026-09-07 |
| requirement-shell-cli-default-interaction | Case 3 TTY empty argv + `menu`/`main`; top **1** grok-auth (**11–16**), **5** language (block **50–69**, assigned **51–63**), **7** sudoers, **8** self-management, **9** Exit, no Back; front **6** is not a row; submenus **0** Back; this-login-only adds **2** run and hides backup/sync-auth/sudoers; logged-out **12** sync-auth-from-remote and **13** sync-auth (hides **11**); logged-in **11** backup (hides **12** and **13**); logged-out line names `backup`; `sync-auth-to-remote` is not a row | shell | Active (2.26.0) | `requirement-shell-cli-default-interaction.md` | 2026-10-10 |
| requirement-shell-cli-language | Menu language: thirteen codes (`en` `zh-Hans` `zh-Hant` `es` `ar` `fr` `pt` `ru` `de` `ja` `ko` `nl` `el`); front **5** / **51–63**; **50** and **64–69** reserved; leaf `${HOME}/.local/${APP_NAME}/language`; `GROK_CLI_LANG` wins for this process and does not write; human help and human about follow the code; `language` is not an argv verb; three menu-hidden sentences (logged-out line names `backup`) | shell | Active (1.1.2) | `requirement-shell-cli-language.md` | 2026-10-10 |
| requirement-shell-path-and-shell-support | Shell-rc PATH + profile ensure (sibling unify, scoped uninstall, heal, routed `rc-test`); zsh PATH **points** at zshenv; ash PATH **points** at alpine | shell | Active (1.2.0) | `requirement-shell-path-and-shell-support.md` | 2026-09-22 |
| requirement-shell-zshenv | Independent zsh PATH: `.zshenv` (not `.zshrc`); `rc-test --file zshenv`; vendor grok block dual mention | shell | Active (1.0.0) | `requirement-shell-zshenv.md` | 2026-09-17 |
| requirement-shell-alpine | Ash PATH on `.profile` when `$0` is ash (leading `-` ignored), and when Alpine `sh` sees `/etc/alpine-release` | shell | Active (1.0.0) | `requirement-shell-alpine.md` | 2026-09-22 |
| requirement-shell-local-self-management | Checkout `install` / `uninstall` / `where-is-me`; **mode 0755**; dual-mode secondary; Termux `USER_BIN` (not `PREFIX/bin`); companion **call site** | shell | Active (1.4.0) | `requirement-shell-local-self-management.md` | 2026-09-09 |
| requirement-shell-online-install | Channel `SCRIPT_URL` + pipe place; dual-mode primary; companion **call site** (already-installed skip still PATH-heals) | shell | Active (1.1.0) | `requirement-shell-online-install.md` | 2026-09-09 |
| requirement-shell-self-management | `version-check` / `self-update` / `self-uninstall`; proceeding `self-update` first INFO names local and remote VERSION; `self-update` heals Android grok wrapper; PATH cleanup **call site** | shell | Active (1.3.0) | `requirement-shell-self-management.md` | 2026-09-09 |
| requirement-shell-automatic-checksum | Companion `${SCRIPT_URL}.sha256` for channel downloads | shell | Active (1.0.0) | `requirement-shell-automatic-checksum.md` | 2026-09-06 |
| requirement-shell-output-requirements | Central `out_*` output SSOT; `out_menu_choice` default CLI main menu style | shell | Active (1.1.0) | `requirement-shell-output-requirements.md` | 2026-09-03 |
| requirement-operator-readable-error | Operator-facing error **wording** (human-intro style: what happened / next step) | shell | Active (1.0.0) | `requirement-operator-readable-error.md` | 2026-08-17 |
| requirement-shell-modular-function-design | Single-file modular prefixes (`out_`/`inst_`/`app_`/`gc_`/`path_add_zshenv`) | shell | Active (1.1.1) | `requirement-shell-modular-function-design.md` | 2026-09-17 |
| requirement-shell-script-coding | POSIX sh coding style (`set -u`, `out_*`, `gc_*`, fail-closed elev; no `$()` of `read` helpers); Termux host writing **points** at `requirement-shell-termux-coding` | shell | Active (1.1.0) | `requirement-shell-script-coding.md` | 2026-09-06 |
| requirement-shell-termux-coding | Termux/Android host writing: honor `PREFIX`, Termux `pkg` (no sudo), `noexec` tmp, FHS-not-assumed; PRoot exit hang (`bash -lc` → `start-services.sh` → leftover `runsvdir`; bind no-op + TSTP-safe reaper) | shell | Active (1.6.0) | `requirement-shell-termux-coding.md` | 2026-09-07 |
| requirement-shell-idempotency | Re-run safety; backup overwrite of same auth.* basenames | shell | Active | `requirement-shell-idempotency.md` | 2026-09-06 |
| requirement-shell-interactive-vs-noninteractive | Interactive vs non-interactive / confirm policy; TTY `setup` already-installed list | shell | Active (1.0.5) | `requirement-shell-interactive-vs-noninteractive.md` | 2026-09-12 |
| requirement-shell-cli-storage | Storage = per-login per-process cache folder (Linux shm → tmp → `~/.cache`; Git Bash tmp → AppData; Mac tmp → Library/Caches → `~/cache`) **and** persistence `${HOME}/.local/${APP_NAME}` (incl. `preferred-remote` and `language`); silent tier miss; Termux cache may be `noexec` | shell | Active (1.4.1) | `requirement-shell-cli-storage.md` | 2026-09-28 |
| requirement-shell-internal-volatile-timer | Named in-process stage timers (volatile); `--debug` menu elapsed of each paint step; not a domain `start`/`stop` catalog | shell | Active (1.0.0) | `requirement-shell-internal-volatile-timer.md` | 2026-09-07 |
| requirement-domain-grok-cli | Domain **surface** SSOT (four pillars); ops defer to grok-auth-backup / grok-crontab; `setup` / `update-grok` / `reinstall` channel+artifact; TTY `setup` reinstall list; grok-auth **16** `reinstall`; `sync-auth-to-remote` is typed and not a numbered row; `run` starts grok without auto-update; `check-session` is live `grok -p hello` (`proot` → reaper else simple `-p`) | domain | Active (1.10.3) | `requirement-domain-grok-cli.md` | 2026-10-10 |
| requirement-domain-folder-backup | Retired folder-archive domain surface | domain | superseded | `requirement-domain-folder-backup.md` | 2026-08-22 |
| requirement-folder-archive-backup | Retired folder tar.gz backup/restore ops | backup | superseded | `requirement-folder-archive-backup.md` | 2026-08-22 |
| requirement-folder-archive-backup-retention-total | Retired total retention | backup | superseded | `requirement-folder-archive-backup-retention-total.md` | 2026-08-22 |
| requirement-folder-archive-backup-retention-daily | Retired daily retention | backup | superseded | `requirement-folder-archive-backup-retention-daily.md` | 2026-08-22 |

## Intentionally absent (by design)

| Surface | Status on grok-cli |
|---------|---------------------|
| Type O-P payload installer | **Absent** (script-alone only) |

**Install mode:** **dual-mode** (primary online channel; secondary checkout `install`). Matrix on `requirement-shell-online-install`.

**Rules for agents:**

1. Treat Active rows above as the **live product-law inventory** for grok-cli.  
2. **Do not invent** additional `requirement-*.md` paths — verify on disk and add a registry row in the same change when creating one.  
3. Product source comments cite **only** these live requirement files — never templates/skills as behavioral authority.  
4. This versioned surface lists **requirement rows only**.  
5. Keep Status and Path in sync with each file’s header when status changes.  
6. **Class gate:** software-development requires exactly one Active `requirement-class-software-dev.md`.  
7. **Domain SSOT:** exactly one Active `requirement-domain-*` (`requirement-domain-grok-cli`).  
8. Online package is **Active** (user-ordered 2026-09-02). Do not drop it without updating this registry and the dual-mode matrix.

When adding a requirement: append a row, create the file under `docs/requirements/`, keep Status in sync with the file header.
