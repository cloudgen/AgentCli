**file**: docs/requirements/requirement-shell-modular-function-design.md  
**Status**: Active (Version 1.1.2)  
**Area**: shell  
**Key**: `requirement-shell-modular-function-design`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the **project Single Source of Truth** for **modular function organization** of the grok-cli POSIX shell CLI.

**Core idea:** Modularity is achieved through **clear function boundaries, consistent prefixes, and full CIAO documentation** — **not** by splitting the installable CLI into multiple shipped files.

Ship unit remains a **single executable** at `src/grok-cli`.

---

### 1.1 Human-facing

One file `src/grok-cli` with prefixes: `out_`, `inst_`, `app_`, `gc_` for grok auth.

| You | Another role | Not this |
|-----|--------------|----------|
| Read functions by prefix | Domain ops live under `gc_*` | Splitting into many shipped files |

**Includes:** prefix table. **Excludes:** grant JSON schema.

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Find backup code | Look for `gc_backup` | Open `src/grok-cli` |


## 2. Core Rules / Requirements (Mandatory)

### 2.1 Overall architecture

| Rule | Meaning |
|------|---------|
| **Single executable** | One primary script file for the installable CLI |
| **Logical modules** | Functions grouped by **strict prefixes** |
| **Documented units** | Public helpers carry defensive headers and safe defaults |
| **Requirements extract policy** | Durable rules live in `requirement-*.md`; code comments encode intent and Protection Zones |

### 2.2 Official function prefix table

**All functions MUST use a defined prefix.** Bare names (`main`, `install`, `help`, `backup`) as function names are forbidden.

| Prefix | Category | Purpose | Example functions |
|--------|----------|---------|-------------------|
| `out_` | Output system | All user-facing and machine-readable output | `out_text`, `out_info`, `out_json`, `out_die` |
| `inst_` | Installation lifecycle | Local install/uninstall detect and place/remove | `inst_local_install`, `inst_local_uninstall`, `inst_is_installed` |
| `util_` | General utilities | Path resolve, storage, safe helpers, named volatile internal-timer | `util_resolve_storage`, `util_get_install_bin_path`, `util_int_timer_start` |
| `app_` | Cross-cutting CLI surface | Entry, dispatch, about/help/version/where-is-me | `app_main`, `app_about`, `app_help`, `app_version`, `app_where_is_me` |
| `path_` | Shell PATH & environment | PATH + profile ensure after user install | `path_add_shell`, `path_add_bashrc`, `path_add_zshenv`, `path_add_zprofile`, `path_ensure_profile`, `path_rc_test` |
| `prompt_` | Interactive prompts | TTY-safe confirmations | `prompt_yes_no` |
| `gc_` | Domain business logic | Grok auth backup/sync + sudoers fragment | `gc_backup`, `gc_check_session`, `gc_sync_auth`, `gc_print_sudoers` |

**Notes:**

- Domain prefix **`gc_`** is short for **grok-cli** (path-safe, stable).  
- **Do not** put domain ops under `app_*`.  
- **Do not** put generic about/help/main under `gc_*`.  
- Online-only prefixes from parent (`ver_check` remote network path, download install family) **MUST NOT** be reintroduced unless product mode changes.

### 2.3 Function documentation standards

Every non-trivial function **MUST** include a defensive header with:

- One-line purpose  
- **GENERAL PURPOSE** paragraph  
- CIAO principles applied (as relevant)  
- Protection / DO NOT SIMPLIFY note for critical helpers  
- Last reviewed date when modified  

Product-source `ALIGNMENT` / “see” comments **MUST** cite only live `docs/requirements/requirement-*.md` paths registered in `index.md`.

### 2.4 Protection Zones

Critical sections (output SSOT, install place/remove, storage resolve, domain archive naming, sudoers fragment generation, elevated deposit invocation) **MUST** remain CIAO-Lite Protection Zones and **MUST NOT** be simplified away without explicit user redesign order.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Ship unit** | `src/grok-cli` |
| **Domain prefix** | `fb_` |
| **Bootstrap inheritance** | Prefix discipline from cli-template; domain prefix `fb_` added |
| **Multi-file authoring** | Optional later only if pack still yields one installable artifact and this requirement is updated |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Prefixes encode ownership.  
- **Principle 6 – Single Point of Entry**: `app_main` stays the dispatcher.  
- **Principle 7 – Reusable function protection**: DO NOT MODIFY markers on critical helpers.  
- **Principle 20 – Protect against AI & human modification**: Visible zones.

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

**This requirement:** prefixes only. Do not add an admin-privilege-only module on this class.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** No bare unscoped helpers.  
- **Intentional:** Domain vs Type 0 separation.  
- **Anti-fragile:** Single file still modular.  
- **Over-protect:** Keep Protection Zones.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Introduce bare function names without an approved prefix.  
2. Merge domain backup logic into `app_*` or `inst_*` without requirement update.  
3. Split into multi-file runtime without a pack story and requirement change.  
4. Strip Protection Zones “for readability.”  
5. Cite templates/skills as product-source behavioral authority.

6. Strip the **Under command line for normal user only** section, or enable admin privilege / a dedicated system user on Termux / Git Bash / Windows cmd.  

**Violating this rule is a critical modular design regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | All functions use the prefix table |
| AC-2 | Domain ops live under `fb_*` |
| AC-3 | Single ship unit at `src/grok-cli` |
| AC-4 | Product comments cite live requirements only |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-shell-cli-interface` | Command → handler map |
| `requirement-shell-output-requirements` | Owns `out_*` |
| `requirement-domain-grok-cli` | Owns `gc_*` behavior |
| `docs/requirements/index.md` | Registry |

---

## Terminologies

### Shell startup files

**Definition:** Shell startup files are the notes a shell reads at start. `path_add_zprofile` is the helper that writes the zsh login note.

**Human daily-life explanation:** Prefixes are labels on the drawers. The zsh door-note helper sits in the `path_` drawer next to the always-on helper.

**Daily-life example:** You find `path_add_zprofile` by the `path_` label. The note it writes is still one login’s `.zprofile`.

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-03 | Active | Modular prefixes for folder-backup |
| 2026-09-17 | Active (1.1.1) | `path_add_zshenv` listed (zsh PATH owner `requirement-shell-zshenv`) |
| 2026-10-12 | Active (1.1.2) | `path_add_zprofile` listed (owner `requirement-shell-startup-files`) |

---

**Last Updated**: 2026-10-12  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
