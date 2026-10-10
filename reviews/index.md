# Review reports index — grok-cli

| Date | Report | Scope | Verdict | Suite |
|------|--------|-------|---------|-------|
| 2026-10-02 | `reports/2026-10-02-language-menu-5.md` | Front **5** language; thirteen codes **51–63**; REQ language 1.1.0 · default-interaction 2.22.0 · interface 2.15.3 · TP-CLI-32 | **Pass** (language rows) | PASS=998 FAIL=56 SKIP=0 |
| 2026-09-13 | `reports/2026-09-13-menu-invalid-choice-coverage.md` | Invalid pick retries every main-menu layer; REQ 2.15.0 · molds · TP-CLI-30 · CL | **Pass (findings closed)** | PASS=848 FAIL=0 SKIP=0 |
| 2026-09-13 | `reports/2026-09-13-checklist-cli-default-interaction-invalid-choice.md` | Filled `CL-CLI-DEFAULT-INTERACTION` for invalid-choice retry at every menu layer | **Pass** | 1.8.32 |
| 2026-09-06 | `reports/2026-09-06-human-readability-coverage.md` | README + REQ human-readable law; coverage vs checklists/tests; TP-CLI-18 | **Pass (findings closed)** | PASS=479 FAIL=0 SKIP=0 |
| 2026-09-05 | `reports/2026-09-05-session-probe-requirement-review.md` | Live `grok -p hello` session gate; Termux coverage; dual mention | **Pass** | PASS=478 FAIL=0 SKIP=0 |
| 2026-09-03 | `reports/2026-09-03-checklist-cli-default-interaction-menu-style.md` | Filled `CL-CLI-DEFAULT-INTERACTION` for default CLI main menu style (SGR 3+37 / `out_menu_choice`) | **Pass** | 1.8.1 |
| 2026-09-03 | `reports/2026-09-03-implementation-ciao-menu-style.md` | Filled `CL-IMPLEMENTATION-CIAO` | **Pass** | 1.8.1 |
| 2026-09-03 | `reports/2026-09-03-menu-header-review.md` | 1.8.0 menu header/session line + setup smoke; human/REQ/checklist/test coverage | **Pass (findings closed)** | PASS=399 FAIL=0 SKIP=0 |
| 2026-09-03 | `reports/2026-09-03-checklist-cli-default-interaction.md` | Filled `CL-CLI-DEFAULT-INTERACTION` | **Pass** | 1.8.0 |
| 2026-09-03 | `reports/2026-09-03-checklist-operator-readable-error-setup-smoke.md` | Filled `CL-OPERATOR-READABLE-ERROR` (setup smoke) | **Pass** | TP-VCLI-16 |
| 2026-09-03 | `reports/2026-09-03-checklist-cli-dual-mention.md` | Filled `CL-CLI-DUAL-MENTION` | **Pass** | 1.8.0 |
| 2026-09-03 | `reports/2026-09-03-code-review-menu-header.md` | Filled `CL-CODE-REVIEW` | **Pass** | 1.8.0 |
| 2026-09-02 | `reports/2026-09-02-requirement-review-online-menu.md` | curl install + TTY menu; test-plan/lessons/molds/checklist | **Approve with follow-ups closed** | PASS=360 FAIL=0 SKIP=0 |
| 2026-09-02 | `reports/2026-09-02-checklist-online-install-script.md` | Filled `CL-ONLINE-INSTALL-SCRIPT` | **Pass** | 1.7.0 |
| 2026-09-02 | `reports/2026-09-02-requirement-review-grok-setup-inline.md` | `setup` inlines studied xAI channel + artifact; no `install.sh` | **Approve with follow-ups closed** | PASS=350 FAIL=0 SKIP=0 |
| 2026-08-23 | `reports/2026-08-23-empty-argv-menu.md` | Empty argv → TTY numbered menu; off-TTY help; Type N | **Pass** | PASS=242 FAIL=0 SKIP=0 |
| 2026-08-23 | `reports/2026-08-23-empty-argv-menu-requirement-review.md` | Zero-arguments 1.3.0 + default-interaction 1.7.0 + interface 2.2.0 | **Approve with follow-ups closed** | PASS=242 FAIL=0 SKIP=0 |
| 2026-10-10 | `cli-routed-verb-table.md` | Kept live-command list; menu paragraph matches logged-out auth **11** `sync-auth` | **21 live** · 1 not-yet-wired (`restore` forbidden) | living |
| 2026-08-22 | `reports/2026-08-22-product-review-grok-cli.md` | Full product grok-cli 1.0.0 | **Pass** | PASS=207 FAIL=0 SKIP=0 |
| 2026-08-22 | `reports/2026-08-22-requirement-review-grok-cli.md` | Requirement review + authorized retarget | **Approve with follow-ups closed** | PASS=207 FAIL=0 SKIP=0 |
| 2026-08-17 | `reports/2026-08-17-review-revision-test-plans.md` | Review/test-plan revision vs 1.9.0 generate + operator-readable errors | **PASS** (plans aligned; suite green) | PASS=242 FAIL=0 SKIP=2 |
| 2026-08-17 | 1.9.0 generate-sudoer-request | Local verified compact JSON; submit compact handoff; TP-24 | living | 1.9.0 |
| 2026-08-17 | INC-20260817-002 | Submit fail-closed error not human-readable; incomplete JSON not a standing class | living | 1.8.2 |
| 2026-08-17 | `reports/2026-08-17-requirement-coverage.md` | C-full-product sufficient-check + AC↔TP | **Sufficient with Gaps** (FB-COV-01..06) | PASS=209 FAIL=0 SKIP=2 |
| 2026-08-17 | host-probe submit **update** | Default `update` when `/etc/sudoers.d/{{APP_NAME}}-<user>` exists; TP-23/23b; AC-22 | living | 1.8.2 |
| 2026-08-17 | `reports/2026-08-17-json-reencode-fidelity.md` | JSON re-encode / inbound **JR-1..8**; suite 22e/22f | **PASS** (FB-JR-01 host inbound residual) | PASS=198 FAIL=0 SKIP=2 |
| 2026-08-17 | `what-to-review` **JR-1..8** | Review plan gate: JSON re-encode / inbound fidelity (pretty convert + submit + S15) | living | PASS=198 FAIL=0 SKIP=2 |
| 2026-08-17 | INC-20260817-001 knowledge lock | Re-encode fidelity: REQ 1.1.0 / three-layer 1.7.0 / S15 / TP-22e/22f | living | PASS=198 FAIL=0 SKIP=2 |
| 2026-08-15 | `reports/2026-08-15-sudoer-json-file.md` | JSON sudoer file = `folder-backup` only; emit 1.8.0 | **PASS** (FB-SUDOER-01 residual runtime) | PASS=189 FAIL=0 SKIP=2 |
| 2026-08-15 | `reports/2026-08-15-coverage-public-inbound.md` | Coverage P0–P2 + public inbound detect | **PASS** (findings closed) | PASS=175 FAIL=0 SKIP=2 |
| 2026-08-13 | `reports/2026-08-13-bootstrap-specialize-cli-template.md` | Origin retarget A=cli-template → B; VERSION 1.6.1 alignment | **PASS** | PASS=157 FAIL=0 SKIP=2 |
| 2026-08-12 | **1.6.0 retention** (daily 5 + total 30; TP-17/18; retention REQs) | `fb_apply_retention` + deposit Type 0 when writable + sudoers rm | **PASS** | PASS=166 FAIL=0 SKIP=0 |
| 2026-08-12 | **1.5.0 restore dest whitelist** (W-ETC-USER; mold/REQ/TP-16; INC-20260812-001 Closed) | `fb_refuse_restore_dest`; checklist `docs/checklists/2026-08-12-checklist-restore-dest-whitelist-w-etc-user.md` | **PASS** | PASS=156 FAIL=0 SKIP=0 |
| 2026-08-11 | **Housekeeping** (version surfaces + lessons residual) | README/SECURITY → 1.4.4; L-SUDOERS-05 renumber; L-PUSH-VAULT-01 | living | PASS=138 FAIL=0 SKIP=2 |
| 2026-08-09 | **Review plans updated** (`what-to-review.md`, `test-plan.md`, `requirement-test-matrix.md`, `lessons.md`) | Plans for 1.4.4 multi-user project-sudoers-file | living | PASS=138 FAIL=0 SKIP=2 |
| 2026-08-09 | `reports/2026-08-09-security-review-folder-backup.md` | Full security review (design + host) | **Pass (design) / Revise (host)** | F1–F8; host still test_local |
| 2026-08-09 | `reports/2026-08-09-sudoers-security-folder-backup.md` | Sudoers security (trust tiers) | **Pass (test only)** | supersedes 2026-08-03 production claim for local-only |
| 2026-08-03 | `reports/2026-08-03-product-review-initial.md` | Full product (law + ship unit + suite) | **Revise** (docs gaps; core suite green) | PASS=82 FAIL=0 SKIP=2 |
| 2026-08-03 | `reports/2026-08-03-sudoers-security-folder-backup.md` | Sudoers security (pre-emit) | **Pass (historical; superseded for production)** | local-only; see 2026-08-09 |
