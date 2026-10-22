**file**: docs/requirements/requirement-domain-grok-cli.md  
**Status**: Active (Version 1.10.4)  
**Area**: domain  
**Key**: `requirement-domain-grok-cli`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

> Ship unit (2026-10-22): Python package **AgentCli**, console script **`agent-cli`**, module `python -m AgentCli`. The product was renamed from grok-cli. Where this file names the product command `grok-cli`, the console script is `agent-cli`. The deposit directory in the package is `/var/agent-cli`. Peer binary remains `grok`. Auth files remain under `~/.grok`. Behavioral MUST rules below stay. Empty argv on a terminal opens the text menu. Empty argv with no terminal prints help and returns 0. Package install is pip. This file does not run a vendor shell installer.

## 1. Purpose

This requirement is the **domain surface Single Source of Truth** for grok-cli: which **specialized CLI verbs** exist, what **help** and **about** must show, and how domain routing is labeled.

**Operational session / deposit / sync behavior** is **not** owned here — it is owned by **`requirement-grok-auth-backup`**.  
**Elevation and sudoers files** (emit / install / submit **workflow**) are owned by **`requirement-three-layer-privilege-model`**.  
**JSON sudoer file body** (grant = **`{{PRJ_NAME}}` only**, verb **`backup`**) is owned by **`requirement-sudoer-json-file`**.

This file is the sole Active **`requirement-domain-*`** (four pillars). It supersedes `requirement-domain-grok-cli`.

### 1.1 Human-facing

This file lists the grok-cli commands a login types after install: place the xAI `grok` program (`setup`), refresh it (`update-grok`), reinstall it (`reinstall`), start grok without auto-update (`run`), check that grok is signed in, push `~/.grok/auth.*` into `/var/grok-cli`, or copy those files back into `~/.grok` without sudo.

| You | Another role | Not this |
|-----|--------------|----------|
| Run `setup`, `run`, `check-session`, `backup`, `sync-auth`, `sync-auth-from-remote`, `sync-auth-to-remote`, `add-crontab`, and the sudoer generate/submit verbs | sudoer-adm approves the JSON grant so `sudo grok-cli backup` is passwordless | Folder tar.gz backup; writing `/etc` yourself; typing `restore` (retired — the program must say unknown); using `setup` to install grok-cli |

**Includes:** verb catalog, help rows, about fields, pointers to ops and privilege law.  
**Excludes:** JWT/token parsing rules, chown/chmod numbers, sudoers schema (peer files).

| Surface | What you open | What for |
|---------|---------------|----------|
| `./src/grok-cli` | ship unit | live behavior |
| `grok-cli help` | command | listed verbs |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Place grok | grok-cli fetches xAI’s version pointer and matching `grok` binary (does not run `install.sh`) | `grok-cli setup` |
| Reinstall grok | Same fetch as `setup --force`; keeps `auth.*`; grok-auth **16** | `grok-cli reinstall` |
| Latest grok | grok-cli fetches the channel again (does not use grok auto-update; not grok-cli `self-update`) | `grok-cli update-grok` |
| Start grok on Termux | grok-cli starts grok with auto-update off so PRoot is not left hanging | `grok-cli run` |
| Confirm login | grok-cli runs `grok -p hello` first (a file that only looks valid is not enough). If `proot` is on PATH, that probe uses the PRoot reaper so the menu does not wait on PRoot | `grok-cli check-session` |
| Push shared auth | After a valid session, grok-cli copies `auth.*` into `/var/grok-cli` as root | `grok-cli backup` |
| Pull shared auth | A normal login copies from `/var/grok-cli` into `~/.grok` with no sudo | `grok-cli sync-auth` |
| Pull from another host | `scp` that host’s store into `~/.grok` | `grok-cli sync-auth-from-remote user@192.0.2.10` |
| Push to another host | `ssh` + `scp` this login’s `~/.grok/auth.*` onto that login’s `~/.grok`. Typed command. Not a numbered row. Still runs when grok is logged in | `grok-cli sync-auth-to-remote user@192.0.2.10` |
| Install the timers | This login’s crontab gets backup every 30 minutes and sync-auth at minute 45 | `grok-cli add-crontab` |

---

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — Specialized CLI subcommands

| Command | Operands / flags | Handler prefix | Behavior summary | Behavior SSOT |
|---------|------------------|----------------|------------------|---------------|
| `setup` | `--force`; TTY keep / reinstall / Exit when grok already runs | `gc_*` | Fetch xAI channel + artifact and place peer `grok`; **MUST NOT** exec `install.sh`; skip if grok already runs off-TTY / `--json`; on a TTY offer reinstall; Android ET_EXEC may place an exec wrapper | **`requirement-grok-setup`** |
| `update-grok` | — | `gc_*` | Refresh peer grok from xAI channel + artifact (same as `setup --force`); missing grok Next `setup`; **MUST NOT** exec grok auto-update | **`requirement-grok-setup`** |
| `reinstall` | — | `gc_*` | Remove existing grok and install again (same as `setup --force`); grok-auth **16**; missing grok still fetches; **MUST NOT** delete `auth.*` | **`requirement-grok-setup`** |
| `run` | remaining grok argv | `gc_*` | Start peer grok with `--no-auto-update` (unless already passed); missing grok Next `setup`; `--json` does not exec | **`requirement-grok-setup`** |
| `check-session` | none | `gc_*` | Confirm grok is logged in (`grok -p hello` first; if `proot` on PATH use the reaper, else simple `-p`) | **`requirement-grok-auth-backup`** (procedure) · **`requirement-shell-termux-coding`** (PRoot writing) |
| `backup` | none | `gc_*` | Check session, then elevated deposit of `auth.*` into `/var/grok-cli` | **`requirement-grok-auth-backup`** |
| `sync-auth` | none | `gc_*` | Copy `/var/grok-cli/auth.*` into `~/.grok` **without sudo**; skip when already logged in | **`requirement-grok-auth-backup`** |
| `sync-auth-from-remote` | SPEC (`user@IPv4`, IPv4, domain, `user@domain`) | `gc_*` | `scp` remote `/var/grok-cli/auth.*` into `~/.grok` **without sudo**; skip when already logged in | **`requirement-grok-auth-backup`** |
| `sync-auth-to-remote` | SPEC (same four forms) | `gc_*` | `ssh` + `scp` this login’s `~/.grok/auth.*` onto the remote login’s `~/.grok` **without sudo**; still runs when already logged in; not a numbered row | **`requirement-grok-auth-backup`** · **`requirement-shell-cli-default-interaction`** |
| `add-crontab` | none | `gc_*` | Install this login’s crontab jobs (backup every 30 min; sync-auth at :45) after **this** login’s backup grant exists | **`requirement-grok-crontab`** |
| `print-sudoers` | optional output path; `--allow-test-local` when test_local | `gc_*` | Emit **project-sudoers-file** (draft; no `/etc` write) | **`requirement-three-layer-privilege-model`** |
| `print-sudoers-install-script` | optional script path; same trust gate | `gc_*` | Admin handoff script under `/dev/shm` or temp | **`requirement-three-layer-privilege-model`** |
| `remove-project-sudoers` | optional path; `--force` | `gc_*` | Remove **project-sudoers-file** draft only (not `/etc`) | **`requirement-three-layer-privilege-model`** |
| `generate-sudoer-request` | optional dest path; `--update` / `--add`; `--allow-test-local` | `gc_*` | Independent JSON grant (compact; **backup** only) to a dest readable without sudo | workflow: **`requirement-three-layer-privilege-model`** · JSON body: **`requirement-sudoer-json-file`** |
| `submit-sudoer-request` | optional sudoers file; `--purpose`; `--update` / `--add`; `--allow-test-local` | `gc_*` | Type 0 submitter into `/var/sudoer-cli/sudoer-request` | workflow: **`requirement-three-layer-privilege-model`** · JSON body: **`requirement-sudoer-json-file`** |

**Routing:** Dispatcher in `app_main` **MUST** route these verbs; unknown operands fail closed.  
**MUST NOT** route `restore` (retired folder-archive verb).

### 2.2 Pillar B — Specialized features (surface map only)

| Feature area | Domain role | Full law |
|--------------|-------------|----------|
| Peer grok install | Expose `setup` (channel + artifact procedure; not grok-cli install; not `install.sh`) | `requirement-grok-setup` |
| Peer grok update | Expose `update-grok` (not grok auto-update; not grok-cli `self-update`) | `requirement-grok-setup` |
| Peer grok reinstall | Expose `reinstall` (grok-auth **16**; not grok-cli `self-update`) | `requirement-grok-setup` |
| Start grok without auto-update | Expose `run` | `requirement-grok-setup` |
| Grok session gate | Expose `check-session`; backup MUST call the same gate | `requirement-grok-auth-backup` |
| PRoot-aware one-shot | Same gate: `command -v proot` → reaper; else simple `grok -p hello`. Hang chain is leftover `runsvdir` from `bash -lc` → `start-services.sh` | `requirement-shell-termux-coding` (writing) · `requirement-grok-auth-backup` (procedure) |
| Auth deposit | Expose `backup` | `requirement-grok-auth-backup` |
| Unprivileged sync | Expose `sync-auth` | `requirement-grok-auth-backup` |
| Remote unprivileged sync | Expose `sync-auth-from-remote` | `requirement-grok-auth-backup` |
| Remote unprivileged push | Expose `sync-auth-to-remote` | `requirement-grok-auth-backup` |
| Per-login crontab timers | Expose `add-crontab` | `requirement-grok-crontab` |
| Sudoers draft print | Expose `print-sudoers` | `requirement-three-layer-privilege-model` |
| Admin sudoers install script | Expose `print-sudoers-install-script` | `requirement-three-layer-privilege-model` |
| Remove project-sudoers draft | Expose `remove-project-sudoers` | `requirement-three-layer-privilege-model` |
| Generate sudoer file | Expose `generate-sudoer-request` | workflow + `requirement-sudoer-json-file` |
| Submit sudoers for approval | Expose `submit-sudoer-request` | workflow + `requirement-sudoer-json-file` |

**Filename grammar** (queued sudoer request — sibling allocator; informative):

```text
sudoer-{{YYYYMMDD}}-grok-cli-{{username}}-{{action}}-{{n}}.json
```

**Worked sample basename (add):** `sudoer-20260822-grok-cli-<id -un>-add-1.json`

**Complete sample JSON grant (add):**

```json
{
  "schema_version": 1,
  "purpose": "Allow <id -un> to run grok-cli backup as root.",
  "username": "<id -un>",
  "service": "grok-cli",
  "action": "add",
  "commands": [
    {
      "runas": "root",
      "tags": ["NOPASSWD"],
      "path": "/usr/local/bin/grok-cli",
      "args": ["backup"]
    }
  ]
}
```

**Complete sample JSON grant (update):** same `commands`; `"action": "update"`.

**Equivalent text dual:**

```text
<id -un> ALL=(root) NOPASSWD: /usr/local/bin/grok-cli backup
```

### 2.3 Pillar C — Specialized project help items

`help` **MUST** show domain rows (in addition to Type 0 lifecycle):

| Help row | Text intent |
|----------|-------------|
| `setup` | Install grok from x.ai (channel + artifact; TTY offers reinstall if grok already runs) |
| `update-grok` | Update grok from x.ai (not grok-cli; avoids grok auto-update) |
| `reinstall` | Remove existing grok and install again (keeps auth.*; not grok-cli) |
| `run` | Start grok without auto-update (avoids Termux hang) |
| `check-session` | Confirm grok is logged in (`grok -p hello` first; PRoot reaper when `proot` is on PATH) |
| `backup` | Check session, push `~/.grok/auth.*` to `/var/grok-cli` (passwordless `sudo grok-cli backup` after sudoer-adm) |
| `sync-auth` | Copy `/var/grok-cli/auth.*` into `~/.grok` with no sudo |
| `sync-auth-from-remote` | Copy a remote host's `/var/grok-cli/auth.*` into `~/.grok` |
| `sync-auth-to-remote` | Copy this login's `~/.grok/auth.*` onto a remote login's `~/.grok` |
| `add-crontab` | Add backup and sync-auth jobs to this login's crontab |
| `print-sudoers` | Emit project-sudoers-file (draft) for admin install |
| `print-sudoers-install-script` | Write admin script for sudo install/uninstall/replace |
| `remove-project-sudoers [path]` | Delete project-sudoers-file draft only |
| `generate-sudoer-request [path]` | Independently write a JSON grant (backup verb) |
| `submit-sudoer-request [file]` | Queue a JSON sudoers-grant request via sudoer-cli |
| Env note | `GROK_HOME`, `GROK_CLI_ROOT` |

Examples in help **MUST** include:

```text
grok-cli install
grok-cli setup
grok-cli update-grok
grok-cli reinstall
grok-cli run
grok-cli run -p hello
grok-cli check-session
grok-cli generate-sudoer-request
grok-cli submit-sudoer-request
grok-cli backup
grok-cli sync-auth
grok-cli sync-auth-from-remote user@192.0.2.10
grok-cli sync-auth-to-remote user@192.0.2.10
grok-cli add-crontab
```

### 2.4 Pillar D — Specialized project about items

`about` **MUST** include domain diagnostics (in addition to Type 0):

| Field / line | Content |
|--------------|---------|
| Grok peer | path of `grok` or `not_found` (`setup` places it) |
| Grok home | effective grok auth directory |
| Session | `valid` / `invalid` / `missing` |
| Deposit directory | effective `GROK_CLI_ROOT` (default `/var/grok-cli`) |
| Sudo deposit status | best-effort probe; honest if not fully probeable |
| sudoer-cli | Detected path or `not_found` |
| sudoer-adm | Detected login or `absent` |
| sudoer inbound | Detected inbound dir or `not_found`; plus writable flag |
| Host sudoers fragment | `host_sudoers_present` / `host_sudoers_path` |

**About is not** a remote version-check and **must not** advertise online install channels.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / APP_NAME** | `grok-cli` |
| **Domain prefix** | `gc_` |
| **Ship unit** | `src/grok-cli` |
| **VERSION** | ship unit SSOT (`1.0.0`) |
| **Primary user install** | `~/.local/bin/grok-cli` |
| **Auth operations SSOT** | `requirement-grok-auth-backup` |
| **Crontab operations SSOT** | `requirement-grok-crontab` |
| **Privilege / sudoers SSOT** | `requirement-three-layer-privilege-model` (workflow) · `requirement-sudoer-json-file` (JSON grant body) |
| **Public inbound (sibling)** | `/var/sudoer-cli/sudoer-request` |
| **Worked queued basename** | `sudoer-20260822-grok-cli-<id -un>-add-1.json` |
| **Bootstrap** | Specialized from sibling **folder-backup**; chain cli-template → folder-backup → grok-cli |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Domain surface is explicit (four pillars) and not mixed with full ops law.  
- **Principle 5 – Output SSOT**: Help/about domain rows via product output system.  
- **Principle 9 – Three Types of Commands**: Domain labels user verbs that invoke a narrow elevated backup sub-step under peer REQs.

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

**This requirement:** `backup` / sudoers verbs stay **unused** on this class. The numbered start list is **1** `grok-auth`, **2** `run`, **6** `self-management`, **7** `language`, and **9** Exit, and it prints the host not-available line (`requirement-shell-cli-default-interaction` **2.27.0**). Auth **11** `backup` and auth **13** `sync-auth` stay off this class. Logged out lists auth **12** and appends the logged-out not-available line. Logged in omits auth **12** and appends the logged-in not-available line. `sync-auth-to-remote` is not a numbered row. `setup`, `update-grok`, `reinstall`, `run`, and `check-session` stay this-login work.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent a second auth-ops SSOT in domain.  
- **Intentional:** Pillars A–D only; ops in grok-auth-backup.  
- **Anti-fragile:** Clear ownership boundaries reduce drift.  
- **Over-protect:** Keep sole Active domain file; supersede before replace.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Duplicate full session/deposit/chmod/sync law here once `requirement-grok-auth-backup` is Active.  
2. Reintroduce folder tar.gz `restore` as a domain verb.  
3. Add online install of **grok-cli** or remote upload as silent domain behavior without new requirements. `setup` installing **peer `grok`** is owned by `requirement-grok-setup` — **MUST NOT** set grok-cli `SCRIPT_URL`.  
4. Put domain law into bootstrap origin folder-backup or cli-template.  
5. Create a second Active `requirement-domain-*` without superseding this one.  
6. Let Type 0 `mkdir` `/var/sudoer-cli/sudoer-request`.

7. Strip the **Under command line for normal user only** section, or enable admin privilege / a dedicated system user on Termux / Git Bash / Windows cmd.  

**Violating this rule is a critical domain regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `help` lists setup, update-grok, reinstall, run, check-session, backup, sync-auth, sync-auth-from-remote, add-crontab and sudoer verbs |
| AC-2 | `about --json` reports grok_cli_root, deposit_dir, session |
| AC-3 | Dispatcher routes those verbs; `restore` is unknown |
| AC-4 | JSON grant sample in this file names backup only |
| AC-5 | Sole Active domain file |
| AC-6 | `check-session` / menu session probe: `proot` on PATH uses reaper; else simple `grok -p hello` |

---

## 6. Related artifacts (versioned surface only)

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry SSOT |
| `docs/requirements/requirement-grok-auth-backup.md` | Ops SSOT |
| `docs/requirements/requirement-grok-crontab.md` | `add-crontab` ops SSOT |
| `docs/requirements/requirement-grok-setup.md` | `setup` / `update-grok` / `reinstall` / `run` / peer grok channel + artifact |
| `docs/requirements/requirement-three-layer-privilege-model.md` | Privilege workflow |
| `docs/requirements/requirement-sudoer-json-file.md` | JSON grant body |
| `docs/requirements/requirement-shell-cli-interface.md` | Dual mention of verbs |
| `docs/requirements/requirement-shell-termux-coding.md` | PRoot exit hang writing + probe dispatch |
| `./src/grok-cli` | Implementation |

---

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-22 | Active (1.0.0) | Specialized from folder-backup domain; grok auth surface |
| 2026-08-25 | Active (1.1.0) | `setup` peer grok installer (xAI curl) |
| 2026-09-02 | Active (1.2.0) | `add-crontab` per-login backup/sync-auth timers |
| 2026-09-02 | Active (1.3.0) | `sync-auth-from-remote` four SPEC forms |
| 2026-09-02 | Active (1.4.0) | `setup` inlines studied xAI procedure (no `install.sh`) |
| 2026-09-04 | Active (1.4.1) | `setup` skip only if grok already runs on this host (dual mention `requirement-grok-setup` 2.2.0) |
| 2026-09-04 | Active (1.4.2) | `setup` Android ET_EXEC wrapper (dual mention `requirement-grok-setup` 2.3.0) |
| 2026-09-04 | Active (1.4.3) | `setup` Termux `pkg install -y proot` when needed (dual mention `requirement-grok-setup` 2.4.0) |
| 2026-09-04 | Active (1.4.4) | `setup` HTTP status on curl fail; keep Android `.failed` artifact (dual mention `requirement-grok-setup` 2.5.0) |
| 2026-09-04 | Active (1.4.5) | `setup` Android proot resolv bind (dual mention `requirement-grok-setup` 2.6.0) |
| 2026-09-05 | Active (1.4.6) | `check-session` live `grok -p hello` (dual mention `requirement-grok-auth-backup` 1.2.0) |
| 2026-09-07 | Active (1.5.0) | `run` starts peer grok without auto-update (dual mention `requirement-grok-setup` 2.8.0) |
| 2026-09-07 | Active (1.6.0) | `check-session` / menu probe: `proot` on PATH → reaper; else simple `grok -p hello` (dual mention Termux writing + auth-backup) |
| 2026-09-10 | Active (1.7.0) | `update-grok` (dual mention `requirement-grok-setup` 2.12.0; **INC-20260910-002**) |
| 2026-09-12 | Active (1.8.0) | TTY `setup` keep / reinstall / Exit (dual mention `requirement-grok-setup` 2.14.0) |
| 2026-09-14 | Active (1.9.0) | `reinstall` (dual mention `requirement-grok-setup` 2.15.0) |
| 2026-09-22 | Active (1.10.0) | `sync-auth-to-remote` (dual mention `requirement-grok-auth-backup` 1.10.0); TTY main menu lists it only when logged in (`requirement-shell-cli-default-interaction` 2.18.0) |
| 2026-10-10 | Active (1.10.1) | Grok-auth **13** only when logged in; **16** `reinstall`; this-login-only start list follows default-interaction **2.24.0** |
| 2026-10-10 | Active (1.10.2) | `sync-auth-to-remote` is not a numbered row; this-login-only omits auth **11** and **13** and lists **12** only when logged out (default-interaction **2.25.0**) |
| 2026-10-10 | Active (1.10.3) | Logged-out not-available line follows default-interaction **2.26.0** |
| 2026-10-12 | Active (1.10.4) | This-login-only start list follows default-interaction **2.27.0** (**1** grok-auth, **2** run, **6** self-management, **7** language, **9** Exit) |

---


## Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-04**, **TP-CLI-06** | `tests/test_cli.sh` | have |
| **TP-VCLI-01**–**09**, **11**–**25** | `tests/test_grok_setup.sh` | have |
| **TP-VCLI-33**–**35** | `tests/test_grok_setup.sh` | have |
| **TP-VCLI-37**–**39** | `tests/test_grok_setup.sh` | have |
| **TP-VCLI-40**–**42** | `tests/test_grok_setup.sh` | have |
| **TP-CLI-31** | `tests/test_cli.sh` | have |
| **TP-GROK-CLI-01**, **01b**, **02**, **11**, **14**, **15**, **15b**, **19**–**25** | `tests/test_domain_grok_cli.sh` | have |
| **TP-GROK-CLI-26**–**29** | `tests/test_domain_grok_cli.sh` | have |
| **TP-GROK-CLI-30**–**38** | `tests/test_domain_grok_cli.sh` | have |
| **TP-GROK-CLI-50** | `tests/test_domain_grok_cli.sh` | have — `sync-auth-to-remote` |
| **TP-GROK-CLI-46** | `tests/test_domain_grok_cli.sh` | have — `run` `--no-auto-update` |
| **TP-GROK-CLI-47**, **TP-GROK-CLI-48** | `tests/test_domain_grok_cli.sh` | have — probe dispatch `command -v proot` → reaper; else simple `-p` |

**Matrix:** `reviews/requirement-test-matrix.md`  
**Map:** `reviews/test-plan.md`.

**Last Updated**: 2026-10-12 (1.10.4 — this-login-only start list follows default-interaction **2.27.0**. 1.10.3 followed **2.26.0**.)  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
