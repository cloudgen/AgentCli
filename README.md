# grok-cli - Alternative online installer for xAI grok

![Version](https://img.shields.io/badge/Version-1.8.47-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
[![CIAO](https://img.shields.io/badge/Philosophy-CIAO%20(Caution%20%E2%80%A2%20Intentional%20%E2%80%A2%20Anti--fragile%20%E2%80%A2%20Over--engineered)-purple.svg)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/cloudgen/grok-cli?style=flat-square)](https://github.com/cloudgen/grok-cli)

**grok-cli** is an alternative online installer for xAI’s `grok` CLI. The official one-liner on [x.ai](https://x.ai) (`curl -fsSL https://x.ai/cli/install.sh | bash`) is built for macOS, Linux, and Windows. It is **not** intended for Termux or other “this login only” phones. This program fetches the **same** vendor `grok` binary from xAI’s CLI channel and places it under `~/.grok` — it does **not** download or run `install.sh`.

### Why grok-cli is a better alternative

x.ai’s installer is the right path on a laptop. On a phone (and on any host that installer does not cover) it typically fails in ways that look like a broken download: wrong CPU if you `scp` grok from an x86_64 PC onto aarch64 Termux; Android’s linker refuses the static Linux file (`unexpected e_type: 2`); Termux has no `nameserver` in `/etc/resolv.conf` so `grok login` hits a DNS error; after a correct install, `grok -p hello` prints the answer and then **hangs until Ctrl-Z**.

This program is a better alternative **there** because it is written for that host instead of hoping `install.sh` will cope:

| Official `install.sh` | grok-cli |
|-----------------------|----------|
| One-liner assumes macOS / Linux / Windows | POSIX `/bin/sh` (does **not** need bash); Termux `PREFIX` / `pkg` as this login |
| Places whatever the script assumes | `setup` fetches the matching `linux-*`, Darwin, or (Git Bash/MSYS/Cygwin) `windows-*.exe` artifact and **smokes `--version` on this host** |
| No check that an x86_64 copy runs on a phone | Wrong ELF is **not** “already installed”; `--force` replaces it |
| Silent skip when grok is already on disk | On a real terminal, **keep** / **reinstall** / **Exit**; scripts and `--json` skip |
| Android `ET_EXEC` refusal looks like a truncated file | Retries `TERMUX_EXEC_OPTOUT`, may `pkg install -y proot` (no sudo), wraps grok **without editing vendor bytes** |
| musl grok reads `/etc/resolv.conf` with no nameserver | Binds `~/.grok/resolv.conf` over `/etc/resolv.conf` via PRoot |
| `grok -p` hangs: leftover Termux `runsvdir` keep PRoot in `do_wait` | From **1.8.22**: bind a no-op over `start-services.sh` so login-shell env capture does not spawn those daemons; reaper as safety net so `-p` returns |
| Login truth is “the file is there” | `check-session` / the numbered list run live `grok -p hello` |

It is **not** a second grok program and **not** official x.ai Termux support. After `setup`, open a new terminal if `grok` is not on this session’s PATH, then `grok login` (or set `XAI_API_KEY`). Sharing `~/.grok/auth.*` across logins on one host is optional later work (`backup` / `sync-auth`), not the reason this tool exists.

| You | Official x.ai installer | Not this |
|-----|-------------------------|----------|
| Install grok-cli, then `grok-cli setup` (no sudo) | `curl -fsSL https://x.ai/cli/install.sh \| bash` on macOS / Linux / Windows | A second grok binary; executing x.ai’s `install.sh`; claiming official Termux support |

## Features

- **Install grok without x.ai’s `install.sh`**: type `grok-cli setup`. It detects this computer, downloads the matching grok program from xAI, checks that `--version` runs from `~/.grok/downloads` (not `/tmp` or the cache folder — some phones refuse to run files from there), and places `~/.grok/bin/grok` (Git Bash: `grok.exe`). If grok already **runs on this host**, a real terminal offers **keep** / **reinstall** / **Exit** (pick **2** to remove and install again). Scripts and `--json` skip. An x86_64 file copied onto an aarch64 phone is replaced. On Termux, if the phone will not run the vendor file, setup may install `proot` with `pkg` (this login, no sudo) and place a wrapper — it still does **not** edit the vendor file. On Git Bash / MSYS / Cygwin it fetches the **windows** `.exe` (copy, not symlink). `--force` downloads again without the list. POSIX `/bin/sh` (does **not** need bash).
- **Termux-aware place**: uses `${PREFIX}/bin` when `PREFIX` is set. A missing `/etc/resolv.conf` is a note, not an install failure, when `--version` succeeded. If grok still will not run: `pkg install proot`, then `grok-cli setup --force`. From **1.8.22** the PRoot wrapper stops leftover `runsvdir` from freezing `grok -p` (see **Platform Compatibility**).
- **Install this program**: paste the curl one-liner; later `version-check`, `self-update`, `self-uninstall`
- **Install from a checkout**: `install`, `uninstall`, `where-is-me`, `version`, `about`, `help`, `menu`
- **Scratch is per login and per process.** `about` prints **Cache folder used**, **preferred**, **1st fallback**, and **2nd fallback** when this computer has one. Linux uses `/dev/shm/cache/cache-<app>-<login>-<pid>`, then `/tmp/cache/...`, then `~/.cache/cache-<app>-<pid>`. Git Bash uses `/tmp/cache/...`, then `~/AppData/Local/Temp/cache-<app>-<pid>`. Mac uses `/tmp/cache/...`, then `~/Library/Caches/cache-<app>-<pid>`, then `~/cache/cache-<app>-<pid>`. A skipped folder is silent. Durable data for this login stays `~/.local/grok-cli`. On a phone, do not run a downloaded program from the cache folder.
- **Update grok without grok auto-update**: type `grok-cli update-grok`. Fetches the latest xAI grok into `~/.grok` (Termux grok updater is unsupported). This is **not** `self-update` (that refreshes grok-cli). Missing grok → `grok-cli setup`.
- **Reinstall grok from the start list**: type `grok-cli reinstall`, or pick **reinstall** on the numbered list. Same fetch as `setup --force`. Keeps `auth.*`. Missing grok still installs. `setup` stays off the list.
- **Start grok without auto-update**: type `grok-cli run` (or `grok-cli run -p hello`). On Termux this avoids the hang until Ctrl-Z. Missing grok → `grok-cli setup`.
- **Prove grok is logged in**: on Termux/PRoot, `check-session` reads local `~/.grok/auth.json` cookies (live `grok -p hello` is skipped — it usually times out). On other hosts it still asks grok a one-line question (`grok -p hello`). Missing grok → `grok-cli setup`, then `grok login`.
- **Optional shared login on one Linux host**: `backup` copies `~/.grok/auth.*` into `/var/grok-cli` as `root:root` `0644` (elevated probe uses **this** login’s grok home, not root’s); `sync-auth` copies that store into this login’s `~/.grok` with **no sudo** (skipped if grok is already logged in — prints `No sync-auth for logged-in environment.`); `sync-auth-from-remote` uses `scp` (same skip) and remembers the last remote; `sync-auth-to-remote` copies this login’s `~/.grok/auth.*` onto that remote login’s `~/.grok` (no sudo; still runs when this grok is already logged in); `add-crontab` adds this login’s timers after **this** login’s backup grant exists
- **Optional passwordless backup grant** (only if you use `backup`): `print-sudoers` prints one line so this login may run `sudo grok-cli backup` without a password. A host admin installs that line. `generate-sudoer-request` / `submit-sudoer-request` hand the same grant to the named approver (`sudoer-adm`).
- **Stops when it should**: grok missing or not answering, unauthorized copy into `/var/grok-cli`, unreadable store, failed grok download

## Quick Installation

**Official grok installer** (macOS / Linux / Windows; not intended for Termux):

```sh
curl -fsSL https://x.ai/cli/install.sh | bash
```

**This project** (POSIX `/bin/sh`; Termux-friendly procedure — still the vendor `grok` binary):

```sh
curl -fsSL https://raw.githubusercontent.com/cloudgen/grok-cli/main/src/grok-cli | sh
grok-cli setup
```

Then open a **new terminal** if this session cannot find `grok`, and run `grok login`.

On **Alpine** the login shell is ash (`echo $0` prints `-ash`). If `~/.profile` is missing, install creates it: bash, zsh, and fish get a login note that sources `~/.bashrc`; ash gets that same note and also `~/.local/bin` on `PATH`. If `~/.profile` is already there, only ash adds the `PATH` line. A zsh login also gets that PATH line on `~/.zshenv` (every start) and on `~/.zprofile` (login, after the system `path_helper`). A bash-only login does not invent those zsh files. A missing `.zshenv` or `.zprofile` is created when this shell is zsh. Open a new login, or run `. ~/.profile`, before `grok-cli setup`. The shell that ran `curl | sh` does not inherit the new PATH by itself.

These lines are the program’s own messages. `$tmpdir` stands for a throw-away folder, not this login’s home. `$HOME` in the PATH lines is that folder’s home:

```text
$ grok-cli rc-test --root "$tmpdir/profile" --file profile --case create
→ Created $tmpdir/profile/.profile (login shell sources ~/.bashrc)
[OK] rc-test profile create under $tmpdir/profile
$ grok-cli rc-test --root "$tmpdir/zshenv" --file zshenv --case create
→ Created $tmpdir/zshenv/.zshenv
→ Added $HOME/.local/bin to PATH for zsh (.zshenv)
[OK] rc-test zshenv create under $tmpdir/zshenv
$ grok-cli rc-test --root "$tmpdir/zprofile" --file zprofile --case create
→ Created $tmpdir/zprofile/.zprofile
→ Added $HOME/.local/bin to PATH for zsh (.zprofile)
[OK] rc-test zprofile create under $tmpdir/zprofile
```

If grok already **runs** on this host, a real terminal offers keep / reinstall / Exit (pick **2** to install again). Scripts and `--json` skip. `--force` skips the list.

```text
$ grok-cli setup
[INFO] **grok-cli**(*1.8.47*) — setup
[INFO] grok is already installed at ~/.grok/bin/grok.
1. keep: Leave the existing grok
2. reinstall: Remove existing grok and install again
9. Exit
Choice [1]:
```

On **Termux (aarch64)** run `grok-cli setup` **on the phone**. `scp` of `~/.grok/bin/grok` from an x86_64 host copies `linux-x86_64` and Termux will reject it (`EM_X86_64` instead of `EM_AARCH64`). `setup` fetches `linux-aarch64` from x.ai; `--force` replaces a copied x86_64 file. If `--version` fails with `unexpected e_type: 2`, setup tries `pkg install -y proot` on Termux and wraps grok. If that still cannot run: `pkg install proot`, then `grok-cli setup --force`.

**Global grok-cli (root):**

```sh
sudo curl -fsSL https://raw.githubusercontent.com/cloudgen/grok-cli/main/src/grok-cli | sudo sh
```

**Integrity (automatic, no env pin):** SHA-256. The program fetches the companion `${SCRIPT_URL}.sha256` itself and prints **link**, **value**, and **result**.

| Result | What happens |
|--------|----------------|
| Match | Install continues |
| Mismatch | Abort (non-zero) |
| Missing sidecar | Warn and continue |

Companion file in-repo: `src/grok-cli.sha256`  
Companion URL: `https://raw.githubusercontent.com/cloudgen/grok-cli/main/src/grok-cli.sha256`

**From a checkout (offline copy of grok-cli, no network):**

```sh
sh src/grok-cli install
# or force refresh after updates
sh src/grok-cli install --force

# Ensure ~/.local/bin is on PATH, then:
grok-cli version
grok-cli setup
```

**Global grok-cli from checkout** (preferred before durable sudoers / production elevation):

```sh
sudo sh src/grok-cli install
# or: grok-cli install --global   # needs write access to /usr/local/bin
# Managed binary mode is always 0755 so every user can run the shell ship unit.
```

**Optional — sudoers** (only if a non-root login will deposit into root-owned `/var/grok-cli`):

```sh
grok-cli print-sudoers-install-script
# Admin (account with sudo rights) — handoff script (path printed by CLI):
sudo sh /dev/shm/grok-cli-<user>-sudoers-admin.sh install

# Or JSON grant for sudoer-adm:
grok-cli generate-sudoer-request
grok-cli submit-sudoer-request
```

Local `~/.local/bin` install is **not** production-secure for host elevation — the user can change the binary. Prefer global install for any host that keeps `/etc/sudoers.d/grok-cli-<user>`. See [`SECURITY.md`](./SECURITY.md).

This product is **dual-mode**: primary install is the curl one-liner; `sh src/grok-cli install` copies the running checkout.

**Source repository:** [cloudgen/grok-cli](https://github.com/cloudgen/grok-cli)  
Config identity: `REPO_USER=cloudgen`, `REPO_NAME=grok-cli`. Default channel: `SCRIPT_URL=https://raw.githubusercontent.com/cloudgen/grok-cli/main/src/grok-cli`.

After install, on a terminal:

```text
$ grok-cli menu
[INFO] **grok-cli**(*1.8.47*) — Alternative online installer for xAI grok
[INFO] logged out
[INFO] backup features are not available for logged-out environment.
1. grok-auth: *Backup, sync, crontab, setup, and reinstall*
5. sudoers: *Grant and drafts*
6. self-management: *Check, update, or remove grok-cli*
7. language: *display language for this menu*
9. Exit
```

Pick **1** for the auth list. Numbers **14–16** stay put when a row is hidden. Logged out lists **12** `sync-auth-from-remote` and **13** `sync-auth`, and hides **11**. Logged in lists **11** `backup` and hides **12** and **13**. `sync-auth-to-remote` is a typed command, not a row:

```text
12. sync-auth-from-remote: *Copy a remote host's auth.* into ~/.grok*
13. sync-auth: *Copy /var/grok-cli/auth.* into ~/.grok*
14. add-crontab: *Add backup and sync-auth jobs to this login's crontab*
15. setup: *Install grok from x.ai*
16. reinstall: *Remove existing grok and install again*
0. Back
9. Exit
```

On Termux / Git Bash / Windows cmd, **backup**, **sync-auth**, and **sudoers** are omitted. Each of those notices is its own `[INFO]` line. The top list is **1** grok-auth, **2** run (start grok without auto-update), **6** self-management, **7** language, and **9** Exit. Row **7** is on every host. Front **8** is not a row. There is no Back row. When the session is **logged out** or **timeout**, an `[INFO]` line is **appended**: `backup features are not available for logged-out environment.` Auth **12** is listed. Auth **11** and **13** stay off this class. When the session is **logged in**, that logged-out line is omitted, auth **12** is omitted, and a second `[INFO]` line is **appended**: `sync-auth and sync-auth-from-remote features are not available for logged-in environment.` Neither line replaces the host line. `sync-auth-to-remote` is not a numbered row. Termux, logged out:

```text
$ grok-cli menu
[INFO] **grok-cli**(*1.8.47*) — Alternative online installer for xAI grok
[INFO] logged out
[INFO] backup, sync-auth and sudoers features are not available in termux.
[INFO] backup features are not available for logged-out environment.
1. grok-auth: *Backup, sync, crontab, setup, and reinstall*
2. run: *Start grok without auto-update*
6. self-management: *Check, update, or remove grok-cli*
7. language: *display language for this menu*
9. Exit
```

Live capture on a multi-user host that is **logged in**:

```text
$ grok-cli menu
[INFO] **grok-cli**(*1.8.47*) — Alternative online installer for xAI grok
[INFO] logged in
[INFO] sync-auth and sync-auth-from-remote features are not available for logged-in environment.
1. grok-auth: *Backup, sync, crontab, setup, and reinstall*
5. sudoers: *Grant and drafts*
6. self-management: *Check, update, or remove grok-cli*
7. language: *display language for this menu*
9. Exit
```

`5` opens sudoers. `6` opens self-management. `7` opens language. **61** install, **62** version, **63** about, and **67** self-install stay unprinted.

```text
51. generate-sudoer-request: *Write a JSON grant you can read*
52. submit-sudoer-request: *Queue the JSON grant inbound*
53. print-sudoers: *Emit sudoers draft*
54. print-sudoers-install-script: *Write admin install script*
55. remove-project-sudoers: *Remove sudoers draft only*
0. Back
9. Exit
```

```text
64. version-check: *Compare local version with the channel*
65. self-update: *Re-download grok-cli from the channel*
66. self-uninstall: *Remove grok-cli*
68. where-is-me: *Show running and install paths*
0. Back
9. Exit
```

```text
80. English: *use English for this menu*
81. 简体中文: *use Simplified Chinese for this menu*
82. 繁體中文: *use Traditional Chinese for this menu*
83. Español: *use Spanish for this menu*
84. العربية: *use Arabic for this menu*
85. Français: *use French for this menu*
86. Português: *use Portuguese for this menu*
87. Русский: *use Russian for this menu*
88. Deutsch: *use German for this menu*
89. 日本語: *use Japanese for this menu*
90. 한국어: *use Korean for this menu*
91. Nederlands: *use Dutch for this menu*
92. Ελληνικά: *use Greek for this menu*
0. Back
9. Exit
```

Choose a number, or type the command name. `7` opens the language list (**80** English, **81** 简体中文, **82** 繁體中文, **83** Español, **84** العربية, **85** Français, **86** Português, **87** Русский, **88** Deutsch, **89** 日本語, **90** 한국어, **91** Nederlands, **92** Ελληνικά). **70–79** and **93–98** are reserved and are not printed. The choice is saved under `~/.local/grok-cli/language` and the next run opens in that language. `GROK_CLI_LANG` overrides one run and does not write the file. `language` is not a command you type on the shell. `9` exits from every list. `0` goes back only inside a submenu. The top list has no Back row. The line under the title is an independent `[INFO]` **logged in**, **timeout**, or **logged out**. On Termux/PRoot that line comes from local `auth.json` cookies (no `grok -p hello` wait). On other hosts it is a live `grok -p hello`; a hang that hits the bound prints **timeout**, not **logged out**. On a real terminal the descriptions after the colon are gray and italic. `setup` and `reinstall` are on the grok-auth list (**15** and **16**), not on the top list. Direct `grok-cli reinstall` still works. A later `sync-auth-from-remote` or `sync-auth-to-remote` remembers the last remote in persistence and offers it as the prompt default.

## Usage

| How you run it | What you get |
|----------------|--------------|
| `grok-cli` or `grok-cli --debug` at a real terminal | Numbered start list (**1** grok-auth, **5** sudoers, **6** self-management, **7** language, **9** Exit; no Back on that list; this-login-only shows **2** run and hides sudoers; **7** stays on every host; front **8** is not a row; **logged in** / **timeout** / **logged out** under the title from `grok -p hello`; Termux / Git Bash / Windows cmd hide backup / sync-auth / sudoers; logged-out session hides **11** `backup` and lists **12** `sync-auth-from-remote` and **13** `sync-auth` on a multi-user host; logged-in session hides **12** and **13** and lists **11** `backup`; `sync-auth-to-remote` is a typed command and is not a numbered row; each session appends its own not-available line; **9** leaves; **0** goes back only inside a submenu). Same as `grok-cli menu`. Overlay switches with no command still follow empty argv. |
| `curl -fsSL … \| sh` or `grok-cli` in a script (no args) | Install-ensure: places `~/.local/bin/grok-cli` or reports already installed. **Not** help. **Not** the menu. |
| `grok-cli help` or `grok-cli --json` (no command) | Help / JSON help. `--json` with no command is empty argv **special case**: JSON help even at a prompt |
| `grok-cli menu` in a script | Help (the list is TTY-only) |
| `grok-cli setup` at a real terminal | If grok already runs: numbered **keep** / **reinstall** / **Exit**. Pick **2** to remove existing grok and install again. Scripts / `--json` skip. `--force` fetches without the list. |
| `grok-cli reinstall` | Remove existing grok and install again (keeps `auth.*`). Same as pick **16** on the grok-auth list. Missing grok still installs. |

```sh
grok-cli                 # numbered list on a real terminal; install-ensure in a script / pipe
grok-cli help
grok-cli menu            # same numbered list as empty argv on a TTY
grok-cli about
grok-cli --json about
grok-cli version-check
grok-cli self-update

grok-cli setup                 # install grok from x.ai (TTY: keep or reinstall if already there)
grok-cli update-grok           # update grok from x.ai (not grok-cli; avoids grok auto-update)
grok-cli reinstall             # remove existing grok and install again (keeps auth.*)
grok-cli run                   # start grok without auto-update (Termux)
grok-cli run -p hello
grok-cli check-session
grok-cli backup
grok-cli sync-auth
grok-cli sync-auth-from-remote user@192.0.2.10
grok-cli sync-auth-to-remote user@192.0.2.10
grok-cli add-crontab

grok-cli print-sudoers
grok-cli generate-sudoer-request
grok-cli submit-sudoer-request
grok-cli uninstall --force
grok-cli self-uninstall --force
```

**Environment (selected):**

| Variable | Role |
|----------|------|
| `SCRIPT_URL` | grok-cli install channel (default github raw `src/grok-cli`) |
| `GROK_HOME` | Grok auth directory (default `~/.grok` of the invoking login) |
| `GROK_VENDOR_BASE_URL` | xAI grok channel/artifact base (default `https://x.ai/cli`) |
| `GROK_CHANNEL` | grok channel (`stable` / `alpha` / `enterprise`; default `stable`) |
| `GROK_BIN` | Override path to peer `grok` |
| `GROK_PROMPT_TIMEOUT` | Seconds to wait for live `grok -p hello` (default 14; kept even when Termux/PRoot skips that probe) |
| `DEBUG` | `1` or flag `--debug`: stderr diagnostics; numbered menu prints elapsed of each paint step |
| `GROK_PROMPT_KILL_AFTER` | SIGKILL grace after that deadline (default 2; GNU `timeout -k`) |
| `GROK_CLI_ROOT` | Durable auth store (default `/var/grok-cli`; optional sharing) |
| `ALLOW_TEST_LOCAL_SUDOERS` | `1` = allow test-mode sudoers emit without `--allow-test-local` |
| `SUDOER_CLI` | Override path to `sudoer-cli` |
| `SUDOER_ADM_USER` | Approver login to detect (default `sudoer-adm`) |

## Examples

```sh
# Place xAI grok (TTY: keep / reinstall / Exit if already there)
grok-cli setup
grok-cli setup --force     # reinstall without the list
grok-cli reinstall             # same fetch; also a start-list row
grok-cli update-grok           # latest grok from x.ai (not grok auto-update)
# open a new terminal if grok is not on this session PATH yet
grok-cli run                   # Termux: start grok without auto-update
# or: grok login

# Optional: confirm grok actually answers, then share auth.* on this host
grok-cli check-session    # runs grok -p hello first
grok-cli backup

# Another login on the same host, no sudo:
grok-cli sync-auth

# Pull the shared store from another host (openssh scp; no sudo):
grok-cli sync-auth-from-remote user@192.0.2.10

# Push this login's ~/.grok/auth.* onto that host's ~/.grok (no sudo):
grok-cli sync-auth-to-remote user@192.0.2.10

# After sudoer-adm approves THIS login's backup grant:
grok-cli add-crontab
```

## Platform Compatibility

| Platform | Status |
|----------|--------|
| Linux, `/bin/sh` (dash/bash) | Supported |
| Termux / Android userspace | Supported for **this installer** (`setup` smokes under `~/.grok/downloads`, honors `$PREFIX/bin`, does not require bash). Vendor `linux-aarch64` grok is often `ET_EXEC`; setup retries `TERMUX_EXEC_OPTOUT`, may `pkg install -y proot`, and may place a wrapper without patching the file. Missing `/etc/resolv.conf` is not an install failure — use `XAI_API_KEY` or a host with working DNS if login fails. **Not** official x.ai Termux support. Why `grok -p` can hang until Ctrl-Z: **Why grok under PRoot does not return to the shell** below. |
| Git Bash / MSYS / Cygwin | Supported: `setup` maps `uname` to `windows-*`, fetches `grok-…-windows-….exe`, copies `~/.grok/bin/grok.exe` (no Developer Mode symlink). cmd.exe / PowerShell still need User PATH `%USERPROFILE%\.grok\bin`. |
| `python3` (optional) | Used for leftover `auth.json` shape helper when present (session gate is `grok -p hello`) |
| `sudo` + narrow sudoers | Required only for non-root `backup` into `/var/grok-cli` |
| macOS | `setup` follows xAI’s Darwin/arch detect; GNU `date -d` / `stat -c` assumptions may differ for other verbs |
| Windows PowerShell / cmd.exe | Official grok: `irm https://x.ai/cli/install.ps1 \| iex`. grok-cli `setup` is POSIX `sh` and does **not** replace that one-liner. |

### How xAI grok is set up by host

Studied from `https://x.ai/cli/install.sh` and `https://x.ai/cli/install.ps1`. grok-cli **does not run** those scripts; `setup` / `update-grok` replay the channel + artifact steps in POSIX `/bin/sh`.

**One-liners**

| Host | Official xAI | grok-cli |
|------|----------------|----------|
| Linux | `curl -fsSL https://x.ai/cli/install.sh \| bash` | `grok-cli setup` (same `linux-*` artifact; does **not** run `install.sh`) |
| macOS | same `install.sh` | `grok-cli setup` (`macos-*`; Rosetta → aarch64) |
| Windows PowerShell | `irm https://x.ai/cli/install.ps1 \| iex` | Not this POSIX `setup` |
| Git Bash / MSYS / Cygwin | `install.sh` maps to **windows** and installs `.exe` | `grok-cli setup` (same `windows-*` `.exe`; copy `grok.exe`) |
| WSL | `install.sh` → **linux** binary | `grok-cli setup` as Linux |
| Termux | **Not intended** | `grok-cli setup` fetches **`linux-aarch64`**, smokes on the phone, often a **PRoot wrapper** |

**Detect OS / arch / artifact**

| Step | Linux `install.sh` | Termux grok-cli | PowerShell `install.ps1` | Git Bash grok-cli |
|------|--------------------|-----------------|--------------------------|-------------------|
| OS | `uname -s` Linux → `linux` | still Linux → **`linux`** | forced **Windows** | `MINGW*`/`MSYS*`/`CYGWIN*` → **`windows`** |
| Arch | `uname -m` → `x86_64` / `aarch64` | same; refuse x86_64 file on an aarch64 phone | `PROCESSOR_ARCHITECTURE` | `uname -m` |
| Artifact | `grok-{ver}-linux-{arch}` (`.zst` / `.gz` / raw) | same **linux** file | `grok-{ver}-windows-{arch}.exe` then without `.exe` | same **windows** `.exe` then uncompressed |
| On disk | no `.exe`; `chmod +x` | same + optional POSIX **wrapper** | `grok.exe` / `agent.exe` **copy** | `grok.exe` / `agent.exe` **copy** |

**Fetch / place / smoke**

| Step | Linux `install.sh` | Termux grok-cli | PowerShell `install.ps1` | Git Bash grok-cli |
|------|--------------------|-----------------|--------------------------|-------------------|
| Transport | `curl` or `wget` | `curl`; HTTP status on fail | `Invoke-WebRequest` / `HttpWebRequest`; **TLS 1.2** | `curl` |
| Channel | `https://x.ai/cli/{stable\|alpha\|enterprise}`; GCS fallback | same | same | same |
| Place | `~/.grok/downloads` + `~/.grok/bin` **symlink** | same; wrapper if ET_EXEC | `%USERPROFILE%\.grok\` **copy** `.exe` | `~/.grok/` **copy** `.exe` |
| Smoke `--version` | yes, before replace | yes, under `downloads` (not `/tmp`); Android retries + PRoot | **no** | **yes**, before replace |
| Termux extras | none | DNS bind; `--no-auto-update` on `-p`; PRoot reaper | none | none (not Android) |

**PATH**

| Step | Linux `install.sh` | Termux grok-cli | PowerShell `install.ps1` | Git Bash grok-cli |
|------|--------------------|-----------------|--------------------------|-------------------|
| PATH now | symlink into `~/.local/bin` or `/usr/local/bin` if already on PATH | same + `${PREFIX}/bin` candidate | **User** `Path` + this session | **no** USER_BIN symlink (like official `install.sh` on windows) |
| PATH later | `# >>> grok installer >>>` in bash/zsh/fish rc | bash `~/.bashrc`; zsh `~/.zshenv` and login `~/.zprofile` (not `.zshrc`) | User PATH (cmd + PowerShell) | bash `~/.bashrc` vendor block; zsh `~/.zshenv` and `~/.zprofile`; INFO for cmd/PowerShell User PATH |

Then `grok login` or `XAI_API_KEY`. On Termux prefer `grok-cli run` and `grok-cli update-grok` instead of grok’s own updater.

### Why grok under PRoot does not return to the shell

**In one sentence:** on Termux, xAI’s `grok` often cannot run as a normal phone program, so `setup` starts it through **PRoot**; grok already printed and exited, but leftover Termux `runsvdir` (started by login-shell env capture) keep PRoot waiting — your shell looks frozen until **Ctrl-Z**.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Type `grok -p hello` on Termux and expect the prompt back | `Hello. How can I help you today?` then `~ $` |
| The other role | PRoot is a user-space trampoline (not real root, not a full Linux distro). It traces grok so a static Linux file can run on Android and can bind `~/.grok/resolv.conf` over `/etc/resolv.conf` | `pkg install proot` then `grok-cli setup` |
| Not this | grok-cli’s numbered list refusing to close; a corrupt `self-update`; byte-patching grok | Choice **9** already exits; SHA-256 passing does not prove `grok -p` returns |

| Includes | Excludes |
|----------|----------|
| What PRoot is; why grok-cli uses it; the causal chain of the `-p` hang; why Ctrl-C fails and Ctrl-Z works; what **1.8.22** does | Claiming official x.ai Termux support; editing vendor grok bytes; treating PRoot as `sudo` or as `proot-distro` |

**What PRoot is.** PRoot (Ptrace ROOT) rewrites grok’s system calls with `ptrace`. It does **not** give you root. grok-cli uses it because the vendor `linux-aarch64` file is a static Linux executable (`ET_EXEC`). Android’s linker refuses that file (`unexpected e_type: 2`). Termux’s `/etc/resolv.conf` also has no `nameserver`, so musl inside grok fails DNS unless PRoot binds a file that does. The wrapper unsets `LD_PRELOAD` (termux-exec would re-hit `e_type` 2) and runs `proot` plus the **unmodified** vendor file.

**Why `-p` does not exit.** Official grok `-p` is one-shot: print, then exit. On-device study (Termux aarch64, `proot` 5.1, `termux-services` + `runit`): `grok-linux` **does** `_exit` after the reply. `grok --help` under the **same** PRoot returns in ~0.3s — proof PRoot can exit when it has no leftover daemons. PRoot’s loop is `wait4(-1, …, __WALL)` (`wchan=do_wait`): it does not return until **every remaining tracee is dead**, including processes that later daemonize and reparent to PID 1. There is **no** `proot -r` rootfs; PRoot is only a syscall translator.

The leftover processes are **not** grok helpers. During session init, grok starts **two login shells** to snapshot the user environment (`bash -lc 'source "$HOME/.bashrc"; …'`). Termux login shells source `$PREFIX/etc/profile`, which sources `profile.d/start-services.sh`, which runs `(service-daemon start &)` → `start-stop-daemon -S -b … runsvdir $SVDIR`. `-b` double-forks. On a normal Termux login that is what you want. **Under PRoot it is fatal:** the new `runsvdir` remains a tracee and lives forever as a supervisor. Two login shells ⇒ two extra `runsvdir` per `grok -p`. They race `$PREFIX/var/run/service-daemon.pid` and usually cannot see Termux’s already-running `runsvdir`, so they start extras instead of no-op’ing.

**Causal chain**

```text
grok -p hello
  → wrapper execs proot (no rootfs) over grok-linux-aarch64
    → grok-linux starts two `bash -lc` env-capture processes
      → bash -l sources $PREFIX/etc/profile
        → profile.d/start-services.sh
          → (service-daemon start &)
            → start-stop-daemon -S -b … runsvdir $SVDIR
              → runsvdir double-forks, PPID=1, STILL a PRoot tracee
    → grok-linux prints the reply and _exit()s
    → proot wait4(-1, __WALL)    # leftover runsvdir still alive
      → grok -p never returns
```

Isolation (same PRoot flags as the wrapper: `proot -b ~/.grok/resolv.conf:/etc/resolv.conf <cmd>`):

| Command | Result |
|---------|--------|
| `grok -p hello` | Reply prints; hang until SIGKILL; two leftover `runsvdir` |
| `grok --help` | Exits in ~0.3s (no env-capture login shells) |
| `proot … bash -lc 'echo LOGIN_OK'` | Hang — **does not need grok at all** |
| `proot … bash -c 'echo NONLOGIN_OK'` | Exits at once |
| `proot … bash --noprofile --norc -lc '…'` | Exits at once |
| `env -u SVDIR grok -p hello` | Still hangs (`start-services.sh` re-exports `SVDIR`) |

Matching leftovers by `ps -o comm=` never fires on Termux (`comm` truncates to `/data/data/com.`). Match **args / exe paths**. Do **not** kill Termux’s own `runsvdir` (sshd / ssh-agent live there). Nested PRoot deadlocks (`ptrace_stop`); do not debug this hang by launching `grok -p` from an agent already under grok’s PRoot.

**Why Ctrl-C fails and Ctrl-Z works.** Ctrl-C is `SIGINT` — grok/PRoot often ignore it (or treat it as “cancel this turn”). Ctrl-Z is `SIGTSTP` — the shell’s job control, usually not caught — so you get `Stopped`. An old wrapper did `exec proot grok …`, so there was no parent left to SIGKILL.

**What grok-cli does (1.8.25).** The wrapper binds `/dev/null` over `$PREFIX/etc/profile.d/start-services.sh` so those login shells do not spawn extra `runsvdir` (it does **not** edit Termux’s file). It still passes `proot --kill-on-exit` (never `-k`) and `--no-auto-update` on `-p`, and keeps a **PRoot-exit reaper** as the safety net: when grok-linux is gone (or stdout is idle, including empty stdout after guest death), kill only new `runsvdir`, then SIGKILL PRoot immediately. The reaper is in its own session (`setsid`) and ignores Ctrl-Z so the watchdog cannot be stopped with the menu. The numbered list prints `checking session (grok -p hello, timeout 14s)...` after the header. If that probe hits the bound, the next line is **timeout** (not **logged out**). Interactive `grok` still `exec`s so the TUI owns the terminal. `grok-cli setup` **and** `grok-cli self-update` rewrite a stale wrapper (no `--force`). After `self-update` to **1.8.25**:

```sh
grok-cli self-update  # also heals ~/.grok/bin/grok
grok-cli run          # start grok without auto-update
grok-cli run -p hello # must return to ~ $ without Ctrl-Z
```

`grep proot-exit-reaper ~/.grok/bin/grok` should match. grok-cli’s own menu (Choice **9**) was already closable in **1.8.14**; that bound only the menu probe, not operator-facing `grok`. On Termux the numbered list starts with **run**.

## Related Projects

- Official grok install: [x.ai](https://x.ai) — `curl -fsSL https://x.ai/cli/install.sh | bash`
- [selfmanaged](https://github.com/cloudgen/selfmanaged) — online `curl\|sh` package specialized onto grok-cli
- [folder-backup](https://github.com/cloudgen/folder-backup) — architecture parent (folder archive backup)
- [CIAO Defensive Programming](https://github.com/cloudgen/ciao)
- [CIAO-Lite](https://github.com/cloudgen/ciao-lite)
- [cli-template](https://github.com/cloudgen/cli-template) — POSIX shell starter this product grew from (hop 0)

## Contributing

Keep changes surgical. Honor **CIAO-Lite Protection Zones** in `src/grok-cli`. Product behavior must stay consistent with live `docs/requirements/requirement-*.md`. Run `sh tests/run.sh` before proposing commits.

## License

MIT License — see [`LICENSE.md`](./LICENSE.md).

## Last Update

2026-10-12 — version **1.8.47**: shell startup files set PATH on the right file for each shell. A zsh login gets the line on `~/.zshenv` and `~/.zprofile`. A missing `.profile`, `.zshenv`, or `.zprofile` is created when that shell owns it. Bash-only does not invent the zsh files. Multi-user front is **1** grok-auth, **5** sudoers, **6** self-management, **7** language (**80** English through **92** Greek), **9** Exit. This-login-only lists **2** run and omits **5**. Front **8** is not a row. Full history: [`CHANGELOG.md`](./CHANGELOG.md).
