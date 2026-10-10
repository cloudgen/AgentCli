# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.8.43] - 2026-10-10

### Changed

- **Auth menu by session.** On a multi-user host, **11** is `backup` only when the session is **logged in**, and **11** `sync-auth` plus **12** `sync-auth-from-remote` only when the session is **logged out** or **timeout**. `sync-auth` copies `/var/grok-cli/auth.*` into `~/.grok`. Termux / Git Bash / Windows cmd still omit **11**. **13** stays hidden when logged out. **14–16** do not slide. **17** is not a row. When the session is not logged in, the main list and the auth list append `[INFO]` `backup and sync-auth-to-remote features are not available for logged-out environment.` That line does not replace the host line or the logged-in line. Direct `grok-cli backup` and `grok-cli sync-auth` stay routed. Law: `requirement-shell-cli-default-interaction` **2.24.0** · `requirement-shell-cli-language` **1.1.1** · `requirement-grok-auth-backup` **1.10.1** · `requirement-domain-grok-cli` **1.10.1** · `requirement-shell-cli-interface` **2.15.4**. Suite **TP-CLI-13** · **TP-CLI-17** · **TP-CLI-19** · **TP-CLI-20** · **TP-CLI-23**.

## [1.8.42] - 2026-10-02

### Changed

- **Menu language.** Front row **5** opens **51** English, **52** 简体中文, **53** 繁體中文, **54** Español, **55** العربية, **56** Français, **57** Português, **58** Русский, **59** Deutsch, **60** 日本語, **61** 한국어, **62** Nederlands, **63** Ελληνικά. **50** and **64–69** stay reserved and are not printed. Front **6** is not a row. The choice is saved at `~/.local/grok-cli/language` (mode 0600) and the next run opens in that language. `GROK_CLI_LANG` overrides one run and does not write the file. Human `help` and human `about` follow the code. Leaf command names, JSON, and argv `version` stay English. `language` is not a shell command. Row **5** is on every host, including Termux, Git Bash, and Windows cmd. Law: `requirement-shell-cli-language` **1.1.0** · `requirement-shell-cli-default-interaction` **2.22.0** · `requirement-shell-cli-storage` **1.4.1** · `requirement-shell-cli-interface` **2.15.3**. Suite **TP-CLI-32** · **TP-CLI-13** · **TP-CLI-19** · **TP-CLI-20** · **TP-CLI-30**.

## [1.8.41] - 2026-09-28

### Added

- **Menu language.** Front row **6** opens **61** English, **62** 繁體中文, **63** Español, **64** Français, **65** Deutsch, **66** 简体中文, **67** 日本語, **68** 한국어. The choice is saved at `~/.local/grok-cli/language` (mode 0600) and the next run opens in that language. `GROK_CLI_LANG` overrides one run and does not write the file. Human `help` and human `about` follow the code. Leaf command names, JSON, and argv `version` stay English. `language` is not a shell command. Row **6** is on every host, including Termux, Git Bash, and Windows cmd. Law: `requirement-shell-cli-language` **1.0.0** · `requirement-shell-cli-default-interaction` **2.21.0** · `requirement-shell-cli-storage` **1.4.1** · `requirement-shell-cli-interface` **2.15.2**. Suite **TP-CLI-32** · **TP-CLI-13** · **TP-CLI-20** · **TP-CLI-30**.

## [1.8.40] - 2026-09-27

### Changed

- **Cache folder.** Each login and each process gets its own leaf. Linux: `/dev/shm/cache/cache-${APP_NAME}-${login}-$$`, then `/tmp/cache/cache-${APP_NAME}-${login}-$$`, then `${HOME}/.cache/cache-${APP_NAME}-$$`. Git Bash: `/tmp/cache/cache-${APP_NAME}-${login}-$$`, then `${HOME}/AppData/Local/Temp/cache-${APP_NAME}-$$`. Mac: `/tmp/cache/cache-${APP_NAME}-${login}-$$`, then `${HOME}/Library/Caches/cache-${APP_NAME}-$$`, then `${HOME}/cache/cache-${APP_NAME}-$$`. Skipping a tier prints no warning and no error. `about` prints **Cache folder used**, **preferred**, **1st fallback**, and **2nd fallback** when that host has one. Law: `requirement-shell-cli-storage` **1.4.0**. Suite **TP-CLI-06** · **TP-CLI-12**.

## [1.8.39] - 2026-09-26

### Changed

- **Top menu:** the start list has no Back row. It is **1** grok-auth, **7** sudoers, **8** self-management, and **9** Exit. This-login-only hosts also show **2** run and omit **7**. **0** / `back` on the top list is a wrong pick and reprints that list. Submenus still use **0** Back and **9** Exit. Auth rows stay **11–16**. Self-management stays **91–94**. Law: `requirement-shell-cli-default-interaction` **2.20.0**. Suite **TP-CLI-13** · **TP-CLI-19** · **TP-CLI-20** · **TP-CLI-30**.

## [1.8.38] - 2026-09-22

### Changed

- **Menu keys:** top list is **1** grok-auth, **7** sudoers, **8** self-management, **9** Exit, **0** Back. Submenus use **0** Back and **9** Exit. Auth rows stay **11–16**. Self-management stays **91–94**. Law: `requirement-shell-cli-default-interaction` **2.19.1**. Suite **TP-CLI-13** · **TP-CLI-19** · **TP-CLI-20** · **TP-CLI-30**.

## [1.8.37] - 2026-09-22

### Changed

- **Main menu families:** the top list is **1** `grok-auth`, **8** `sudoers`, **9** `self-management`, and **0** Exit. This-login-only hosts also show **2** `run` and omit **8**. Inside **1**: **11** backup, **12** sync-auth-from-remote (hidden when logged in), **13** sync-auth-to-remote (hidden when logged out), **14** add-crontab, **15** setup, **16** reinstall. Inside **9**: **91** version-check, **92** self-update, **93** self-uninstall, **94** where-is-me. Law: `requirement-shell-cli-default-interaction` **2.19.0**. Suite **TP-CLI-13** · **TP-CLI-19** · **TP-CLI-20** · **TP-CLI-31**.

## [1.8.36] - 2026-09-22

### Added

- **Alpine ash PATH on `.profile`:** one missing-file step. Bash, zsh, and fish **generate** `~/.profile` (login sources `~/.bashrc`) and do not put `~/.local/bin` on that new file. Ash, including Alpine `curl | sh` (`$0` is `sh` and `/etc/alpine-release` exists), generates that same file and adds `export PATH="$HOME/.local/bin:$PATH"` in the same step. If `.profile` already exists, only ash modifies it by appending that line. Law: `requirement-shell-alpine` **1.0.0** · `requirement-shell-path-and-shell-support` **1.2.0** · `requirement-shell-cli-interface` **2.15.0**. Suite **TP-LC-37** · **TP-LC-38** · **TP-LC-39** · **TP-LC-40** · **TP-LC-41** · **TP-LC-42**.

## [1.8.35] - 2026-09-22

### Added

- **`sync-auth-to-remote`:** copy this login’s `~/.grok/auth.*` onto a remote login’s `~/.grok` (`ssh` + `scp` BatchMode, no sudo, remote `auth.json` mode `0600`). Same SPEC forms as `sync-auth-from-remote`. A grok session that is already logged in still pushes. The numbered start list shows this row only when logged in (multi-user **2**; Termux / Git Bash / Windows cmd **3**) and hides it when logged out. Logged-out multi-user order stays backup, sync-auth, sync-auth-from-remote, add-crontab, reinstall, sudoers (**6**). Law: `requirement-grok-auth-backup` **1.10.0** · `requirement-shell-cli-interface` **2.14.0** · `requirement-shell-cli-default-interaction` **2.18.0** · `requirement-domain-grok-cli` **1.10.0**. Suite **TP-GROK-CLI-50** · **TP-CLI-13** · **TP-CLI-19** · **TP-CLI-20**.

## [1.8.34] - 2026-09-17

### Changed

- **Zsh PATH lives on `.zshenv`, not `.zshrc`:** user-bin install writes the shared `export PATH="$HOME/.local/bin:$PATH"` line to `.zshenv` (create when `$SHELL` is zsh or `ZSHENV` is set; modify if the file exists). `.zshrc` is left alone. `rc-test --file zshenv` is routed; `--file zshrc` fails closed. Peer grok vendor `# >>> grok installer >>>` block for `~/.grok/bin` also lands on `.zshenv` when `$SHELL` is zsh. Law: `requirement-shell-zshenv` **1.0.0** · `requirement-shell-path-and-shell-support` **1.1.0** · `requirement-shell-cli-interface` **2.13.0** · `requirement-grok-setup` **2.16.0**. Suite **TP-LC-23** · **TP-LC-24** · **TP-LC-34** · **TP-LC-35** · **TP-LC-36**.

## [1.8.33] - 2026-09-14

### Added

- **`reinstall`:** remove existing grok and install again from xAI (same place path as `setup --force`). Keeps `auth.*`. Does **not** update grok-cli (`self-update` stays that). Missing grok still fetches. JSON `type=reinstall` `status=reinstalled`. On the numbered start list: **5** on a multi-user host when logged out (before **sudoers**); **2** on Termux / Git Bash / Windows cmd (after **`run`**). `setup` and `update-grok` stay off that list. Law: `requirement-grok-setup` **2.15.0** · `requirement-shell-cli-interface` **2.12.0** · `requirement-domain-grok-cli` **1.9.0** · `requirement-shell-cli-default-interaction` **2.16.0**. Suite **TP-VCLI-40** · **TP-VCLI-41** · **TP-VCLI-42** · **TP-CLI-31**.

## [1.8.32] - 2026-09-13

### Fixed

- **Wrong pick on the numbered menu (or the sudoers list) no longer looks like a dead end:** unused numbers and unknown names print `[ERROR]`, show **that same list** again, and wait for another pick. They do not quit and they are not treated as an unknown CLI command. Law: `requirement-shell-cli-default-interaction` **2.15.0**. Suite **TP-CLI-30**.

## [1.8.31] - 2026-09-12

### Added

- **TTY `setup` reinstall list:** when grok already runs on this host, `grok-cli setup` at a real terminal shows **keep** / **reinstall** / **Exit** instead of a silent skip. Pick **2** fetches a new grok (same as `--force`); the old file stays until `--version` succeeds; `auth.*` is not deleted. `--json` / pipes still skip. `--force` still skips the list. Law: `requirement-grok-setup` **2.14.0** · `requirement-shell-cli-interface` **2.11.0** · `requirement-domain-grok-cli` **1.8.0** · `requirement-shell-interactive-vs-noninteractive` **1.0.5**. Suite **TP-VCLI-37** · **TP-VCLI-38** · **TP-VCLI-39**.

## [1.8.30] - 2026-09-10

### Added

- **Git Bash / MSYS / Cygwin `setup`:** `uname` maps to `windows-*`; fetch `grok-{{version}}-windows-{{arch}}.exe`; copy `~/.grok/bin/grok.exe` and `agent.exe` (no USER_BIN symlink). Native PowerShell stays `irm https://x.ai/cli/install.ps1 | iex`. README host comparison tables. Law: `requirement-grok-setup` **2.13.0**. Suite **TP-VCLI-36**.

## [1.8.29] - 2026-09-10

### Added

- **`update-grok`:** refresh peer `grok` from the xAI channel + artifact (same place path as `setup --force`). Does **not** use grok auto-update (unsupported on Termux). Does **not** update grok-cli (`self-update` stays that). Missing grok Next `grok-cli setup`. Help one-liner: `Update grok from x.ai (not grok-cli; avoids grok auto-update)`. Law: `requirement-grok-setup` **2.12.0** · `requirement-shell-cli-interface` **2.10.0** · `requirement-domain-grok-cli` **1.7.0**. Suite **TP-VCLI-33** · **TP-VCLI-34** · **TP-VCLI-35**. Incident **INC-20260910-002**.

## [1.8.28] - 2026-09-09

### Fixed

- **Menu login status and not-available lines had no `[INFO]`:** on Termux the list printed `[INFO] grok-cli(…)` then untagged `logged out` and untagged `backup, sync-auth and sudoers features are not available in termux.` Each of those lines is now its own `out_info`. Same for `timeout`, `logged in`, and the logged-in not-available sentence. Law: `requirement-shell-cli-default-interaction` **2.14.0**. Suite **TP-CLI-17** · **TP-CLI-19** · **TP-CLI-20** · **TP-CLI-23**.

## [1.8.27] - 2026-09-09

### Added

- **Shell-rc topic-owner:** `requirement-shell-path-and-shell-support` — one shared `USER_BIN` PATH line, create `.bashrc` / `.profile` if missing, sibling unify with sshd-cli / sudoer-cli / dns-cli, scoped uninstall (only `# Added by grok-cli installer`), heal on already-installed skip (**L-PATH-01**), routed Type 0 `rc-test --root`. Dual mention `requirement-shell-cli-interface` **2.9.0**. Suite **TP-LC-11..14**, **TP-LC-20..29**, **TP-LC-31..33**.

### Changed

- User-bin `install` / channel ensure / `self-update` always run PATH+profile companion, including already-installed. `uninstall` / `self-uninstall` remove only grok-cli stickers; keep the shared PATH line while `~/.local/bin` still has files; never delete `.profile` or the vendor `# >>> grok installer >>>` block.

## [1.8.26] - 2026-09-07

### Changed

- **PRoot/Termux login check uses local auth cookies:** `grok -p hello` under PRoot is usually timeout and is no longer the session gate there. The numbered list, `check-session`, `about`, and `backup` read `~/.grok/auth.json` (`refresh_token` / `key` / future `expires_at`). No `checking session (grok -p hello, timeout 14s)...` wait on that class. **`GROK_PROMPT_TIMEOUT`** (default 14) and the live-probe functions stay in the ship unit, **protected**, for future / non-PRoot use. Law: `requirement-grok-auth-backup` **1.9.0** · `requirement-shell-cli-default-interaction` **2.13.0**. Suite **TP-CLI-21** · **TP-CLI-22** · **TP-CLI-23** · **TP-GROK-CLI-03..05** · **TP-GROK-CLI-35** · **TP-GROK-CLI-38** · **TP-GROK-CLI-44** · **TP-GROK-CLI-45**.

## [1.8.25] - 2026-09-07

### Fixed

- **Session probe timeout was reported as logged out:** after `checking session (grok -p hello, timeout 20s)...` a hang (Termux PRoot reaper path especially) printed **logged out**. That line is now **timeout**. A fast missing/failed peer is still **logged out**. `check-session` / `backup` say the probe timed out instead of “not logged in.” Default `GROK_PROMPT_TIMEOUT` is **14** (was 20). The PRoot reaper checks stdout/guest-death before the wall clock so a reply at the bound still counts as logged in, and empty stdout at the bound is exit 124. Law: `requirement-shell-cli-default-interaction` **2.12.0** · `requirement-grok-auth-backup` **1.8.0**. Suite **TP-CLI-21** · **TP-CLI-23** · **TP-GROK-CLI-44** · **TP-GROK-CLI-45**.

## [1.8.24] - 2026-09-07

### Fixed

- **Termux menu session probe looked hung (or never returned):** after the INFO header the live `grok -p hello` check had no non-DEBUG progress; Ctrl-Z stopped grok-cli **and** the PRoot reaper (same process group), so leftover `proot` stayed in `do_wait`. Empty stdout never counted as idle. `self-update` did not rewrite `~/.grok/bin/grok`, so a 2026-09-04 436-byte launcher could survive a grok-cli-only update. The menu now prints `checking session (grok -p hello, timeout Ns)...` before the probe. The reaper `setsid`s the collector, ignores SIGTSTP, waits the reaper first, treats first stdout byte (or guest-gone / stderr guest-death) as done, and SIGKILLs PRoot immediately. `self-update` (including already-at-remote) and the session probe heal a stale Android wrapper. Law: `requirement-shell-cli-default-interaction` **2.11.0** · `requirement-shell-termux-coding` **1.6.0** · `requirement-grok-setup` **2.11.0** · `requirement-shell-self-management` **1.2.0** · `requirement-grok-auth-backup` **1.7.0**. Suite **TP-CLI-21/23/26** · **TP-GROK-CLI-49** · **TP-VCLI-32**. Incident **INC-20260907-004**.

## [1.8.23] - 2026-09-07

### Changed

- **`self-update` start line names versions:** first INFO is `Starting the self-update of grok-cli({{local}}) to new version:{{remote}}...` after the channel `VERSION=` is fetched. No version-less `Starting self-update of grok-cli...`. Already-at-remote without `--force` does not print that start line. Law: `requirement-shell-self-management` **1.1.0** · `requirement-shell-cli-interface` **2.8.1**. Suite **TP-ONL-05**.

## [1.8.22] - 2026-09-07

### Fixed

- **On-device PRoot hang chain:** grok-linux **does** `_exit` after the reply (`grok --help` under the same PRoot returns). PRoot `wait4(-1, __WALL)` waits for leftover `runsvdir` spawned because grok’s env capture uses `bash -lc`, which sources Termux `profile.d/start-services.sh`. The wrapper now binds `/dev/null` over that file when `PREFIX` is set (does not edit Termux). The 1.8.21 reaper stays as the safety net. Law: `requirement-shell-termux-coding` **1.5.0** · `requirement-grok-setup` **2.10.0**. Suite **TP-VCLI-31**. README Introduction states why grok-cli is a better alternative than `install.sh` on Termux; Platform Compatibility prints the causal chain.

## [1.8.21] - 2026-09-07

### Fixed

- **PRoot cannot determine grok exited:** leftover discovery via truncated `comm` was inexact. `grok-linux` already exits after the reply; PRoot stays in `do_wait` (often new Termux `runsvdir` PIDs). `--kill-on-exit` never fires. Session probe: if `proot` is on PATH, run the collector/reaper (`gc_grok_p_once_run` — match args/exe, reap only new `runsvdir`, SIGKILL PRoot if needed); else simple `grok -p hello`. Android wrapper `-p` includes the same reaper (`proot-exit-reaper`); `setup` heals a wrapper that lacks the marker. Law: `requirement-shell-termux-coding` **1.4.0** · `requirement-grok-setup` **2.9.0** · `requirement-grok-auth-backup` **1.6.0** · `requirement-domain-grok-cli` **1.6.0**. Suite **TP-VCLI-29** · **TP-VCLI-30** · **TP-GROK-CLI-47** · **TP-GROK-CLI-48**. Incident **INC-20260907-003**.

## [1.8.20] - 2026-09-07

### Added

- **`run`:** start the peer grok without auto-update (`grok-cli run`, `grok-cli run -p hello`). On Termux / Git Bash / Windows cmd the numbered list puts **run** first so you do not type bare `grok` and hang until Ctrl-Z. `--json` does not exec grok. Missing grok → Next `grok-cli setup`. Law: `requirement-grok-setup` **2.8.0** · `requirement-shell-cli-interface` **2.8.0** · `requirement-domain-grok-cli` **1.5.0** · `requirement-shell-cli-default-interaction` **2.9.0**. Suite **TP-GROK-CLI-46** · **TP-CLI-04** · **TP-CLI-19** · **TP-CLI-20**.

## [1.8.19] - 2026-09-07

### Fixed

- **Termux `grok -p` hung after the answer until Ctrl-Z:** grok-cli’s menu could exit (1.8.14 bounded probe), but the operator-facing `~/.grok/bin/grok` wrapper still `exec`’d `proot` with no `--kill-on-exit` and no SIGKILL on Ctrl-C. The wrapper now passes `proot --kill-on-exit` when advertised (never `-k`, which is `--kernel-release`), injects grok `--no-auto-update` for `-p` / `--single`, and SIGKILLs the child on SIGINT so `grok -p hello` returns to the shell. `setup` rewrites a stale wrapper on skip (no `--force`, no re-download). README **Platform Compatibility** explains what PRoot is and why `-p` can hang until Ctrl-Z. Law: `requirement-grok-setup` **2.7.0** · `requirement-shell-termux-coding` **1.3.0**. Suite **TP-VCLI-26** · **TP-VCLI-27** · **TP-VCLI-28**. Incident **INC-20260907-002**.

## [1.8.18] - 2026-09-07

### Changed

- **`--json` with no command is 0-argv, special case JSON help:** even on a TTY, `grok-cli --json` prints JSON help (not the numbered list, not install-ensure). It is still empty argv (no command token). Distinct from `grok-cli menu --json` on a TTY, which still ignores `--json` and draws the list. Law: `requirement-shell-cli-zero-arguments` **2.2.0**. Suite **TP-CLI-07** TTY `--json`.

## [1.8.17] - 2026-09-07

### Fixed

- **Empty argv includes overlay switches:** `grok-cli --debug` (and `--quiet` / `--force` with no command) follows the same 0-argv path as `grok-cli` and as `DEBUG=1 grok-cli` — TTY numbered menu, off-TTY Type O install-ensure. Empty argv is **no command token** after flag parse, not `$# -eq 0`. `--json` with no command still stays JSON help. Law: `requirement-shell-cli-zero-arguments` **2.1.0**. Suite **TP-CLI-29**.

## [1.8.16] - 2026-09-07

### Added

- **Debug mode menu elapsed:** `grok-cli --debug menu` prints how many seconds each numbered-list paint step took (`header`, `session`, `host`, `logged-in`, `rows`, outer `paint`; sudoers submenu uses `sudoers.*`). Named in-process start/stop/status/elapsed/kill/reset/list helpers specialize sibling **timer** contracts without adding `grok-cli start` domain verbs. Stage ids allow only `[-._a-zA-Z0-9]` (no glob/shell metas). Law: `requirement-shell-internal-volatile-timer` **1.0.0** · `requirement-shell-cli-default-interaction` **2.8.0**. Suite **TP-CLI-25** · **TP-CLI-26** · **TP-CLI-27** · **TP-CLI-28** (AC-6 double-start).

## [1.8.14] - 2026-09-07

### Fixed

- **Main menu freeze on Termux:** `grok -p hello` under the Termux `proot` wrapper can ignore SIGTERM, so GNU `timeout` without `--kill-after` waited forever after the header. The live probe is **always** bounded (`GROK_PROMPT_TIMEOUT`, default 20) even when `timeout` is missing. GNU `timeout -k` (`GROK_PROMPT_KILL_AFTER`, default 2) sends SIGKILL after the deadline; otherwise a POSIX watchdog (`kill` then `kill -9`). A bad menu pick no longer runs a second probe. Law: `requirement-grok-auth-backup` **1.5.0** · `requirement-shell-termux-coding` **1.2.0** · `requirement-shell-cli-default-interaction` **2.7.0**. Suite **TP-GROK-CLI-44** · **TP-GROK-CLI-45** · **TP-CLI-21**. Incident **INC-20260907-001**.

## [1.8.13] - 2026-09-07

### Changed

- **Main menu when grok is already logged in:** do not list **sync-auth** or **sync-auth-from-remote**. Immediately under the login status (and **after** any host not-available line) **append** `sync-auth and sync-auth-from-remote features are not available for logged-in environment.` That line does **not** replace `backup, sync-auth and sudoers features are not available in {{termux/gitbash/windows-cmd}}.`. Remaining rows start at **1** (multi-user: backup, add-crontab, sudoers; Termux / Git Bash / Windows cmd: add-crontab). Direct CLI skip is unchanged. Law: `requirement-shell-cli-default-interaction` **2.6.0**. Suite **TP-CLI-20**.

## [1.8.12] - 2026-09-07

### Changed

- **`sync-auth` / `sync-auth-from-remote` skip when grok is already logged in.** They run the live `grok -p hello` check first (or reuse the main-menu **logged in** / **logged out** line in the same process). If the session is valid they do **not** copy from `/var/grok-cli` or `scp` a remote store; they print `No sync-auth for logged-in environment.` and exit 0. `--force` does not override. Law: `requirement-grok-auth-backup` **1.4.0**. Suite **TP-GROK-CLI-42** · **TP-GROK-CLI-43**.

## [1.8.11] - 2026-09-07

### Added

- **Main menu on Termux / Git Bash / Windows cmd:** do not list **backup**, **sync-auth**, or **sudoers**. Immediately under the login status print `backup, sync-auth and sudoers features are not available in {{termux/gitbash/windows-cmd}}.` Remaining rows start at **1** (`sync-auth-from-remote`, `add-crontab`, Exit **9**). Law: `requirement-shell-cli-default-interaction` **2.5.0**. Suite **TP-CLI-19**.
- **Preferred remote for `sync-auth-from-remote`:** save the SPEC that worked under persistence `${HOME}/.local/grok-cli/preferred-remote` (mode 0600). On a TTY with no operand, the prompt shows that value at the end as `[user@host]`; Enter uses it. Law: `requirement-grok-auth-backup` **1.3.0**. Suite **TP-GROK-CLI-41**.

## [1.8.10] - 2026-09-06

### Fixed

- **`backup` after sudo said grok was logged out.** Menu **1** / `grok-cli backup` could print `Session valid. Elevating: sudo -n /usr/local/bin/grok-cli backup`, then `Cannot backup: grok is not logged in (exit 1: login required)`, then tell you to generate a sudoer request even when `/etc/sudoers.d/grok-cli-<login>` already granted `NOPASSWD: /usr/local/bin/grok-cli backup`. The elevated process ran `grok -p hello` with root’s `HOME=/root` (sudo `env_reset`), so grok looked at `/root/.grok` instead of this login’s `~/.grok`. The probe now pins `HOME` and `GROK_HOME` to the invoking login (`SUDO_USER`). If sudo did run and the child failed, Next is `grok login` then `grok-cli backup` — not `generate-sudoer-request`. Law: `requirement-grok-auth-backup` **1.2.1**. Suite **TP-GROK-CLI-39** · **TP-GROK-CLI-40**.

## [1.8.9] - 2026-09-06

### Changed

- **README for people:** Features and Related Projects lead with everyday words (who types what). Last Update is the current date; full history stays in this file.
- **Requirement samples:** JSON/sudoers grant examples use `id -un`, not a frozen Unix login.
- **Termux / Git Bash / Windows cmd:** related shell requirements print **Under command line for normal user only** — this-login work only; no `sudo curl | sh` on that class.

### Fixed

- CLI interface Type 1 deposit still named leftover `/var/backup`.
- Idempotency human-facing still talked about dated tar.gz archives.
- Ship unit header still said online install was absent.

## [1.8.8] - 2026-09-05

### Fixed

- **Login check was a file guess.** `check-session`, `backup`, and the menu **logged in** / **logged out** line used to read `~/.grok/auth.json` (refresh token / future `expires_at`). That can look valid while grok cannot talk to xAI (revoked session, Termux DNS, missing wrapper). They now run **`grok -p hello` first** (stdin closed; `timeout` when present; grok’s answer is not printed). Missing grok → Next `grok-cli setup` then `grok login`. Probe fail → Next `grok login`. Core tests inject a fake `GROK_BIN` (no public network). Law: `requirement-grok-auth-backup` **1.2.0**. Suite **TP-GROK-CLI-03**–**05** · **35**–**38** · **TP-CLI-17**.

## [1.8.7] - 2026-09-04

### Added

- **Termux CLI coding-style law:** `requirement-shell-termux-coding` — how grok-cli is written on Termux/Android (`PREFIX`, Termux `pkg` never sudo, `noexec` tmp, do not assume `/usr/local/bin` or `/var`). Path classes on `requirement-project-folder` **1.2.0**. POSIX coding-style **points** (`requirement-shell-script-coding` **1.1.0**). `setup` procedure stays `requirement-grok-setup` **2.6.1**.

### Fixed

- **`setup` Termux DNS:** vendor grok (musl) reads `/etc/resolv.conf`, which on Termux has no `nameserver`, so `grok login` failed with `dns error` for `auth.x.ai`. Write `~/.grok/resolv.conf` and rewrite the wrapper as `proot -b thatfile:/etc/resolv.conf` (still no vendor byte-patch). If proot cannot bind, INFO still points at `XAI_API_KEY`. Law: `requirement-grok-setup` **2.6.0**. Suite **TP-VCLI-25**.

## [1.8.6] - 2026-09-04

### Fixed

- **`setup` download diagnosis:** curl failures now name **HTTP status** (`HTTP 404`, `HTTP 000` + curl exit). The xAI `linux-aarch64` grok 1.0.13 artifact is a valid static ELF `ET_EXEC` (not a truncated download). On Android `e_type` 2 refusal, leave `~/.grok/downloads/grok-{{os}}-{{arch}}.failed` instead of deleting it. `proot` smoke/wrapper now unsets `LD_PRELOAD` (termux-exec otherwise re-hits `e_type` 2). Law: `requirement-grok-setup` **2.5.0**. Suite **TP-VCLI-19** · **TP-VCLI-21** · **TP-VCLI-24**.

## [1.8.5] - 2026-09-04

### Fixed

- **`setup` on Termux:** when the vendor grok still cannot exec (`e_type` 2) and `proot` is missing, run `pkg install -y proot` (Android + Termux `pkg` only; no sudo; stdin closed) then retry the proot wrapper. Do not call `pkg` on non-Android. A failed `pkg` still fail-closes with Next `pkg install proot`. Law: `requirement-grok-setup` **2.4.0**. Suite **TP-VCLI-22** · **TP-VCLI-23**.

## [1.8.4] - 2026-09-04

### Fixed

- **`setup` on Termux/Android ET_EXEC:** the vendor `linux-aarch64` grok is a static Linux executable (`e_type` 2). Android `linker64` (via termux-exec) refuses it, so `--version` failed even after a correct-arch download. Retry with `TERMUX_EXEC_OPTOUT=1` / `LD_PRELOAD` unset, then `proot` if present; on success place a POSIX wrapper under `~/.grok/bin` (vendor file unchanged). If both fail: Next `pkg install proot`, then `grok-cli setup --force`. Law: `requirement-grok-setup` **2.3.0**. Suite **TP-VCLI-19** · **TP-VCLI-20** · **TP-VCLI-21**.

## [1.8.3] - 2026-09-04

### Fixed

- **`setup` on Termux/aarch64:** do not treat an x86_64 `grok` (execute bit on, `scp` from a linux-x86_64 host) as already installed. Skip only if `grok --version` succeeds on this host; refuse a downloaded ELF whose `e_machine` does not match `uname` (EM_X86_64 vs aarch64). Next: run `grok-cli setup --force` on the phone, do not scp grok from an x86_64 machine. Law: `requirement-grok-setup` **2.2.0**. Suite **TP-VCLI-17** · **TP-VCLI-18**.

## [1.8.2] - 2026-09-03

### Changed

- **Main menu short desc:** header board title is **Alternative online installer for xAI grok** (`APP_DESC` / `SHORT_DESCRIPTION`). No longer the generic “numbered list of live commands”. Law: `requirement-shell-cli-default-interaction` **2.3.0**. Suite **TP-CLI-17**.
- **README pitch:** product is an alternative online installer for xAI grok (vs `https://x.ai/cli/install.sh`); Termux-friendly `setup`; auth backup/sync is optional later work.

## [1.8.1] - 2026-09-03

### Changed

- **Main menu look** is **default CLI main menu style**: explain text after `: ` is *italic* and light gray (SGR **3** + **37**) via `out_menu_choice` (replaces `out_menu_row` / SGR 90). Number and command name stay unstyled. Header **grok-cli**(*version*) is unchanged. Law: `requirement-shell-cli-default-interaction` **2.2.0** · `requirement-shell-output-requirements` **1.1.0**. Suite **TP-CLI-17**.

## [1.8.0] - 2026-09-03

### Changed

- **Main menu:** header is **grok-cli**(*version*) (`APP_NAME(APP_VERSION)`). The next line is **logged in** or **logged out**. `check-session` is no longer a numbered row (the command still exists). Numbered rows start at **backup** (**1**); family **sudoers** is **5**. Explain text after `: ` is light gray *italic* on a TTY. Law: `requirement-shell-cli-default-interaction` **2.1.0**. Suite **TP-CLI-13** · **TP-CLI-17**.

### Fixed

- **Menu locators:** live AC/TP/lesson rows now name **3** for `sync-auth-from-remote` (pick **4** is `add-crontab`). Historical 1.7.1 changelog wording is unchanged.
- **`setup` download vs smoke:** the version pointer may land in product storage; the chmod’d/smoked binary is a `mktemp` sibling under `~/.grok/downloads` (not cache/`/tmp`/`/dev/shm`).
- **Menu nametag:** `APP_VERSION` is always Config `VERSION` (an inherited env value cannot relabel the header).
- **`setup` smoke `[ERROR]`:** a full stop after the happened clause before “This did not install”.

## [1.7.3] - 2026-09-02

### Fixed

- **`setup` on Termux/Android:** smoke `--version` on the file under `~/.grok/downloads` (same as xAI’s installer), not the cache folder / `/tmp` / `/dev/shm` which may be `noexec`. Failure now includes the smoke exit status and a short stderr snippet. Law: `requirement-grok-setup` **2.1.0**. Suite **TP-VCLI-15** · **TP-VCLI-16**.

## [1.7.2] - 2026-09-02

### Fixed

- **`prompt_ask` call shape:** assign `PROMPT_ASK_VALUE` in the current shell. **MUST NOT** `_x=$(prompt_ask …)` (T1-PROMPT-CAPTURE). Menu pick 4 and draft chooser updated. Static **TP-CLI-15**. Law: `requirement-shell-script-coding` **1.0.2**.

## [1.7.1] - 2026-09-02

### Fixed

- **Menu pick 4 (`sync-auth-from-remote`)** no longer freezes with no prompt. `prompt_ask` keeps UI off captured stdout (`>&2`) and reads `/dev/tty` when it opens, so `_spec=$(prompt_ask …)` shows `Remote (user@host, IPv4, domain, or user@domain):` instead of a silent hang (INC-20260902-001). Law: `requirement-grok-auth-backup` **1.1.1**. Suite **TP-GROK-CLI-34**.

## [1.7.0] - 2026-09-02

### Added

- **Online install** from selfmanaged, specialized onto grok-cli: `curl -fsSL https://raw.githubusercontent.com/cloudgen/grok-cli/main/src/grok-cli | sh`. Companion `${SCRIPT_URL}.sha256`. Verbs `version-check`, `self-update`, `self-uninstall`.
- **Empty argv:** TTY still opens the numbered menu. Off-TTY empty argv is Type O install-ensure (**not** help), so the pipe one-liner works. Checkout `install` remains an offline copy. Dual-mode matrix: `requirement-shell-online-install` **1.0.0**. Suite **TP-ONL-01..04** · **TP-CLI-07** / **13**.

## [1.6.0] - 2026-09-02

### Changed

- **`setup`**: install peer `grok` by the studied xAI procedure (platform detect, channel version pointer, `grok-{version}-{os}-{arch}` artifact, place under `~/.grok/downloads` and `~/.grok/bin`). **Does not** download or execute `https://x.ai/cli/install.sh` and **does not** require bash. Idempotent if `grok` is already present; `--force` fetches again. Core tests use a fake `curl` (no public network). Law: `requirement-grok-setup` **2.0.0**. Suite **TP-VCLI-01..09 · 11..14**.

## [1.5.0] - 2026-09-02

### Added

- **`sync-auth-from-remote`**: `scp` a remote host’s `/var/grok-cli/auth.*` into this login’s `~/.grok` (dest `auth.json` mode `0600`, no sudo). SPEC forms: `user@IPv4`, IPv4, domain-name, `user@domain-name` (documentation examples `192.0.2.10` / `host.example.com`). BatchMode scp (no password hang). Main menu row **4**; `add-crontab` **5**; family `sudoers` **6**. Law: `requirement-grok-auth-backup` **1.1.0**. Suite **TP-GROK-CLI-30..33**.

## [1.4.0] - 2026-09-02

### Added

- **`add-crontab`**: install this login’s crontab jobs matching the studied host timers — `*/30 * * * * sudo /usr/local/bin/grok-cli backup` and `45 * * * * /usr/local/bin/grok-cli sync-auth`. Uses `id -un` (any login with the matching `/etc/sudoers.d/grok-cli-<user>` NOPASSWD backup grant). Does not write `/etc`. Re-run does not duplicate. Main menu row **4**; family `sudoers` is **5**. Law: `requirement-grok-crontab` **1.0.0**. Suite **TP-GROK-CLI-26..29**.

## [1.3.0] - 2026-08-30

### Added

- **Persistence storage.** Storage law covers two classes: **cache folder** (`/dev/shm/cache/cache-grok-cli` preferred, XDG `cache-grok-cli` fallback) and **persistence storage** `${HOME}/.local/grok-cli`. `about` prints **Persistence storage**; JSON adds `persistence_storage`. Not `~/.local/bin` (install) and not `/var/grok-cli` (Type 1 deposit). Law: `requirement-shell-cli-storage` **1.2.0**. Suite **TP-CLI-06 / 12**.

## [1.2.2] - 2026-08-30

### Changed

- **Cache folder labels and preferred path.** `about` prints **Cache folder (preferred)** and **Cache folder (fallback)** (not Storage (effective)/(fallback)). Preferred leaf is `/dev/shm/cache/cache-grok-cli` so it is not confused with a ram-drive project tree. Fallback is `${XDG_CACHE_HOME}/cache-grok-cli`. JSON adds `cache_preferred` / `cache_fallback`. Law: `requirement-shell-cli-storage` **1.1.0**. Suite **TP-CLI-06 / 12**.

## [1.2.1] - 2026-08-30

### Fixed

- **`setup`**: after the xAI installer writes grok under `~/.grok/bin` and a PATH line in `~/.bashrc`, do not print `[ERROR] grok is not on PATH` and do not send the operator to `~/.local/bin`. grok on disk is success; this session still needs a new terminal before `grok login`.

## [1.2.0] - 2026-08-25

### Added

- **`setup`**: download xAI’s grok installer (`https://x.ai/cli/install.sh`) and run it so the peer `grok` CLI is on PATH. Idempotent if `grok` is already present; `--force` fetches again. Does not install grok-cli and does not add a grok-cli online-install channel. Core tests use a fake `curl` (no public network).

## [1.1.0] - 2026-08-23

### Changed

- Empty argv on a real terminal now opens the numbered start list (same handler as `grok-cli menu` / `main`). Off-TTY empty argv still prints help. `--json` with no command still prints JSON help. Local-only Type N is unchanged: empty argv never install-ensures.

## [1.0.0] - 2026-08-23

### Added

- Product **grok-cli** specialized from sibling **folder-backup** (chain: cli-template → folder-backup → grok-cli).
- **`check-session`**: fail closed unless grok is logged in with a valid `~/.grok/auth.json` session.
- **`backup`**: after a valid session, copy `~/.grok/auth.*` into `/var/grok-cli`, `chown root:root`, `chmod 0644`. Non-root re-execs passwordless `sudo /usr/local/bin/grok-cli backup` after sudoer-adm approves the JSON grant.
- **`sync-auth`**: copy `/var/grok-cli/auth.*` into `~/.grok` as the invoking login (`auth.json` mode `0600`). Does not use sudo.
- JSON sudoer file grants **`grok-cli backup` only** (no OS-tool `cp`/`chmod`, no `restore`).
- Suite **TP-GROK-CLI-*** plus inherited Type 0 **TP-CLI-*** / **TP-LC-***.

### Removed

- Folder archive `backup <folder>` / `restore` / tar.gz retention (daily 5 / total 30).
