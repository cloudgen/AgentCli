**file**: docs/requirements/requirement-shell-cli-default-interaction.md  
**Status**: Active (Version 2.24.0)  
**Area**: shell  
**Key**: `requirement-shell-cli-default-interaction`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **product Single Source of Truth** for grok-cli’s **default interaction**: a **short numbered main menu** of daily **auth work**, with sudoers grant/draft commands behind one **family** row. grok-cli has `requirement-shell-cli-zero-arguments` (**case 3**): that REQ **defers TTY empty argv** to this menu and **owns off-TTY empty argv as Type O ensure**. The menu **MUST** also be the command **`menu`**. **`main` MAY** be accepted as the same handler.

On a **real terminal**, empty argv (no command token — overlay switches such as `--debug` allowed) and `grok-cli menu` (or `main`) **MUST** show the main menu. `menu`/`main` **MUST ignore `--json`**. Off-TTY, **`menu`/`main` MUST** print **help**, following `--json`. Off-TTY **empty argv** is **not** this file — it is channel ensure. Command rows **MUST** be `command: what it does`. The family row **MUST NOT** be a live dispatcher command.

Empty-argv type and the TTY vs off-TTY split for **no command token** stay on `requirement-shell-cli-zero-arguments`. Confirm / no-hang stays on `requirement-shell-interactive-vs-noninteractive`. Live command inventory stays dispatcher truth (`requirement-shell-cli-interface`).

### 1.1 Human-facing

Typing only `grok-cli` at a real terminal shows the numbered start list. In a script, bare `grok-cli` installs or reports already installed (not this menu). `grok-cli menu` (or `grok-cli main`) still opens the list on a TTY and prints help in a script. The list header is **grok-cli**(*version*) — **Alternative online installer for xAI grok** and the next line is an independent **`[INFO]`** **logged in**, **timeout**, or **logged out**. On a multi-user host the top list is **1** `grok-auth`, **5** `language`, **7** `sudoers`, **8** `self-management`, and **9** Exit, with no Back row. On Termux / Git Bash / Windows cmd (this login only), **backup**, **sync-auth**, and **sudoers** are omitted; the top list is **1** `grok-auth`, **2** `run`, **5** `language`, **8** `self-management`, and **9** Exit, with no Back row; Front **6** is not a row. immediately under the login status the list prints an independent **`[INFO]`** **backup, sync-auth and sudoers features are not available in {{termux/gitbash/windows-cmd}}.** When the session is **logged out** (or **timeout**), auth **13** `sync-auth-to-remote` is omitted on every host, and a multi-user host lists auth **11** `sync-auth` (not `backup`; copy the global store `/var/grok-cli/auth.*` into `~/.grok`) and auth **12** `sync-auth-from-remote`. When the session is **logged in**, auth **11** is `backup` (not `sync-auth`) and auth **12** `sync-auth-from-remote` is omitted, and a multi-user host lists auth **13** `sync-auth-to-remote`; immediately under any host not-available line (or under the login status when there is none) the list **appends** an independent **`[INFO]`** **`sync-auth and sync-auth-from-remote features are not available for logged-in environment.`** — it **MUST NOT** replace the host line. Remaining rows start at **1**. On a real terminal the “what it does” text after the colon is gray and italic (default CLI main menu style). `check-session` is not a row — login status is already under the title. Install, uninstall, self-update, where-is-me, version, and about stay off this list. Pick **1** `grok-auth` for backup, sync from the global store, remote sync, crontab, setup, and reinstall (**11–16**). On a multi-user host **11** is `backup` only when **logged in** and `sync-auth` only when **logged out**. **12** `sync-auth-from-remote` is listed only when **logged out**. Pick **7** `sudoers` for the grant list. Pick **8** `self-management` for version-check, self-update, self-uninstall, and where-is-me (**91–94**). **9** leaves from every list. **0** goes back only inside a submenu. **0** or `back` on the top list is a wrong pick and shows that same list again. A wrong number or name on the start list or on the sudoers list prints an error and shows **that same list** again so you can pick again — it does not quit. On a real terminal the `menu`/`main` list appears even if you also passed `--json`.

| You | Another role | Not this |
|-----|--------------|----------|
| Type `grok-cli`, `grok-cli --debug`, or `grok-cli menu`, pick a number | CI / pipe: empty argv ensures install; `menu` prints help; `--json` with no command gets JSON help | A menu that hangs a pipeline; a wrong pick that quits; help because `--debug` was present; `restore` on the list; install/version on the list; `sudoers` as a typed CLI command |

**Includes:** TTY empty argv numbered list; `menu`/`main` numbered TTY main list; default CLI main menu style (header `APP_NAME(APP_VERSION)`; TTY explain italic + light gray); session line under the title (**logged in** / **timeout** / **logged out**); **not-available** line on this-login-only hosts; **appended** logged-in not-available line when the session is valid; family row **sudoers** + submenu on multi-user hosts; invalid pick retries **this** layer (main, grok-auth, sudoers, self-management); Exit **9** on every layer; Back **0** on submenus only (no Back on the top list); off-TTY `menu` help. **Excludes:** a Back row on the top list; **0** / `back` leaving the top list; off-TTY empty argv (Type O); `help` as a list row; `check-session` as a numbered row; install / uninstall / self-update / where-is-me / version / about on either list; a live `sudoers` dispatcher token; showing backup / sync-auth / sudoers on Termux / Git Bash / Windows cmd; showing **sync-auth** / **sync-auth-from-remote** when **logged in**; showing **sync-auth-to-remote** when **logged out**; hiding **sync-auth-to-remote** when **logged in**; replacing the host not-available line with the logged-in line; a second TTY look (unstyled explain, SGR 90, styled number/name); `out_die` / process exit on a TTY menu typo.

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start at a prompt | Daily work; top **1** is `grok-auth`; Termux / Git Bash / Windows cmd also lists **2** `run`; the top list has no Back; login status is under the title | `grok-cli` then `1` |
| Open grok auth | Top **1**, then **11–16** | `grok-cli` then `1` |
| Start grok without auto-update | Top **2** on Termux / Git Bash / Windows cmd only | `grok-cli` then `2` (or `grok-cli run`) |
| Choose the menu language | Top **5**, then **51** English through **63** Ελληνικά. **50** and **64–69** are not printed. Front **6** is not a row | `grok-cli` then `5` |
| Push auth to the store | Auth **11**, listed only when **logged in** (not on this-login-only) | `grok-cli` then `1` then `11` |
| Pull auth from the global store | Auth **11** `sync-auth`, listed only when **logged out** on a multi-user host | `grok-cli` then `1` then `11` |
| Pull from another host | Auth **12**, listed only when **logged out** | `grok-cli` then `1` then `12` |
| Push to another host | Auth **13**, listed only when **logged in** | `grok-cli` then `1` then `13` |
| Install the timers | Auth **14** | `grok-cli` then `1` then `14` |
| Install grok from x.ai | Auth **15** `setup` | `grok-cli` then `1` then `15` |
| Reinstall grok | Auth **16** | `grok-cli` then `1` then `16` |
| Open grant/drafts | Top **7** `sudoers`. **Not listed** on Termux / Git Bash / Windows cmd | `grok-cli` then `7` then `1` |
| Check, update, or remove grok-cli | Top **8** `self-management`, then **91–94** | `grok-cli` then `8` |
| Step back | Back to the top list, only from a submenu | `0` |
| Leave the menu | Exit | `9` |
| Install the program | Not on this list | `grok-cli install` |
| Run with no args in a script | Channel ensure (not this menu) | `curl -fsSL … \| sh` |
| Run `menu` in a script | Help screen, no pick | `grok-cli menu </dev/null` |

---

## 2. Core Rules (Mandatory)

### 2.1 Claim and case

grok-cli **claims** a default function. **Case 3** applies: `requirement-shell-cli-zero-arguments` exists. That REQ **defers TTY empty argv** to this menu. Off-TTY empty argv is Type O ensure on that REQ — **this file MUST NOT** print help for bare off-TTY empty argv. Off-TTY **`menu`/`main`** still print help.

### 2.2 Routed verb `menu` / `main` and TTY empty argv

| Token | Role |
|-------|------|
| empty argv (no command token; overlay `--debug` / `--quiet` allowed) | Same handler as `menu` when TTY=1; Type O ensure when TTY=0 (owned by zero-arguments; **not** `app_default`) |
| `menu` | Primary named command for this default |
| `main` | Same handler (alias) |

After flag parse, when the command token is `menu` or `main`, **or** when no command token was present and `--json` is off (zero-arguments routes `COMMAND=menu` on a TTY — including `grok-cli --debug`), grok-cli **MUST** branch (`TTY` measured in the main process, **not** inside helpers):

| # | Condition | MUST | MUST NOT |
|---|-----------|------|----------|
| 1 | Interactive (`TTY=1`) | **Main menu** (§2.3). For `menu`/`main`, **ignore `--json`** even if `JSON=1` | JSON help; hang |
| 2 | Not interactive (`TTY=0`) and `JSON=0` | **Human help screen** — `app_help` (not JSON) | Menu; silent return; hang |
| 3 | Not interactive (`TTY=0`) and `JSON=1` | **JSON help** — `app_help` in JSON mode | Menu; human banners; hang |

`--quiet` without a TTY on **`menu`/`main`** still takes the **help screen** path (do not swallow `menu` help). Flags-only `--json` **is** empty argv on `requirement-shell-cli-zero-arguments`; **special case** = JSON help **even on a TTY** (this file **MUST NOT** steal it onto the numbered list). Overlay flags-only (`--debug`, `--quiet` with no command) follow the ordinary empty-argv path on that REQ. `grok-cli menu --json` on a TTY still ignores `--json` (rule 1).

### 2.3 Main menu

1. Print a **numbered list** of **daily auth work** plus one **family** row, then **Exit**.  
2. The **top** list **MUST** be families plus **9** Exit. The top list **MUST NOT** print a Back row. **`update-grok`** stays off every list. **`setup`** and **`reinstall`** **MUST** be on the **grok-auth** submenu (**15**, **16**), not on the top list. **`where-is-me`**, **`version-check`**, **`self-update`**, and **`self-uninstall`** **MUST** be on the **self-management** submenu (**91–94**), not on the top list. **Diagnostics** (`version`, `about`) and **test-purpose** verbs stay off every list.  
3. Command-row text **MUST** be `command: what it does`. The numbered list **MUST** follow **default CLI main menu style**: header as in rule 10; each numbered row `command: what it does` with the number and command name **unstyled**; on a TTY the **explain** text after `: ` **MUST** be *italic* **and** light gray (SGR **3** + **37**, CSI `ESC[3;37m` … `ESC[0m` via `out_menu_choice`). Off-TTY: plain. **MUST NOT** print explain unstyled on a TTY. **MUST NOT** a second house look (SGR 90, italic-only, gray-only, styled number/name).  
4. **MUST NOT** list `help`, `restore`, `menu`/`main`, `check-session`, or the five sudoers verbs on the **main** list (sudoers verbs live on the submenu; session status is under the title).  
5. Top numbers are **fixed**. Multi-user: **1** `grok-auth`, **5** `language`, **7** `sudoers`, **8** `self-management`, **9** Exit. This-login-only (Termux / Git Bash / Windows cmd): **1** `grok-auth`, **2** `run`, **5** `language`, **8** `self-management`, **9** Exit, and **MUST NOT** list **7** `sudoers`. Row **5** is on every host and is not a hide cause. Front **6** is not a row. The top list **MUST NOT** print Back. Exit **MUST** be **9** on every layer. Back **MUST** be **0** and **MUST** appear only on a submenu. On the top list, **0** / `back` is an invalid choice (rule 6b) and **MUST NOT** leave. **9** / `exit` / `quit` leaves from every layer.  
6. Accept a **number** or a **listed token**. **9** / `exit` / `quit` returns 0. **0** / `back` on a submenu returns to the top list. **0** / `back` on the top list **MUST NOT** return 0; it is an invalid choice (rule 6b).  
6b. **Invalid choice retries this layer (mandatory):** unused number, unknown name, leftover integer between **N** and Exit, or a hidden verb. The CLI **MUST** `out_error` (operator-readable: name the pick and the listed numbers), **reprint this layer**, and re-prompt in the current shell. **MUST NOT** `out_die` / process exit. **MUST NOT** leave this layer. **MUST NOT** treat the pick as unknown argv. Nested sudoers submenu: the same rule on **that** layer (invalid pick **MUST NOT** dump the operator back to the start list or out of the CLI). EOF / failed `read` **MUST** leave this layer without spinning. Reprint **MUST NOT** run a second live probe (reuse `GC_SESSION_STATUS_CACHE`). Proof **TP-CLI-30**.  
7. **`sudoers` is not a live CLI command.** On a multi-user host, choosing **7** or typing `sudoers` **MUST** open the sudoers submenu (§2.4). Choosing **1** or `grok-auth` **MUST** open the auth submenu (§2.4b). Choosing **8** or `self-management` **MUST** open the self-management submenu (§2.4c). Choosing **5** or `language` **MUST** open the language board (`requirement-shell-cli-language`). `language` is menu-only and **MUST NOT** be an argv verb. On Termux / Git Bash / Windows cmd, **sudoers** is not a listed row — choosing **7** or typing `sudoers` **MUST** be “not a menu choice”. `grok-cli sudoers` **MUST** remain unknown. Row **5** stays listed on that class. Choosing **6** on the front board **MUST** be “not a menu choice” and **MUST NOT** open the language board.  
8. Typing a submenu verb at the **main** pick prompt **MAY** run that handler (shortcut) when that verb is listed on this host’s menu. Live verbs excluded from both lists **MUST NOT** run from the pick prompt (typed `check-session` **MAY** still run as a shortcut). Hidden **backup** / **sync-auth** / **sudoers** on this-login-only hosts **MUST NOT** run from a listed number. Hidden **backup** when the session is not **valid** **MUST NOT** run from a listed number. Hidden **sync-auth** / **sync-auth-from-remote** when **logged in** **MUST NOT** run from a listed number.  
9. The choice **MUST** be read in the **current shell**. **MUST NOT** `$()` / backticks a helper whose body contains `read` (**do-not-capture-read** / **PP-A-22**; current-shell `PROMPT_ASK_VALUE`).  
10. **Header (mandatory — default CLI main menu style):** the first human line that names the program **MUST** be live **`APP_NAME(APP_VERSION)`** (`APP_VERSION` = Config `VERSION`) with **bold** name and *italic* version, then the product short description (`SHORT_DESCRIPTION` / `APP_DESC`). Typical: `out_info "$(util_app_ident) — ${SHORT_DESCRIPTION}"` which prints **Alternative online installer for xAI grok**. TTY: SGR 1 / SGR 3. Off-TTY: plain. **MUST NOT** a bare `APP_NAME` on that header. **MUST NOT** the generic board title “numbered list of live commands”.  
11. **Session line (mandatory):** immediately under the header, print an independent **`out_info`** line (**`[INFO]`** on its own line) — **`logged in`** when `gc_session_status_word` is `valid`, **`timeout`** when it is `timeout`, otherwise **`logged out`**. **MUST NOT** `out_plain` this word (it would lack `[INFO]`). That word **MUST** use the session gate on `requirement-grok-auth-backup`. On PRoot/Termux **MUST** use local `auth.json` cookies and **MUST NOT** exec `grok -p hello` for this line. On other hosts **MUST** use the live `grok -p hello` probe — **MUST NOT** treat `auth.json` parse alone as logged-in there. **MUST NOT** print **`logged out`** when a live probe hit `GROK_PROMPT_TIMEOUT` (default **14** seconds) — that line is **`timeout`**. `timeout` is **not** logged-in: hide-sync-auth / logged-in not-available apply only when the word is `valid`. When the live probe runs it **MUST** close stdin and **MUST NOT** hang the menu — **MUST** bound even when GNU `timeout` is missing, and **MUST** SIGKILL-follow (`timeout -k` or POSIX watchdog). On a **first** paint (no `GC_SESSION_STATUS_CACHE` yet) on hosts that still run the live probe, **MUST** print a non-DEBUG progress line **`checking session (grok -p hello, timeout {{GROK_PROMPT_TIMEOUT}}s)...`** after the header and before the probe so a wait up to the bound is not indistinguishable from deadlock. On PRoot/Termux **MUST NOT** print that grok -p hello checking line. **MUST NOT** print the checking line on a reprint that reuses the cache. A reprint after a bad pick **MUST NOT** run a second live probe (reuse `GC_SESSION_STATUS_CACHE`). **MUST NOT** make this a numbered row.  
12. **Not-available line (mandatory on this-login-only hosts):** immediately under the session line, when the host is Termux / Git Bash / Windows cmd (detect in **Under command line for normal user only**), print an independent **`out_info`** line (**`[INFO]`** on its own line) whose text is exactly **`backup, sync-auth and sudoers features are not available in {{label}}.`** where **label** is **`termux`**, **`gitbash`**, or **`windows-cmd`**. **MUST NOT** `out_plain` this sentence. **MUST NOT** make this a numbered row. **MUST NOT** print this line on a multi-user host.  
13. **Logged-in not-available line (mandatory when session is valid):** when `gc_session_status_word` is `valid`, **MUST NOT** display **sync-auth** or **sync-auth-from-remote**. **MUST** display **sync-auth-to-remote**. When the session is not **valid**, **MUST NOT** display **sync-auth-to-remote**. Immediately under the host not-available line when that line is printed, otherwise immediately under the session line, **MUST** print an independent **`out_info`** line (**`[INFO]`** on its own line) whose text is exactly **`sync-auth and sync-auth-from-remote features are not available for logged-in environment.`** This line **MUST** be an **additional** `out_info` line — **MUST NOT** replace, rewrite, or drop the host not-available line. **MUST NOT** `out_plain` this sentence. **MUST NOT** make this a numbered row. **MUST NOT** print this line when the session is not valid. **MUST NOT** name **sync-auth-to-remote** in that sentence.  
13b. **Auth submenu session rows (mandatory):** on a multi-user host, when the session word is `valid`, the grok-auth list **MUST** display **11** `backup` and **MUST NOT** display **11** `sync-auth`. When the session word is not `valid` (`logged out` or `timeout`), that list **MUST** display **11** `sync-auth` (copy the global store into `~/.grok`) and **12** `sync-auth-from-remote`, and **MUST NOT** display **11** `backup`. On Termux / Git Bash / Windows cmd, **MUST NOT** display **11** in either session. Numbers **12–16** **MUST NOT** slide. **17** is not an auth row. Direct CLI `backup` and `sync-auth` stay routed.  
13c. **Logged-out not-available line (mandatory when session is not valid):** when `gc_session_status_word` is not `valid` (`logged out` or `timeout`), **MUST** print an independent **`out_info`** line whose text is exactly **`backup and sync-auth-to-remote features are not available for logged-out environment.`** Place it in the same slot as the logged-in line: immediately under the host not-available line when that line is printed, otherwise immediately under the session line. **MUST** print the same line again on the grok-auth submenu. **MUST NOT** print this line when the session is `valid`. **MUST NOT** replace or drop the host line or the logged-in line. **MUST NOT** `out_plain` this sentence. **MUST NOT** make it a numbered row. **MUST NOT** name **sync-auth** or **sync-auth-from-remote** in that sentence. Timeout uses this same logged-out sentence.  
14. **Debug elapsed (mandatory when `DEBUG=1`):** the numbered list **MUST** print elapsed wall-clock of each paint step on stderr via `out_debug` (`requirement-shell-internal-volatile-timer`). Stages: `paint`, `header`, `session`, `host`, `logged-in`, `rows` (plus `sudoers.*` on the submenu). **MUST NOT** put elapsed on numbered choice rows. **MUST NOT** print those lines when `DEBUG=0`. **MUST NOT** hang or skip the list because a timer helper failed.

Normative **main** order (multi-user host, **logged out**):

| # | Token | Label |
|---|-------|-------|
| *(header)* | — | `**APP_NAME**(*APP_VERSION*) — Alternative online installer for xAI grok` |
| *(status)* | — | `[INFO] logged in` / `[INFO] timeout` / `[INFO] logged out` |
| *(not-available)* | — | `[INFO] backup and sync-auth-to-remote features are not available for logged-out environment.` |
| 1 | `grok-auth` | `grok-auth: Backup, sync, crontab, setup, and reinstall` |
| 5 | `language` | `language: display language for this menu` |
| 7 | family `sudoers` | `sudoers: Grant and drafts` |
| 8 | `self-management` | `self-management: Check, update, or remove grok-cli` |
| **9** | **Exit** | leave the menu |

### 2.3b Main menu on command line for normal user only

When detect is Termux / Git Bash / Windows cmd, the start list **MUST NOT** display **backup**, **sync-auth**, or **sudoers**. Remaining listed verbs **MUST** be numbered from **1**. Direct CLI `{{APP_NAME}} backup` / `sync-auth` stay routed (unused on this class is menu honesty, not a second dispatcher).

Normative **main** order (this-login-only host, **logged out**):

| # | Token | Label |
|---|-------|-------|
| *(header)* | — | `**APP_NAME**(*APP_VERSION*) — Alternative online installer for xAI grok` |
| *(status)* | — | `[INFO] logged in` / `[INFO] timeout` / `[INFO] logged out` |
| *(not-available)* | — | `[INFO] backup, sync-auth and sudoers features are not available in {{termux\|gitbash\|windows-cmd}}.` |
| *(not-available)* | — | `[INFO] backup and sync-auth-to-remote features are not available for logged-out environment.` |
| 1 | `grok-auth` | `grok-auth: Backup, sync, crontab, setup, and reinstall` |
| 2 | `run` | `run: Start grok without auto-update` |
| 5 | `language` | `language: display language for this menu` |
| 8 | `self-management` | `self-management: Check, update, or remove grok-cli` |
| **9** | **Exit** | leave the menu |

### 2.3c Main menu when logged in

When the session line is **logged in**, the start list **MUST NOT** display **sync-auth** or **sync-auth-from-remote** (any host) and **MUST** display **sync-auth-to-remote**. When the session is **logged out** (or **timeout**), the start list **MUST NOT** display **sync-auth-to-remote**. Direct CLI `{{APP_NAME}} sync-auth` / `sync-auth-from-remote` stay routed; the copy skip is `requirement-grok-auth-backup`. Direct CLI `sync-auth-to-remote` stays routed and **MUST NOT** skip. Remaining listed verbs **MUST** be numbered from **1**.

Normative **main** order (multi-user host, **logged in**):

| # | Token | Label |
|---|-------|-------|
| *(header)* | — | `**APP_NAME**(*APP_VERSION*) — Alternative online installer for xAI grok` |
| *(status)* | — | `[INFO] logged in` |
| *(not-available)* | — | `[INFO] sync-auth and sync-auth-from-remote features are not available for logged-in environment.` |
| 1 | `grok-auth` | `grok-auth: Backup, sync, crontab, setup, and reinstall` |
| 5 | `language` | `language: display language for this menu` |
| 7 | family `sudoers` | `sudoers: Grant and drafts` |
| 8 | `self-management` | `self-management: Check, update, or remove grok-cli` |
| **9** | **Exit** | leave the menu |

Normative **main** order (this-login-only host, **logged in**) — host line **then** logged-in line (**append**, never replace):

| # | Token | Label |
|---|-------|-------|
| *(header)* | — | `**APP_NAME**(*APP_VERSION*) — Alternative online installer for xAI grok` |
| *(status)* | — | `[INFO] logged in` |
| *(not-available)* | — | `[INFO] backup, sync-auth and sudoers features are not available in {{termux\|gitbash\|windows-cmd}}.` |
| *(not-available)* | — | `[INFO] sync-auth and sync-auth-from-remote features are not available for logged-in environment.` |
| 1 | `grok-auth` | `grok-auth: Backup, sync, crontab, setup, and reinstall` |
| 2 | `run` | `run: Start grok without auto-update` |
| 5 | `language` | `language: display language for this menu` |
| 8 | `self-management` | `self-management: Check, update, or remove grok-cli` |
| **9** | **Exit** | leave the menu |

### 2.4 Sudoers submenu

On a multi-user host, choosing **7** / `sudoers` **MUST** print a second numbered list of the grouped live verbs. On Termux / Git Bash / Windows cmd the family row is omitted (§2.3b). Submenu header **MUST** use the same `APP_NAME(APP_VERSION)` nametag. Explain text **MUST** follow the same default CLI main menu style as the main list (*italic* + light gray SGR **3** + **37** on a TTY via `out_menu_choice`). **MUST NOT** hang off-TTY (submenu exists only on the interactive menu path).

| # | Command | Label |
|---|---------|-------|
| 1 | `generate-sudoer-request` | `generate-sudoer-request: Write a JSON grant you can read` |
| 2 | `submit-sudoer-request` | `submit-sudoer-request: Queue the JSON grant inbound` |
| 3 | `print-sudoers` | `print-sudoers: Emit sudoers draft` |
| 4 | `print-sudoers-install-script` | `print-sudoers-install-script: Write admin install script` |
| 5 | `remove-project-sudoers` | `remove-project-sudoers: Remove sudoers draft only` |
| **0** | **Back** | return to the main list (not a command) |
| **9** | **Exit** | leave the menu |

Submenu command rows **N = 5**. Exit **MUST** be **9**. **Back MUST** be **0** on every submenu (auth, sudoers, self-management). The top list **MUST NOT** print Back.

- **0** / `back` / `Back` on a submenu returns to the main list (does not run a handler).  
- **9** / `exit` / `quit` returns 0 from `menu` (same as main Exit).  
- A listed number or verb runs that handler, then returns 0 from `menu` (one command, then done).  
- An invalid submenu pick **MUST** `out_error`, reprint **this** grant list, and re-prompt (§2.3 rule 6b). **MUST NOT** return to the start list. **MUST NOT** exit.  
- All five grouped verbs **MUST** appear here. **MUST NOT** put install/version/about/`help`/`restore` on this list.

### 2.4b grok-auth submenu

Choosing **1** / `grok-auth` **MUST** print this list. Numbers are fixed. A hidden row is not printed and is not a choice. **11** `sync-auth` (logged out) is the pull from the global store (`/var/grok-cli/auth.*` into `~/.grok`). **11** `backup` (logged in) is the push the other way. One of those two tokens is listed, never both.

| # | Command | When listed | Label |
|---|---------|-------------|-------|
| 11 | `backup` | multi-user and session **valid** | `backup: Push ~/.grok/auth.* to /var/grok-cli` |
| 11 | `sync-auth` | multi-user and session not **valid** | `sync-auth: Copy /var/grok-cli/auth.* into ~/.grok` |
| 12 | `sync-auth-from-remote` | session not **valid** | `sync-auth-from-remote: Copy a remote host's auth.* into ~/.grok` |
| 13 | `sync-auth-to-remote` | session **valid** | `sync-auth-to-remote: Copy ~/.grok/auth.* onto a remote host` |
| 14 | `add-crontab` | always | `add-crontab: Add backup and sync-auth jobs to this login's crontab` |
| 15 | `setup` | always | `setup: Install grok from x.ai` |
| 16 | `reinstall` | always | `reinstall: Remove existing grok and install again` |
| **0** | **Back** | submenu | return to the top list |
| **9** | **Exit** | every layer | leave the menu |

Logged-out (or **timeout**) multi-user order: **11** `sync-auth`, **12**, **14**, **15**, **16**. **13** is omitted. Logged-in multi-user order: **11** `backup`, **13**, **14**, **15**, **16**. **12** is omitted. This-login-only omits **11** in both sessions. **17** is not a row.

### 2.5 Implementation Notes (this product)

| Item | Value |
|------|--------|
| **Product** | grok-cli |
| **Ship unit** | `src/grok-cli` |
| **Claimed** | yes |
| **Case** | **3** (zero-argument REQ exists; that REQ defers TTY empty argv here; off-TTY empty argv is Type O, not this file) |
| **Empty argv** | TTY → this menu; off-TTY → Type O ensure (`requirement-shell-cli-zero-arguments`; not this handler) |
| **Verb** | `menu` (alias `main`); TTY empty argv (including `--debug` with no command) sets `COMMAND=menu` |
| **Handler** | `app_default` (`menu` / `main` / TTY empty argv); submenu printer/loop under the same `app_default_*` family |
| **Family row** | `sudoers` — menu-only; **not** dispatched |
| **Label source** | `reviews/cli-routed-verb-table.md` **human-readable** for command rows; family explain is this file’s table |
| **Interactive + `--json`** | Ignore json on `menu`/`main`; still the menu |
| **Non-interactive** | `app_help` (human; `--quiet` still prints help) |
| **Look** | **default CLI main menu style** — header `APP_NAME(APP_VERSION)`; TTY explain *italic* + light gray (SGR 3+37) via `out_menu_choice`; number and name unstyled |
| **Honesty** | **Implemented.** TTY empty argv (including `--debug` with no command) draws this menu. Off-TTY empty argv is Type O ensure (not help, not this menu). Header `APP_NAME(APP_VERSION)`; session line under the title is independent **`out_info`** (**`[INFO] logged in`** / **`timeout`** / **`logged out`**; default bound 14s; reprint reuses `GC_SESSION_STATUS_CACHE`); host not-available and logged-in not-available are each their own **`out_info`** line; top list **1** grok-auth, **5** language (every host), **7** sudoers (multi-user), **8** self-management, **2** run (this-login-only); auth **11–16** with **11** `sync-auth` and **12** when logged out (**13** hidden), **11** `backup` and **13** when logged in (**12** hidden), and **11** hidden on this-login-only; self-management **91–94**; language block **50–69** (assigned **51–63**); front **6** is not a row; sudoers submenu **N = 5**; Exit **9** on every layer; Back **0** on submenus only (the top list has no Back row; **0** / `back` there is an invalid choice). Invalid pick at **any** listed layer is `out_error` + reprint this layer (not `out_die`). `--debug` prints elapsed of each paint step (`requirement-shell-internal-volatile-timer`). Copy for non-English follows `requirement-shell-cli-language`. |
| **Host detect** | `gc_host_is_normal_user_only` / `gc_host_normal_user_only_label` (`termux` · `gitbash` · `windows-cmd`) |

### 2.6 Why this requirement exists (CIAO)

- **Intentional**: Daily auth work is the start list; grant/draft commands are one extra pick.  
- **Caution**: Scripts never hang; `--json` on a real terminal does not hide the `menu` list.  
- **Anti-fragile**: Back on a submenu returns to the start list; the top list has no Back; Exit leaves from every screen; a wrong pick reprints **that** layer.  
- **Over-protect**: `sudoers` is not a live dispatcher token; install / version / about / `help` / `restore` stay off both lists; Exit is **9**, not **5**.

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

**This requirement:** omit **backup**, **sync-auth** (auth **11**), and **sudoers** from the numbered list on detect. The top list is **1** `grok-auth`, **2** `run`, **5** `language`, **8** `self-management`, and **9** Exit, with no Back row. Row **5** is not a hide cause. Front **6** is not a row. Omit auth **13** `sync-auth-to-remote` when **logged out**. Immediately under the login status print an independent **`[INFO]`** **`backup, sync-auth and sudoers features are not available in {{termux/gitbash/windows-cmd}}.`** When **logged in**, **also** omit auth **12** `sync-auth-from-remote`, **list** **13** `sync-auth-to-remote`, and **append** the logged-in not-available **`[INFO]`** line (§2.3c) after the host line. Do not add sudo-install rows.

---

## 3. Design Principles

- The start list is **daily work**, not a reprint of `help`.  
- Related rare commands share one family row.  
- Dispatcher remains routing SSOT (`sudoers` is not added there).  
- Fail closed off-TTY.  
- Zero-arguments owns Type O off-TTY vs TTY menu; this file owns the list body.

---

## 4. Protection Rule (Sacred)

Future agents **MUST NOT**:

1. Put `install`, `uninstall`, `where-is-me`, `version`, `about`, `help`, `menu`/`main`, or `restore` on the main list or the sudoers submenu.  
2. Put the five sudoers verbs on the **main** list.  
2b. Put `check-session` on the numbered main list (login status **MUST** stay under the title).  
3. Drop a grouped sudoers verb from the submenu.  
4. Put a Back row on the top list, treat top-list **0** / `back` as leave, number Exit as anything but **9**, or number submenu Back as anything but **0**. Exit **MUST** be **9** on every layer. Back **MUST** be **0** and **MUST** appear only on a submenu.  
5. Wire `sudoers` as a live `app_main` command.  
6. Draw this menu on **off-TTY** empty argv, or hang a pipe on empty argv / `menu` / `main`.  
7. Steal Type O install-ensure onto **TTY** empty argv (menu stolen).  
8. Invent command-row labels that are not `command: what it does`.  
9. Replace TTY empty argv with the help dump while zero-arguments **1.3.0+** defers that path here.  
9b. Treat TTY `grok-cli --debug` (no command) as help instead of this menu. Overlay flags-only is empty argv (`requirement-shell-cli-zero-arguments` **2.1.0+**).  
9c. Draw this menu for TTY `grok-cli --json` (no command). That invocation **is** empty argv but the special-case outcome is JSON help (`requirement-shell-cli-zero-arguments` **2.2.0+**).  
10. Print a main-menu (or APP_NAME-led submenu) header as a bare `APP_NAME` without live `VERSION` / `APP_VERSION`, or unstyled on TTY.  
11. Capture the menu choice with `$()` of a `read` helper.  
12. Draw the numbered list off **default CLI main menu style** — **MUST NOT** print numbered-choice explain unstyled on a TTY (it **MUST** be *italic* and light gray, SGR **3** + **37**, via `out_menu_choice`). **MUST NOT** invent a second house look (SGR 90, italic-only, gray-only, styled number/name).  
13. Print the generic board title “numbered list of live commands” instead of Config `SHORT_DESCRIPTION` / `APP_DESC` (**Alternative online installer for xAI grok**).  
14. Print **logged in** from `auth.json` parse alone (the session line **MUST** use `grok -p hello`).  
15. Strip the **Under command line for normal user only** section, or enable admin privilege / a dedicated system user on Termux / Git Bash / Windows cmd.  
16. Display **backup**, **sync-auth**, or **sudoers** on the main list on Termux / Git Bash / Windows cmd.  
17. Omit the **host not-available** line on that class, print it on a multi-user host, or invent a different wording / host label (`termux` · `gitbash` · `windows-cmd`).  
18. Display **sync-auth** or **sync-auth-from-remote** on the main list when the session is **logged in**, omit **sync-auth-to-remote** on that session, display **sync-auth-to-remote** when the session is **logged out**, or omit the logged-in not-available line on a logged-in session.  
19. Replace the host not-available line with the logged-in line, merge them into one sentence, or skip the host line because the session is logged in. The logged-in line **MUST** append.  
20. Freeze the numbered menu on Termux (or any host) while waiting for `grok -p hello` — missing `timeout`, a peer that ignores SIGTERM, or a second probe on reprint.  
21. Skip `--debug` elapsed of each paint step, print those lines when `DEBUG=0`, or put elapsed onto numbered choice rows.  
22. Omit **`run`** from the this-login-only start list, or number it after backup/sync-auth/sudoers on that class.  
22b. Omit **`reinstall`** from the numbered start list (any host), list **`setup`** or **`update-grok`** instead of **`reinstall`**, or number **`reinstall`** before **`run`** on this-login-only hosts.  
23. Leave the menu silent between the INFO header and **logged in** / **timeout** / **logged out** while a live `grok -p hello` probe can take more than a few seconds. **MUST** print the checking-session progress line on first paint **when the live probe runs**.  
24. Print **logged out** when the live probe hit the deadline. That line **MUST** be **timeout**. Default `GROK_PROMPT_TIMEOUT` **MUST** be **14** (override still allowed).  
25. On PRoot/Termux, print the grok -p hello checking-session line, or exec `grok -p hello` for the session line. That class **MUST** use local auth cookies.  
26. Print the session word or a not-available sentence with `out_plain` (no `[INFO]`). Each of those lines **MUST** be its own `out_info` so the operator sees `[INFO]` on every such line.  
27. **`out_die` / exit** on an invalid TTY menu choice at any layer (unused number, unknown name, leftover integer, nested-layer typo) — **MUST** `out_error`, reprint **this** layer, and re-prompt (**TP-CLI-30**). **MUST NOT** treat that pick as unknown argv.
28. Omit front **5** `language`, or treat **5** as an invalid pick. **5** opens the language board on every host (`requirement-shell-cli-language`). Front **6** is not a row. An unused front integer for the invalid-pick proof is **4**. On Termux / Git Bash / Windows cmd the unused front integer that replaced **5** is **6**.  
29. On a multi-user host, display auth **11** `backup` when the session is not **valid**, omit auth **11** `backup` when the session is **valid**, omit auth **11** `sync-auth` when the session is not **valid**, display auth **11** `sync-auth` when the session is **valid**, or number `sync-auth` as anything other than **11**. On Termux / Git Bash / Windows cmd, display auth **11**.  
30. Omit **`backup and sync-auth-to-remote features are not available for logged-out environment.`** when the session is not **valid**, print that line when the session is **valid**, replace the host line or the logged-in line with it, or `out_plain` it.  


## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-07** | `tests/test_cli.sh` | have (TTY empty argv = this menu; off-TTY empty argv = Type O ensure) |
| **TP-CLI-29** | `tests/test_cli.sh` | have (TTY `--debug` no command = this menu; off-TTY `--debug` no command = Type O ensure) |
| **TP-CLI-13** | `tests/test_cli.sh` | have (main list has no Back, family row, top **0** retries, submenu Back/Exit, off-TTY help) |
| **TP-CLI-17** | `tests/test_cli.sh` | have (default CLI main menu style: header `APP_NAME(APP_VERSION)` bold/italic; board title **Alternative online installer for xAI grok**; numbered explain italic + light gray SGR 3+37; number/name unstyled; logged in / timeout / logged out from live `grok -p hello`; no check-session row) |
| **TP-CLI-19** | `tests/test_cli.sh` | have (Termux / Git Bash / Windows cmd: hide backup / sync-auth / sudoers; **run** is **1**; not-available line under session; remaining rows from **1**) |
| **TP-CLI-20** | `tests/test_cli.sh` | have (logged in: hide sync-auth / sync-auth-from-remote; append logged-in not-available line; host line still present on this-login-only; remaining rows from **1**; listed sudoers number opens submenu) |
| **TP-CLI-21** | `tests/test_cli.sh` | have (Termux hang-grok uses local cookies: **logged out** with no auth; no grok -p hello checking line; no freeze) |
| **TP-CLI-22** | `tests/test_cli.sh` | have (bad pick reprints without a second hang-grok probe) |
| **TP-CLI-23** | `tests/test_cli.sh` | have (`timeout -k` + watchdog + setsid + ignore TSTP + wait reaper first + checking-session source; default `GROK_PROMPT_TIMEOUT` 14; menu prints `timeout`) |
| **TP-CLI-25** | `tests/test_cli.sh` | have (`--debug menu` elapsed of each paint step, including `sudoers.*`) |
| **TP-CLI-26** | `tests/test_cli.sh` | have (no `--debug` → no menu-step elapsed; still prints checking-session) |
| **TP-CLI-30** | `tests/test_cli.sh` | have (invalid choice at any menu layer: `out_error` + reprint this layer; unused front integer **4** and unknown name; sudoers submenu unused **6** stays on that list; Termux front unused **6**; process does not exit; not unknown argv) |
| **TP-CLI-31** | `tests/test_cli.sh` | have (TTY main list includes `reinstall`; `setup` / `update-grok` stay off) |
| **TP-CLI-32** | `tests/test_cli.sh` | have (front **5** language board **51–63**; **50** and **64–69** unprinted; front **6** does not open the board; save; `GROK_CLI_LANG`; Back does not write) |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`

---

**Last Updated**: 2026-10-10 (2.24.0 — logged-out auth **11** is `sync-auth` and **12** is `sync-auth-from-remote`; logged-in **11** stays `backup`. 2.23.0 had parked the pull on **17**.)  
**Owner**: product  
**Alignment**: `requirement-shell-cli-zero-arguments` · `requirement-shell-cli-interface` · `requirement-shell-cli-language` · `requirement-shell-interactive-vs-noninteractive` · `requirement-shell-output-requirements` · `requirement-shell-internal-volatile-timer` (`--debug` elapsed) · `requirement-grok-auth-backup` (session probe) · `requirement-domain-grok-cli` (no `restore`) · CIAO / CIAO-Lite
