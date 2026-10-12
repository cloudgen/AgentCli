# Live command list — grok-cli

This file is the kept list of commands `app_main` actually runs: name, function, who may run it, date on that function’s comment, and the same one-line explanation `help` prints. It is **not** help text as the routing inventory.

**Ship unit:** `src/grok-cli`  
**Dispatcher:** `app_main`  
**Scan date:** 2026-09-22 (handlers); menu paragraph refreshed 2026-10-12  
**Mode:** incremental (menu paragraph only; handlers not re-walked)  
**Copied:** prior live · **Re-checked:** `sync-auth-to-remote` (`gc_sync_auth_to_remote`) · `app_default` menu tokens  
**Inventory:** dispatcher `case "${COMMAND}"` — not `app_help` for routing; help one-liners copied into **human-readable**

## Live commands

| verb | handler | privilege | last modified date | human-readable |
|------|---------|-----------|--------------------|----------------|
| about | `app_about` | you (Type 0) | 2026-08-03 | `about: Show diagnostics (incl. sudoers trust tier)` |
| add-crontab | `gc_add_crontab` | you (Type 0) | 2026-09-02 | `add-crontab: Add backup and sync-auth jobs to this login's crontab` |
| backup | `gc_backup` | change-the-computer (Type 1) | missing | `backup: Push ~/.grok/auth.* to /var/grok-cli` |
| check-session | `gc_check_session` | you (Type 0) | 2026-09-05 | `check-session: Confirm grok is logged in (runs grok -p hello first)` |
| generate-sudoer-request | `gc_generate_sudoer_request` | you (Type 0) | 2026-08-17 | `generate-sudoer-request: Write a JSON grant you can read` |
| help | `app_help` | you (Type 0) | missing | `help: Show this help` |
| main | `app_default` | you (Type 0) | 2026-09-03 | `main: Same as menu` |
| menu | `app_default` | you (Type 0) | 2026-09-03 | `menu: Show the numbered list of live commands` |
| install | `inst_local_install` | you (Type 0) | 2026-08-09 | `install: Install grok-cli (root→global, user→~/.local/bin)` |
| version-check | `ver_check` | you (Type 0) | 2026-09-02 | `version-check: Compare local vs remote VERSION on SCRIPT_URL` |
| self-update | `inst_self_update` | you (Type 0) | 2026-09-07 | `self-update: Re-download grok-cli from SCRIPT_URL (start line names local and remote VERSION)` |
| self-uninstall | `inst_self_uninstall` | you (Type 0) | 2026-09-02 | `self-uninstall: Same remove as uninstall (channel name)` |
| setup | `gc_setup` | you (Type 0) | 2026-09-12 | `setup: Install grok from x.ai (channel + artifact; TTY offers reinstall if grok already runs)` |
| update-grok | `gc_update_grok` | you (Type 0) | 2026-09-10 | `update-grok: Update grok from x.ai (not grok-cli; avoids grok auto-update)` |
| reinstall | `gc_reinstall` | you (Type 0) | 2026-09-14 | `reinstall: Remove existing grok and install again` |
| run | `gc_run_grok` | you (Type 0) | 2026-09-07 | `run: Start grok without auto-update` |
| print-sudoers | `gc_print_sudoers` | you (Type 0) | 2026-08-14 | `print-sudoers: Emit sudoers draft` |
| print-sudoers-install-script | `gc_print_sudoers_install_script` | you (Type 0) | 2026-08-09 | `print-sudoers-install-script: Write admin install script` |
| remove-project-sudoers | `gc_remove_project_sudoers` | you (Type 0) | 2026-08-09 | `remove-project-sudoers: Remove sudoers draft only` |
| submit-sudoer-request | `gc_submit_sudoer_request` | you (Type 0) | 2026-08-17 | `submit-sudoer-request: Queue the JSON grant inbound` |
| sync-auth | `gc_sync_auth` | you (Type 0) | missing | `sync-auth: Copy /var/grok-cli/auth.* into ~/.grok` |
| sync-auth-from-remote | `gc_sync_auth_from_remote` | you (Type 0) | 2026-09-02 | `sync-auth-from-remote: Copy a remote host's auth.* into ~/.grok` |
| sync-auth-to-remote | `gc_sync_auth_to_remote` | you (Type 0) | 2026-09-22 | `sync-auth-to-remote: Copy ~/.grok/auth.* onto a remote host` |
| uninstall | `inst_local_uninstall` | you (Type 0) | 2026-08-03 | `uninstall: Remove managed binary (confirm or --force); not sudoers` |
| version | `app_version` | you (Type 0) | missing | `version: Show local version` |
| where-is-me | `app_where_is_me` | you (Type 0) | 2026-08-03 | `where-is-me: Show running and install paths` |

A TTY main menu **MUST** print a numbered **top** list of families, then **9** Exit. The top list **MUST NOT** print **Back**. Multi-user: **1** `grok-auth`, **5** `sudoers`, **6** `self-management`, **7** `language`. This-login-only: **1** `grok-auth`, **2** `run`, **6** `self-management`, **7** `language` (no **5**). Front **8** is not a row. **3** and **4** stay reserved. `language` is menu-only, not a dispatcher token. The language board is **80–92** (reserved **70–79** and **93–98** are not printed). Submenus print **0** Back and **9** Exit. Auth submenu **11–16**. **11** `backup` is listed only on a multi-user host when logged in. **12** `sync-auth-from-remote` is listed only when the session is not logged in. **13** `sync-auth` is listed only on a multi-user host when the session is not logged in. `sync-auth-to-remote` is not a row. This-login-only hides **11** and **13**. **14–16** do not slide. **17** is not a row. Self-management printed rows are **64** version-check, **65** self-update, **66** self-uninstall, and **68** where-is-me (**61**, **62**, **63**, and **67** stay unprinted). Sudoers submenu is **51–55**. Header is **`APP_NAME(APP_VERSION)`**; the next line is **logged in** / **timeout** / **logged out**. grok-cli is **case 3**: verb **`menu`** (alias **`main`**). Off-TTY empty argv is Type O ensure (not this list). **Exclude** from every numbered list: `help`, `menu`/`main`, `check-session` (status is under the title), `update-grok`, diagnostics (`version`, `about`), and test-purpose. **`setup`** and **`reinstall`** are on the grok-auth submenu. Self-managed verbs are on the self-management submenu. **`sudoers` is not a live dispatcher token.** **0** / `back` on the top list is an invalid choice. **9** leaves from every layer. Internal `ensure` is not a help verb.

## Not yet wired

| verb | handler | privilege | last modified date | human-readable | status |
|------|---------|-----------|--------------------|----------------|--------|
| restore | — | — | — | — | forbidden — domain law says do not wire it (retired folder-archive). **Not** a planned Gap. |

---

**Last Updated:** 2026-10-12 (front **5** sudoers **51–55**; **6** self-management **64**, **65**, **66**, **68**; **7** language **80–92**; front **8** is not a row; auth **11–16** unchanged)  
**Alignment:** term `cli-routed-verb-table` · **`SK-CLI-ROUTED-VERB-TABLE`** · **`SK-CLI-DEFAULT-INTERACTION`**
