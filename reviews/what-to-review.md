# What to review — grok-cli

**Living checklist** (review plan). Product: **grok-cli** — alternative online installer for xAI grok.  
**Class:** software-development · domain SSOT present · **dual-mode** install (channel `curl\|sh` primary; checkout `install` secondary).  
**Always load first:** `reviews/lessons.md`

**Last plan update:** 2026-10-10 (logged-out auth **11** `sync-auth`, **12** `sync-auth-from-remote`; logged-in **11** `backup`)  
**Ship unit VERSION:** 1.8.43  
**Suite baseline:** `reviews/test-plan.md`

---

## Pre-flight

| # | Check | Notes |
|---|--------|--------|
| P1 | Read `docs/requirements/index.md` | Class + architecture + shell + domain grok-cli + grok-auth-backup + three-layer |
| P2 | Confirm ship unit `src/grok-cli` | `APP_NAME` / `VERSION` hard-assign (**1.8.43**) |
| P3 | Load `reviews/lessons.md` and re-check every open L-* | Mandatory (esp. **L-MAP-01** · **L-EXPOSE-01** · **L-SUDOERS-01/02** · **L-SUDOERS-06** · **L-OUTPUT-01** · **L-AUTH-01** · **L-PROMPT-CAPTURE-01** · **L-MENU-06**) |
| P4 | Run `./tests/run.sh` | Record PASS/FAIL/SKIP; **must include TP-GROK-CLI-22e** and **TP-24*/25*** when generate/submit is in scope |
| P5 | Confirm install **channel** | `SCRIPT_URL` default github raw `src/grok-cli`; companion `.sha256`; dual-mode matrix |
| P6 | Privilege law | three-layer **2.0.0** · sudoer-json **2.0.0** (`backup` only) · operator-readable-error |
| P7 | Host elev posture | Global vs local binary; trust tier; `/etc/sudoers.d/grok-cli-<user>` |
| P8 | **JSON re-encode / inbound fidelity** | Pretty convert + submit inbound still has `backup` |
| P9 | **Host fragment → submit update** | TP-GROK-CLI-23* |
| P10 | **Independent generate dest** | TP-GROK-CLI-24* |
| P11 | **Operator-readable errors** | TP-GROK-CLI-25* |
| P12 | **Session gate + sync-auth** | TP-GROK-CLI-03..10 · 12 |
| P13 | **sync-auth-from-remote** / **sync-auth-to-remote** | TP-GROK-CLI-30..34 · **41** (preferred SPEC) · **42/43** (skip pull when logged in) · **50** (push to remote `~/.grok`; still runs when logged in) · **TP-CLI-13/19/20** (menu lists the push only when logged in) |
| P14 | **Empty argv split** | TTY menu; off-TTY Type O; TP-CLI-07/13 · TP-ONL-01 |
| P15 | **Online lifecycle** | version-check / self-update (start line names local and remote VERSION) / self-uninstall; TP-ONL-02..05 · TP-CLI-10 |
| P16 | **Human-readable law** | Every Active REQ has §1.1 Human-facing; grant samples use `id -un`; no frozen login (TP-CLI-18) |
| P17 | **Command line for normal user only** | Related shell REQs print that exact heading; Termux/Git Bash/Windows cmd stay this-login; main menu hides backup/sync-auth/sudoers, lists **2** `run` (row **1** stays grok-auth), and prints the not-available line (TP-CLI-19); logged-out session hides **backup** and **sync-auth-to-remote** and lists auth **11** `sync-auth` and **12** `sync-auth-from-remote` on a multi-user host (TP-CLI-13 · TP-CLI-17 · TP-CLI-19); logged-in session hides sync-auth / sync-auth-from-remote, lists **11** `backup` and **sync-auth-to-remote**, and **appends** the logged-in not-available line (TP-CLI-20) |
| P18 | **`run` without auto-update** | Dispatcher `gc_run_grok`; inject `--no-auto-update`; `--json` fail-closed Next `run`; missing grok Next `setup`; dual mention grok-setup + CLI-interface + domain; TP-GROK-CLI-46 · TP-CLI-04 |
| P18b | **TTY `setup` reinstall** | Already-installed TTY list keep / reinstall / Exit; `--json` skip; `--force` skips list; no `$()` of `prompt_ask`; no wipe of `auth.*`; TP-VCLI-37..39 |
| P18c | **`reinstall` verb + menu** | Routed Type 0; grok-auth **16**; missing grok still fetches; `auth.*` kept; JSON `reinstall`/`reinstalled`; `setup` is grok-auth **15**; TP-VCLI-40..42 · TP-CLI-31 |
| P18c | **Invalid menu-choice retry** | Unused number / unknown name on the start list **and** the sudoers list: `[ERROR]`, reprint **this** layer, re-prompt; MUST NOT `out_die` / unknown argv; TP-CLI-30. Unused front integer is **4**. On Termux the unused integer that replaced language is **6**. Sudoers unused **6** stays |
| P18d | **Menu language** | Front **5** on every host. Block **50–69**. Assigned **51** English through **63** Ελληνικά. **50** and **64–69** are not printed. Front **6** warns and does not write. Save `${HOME}/.local/grok-cli/language` mode 0600. `GROK_CLI_LANG` does not write. Human help and about follow the code. JSON and argv `version` stay English. `language` is not an argv verb. TP-CLI-32 · TP-CLI-13 · TP-CLI-19 · TP-CLI-20 |
| P19 | **Dest maps vs disk** | `AGENTS.md` + `docs/README.md` live inventory = this dest class/REQ/incident **file** count; no `/home/<login>/`; no phantom `incident-*.md`; **L-MAP-01** · **L-EXPOSE-01** · **INC-20260910-001** |

---

## Product law surfaces

| Surface | Path | Review focus |
|---------|------|--------------|
| Class | `requirement-class-software-dev.md` | posix-sh, dual-mode, coding-style pointer |
| Bootstrap chain | `requirement-bootstrap-chain.md` | cli-template → folder-backup → grok-cli + selfmanaged channel |
| Project folder | `requirement-project-folder.md` | `src/grok-cli`, bins, `/var/grok-cli`, Termux `PREFIX` / `~/.grok` |
| **Privilege / sudoers** | `requirement-three-layer-privilege-model.md` | Type 0/1; `sudo grok-cli backup` only |
| **JSON sudoer file** | `requirement-sudoer-json-file.md` | `grok-cli backup` only; no OS tools |
| **Auth ops** | `requirement-grok-auth-backup.md` | Session gate; deposit; sync-auth; sync-auth-from-remote; sync-auth-to-remote |
| **Operator-readable error** | `requirement-operator-readable-error.md` | Blocking `[ERROR]` next step |
| CLI interface | `requirement-shell-cli-interface.md` | setup / run / check-session / backup / sync-auth |
| Empty argv | `requirement-shell-cli-zero-arguments.md` | TTY = numbered menu; off-TTY = Type O ensure |
| Default interaction | `requirement-shell-cli-default-interaction.md` | case 3 menu; off-TTY `menu` = help |
| Local self-management | `requirement-shell-local-self-management.md` | checkout install/uninstall; 0755 |
| **Shell-rc PATH / profile** | `requirement-shell-path-and-shell-support.md` | sibling unify; heal on already-installed; routed `rc-test`; APP_NAME-only uninstall |
| Online install | `requirement-shell-online-install.md` | `SCRIPT_URL`; dual-mode matrix |
| Self-management | `requirement-shell-self-management.md` | version-check / self-update / self-uninstall |
| Automatic checksum | `requirement-shell-automatic-checksum.md` | companion mismatch abort |
| Output SSOT | `requirement-shell-output-requirements.md` | `out_*` |
| Modular design | `requirement-shell-modular-function-design.md` | `gc_*` |
| Coding style | `requirement-shell-script-coding.md` | `set -u`, fail-closed; Termux **points** |
| Termux writing | `requirement-shell-termux-coding.md` | `PREFIX`, `pkg`, `noexec`, FHS-not-assumed |
| Domain | `requirement-domain-grok-cli.md` | Four pillars; `setup` / `run` |
| Superseded | folder-archive + domain-folder-backup | Must stay superseded; do not revive restore |

**Intentionally absent:** Type O-P payload installer; dest fence-test (no dest machine).

---

## High-risk paths (ship unit)

| Path / symbol | Risk | Lesson / TP |
|--------------|------|-------------|
| Empty argv | TTY stolen by install-ensure; off-TTY hang on numbered menu | L-TYPE-N-01 · L-ARGV-01 · TP-CLI-07/13 · TP-ONL-01 |
| `inst_channel_ensure` / `path_add_bashrc` | Termux `curl\|sh` already-installed skip never writes `USER_BIN` into `.bashrc`; missing `.bashrc` is a silent PATH miss | L-PATH-01 · **INC-20260909-001** |
| `gc_run_grok` | `--json` execs grok / hangs; missing grok no Next setup; this-login-only menu omits `run` | L-WRAP-02 · TP-GROK-CLI-46 · TP-CLI-19/20 |
| `app_default_print_menu` / `gc_grok_p_once_run` | Silent ~14s after INFO header; DEBUG looks like a different path; Ctrl-Z stops the reaper; empty stdout never idles | L-MENU-04 · **INC-20260907-004** |
| `inst_self_update` / `gc_setup_heal_android_wrapper` | grok-cli-only update leaves 2026-09-04 `bin/grok` (no `--kill-on-exit` / start-services bind / reaper) | L-WRAP-04 · **INC-20260907-004** |
| `gc_backup` | Deposit without session or without grant | L-AUTH-01 · L-DEPOSIT-01 · TP-GROK-CLI-06/12 |
| `gc_sync_auth` | Uses sudo or leaves dest world-readable | L-SYNC-01 · TP-GROK-CLI-09 |
| `gc_print_sudoers` | Restore verb or OS-tool Cmnds | L-SUDOERS-01 · TP-GROK-CLI-01/22 |
| `gc_submit_sudoer_request` | Inbound drop backup; jargon-only error | L-SUDOERS-06 · L-OUTPUT-01 · TP-25* |
| Tokens in logs | Printing JWT/refresh | L-AUTH-01 · (static: no token print) |
