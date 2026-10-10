# Test plan — grok-cli

Maps **TP-*** coverage to `tests/`.  
**Suite entry:** `./tests/run.sh`  
**Ship unit:** `src/grok-cli`  
**Product VERSION:** 1.8.43  
**Last plan update:** 2026-10-10  
**Last suite run:** CLI surface only, 2026-10-10: `run_test_cli` PASS=485 FAIL=0 SKIP=0 (logged-out auth **11** `sync-auth` and **12** `sync-auth-from-remote`; logged-in **11** `backup`). Full suite was not re-run. Previous full run 2026-10-02 was PASS=998 FAIL=56 SKIP=0; those 56 fails were **TP-VCLI-19** through **TP-VCLI-36** (Termux/proot grok place and Windows `.exe` place).

Status: **have** = automated today · **todo** = needed · **optional** · **n/a** · **skip** (environment)

---

## Baseline coverage

| Area | Status | Evidence |
|------|--------|----------|
| Syntax `sh -n` | have | TP-CLI-01 |
| Active REQ samples do not freeze a session login | have | TP-CLI-18 |
| version / help / about human + JSON | have | TP-CLI-02..06 |
| Empty argv: TTY menu; off-TTY Type O ensure (not help); overlay `--debug` follows 0-argv | have | TP-CLI-07 · TP-CLI-29 · TP-ONL-01 |
| Numbered menu verb `menu`/`main` (case 3; TTY empty argv shares handler; off-TTY `menu` = help; front **5** language, **51–63**) | have | TP-CLI-13 · TP-CLI-17 · TP-CLI-19 · TP-CLI-20 · TP-CLI-21 · TP-CLI-22 · TP-CLI-23 · TP-CLI-30 · TP-CLI-32 |
| `--debug` menu elapsed of each paint step (internal-timer) | have | TP-CLI-25 · TP-CLI-26 · TP-CLI-27 · TP-CLI-28 |
| Unknown + quiet + set -u HOME | have | TP-CLI-08..11 |
| Cache folder + persistence storage | have | TP-CLI-12 |
| Termux/Android host writing (`PREFIX`, `pkg`, `noexec` smoke) | have | TP-VCLI-15..25 · TP-LC-01 |
| Help lists setup / check-session / backup / sync-auth / sync-auth-from-remote / add-crontab; no restore operand | have | TP-CLI-04 |
| `setup` grok channel + artifact (fake curl; no `install.sh`) | have | TP-VCLI-01..09 · 11..16 |
| Local install / idempotent / uninstall / mode 0755 | have | TP-LC-01..10 |
| Session gate | have | TP-GROK-CLI-03..06 · 44 · 45 |
| Backup to writable GROK_CLI_ROOT + overwrite | have | TP-GROK-CLI-07/08 |
| sync-auth no sudo + dest 0600 | have | TP-GROK-CLI-09/10 |
| Production `/var/grok-cli` without global binary fail-closed | have | TP-GROK-CLI-12 |
| JSON grant is `grok-cli backup` only | have | TP-GROK-CLI-22* |
| Independent generate dest readable | have | TP-GROK-CLI-24* |
| Operator-readable inbound-fidelity `[ERROR]` | have | TP-GROK-CLI-25* |
| add-crontab grant gate + isolated jobs + idempotent | have | TP-GROK-CLI-26..29 |
| sync-auth-from-remote four SPEC forms + fake scp; TTY menu row 3 SPEC prompt | have | TP-GROK-CLI-30..34 |
| Online curl / companion checksum / version-check / self-update start line / self-uninstall | have | TP-ONL-01..05 · TP-CLI-10 |
| Folder tar.gz restore / retention | n/a | Superseded; TP-GROK-CLI-11 proves `restore` unknown |

---

## TP rows

### TP-CLI (CLI surface)

| TP-ID | Intent | Suite | Primary requirement(s) | Status |
|-------|--------|-------|------------------------|--------|
| TP-CLI-01 | `sh -n` ship unit | `tests/test_cli.sh` | requirement-shell-cli-interface · requirement-shell-script-coding | **have** |
| TP-CLI-02 | version human | test_cli | requirement-shell-cli-interface | **have** |
| TP-CLI-03 | version JSON | test_cli | requirement-shell-output-requirements | **have** |
| TP-CLI-04 | help: setup, auth verbs, version-check / self-update / self-uninstall, SCRIPT_URL; no restore; no CHECKSUM | test_cli | requirement-shell-cli-interface · requirement-domain-grok-cli · requirement-grok-setup · requirement-grok-crontab · requirement-grok-auth-backup · requirement-shell-self-management | **have** |
| TP-CLI-05 | help JSON short | test_cli | requirement-shell-output-requirements | **have** |
| TP-CLI-06 | about JSON cache_used / cache_preferred / cache_fallback / cache_fallback_2 / persistence_storage + grok_cli_root + session; human Cache folder used, preferred, 1st, 2nd + Persistence storage | test_cli | requirement-shell-cli-storage · requirement-domain-grok-cli | **have** |
| TP-CLI-07 | empty argv: off-TTY Type O already-installed (not help); `--json` no command JSON help (TTY **and** off-TTY — 0-argv special case, not the list); TTY numbered list | test_cli | requirement-shell-cli-zero-arguments · requirement-shell-cli-default-interaction | **have** |
| TP-CLI-29 | overlay flags-only (`--debug`, `--quiet`) follow empty argv (TTY menu / off-TTY Type O ensure); `--json --debug` no command stays JSON help | test_cli | requirement-shell-cli-zero-arguments · requirement-shell-cli-default-interaction · requirement-shell-cli-interface | **have** |
| TP-CLI-08 | unknown fail-closed | test_cli | requirement-shell-cli-interface | **have** |
| TP-CLI-09 | quiet suppresses version | test_cli | requirement-shell-output-requirements | **have** |
| TP-CLI-10 | version-check / self-update routed (not unknown) | test_cli | requirement-shell-self-management · requirement-bootstrap-chain | **have** |
| TP-CLI-11 | env -u HOME version | test_cli | requirement-shell-script-coding | **have** |
| TP-CLI-12 | Linux preferred `/dev/shm/cache/cache-${APP_NAME}-${login}-$$`; Git Bash and Mac chains and about lines; silent skip of preferred; leaf mode 0700; persistence `${HOME}/.local/${APP_NAME}`; live dir exists; not `/dev/shm/${APP_NAME}-${login}`; persistence not USER_BIN | test_cli | requirement-shell-cli-storage | **have** |
| TP-CLI-13 | `menu`/`main`: TTY top list is **1** grok-auth, **7** sudoers, **8** self-management, **9** Exit, and has no Back row; **0** on the top list retries; auth submenu **11–16** (**13** hidden when logged out) with **0** Back and **9** Exit; sudoers submenu **0** Back / **9** Exit; ignore `--json` on TTY; off-TTY `menu` help; empty argv off-TTY is Type O ensure (not help); `sudoers` not dispatched | `tests/test_cli.sh` | requirement-shell-cli-default-interaction · requirement-shell-cli-zero-arguments | **have** |
| TP-CLI-15 | Static: ship unit has no `$(prompt_ask` / `$(prompt_yes_no` (T1-PROMPT-CAPTURE; **TP-ELEV-10**) | `tests/test_cli.sh` | requirement-shell-script-coding · interactive-vs-noninteractive | **have** |
| TP-CLI-17 | Default CLI main menu style: header `APP_NAME(APP_VERSION)` bold/italic; numbered explain italic + light gray SGR 3+37; number/name unstyled; not SGR 90; session line under title is independent `[INFO]`; no `check-session` row; submenu nametag; inherited `APP_VERSION` ignored | `tests/test_cli.sh` | requirement-shell-cli-default-interaction · requirement-shell-output-requirements | **have** |
| TP-CLI-18 | Active `requirement-*.md` samples do not freeze a session Unix login | `tests/test_cli.sh` | requirement-sudoer-json-file · requirement-three-layer-privilege-model · requirement-domain-grok-cli | **have** |
| TP-CLI-19 | Termux / Git Bash / Windows cmd top list is **1** grok-auth, **2** run, **8** self-management, **9** Exit, no Back, and hides sudoers; host not-available is independent `[INFO]` under session; auth hides backup and, when logged out, `sync-auth-to-remote`; pick **5** does not open sudoers; multi-user host unchanged | `tests/test_cli.sh` | requirement-shell-cli-default-interaction | **have** |
| TP-CLI-20 | Logged-in top list keeps **1** grok-auth, **7** sudoers, **8** self-management, **9** Exit, and has no Back; auth hides **12** and lists **13**; appends logged-in not-available line; host not-available line kept on this-login-only; this-login-only still lists **2** run; listed **7** opens the sudoers submenu; pick of a hidden verb is not a menu choice | `tests/test_cli.sh` | requirement-shell-cli-default-interaction | **have** |
| TP-CLI-21 | Termux menu uses local auth cookies (no live grok -p hello); hang grok + no cookies → **logged out** instantly; no freeze | `tests/test_cli.sh` | requirement-shell-cli-default-interaction · requirement-grok-auth-backup · requirement-shell-termux-coding | **have** |
| TP-CLI-22 | Termux hang-grok: bad pick reprints the list; `grok -p hello` runs once | `tests/test_cli.sh` | requirement-shell-cli-default-interaction · requirement-grok-auth-backup | **have** |
| TP-CLI-23 | Ship unit always bounds the probe (`timeout -k` + watchdog `kill -9` + setsid + ignore TSTP + wait reaper first + checking-session; default `GROK_PROMPT_TIMEOUT` 14; menu prints `out_info "timeout"`) | `tests/test_cli.sh` | requirement-grok-auth-backup · requirement-shell-termux-coding · requirement-shell-cli-default-interaction | **have** |
| TP-CLI-25 | `--debug menu` prints start + elapsed for each paint step (`paint` `header` `session` `host` `logged-in` `rows` plus `sudoers.*` on the submenu) | `tests/test_cli.sh` | requirement-shell-internal-volatile-timer · requirement-shell-cli-default-interaction | **have** |
| TP-CLI-26 | `menu` without `--debug` has no menu-step elapsed lines | `tests/test_cli.sh` | requirement-shell-internal-volatile-timer · requirement-shell-cli-default-interaction | **have** |
| TP-CLI-27 | `--json --debug version` stdout stays JSON (no `[DEBUG]`) | `tests/test_cli.sh` | requirement-shell-internal-volatile-timer · requirement-shell-cli-interface · requirement-shell-output-requirements | **have** |
| TP-CLI-28 | Ship unit has `util_int_timer_*`; AC-6 double-start fail-closed; invalid stage names rejected; help lists `--debug`; help has no timer `start` verb | `tests/test_cli.sh` | requirement-shell-internal-volatile-timer · requirement-shell-cli-interface | **have** |
| TP-CLI-30 | Invalid TTY menu choice at any layer retries that layer (`out_error` + reprint; unused front integer **4** and unknown name; sudoers submenu unused **6** stays on that list; Termux unused front integer is **6**; not unknown argv). Top list has no Back, so **0** there retries; submenu **0** is still Back. Portable proof mold names this **TP-CLI-19**; this product already assigned **TP-CLI-19** to this-login-only host menu | `tests/test_cli.sh` | requirement-shell-cli-default-interaction | **have** |
| TP-CLI-32 | Menu language: front **5** lists **51–63**; **50** and **64–69** are not printed; front **6** warns and does not write; save writes `${HOME}/.local/${APP_NAME}/language` mode 0600; Back does not write; next run uses the file; `GROK_CLI_LANG` overrides without writing; human help and about follow the code; English menu stays the existing literals | `tests/test_cli.sh` | requirement-shell-cli-language · requirement-shell-cli-default-interaction · requirement-shell-cli-storage | **have** |
| TP-CLI-31 | TTY main list includes `reinstall` (multi-user **5**; this-login-only **2**); `setup` and `update-grok` stay off | `tests/test_cli.sh` | requirement-shell-cli-default-interaction · requirement-grok-setup | **have** |

### TP-LC (local lifecycle)

| TP-ID | Intent | Suite | Primary requirement(s) | Status |
|-------|--------|-------|------------------------|--------|
| TP-LC-01 | install → USER_BIN | test_local_lifecycle | requirement-shell-local-self-management · requirement-shell-termux-coding | **have** |
| TP-LC-02 | installed binary version | test_local_lifecycle | local self-management | **have** |
| TP-LC-03 | reinstall already-installed | test_local_lifecycle | requirement-shell-idempotency | **have** |
| TP-LC-04 | where-is-me | test_local_lifecycle | local self-management | **have** |
| TP-LC-05 | uninstall JSON no force fail-closed | test_local_lifecycle | interactive-vs-noninteractive | **have** |
| TP-LC-06 | uninstall --force removes | test_local_lifecycle | local self-management | **have** |
| TP-LC-07 | uninstall absent no-op | test_local_lifecycle | idempotency | **have** |
| TP-LC-08 | about shows installed | test_local_lifecycle | local self-management | **have** |
| TP-LC-09 | installed mode is `0755` | test_local_lifecycle | local self-management | **have** |
| TP-LC-10 | reinstall heals `0711` → `0755` | test_local_lifecycle | local self-management | **have** |
| TP-LC-11 | install creates `~/.bashrc` with exact PATH | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-12 | install creates `~/.profile` sourcing bashrc | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-13 | second install does not duplicate PATH | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-14 | existing `.profile` body kept | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-20 | `BASHRC` env create-if-missing | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-21 | `BASHRC` env modify dongle | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-22 | `BASHRC` env VERSION+exact-PATH no-op | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-23 | `ZSHENV` env modify existing | test_local_lifecycle | requirement-shell-zshenv | **have** |
| TP-LC-24 | `ZSHENV` env no-op | test_local_lifecycle | requirement-shell-zshenv | **have** |
| TP-LC-25 | `PROFILE` env create-if-absent | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-26 | `PROFILE` env keep body | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-27 | already-installed skip heals missing PATH | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-28 | sibling comment + exact PATH, grok-cli sticker MAY | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-29 | grok-cli comment present, PATH restored | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-31 | vendor grok installer block unchanged | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-32 | uninstall keeps PATH while `USER_BIN` has files | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-33 | sudoer-cli login-hook block kept | test_local_lifecycle | requirement-shell-path-and-shell-support | **have** |
| TP-LC-34 | `ZSHENV` env create-if-missing | test_local_lifecycle | requirement-shell-zshenv | **have** |
| TP-LC-35 | bash-only does not invent `.zshenv` | test_local_lifecycle | requirement-shell-zshenv | **have** |
| TP-LC-36 | `.zshrc` unchanged for PATH | test_local_lifecycle | requirement-shell-zshenv | **have** |
| TP-LC-37 | `$0` `-ash` writes shared PATH on `.profile` and keeps the bash source block | test_local_lifecycle | requirement-shell-alpine | **have** |
| TP-LC-38 | `$0` `sh` without alpine-release does not write that PATH line | test_local_lifecycle | requirement-shell-alpine | **have** |
| TP-LC-39 | Alpine `sh` (`$0` `sh` plus release file) writes the PATH line | test_local_lifecycle | requirement-shell-alpine | **have** |
| TP-LC-40 | `rc-test --file ash` writes the fixture `.profile` only | test_local_lifecycle | requirement-shell-alpine · requirement-shell-cli-interface | **have** |
| TP-LC-41 | Missing `.profile` for bash, zsh, and fish is generated (source `.bashrc`) with no PATH export | test_local_lifecycle | requirement-shell-alpine · requirement-shell-path-and-shell-support | **have** |
| TP-LC-42 | Existing `.profile` plus ash appends PATH and keeps the old body | test_local_lifecycle | requirement-shell-alpine | **have** |
| rc-test | routed `--root` create; real home rc untouched | test_local_lifecycle | requirement-shell-path-and-shell-support · requirement-shell-cli-interface · requirement-shell-zshenv | **have** |

### TP-VCLI (vendor peer grok installer)

| TP-ID | Intent | Suite | Primary requirement(s) | Status |
|-------|--------|-------|------------------------|--------|
| TP-VCLI-01 | `setup` is routed | `tests/test_grok_setup.sh` | requirement-grok-setup · requirement-shell-cli-interface | **have** |
| TP-VCLI-02 | help lists setup, self-update, SCRIPT_URL; no `install.sh` | test_grok_setup | requirement-grok-setup · requirement-domain-grok-cli | **have** |
| TP-VCLI-03 | TTY menu excludes setup | test_cli (TP-CLI-13) | requirement-shell-cli-default-interaction | **have** |
| TP-VCLI-04 | grok already on PATH → no-op, no curl | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-05 | `--force` fetches channel pointer + artifact (not `install.sh`) | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-06 | curl fail → operator-readable Next | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-07 | missing curl → fail closed | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-08 | fake fetch places `grok` under `~/.grok/bin`, not grok-cli | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-09 | JSON `status` installed / already_installed | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-10 | live x.ai fetch | — | requirement-grok-setup | **optional** |
| TP-VCLI-11 | vendor `~/.grok/bin` + stale session PATH → exit 0, not `[ERROR]` | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-12 | binary download fail → fail closed, no USER_BIN PATH hint | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-13 | curl log MUST NOT contain `install.sh` | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-14 | curl log contains channel pointer and `grok-` artifact | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-15 | smoke `--version` runs under `~/.grok/downloads` (not cache/`/tmp`/`/dev/shm`) | test_grok_setup | requirement-grok-setup · requirement-shell-termux-coding · requirement-project-folder | **have** |
| TP-VCLI-16 | smoke `--version` fail → operator-readable Next + captured stderr | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-17 | existing grok that cannot run (wrong arch / exec fail) is not `already_installed`; fetch proceeds | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-18 | downloaded ELF `e_machine` mismatch → fail closed, no place | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-19 | Android `e_type` 2 smoke fail after retries → Next `pkg install proot` (not “check the download”) | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-20 | Android smoke succeeds only with TERMUX_EXEC_OPTOUT → POSIX wrapper; vendor file unchanged | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-21 | Android smoke succeeds only under `proot` → wrapper execs `proot` | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-22 | Termux: opt-out fail, `proot` missing, `pkg` present → `pkg install -y proot` then proot wrapper | test_grok_setup | requirement-grok-setup · requirement-shell-termux-coding | **have** |
| TP-VCLI-23 | Termux `pkg install` fail → fail closed, Next `pkg install proot`, no place | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-24 | artifact HTTP 403 → error names `HTTP 403` | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-25 | Android + no nameserver → `~/.grok/resolv.conf` + wrapper `proot -b …:/etc/resolv.conf` | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-26 | Android `proot` wrapper source contains `--kill-on-exit` (not `-k`) | test_grok_setup | requirement-grok-setup · requirement-shell-termux-coding | **have** |
| TP-VCLI-27 | Android wrapper injects `--no-auto-update` for `-p` and SIGKILLs the child on SIGINT | test_grok_setup | requirement-grok-setup · requirement-shell-termux-coding | **have** |
| TP-VCLI-28 | Already-installed Android `proot` wrapper lacking `--kill-on-exit` is rewritten with no curl | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-29 | Android `proot` wrapper source contains `proot-exit-reaper` and matches args/exe | test_grok_setup | requirement-grok-setup · requirement-shell-termux-coding | **have** |
| TP-VCLI-30 | Already-installed wrapper with `--kill-on-exit` but no `proot-exit-reaper` is rewritten with no curl | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-31 | Android `proot` wrapper binds `/dev/null` over `profile.d/start-services.sh` | test_grok_setup | requirement-grok-setup · requirement-shell-termux-coding | **have** |
| TP-GROK-CLI-46 | `run` injects `--no-auto-update`; missing grok Next setup; `--json` does not exec | test_domain_grok_cli | requirement-grok-setup · requirement-shell-cli-interface · requirement-domain-grok-cli | **have** |

### TP-ONL (grok-cli channel install)

| TP-ID | Intent | Suite | Primary requirement(s) | Status |
|-------|--------|-------|------------------------|--------|
| TP-ONL-01 | off-TTY empty argv places `USER_BIN/grok-cli` (fake curl; not help; not x.ai `install.sh`) | `tests/test_online_install.sh` | requirement-shell-online-install · requirement-shell-cli-zero-arguments | **have** |
| TP-ONL-02 | companion digest mismatch aborts | test_online_install | requirement-shell-automatic-checksum | **have** |
| TP-ONL-03 | `version-check --json` reports remote_version | test_online_install | requirement-shell-self-management | **have** |
| TP-ONL-04 | `self-uninstall --force` removes managed binary | test_online_install | requirement-shell-self-management | **have** |
| TP-ONL-05 | proceeding `self-update` first INFO is `Starting the self-update of {{APP_NAME}}({{local}}) to new version:{{remote}}...` | test_online_install | requirement-shell-self-management · requirement-shell-cli-interface | **have** |

### TP-GROK-CLI (domain + privilege + auth ops)

| TP-ID | Intent | Suite | Primary requirement(s) | Status |
|-------|--------|-------|------------------------|--------|
| TP-GROK-CLI-01 | print-sudoers NOPASSWD grok-cli backup; no restore; no OS tools; no `/etc` write | test_domain_grok_cli | three-layer · domain | **have** |
| TP-GROK-CLI-01b | refuse test_local without `--allow-test-local` | test_domain_grok_cli | three-layer | **have** |
| TP-GROK-CLI-02 | print-sudoers to path; user-bound | test_domain_grok_cli | three-layer | **have** |
| TP-GROK-CLI-03 | check-session missing peer grok; Next setup then grok login | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-04 | `auth.json` looks valid but `grok -p hello` fails | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-05 | `grok -p hello` exit 0; no grok answer leak | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-06 | backup without session fail-closed | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-07 | backup writable GROK_CLI_ROOT; dest 0644 | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-08 | backup overwrite same basenames | test_domain_grok_cli | grok-auth-backup · idempotency | **have** |
| TP-GROK-CLI-09 | sync-auth dest 0600 no sudo | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-10 | sync-auth missing store fail-closed | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-11 | `restore` is unknown | test_domain_grok_cli | domain | **have** |
| TP-GROK-CLI-12 | `/var/grok-cli` without global binary fail-closed | test_domain_grok_cli | grok-auth-backup · three-layer | **have** |
| TP-GROK-CLI-14 | print-sudoers-install-script | test_domain_grok_cli | three-layer | **have** |
| TP-GROK-CLI-15 | remove-project-sudoers draft-only | test_domain_grok_cli | three-layer · interactive | **have** |
| TP-GROK-CLI-15b | multi-draft needs path | test_domain_grok_cli | three-layer | **have** |
| TP-GROK-CLI-19 | submit missing sudoer-cli | test_domain_grok_cli | three-layer | **have** |
| TP-GROK-CLI-20 | submit stub inbound | test_domain_grok_cli | three-layer | **have** |
| TP-GROK-CLI-21 / 21b | public inbound first; env override; no Type 0 mkdir | test_domain_grok_cli | three-layer · domain | **have** |
| TP-GROK-CLI-22 / 22b / 22c / 22d / 22e / 22f | JSON grant backup only; no OS tools; convert; inbound | test_domain_grok_cli | sudoer-json-file | **have** |
| TP-GROK-CLI-23 / 23b / 23c | host fragment → update default | test_domain_grok_cli | three-layer | **have** |
| TP-GROK-CLI-24 / 24b / 24c / 24d | independent generate dest readable | test_domain_grok_cli | sudoer-json-file · three-layer | **have** |
| TP-GROK-CLI-25 / 25b / 25c | operator-readable inbound incomplete | test_domain_grok_cli | operator-readable-error | **have** |
| TP-GROK-CLI-26 / 26b | add-crontab fail-closed without this login’s backup grant; wrong-user / wrong-argv / sibling fragment refused | test_domain_grok_cli | grok-crontab | **have** |
| TP-GROK-CLI-27 | add-crontab fail-closed without global binary | test_domain_grok_cli | grok-crontab | **have** |
| TP-GROK-CLI-28 / 28b | isolated crontab gets studied backup + sync-auth jobs on GLOBAL_BIN; user is `id -un` | test_domain_grok_cli | grok-crontab | **have** |
| TP-GROK-CLI-29 / 29b | re-run does not duplicate; other crontab lines kept | test_domain_grok_cli | grok-crontab · idempotency | **have** |
| TP-GROK-CLI-30 / 30b | sync-auth-from-remote missing/invalid SPEC fail-closed | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-31 / 31b / 31c / 31d | four SPEC forms (IPv4, user@IPv4, domain, user@domain) via fake scp | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-32 | dest auth.json mode 0600 | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-33 | missing remote auth fail-closed with Next: | test_domain_grok_cli | grok-auth-backup · operator-readable-error | **have** |
| TP-GROK-CLI-34 | TTY menu `sync-auth-from-remote` row (main **3**) shows SPEC prompt; typed SPEC is not mixed with prompt text; fake scp completes (INC-20260902-001) | test_domain_grok_cli | grok-auth-backup · interactive-vs-noninteractive · output | **have** |
| TP-GROK-CLI-35 | expired `auth.json` + `grok -p hello` ok → logged in (live probe wins) | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-36 | grok `-p hello` stdout/stderr not printed (no token leak) | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-37 | Core tests fake `GROK_BIN`; no public network | test_domain_grok_cli | grok-auth-backup · termux-coding | **have** |
| TP-GROK-CLI-38 | valid-looking `auth.json` without grok is not logged in | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-39 | elevated (`uid 0` + `SUDO_USER`) `grok -p hello` uses invoking grok home, not `/root` | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-40 | grant present + elevated child fail → Next `grok login` (not generate-sudoer-request) | test_domain_grok_cli | grok-auth-backup · operator-readable-error | **have** |
| TP-GROK-CLI-41 | successful `sync-auth-from-remote` saves SPEC to persistence `preferred-remote` (0600); TTY prompt shows `[SPEC]` at the end; Enter uses that default | test_domain_grok_cli | grok-auth-backup · shell-cli-storage | **have** |
| TP-GROK-CLI-42 | `sync-auth` with valid live session does not copy; prints `No sync-auth for logged-in environment.`; dest unchanged; menu hides the row | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-43 | `sync-auth-from-remote` with valid live session does not scp; same skip message; dest unchanged | test_domain_grok_cli | grok-auth-backup | **have** |
| TP-GROK-CLI-44 | SIGTERM-ignoring grok still fail-closes `check-session` within the bound as **timed out** (not “not logged in”; GNU `timeout -k`; no freeze) | test_domain_grok_cli | grok-auth-backup · termux-coding | **have** |
| TP-GROK-CLI-45 | same hang without GNU `timeout -k` uses POSIX watchdog; still fail-closes as **timed out** | test_domain_grok_cli | grok-auth-backup · termux-coding | **have** |
| TP-GROK-CLI-47 | Ship unit dispatches `command -v proot` → `gc_grok_p_once_run` (reaper marker) | test_domain_grok_cli | grok-auth-backup · termux-coding · domain | **have** |
| TP-GROK-CLI-48 | Fake `proot` on PATH: instant grok `check-session` still exit 0 (reaper path, no freeze) | test_domain_grok_cli | grok-auth-backup · termux-coding | **have** |
| TP-GROK-CLI-49 | Reaper `setsid` / ignore TSTP / wait reaper first; `self-update` calls wrapper heal | test_domain_grok_cli | grok-auth-backup · termux-coding · self-management | **have** |
| TP-GROK-CLI-50 | `sync-auth-to-remote` pushes local `auth.json` to remote `~/.grok` via fake ssh+scp (0600 chmod); missing local auth and bad SPEC fail closed; a valid session still pushes; JSON has no token | test_domain_grok_cli | grok-auth-backup · shell-cli-interface · operator-readable-error | **have** |
| TP-VCLI-32 | `self-update` already-at-remote heals a stale Android wrapper (no vendor re-download) | test_grok_setup | grok-setup · self-management | **have** |
| TP-VCLI-33 | `update-grok` is routed; help lists it distinct from grok-cli `self-update` | test_grok_setup | requirement-grok-setup · requirement-shell-cli-interface · INC-20260910-002 | **have** |
| TP-VCLI-34 | `update-grok` with no grok fail-closes; Next `setup` | test_grok_setup | requirement-grok-setup · requirement-operator-readable-error | **have** |
| TP-VCLI-35 | already-installed grok is fetched again (channel+artifact; not grok auto-update); JSON `update-grok`/`updated` | test_grok_setup | requirement-grok-setup · INC-20260910-002 | **have** |
| TP-VCLI-36 | Git Bash/MINGW: `windows-*` `.exe` fetch; `bin/grok.exe` copy; no USER_BIN symlink | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-37 | TTY `setup` when grok already runs: pick keep / `1` is already_installed, no curl | test_grok_setup | requirement-grok-setup · interactive | **have** |
| TP-VCLI-38 | TTY `setup` pick reinstall / `2` fetches channel+artifact; `auth.json` kept | test_grok_setup | requirement-grok-setup · interactive | **have** |
| TP-VCLI-39 | TTY `setup` pick Exit / `9` is cancelled, no curl | test_grok_setup | requirement-grok-setup · interactive | **have** |
| TP-VCLI-40 | `reinstall` is routed; help lists it (keeps auth; not grok-cli) | test_grok_setup | requirement-grok-setup · requirement-shell-cli-interface | **have** |
| TP-VCLI-41 | `reinstall` with no grok still fetches (JSON `reinstall`/`reinstalled`) | test_grok_setup | requirement-grok-setup | **have** |
| TP-VCLI-42 | already-installed grok is fetched again; `auth.json` kept; JSON `reinstall`/`reinstalled`; no `install.sh` / grok auto-update | test_grok_setup | requirement-grok-setup | **have** |
