**file**: docs/requirements/requirement-class-software-dev.md  
**Status**: Active (Version 1.3.7 – leftover startup-file family points at requirement-shell-startup-files)  
**Area**: class  
**Key**: `requirement-class-software-dev`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (CIAO = Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file says two things:

1. This workspace is a **software-development** project: a real program people can install, named `grok-cli`.  
2. It holds leftover software-stack facts that no other requirement file already owns.

**SSOT** means **single source of truth**: the one official copy of a fact. This file is the class rulebook and the SSOT for those leftover stack facts.

It covers:

- The main programming language
- The toolchain policy (how versions are handled)
- Package / build / test tools
- The runtime / OS (operating system) family

It does **not** repeat details that already live in other requirement files (backup, install steps, sudoers rules, CLI commands, or online-install details).

**CLI** means **command-line interface** (the program you run in a terminal).  
**sudoers** means the system rules that say who may run which commands with `sudo`.

### 1.1 Human-facing

This file tells anyone (a person or an AI agent): this folder’s **project nature** is software-development — grok-cli is a finished program people can install — and here are the leftover stack facts that no other requirement owns.

**Dest** (short for destination reviewer) means a dedicated account that reviews and approves inbound request files. This product has none.

| You | Another role | Not this |
|-----|--------------|----------|
| You (developer / maintainer) get the project nature and leftover stack (language, tools, “no dest approver”) | Agents and reviewers get clear ownership of stack facts until a more specific requirement takes them over | A dest approval machine, a second class file, or a place to invent new approver accounts |

**Includes:** project-nature membership; leftover stack facts; an honest statement that there is no dest approver and no dest fence (no listed reasons for that reviewer to refuse a file).  
**Excludes:** making up an approver account; inventing dest fence rows; copying full tables that already exist in other requirement files.

| You open | What you get |
|----------|----------------|
| This file | Project nature + leftover stack |
| A peer key in the leftover-ownership table below | The topic that peer file already owns |

| Step | What it means | What you do |
|------|---------------|-------------|
| Classify | Agents treat this folder as software-development, not a blank starter kit. | Open `docs/requirements/requirement-class-software-dev.md` |
| Own-or-point | Stack facts live here unless another requirement owns them. | Follow the leftover-ownership table in this file |

---

## 2. Core Rules (Must Follow)

### 2.0 Project class membership

**Harness knowledge** means the reusable agent workshop (shared skills and wording), not this product’s own rules.

1. **MUST** treat this workspace as **software-development** (a finished program people can install), not a blank starter kit (genesis-template) and not a server-maintenance project.  
2. **MUST** use the filename **`requirement-class-software-dev.md`** as the only Active class-law file for this class.  
3. **MUST NOT** register an Active `requirement-class-server-maintenance.md` at the same time as this class.  
4. **MUST** keep general harness knowledge portable (usable on the next project). Product-specific knowledge lives in this file and other `requirement-*.md` files.  
5. **MUST** follow the software-development SSOT and gate rules when they apply: identity, what counts as the program file people install, and precommit checks when git is used.  
5a. When git is used on a host that has more than one SSH (secure shell) identity (a **multi-vault host**), **MUST** treat the identity used to push to the forge (GitHub / GitLab) as the **product repository-user** SSOT (Config `REPO_USER` or the project repo owner), not the machine’s default SSH key. Agents **MUST** run precommit / SSH-profile checks before git pushes. Host vault folder names are **not** product law.  
6. **MUST NOT** invent empty product docs just to look specialized. Collect real values or say “not defined yet”.

### 2.1 Leftover facts (SSOT hygiene)

7. **MUST** treat this file as the **default home** for any software-stack fact that is not owned by another Active requirement.  
8. **MUST NOT** copy full tables that already live in a more specific Active requirement. Add a one-line pointer to that requirement’s key instead.  
9. When a new, more specific requirement takes over a topic that used to live only here, **MUST** update this file in the **same change**: remove or shrink the old entry and point to the new owner.  
10. **MUST NOT** leave contradictory stack facts between this file and other requirements.

### 2.2 Programming language(s)

11. **MUST** declare at least one **primary programming language** for the program file people install.  
12. **SHOULD** list secondary languages only if they are truly part of the product rules.  
13. **MUST** state whether the product is mainly: **interpreted** (run as source, no compile step), **compiled**, **polyglot** (more than one language as product law), or uses multiple languages via packages.  
14. **MUST NOT** treat a marketing product name as if it were the language name.

### 2.3 Compilers, interpreters, and toolchains

A **toolchain** is the compiler or interpreter used to build or run the product.  
**Cross-compilation** means building on one computer for a different kind of computer.

15. **MUST** declare the type of toolchain used to build or run the product.  
16. **MUST** state the version policy as one of: unconstrained · minimum version · version range · pinned version.  
17. **SHOULD** say whether cross-compilation is in scope.  
18. **MUST NOT** claim “supports all compilers” in CI (continuous integration) or docs unless that is actually tested, or the policy is explicitly unconstrained.

### 2.4 Project / package / build tools

A **lockfile** is a frozen list of dependency versions.

19. **MUST** declare the main project or package tool used for dependencies and builds.  
20. **MUST** say how dependencies are resolved when the ecosystem supports lockfiles.  
21. **SHOULD** name the test runner and linter/formatter types when they are part of the project rules.  
22. **MUST NOT** store secret tokens or private registry passwords in this file.

### 2.5 Runtime and platform (leftover facts)

23. **MUST** declare the intended main runtime / OS family when no other architecture requirement fully owns this.  
24. **SHOULD** declare minimum CPU / architecture support only when it is a real product rule.  
25. **MUST** separate developer-machine toolchain requirements from end-user runtime requirements when they differ.

### 2.6 Do not hard-code / two-layer policy (class file)

**Hard-code** means freezing one live brand, hostname, or person into the reusable core rules.  
**Two-layer policy** means: portable rules in the core; live product names and stack choices in Implementation Notes.

26. **MUST NOT** hard-code a single product / app brand, one organization’s production hostname, or a personal owner identity as universal core law.  
27. **MUST** put the live product name, repo slug, and concrete stack choices in the **Implementation Notes** section once the status is Active.  
28. **MUST NOT** store secrets, PATs (personal access tokens), or test credentials in this file.

### 2.7 Implementation Notes (this project)

**POSIX sh** means the portable Unix shell `/bin/sh` (a small subset that works on dash and on bash when it runs as `sh`).

| Field | Value (grok-cli) |
|-------|---------------------|
| **Project display name** | `grok-cli` |
| **Project class** | software-development |
| **Class requirement filename** | `requirement-class-software-dev.md` |
| **Primary language(s)** | `posix-sh` (`/bin/sh`) |
| **Language role** | primary only — one shell script file under `src/` |
| **Execution model** | **interpreted** — no compile step |
| **Toolchain / interpreter** | POSIX `/bin/sh` (dash / bash-as-sh compatible subset); no compiler |
| **Toolchain version policy** | **unconstrained** among POSIX sh implementations that pass product tests |
| **Cross-compile in scope?** | no |
| **Primary project/package tool** | **none** — no language module system; the source file is the program people install |
| **Lockfile policy** | not used |
| **Test runner** | POSIX shell test suite under `tests/` when present (for example `tests/run.sh`) |
| **Linter/formatter** | none as a project rule (shellcheck is optional for maintainers) |
| **Primary runtime / OS family** | POSIX Linux (and compatible UNIX where `/bin/sh`, `tar`, `gzip` / `tar -z`, and `mktemp` exist); **Termux / Android userspace** writing owned by `requirement-shell-termux-coding` |
| **Architectures supported** | any architecture with POSIX sh and the external tools the script uses |
| **Git surface** | used when the product is published |
| **Ship unit / install** | yes — the **ship unit** (the program file people install) is `src/grok-cli` → `${USER_BIN}/grok-cli`; **dual-mode** (two install methods: primary `curl \| sh`; secondary checkout + `install`) |
| **Product version SSOT** | `VERSION=` hard-assigned in `src/grok-cli` (do not pin an old number here) |
| **Bootstrap origin** | sibling product **folder-backup**; chain: cli-template → folder-backup → grok-cli (domain retarget: keep the shell framework, change the product’s job) |

**Leftover-ownership table** (who owns each topic):

| Topic | Owner | Notes |
|-------|-------|--------|
| Project class membership | **this file** | Fixed |
| Primary language + toolchain policy | **this file** | posix-sh, unconstrained |
| Package/build tool + lockfile | **this file** | none / not used |
| Bootstrap lineage / keep-extend | `requirement-bootstrap-chain` | A=cli-template → B + domain extend |
| Project layout / install path | `requirement-project-folder` | `src/` + bin targets + Termux `PREFIX` / `~/.grok` classes |
| Commands you run as yourself / flags / dispatch | `requirement-shell-cli-interface` | **Type 0** = you run the command as yourself. Do not duplicate |
| Empty argv: terminal numbered menu; off-terminal install-or-recheck | `requirement-shell-cli-zero-arguments` | **Empty argv** = no command token after flag parse (overlay `--debug` still counts). Dual-mode. **Type O** = with no command, off a terminal, install or re-check install (not help) |
| Local self-managed lifecycle | `requirement-shell-local-self-management` | checkout `install` / `uninstall` / `where-is-me` |
| Online channel + checksum + remote lifecycle | `requirement-shell-online-install` · `requirement-shell-automatic-checksum` · `requirement-shell-self-management` | Specialized from selfmanaged. A **checksum** is a fingerprint used to verify the download |
| Output SSOT (`out_*`) | `requirement-shell-output-requirements` | Do not duplicate |
| Operator-readable error wording | `requirement-operator-readable-error` | Human-style `[ERROR]` messages; do not duplicate |
| Scratch/cache storage resolve | `requirement-shell-cli-storage` | Do not duplicate |
| Idempotency / re-run safety | `requirement-shell-idempotency` | **Idempotent** = safe to run again with the same result |
| Interactive vs non-interactive | `requirement-shell-interactive-vs-noninteractive` | Do not duplicate |
| Modular prefixes / single-file layout | `requirement-shell-modular-function-design` | Do not duplicate |
| POSIX sh coding style | `requirement-shell-script-coding` | `set -u`, `out_*`, stop rather than guess when extra privilege is needed; do not duplicate |
| Termux / Android host writing | `requirement-shell-termux-coding` | `PREFIX`, Termux `pkg`, `noexec` tmp, FHS-not-assumed; do not duplicate |
| PATH / profile / shell-rc sibling unify | `requirement-shell-path-and-shell-support` | One shared `USER_BIN` PATH line on bash/Fish; create `.profile` if missing; do not duplicate |
| Zsh PATH (`.zshenv`, not `.zshrc`) | `requirement-shell-zshenv` | Independent zsh always-on rc; do not duplicate |
| Ash / Alpine PATH (`.profile` when `$0` is ash) | `requirement-shell-alpine` | Login ash reads `.profile`; do not duplicate |
| Shell startup files (missing `.profile` / `.zprofile` / `.zshenv`; zsh login PATH on `.zprofile`) | `requirement-shell-startup-files` | Family matrix; do not duplicate `.zshenv` or ash `.profile` |
| Login-review hook | **this file** (leftover) | **considered — no login-hook**. This product has no dest review scrap. **MUST NOT** plant one or strip another product’s hook |
| Privilege layers + sudoers files (print / install / stop if not allowed) | `requirement-three-layer-privilege-model` | Daily work as yourself + a narrow `sudo grok-cli backup` grant (**Type 0** + **Type 1** deposit: Type 1 = the command changes the computer). §2.3 sudoers workflow is the SSOT |
| JSON sudoer file (grant body) | `requirement-sudoer-json-file` | **JSON** = a structured text format. `{{PRJ_NAME}}` only; no `cp` / `mkdir` / OS-tool commands |
| Grok auth backup operations | `requirement-grok-auth-backup` | Session check / deposit / sync-auth (not domain) |
| Domain surface (verbs, help, about) | `requirement-domain-grok-cli` | Four pillars only (the product’s own commands, features, help, and about); ops pointer |
| Actor / role / subject / approver | **this file** (leftover) | **considered — no dest approver and no approval subject**. This product has no dest approval machine. **MUST NOT** invent an approver. |
| Dest fence conditions | **this file** (leftover) | **considered — no dest fence conditions**. No dest Fence table. **MUST NOT** invent a dest fence. |
| Online install / remote self-management / companion checksum | peer REQs (Active 2026-09-02) | **REQ** = requirement file. User-ordered specialization from selfmanaged |

---

## 3. Why This Requirement Exists (CIAO Alignment)

- **CIAO Principle 2 – Intentional**: The project nature and stack choices are written down, not guessed from folder names.  
- **CIAO Principle 5 – SSOT**: Leftover stack facts have one home until more specific requirements take ownership.  
- **CIAO Principle 1 – Caution**: Toolchain policies are declared; agents do not invent compilers.  
- **CIAO Principle 21 – Dual Policies** (two-layer policy): Portable core rules; filled Implementation Notes.  
- **CIAO Principle 4 (O) + Principle 20**: Protection against two conflicting stack copies, and against mixing up project natures.

---

## 4. Design Principles (CIAO / CIAO-Lite)

- **Caution**: Assume toolchain and package tools are missing until they are declared and verified.  
- **Intentional**: The leftover collection is deliberate — not a dump of every possible tool.  
- **Anti-fragile**: The unconstrained POSIX sh policy survives multiple environments as long as tests pass.  
- **Over-protect**: The protection rule prevents duplicate stack copies and confusion between a blank starter kit and a software project.

---

## 5. Protection Rule (Do Not Break)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Delete this file while the workspace is still software-development with other Active product requirements.  
2. Rename the file away from `requirement-class-software-dev.md` without an explicit class-model change.  
3. Hard-code secrets, personal owner identities, or production hostnames into core rules as universal law.  
4. Copy full peer requirement bodies into this leftover section.  
5. Leave the Implementation Notes as empty stubs when the status claims Active.  
6. Remove Active rules for online install / self-update / self-uninstall / checksum without updating this leftover section and the dual-mode matrix.  
7. Treat this file as server-maintenance allowlist law, or create an Active server-maintenance class file in parallel.  
8. Invent a second primary-language SSOT that contradicts peer modular / CLI requirements.

**Breaking any of these is a critical regression** (a serious step backward).

---

## 6. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-1 | An Active `requirement-class-software-dev.md` exists and matches the software-development class |
| AC-2 | Primary language, toolchain policy, and package tool are declared and complete in Implementation Notes |
| AC-3 | The leftover-ownership table is honest: no hidden duplicate SSOTs with peer requirements |
| AC-4 | Core rules do not contain hardcoded secrets or hostnames |
| AC-5 | No conflict with `requirement-class-server-maintenance` (only one Active class file) |
| AC-6 | The program people install (single-file POSIX shell, dual-mode install) is consistent with other shell requirements |
| AC-7 | The online install package is Active; leftover entries point to peer requirements (no duplicated channel tables here) |

---

## 7. Related Requirements (Peer Keys Only)

| Key | Relationship |
|-----|--------------|
| `requirement-bootstrap-chain` | Lineage: A=cli-template → B=grok-cli (domain retarget) |
| `requirement-project-folder` | Layout and install locations |
| `requirement-shell-cli-interface` | Command surface, flags, dispatch |
| `requirement-shell-cli-zero-arguments` | Terminal menu; off-terminal install-or-recheck |
| `requirement-shell-local-self-management` | Checkout install lifecycle |
| `requirement-shell-online-install` | Channel `SCRIPT_URL` + dual-mode |
| `requirement-shell-self-management` | `version-check` / `self-update` / `self-uninstall` |
| `requirement-shell-automatic-checksum` | Companion `${SCRIPT_URL}.sha256` |
| `requirement-shell-output-requirements` | `out_*` SSOT |
| `requirement-operator-readable-error` | Operator error wording |
| `requirement-shell-cli-storage` | Scratch/cache resolve |
| `requirement-shell-idempotency` | Re-run safety |
| `requirement-shell-interactive-vs-noninteractive` | Mode policy |
| `requirement-shell-modular-function-design` | Prefixes / single-file modularity |
| `requirement-shell-script-coding` | POSIX sh coding style |
| `requirement-shell-termux-coding` | Termux / Android host writing |
| `requirement-shell-path-and-shell-support` | PATH / profile / sibling unify (bash / Fish) |
| `requirement-shell-zshenv` | Zsh PATH on `.zshenv` (not `.zshrc`) |
| `requirement-shell-alpine` | Ash PATH on `.profile` |
| `requirement-three-layer-privilege-model` | Privilege + working with sudoers fragment files |
| `requirement-sudoer-json-file` | JSON sudoer file body (`{{PRJ_NAME}}` only) |
| `requirement-grok-auth-backup` | Grok auth backup operations SSOT |
| `requirement-domain-grok-cli` | Domain four pillars |
| `docs/requirements/index.md` | Registry SSOT |

---

## Terminologies

### Shell startup files

**Definition:** Shell startup files are the family of notes a shell reads at login or when a session starts. This class file does not own that family.

**Human daily-life explanation:** The class rulebook points at the kitchen-note owner. It does not copy every note.

**Daily-life example:** A missing zsh door note is hung by `requirement-shell-startup-files`, not by this leftover list.

## 8. Status History

| Date | Status | Note |
|------|--------|------|
| 2026-08-03 | Active | Specialized class law for folder-backup (left genesis; then named selfmanaged as origin) |
| 2026-08-13 | Active | Origin retarget: A=cli-template → B=folder-backup |
| 2026-08-15 | Active | Leftover: JSON sudoer file → `requirement-sudoer-json-file` |
| 2026-08-19 | Active (1.1.0) | Leftover: **considered — no dest approver and no approval subject**; **considered — no dest fence conditions**. §1.1 Human-facing. Version SSOT note 1.9.0. |
| 2026-08-22 | Active (1.2.0) | Identity retarget to grok-cli; ops leftover → grok-auth-backup; domain → grok-cli. Version SSOT 1.0.0. |
| 2026-09-02 | Active (1.3.0) | Dual-mode install; online package leftover points to peer REQs |
| 2026-09-02 | Active (1.3.1) | Same law in plainer English. Dest vocabulary kept. Numbered MUST rules kept. |
| 2026-09-02 | Active (1.3.2) | Everyday-English pass: abbreviations expanded on first use; leftover jargon explained; no new rules. |
| 2026-09-04 | Active (1.3.3) | Leftover: Termux / Android host writing → `requirement-shell-termux-coding` |
| 2026-09-09 | Active (1.3.4) | Leftover: PATH / profile / sibling unify → `requirement-shell-path-and-shell-support`; login-hook considered none |
| 2026-09-17 | Active (1.3.5) | Leftover: zsh PATH → `requirement-shell-zshenv` (`.zshenv`, not `.zshrc`) |
| 2026-09-22 | Active (1.3.6) | Leftover: ash / Alpine PATH → `requirement-shell-alpine` (`.profile` when `$0` is ash) |
| 2026-10-12 | Active (1.3.7) | Leftover: shell startup files → `requirement-shell-startup-files` |

---

**Last Updated**: 2026-10-12  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
