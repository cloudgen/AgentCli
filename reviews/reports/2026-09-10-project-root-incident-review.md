# Report: project-root incident — grok-cli 1.8.28

**Date:** 2026-09-10
**Mode:** review of the project-root (`AGENTS.md`) incident surface vs `docs/incidents/` disk
**Status:** open items
**Method:** disk read (`ls` / `git check-ignore` / `git ls-files`); lessons loaded; suite **not** re-run (out of scope)
**Baseline:** ship unit `src/grok-cli` `VERSION=1.8.28`; cwd `{{PROJECTS_ROOT}}/grok-cli`; no `/dev/shm/grok-cli`

## Council (single session, five lenses)

| Role | Focus | Short summary |
|------|--------|----------------|
| Explore | Facts | `AGENTS.md` lists 5 incident bodies; glob empty. `docs/README.md` says genesis 0 REQs. Registry has 26 Active + 4 superseded. `AGENTS.md` gitignored. |
| Plan | Sequencing | Rebind maps first; thin AGENTS incident row; reconstruct Termux INC files only if owner asks. |
| Implement | What to change | Not this turn. Next: `SK-DEST-SSOT-MAP-REBIND`. |
| Review | Quality | Verdict **Block** on map honesty. Path leak of `AGENTS.md` is already closed. |
| Security | Privilege / disclosure | A literal home path in AGENTS is a host-path leak. Thick INC table is process-history concentration (`avoid-expose-agents`). |

Honest: one writer, not five independent agents.

## Summary

The project-root incident is that **`AGENTS.md` sells a specialized grok-cli workshop with five postmortem files that are not on this dest**, while **`docs/README.md` still sells stripped genesis**. Runtime lessons for INC-20260907-001..004 and INC-20260909-001 survive in CHANGELOG and `reviews/lessons.md`. That is not the same as incident bodies. **Do not treat the five Termux IDs as filed here.**

## Strengths

| Area | Notes |
|------|--------|
| Path firewall | Root `.gitignore` ignores `AGENTS.md`; `docs/**` except `docs/requirements/**`. `git ls-files AGENTS.md` empty. |
| Product law | `docs/requirements/index.md` matches the 30 `requirement-*.md` files (26 Active + 4 superseded). |
| Runtime memory | Lessons L-MENU-03/04, L-WRAP-01/03/04, L-PATH-01 still name the Termux INC IDs with prevention. |
| H1 note | `docs/README.md` Last H1 says incidents excluded — that exclusion is correct payload policy. |

## Issues

### Issue 1 -- Severity: bug
- File: `AGENTS.md:54`
- Description: Live inventory claims **5** bodies under `docs/incidents/` (INC-20260907-001..004, INC-20260909-001). `ls docs/incidents/incident-*.md` is empty. Agents will load missing paths or invent files.
- Suggestion: Count the glob; write “**0** bodies on this dest” (or the real count after this report) and a pointer to `docs/incidents/`. Do not keep an ID table in AGENTS (`avoid-expose-agents`).
- Lesson: L-MAP-01 · **INC-20260910-001**
- Test: none (harness map). Re-check: `ls docs/incidents/incident-*.md`
- Status: open

### Issue 2 -- Severity: bug
- File: `docs/README.md:75`
- Description: Live inventory snapshot says **genesis-template**, **0** product REQs, **ship unit none**. Disk is software-development grok-cli with `src/grok-cli` and 26 Active requirements. H1 leftover. `SK-DEST-SSOT-MAP-REBIND` Protection Rule 2.
- Suggestion: Rebind from dest disk. Keep template-name/blacklist only if this dest were still stripped genesis — it is not.
- Lesson: L-MAP-01 · **INC-20260910-001**
- Test: none. Re-check: class + `ls docs/requirements/requirement-*.md` vs both maps.
- Status: open

### Issue 3 -- Severity: bug
- File: `AGENTS.md:47`
- Description: PROJECT_SSOT is hardcoded as a literal `/home/<login>/prjs/grok-cli`. This dest is a different workspace root. Violates **`PO-NON-EXPOSE-LOCAL-MACHINE`**. Wrong host for ram-drive-first resolution.
- Suggestion: Map host as hard-disk `{{PROJECTS_ROOT}}/grok-cli` family or “this workspace root”; never `/home/<login>/…`.
- Lesson: L-NEX-01 (related) · L-MAP-01
- Test: TP-CLI-18 covers product samples, not AGENTS. Map scrub is review-only.
- Status: open

### Issue 4 -- Severity: suggestion
- File: `AGENTS.md:49`
- Description: Stale harness/product counts (19 Active REQs / 80 skills / 387 terms / 18 policies / 109 human-intro) vs disk (26 Active+4 superseded / 65 / 354 / 19 / 134). `docs/README.md` harness counts match disk; class does not.
- Suggestion: Same rebind pass; counts from dest `ls` only.
- Lesson: L-MAP-01
- Status: open

### Issue 5 -- Severity: suggestion
- File: `AGENTS.md:54`
- Description: Thick incident ID + one-line lesson re-export in the boot contract. Even gitignored, this is `avoid-expose-agents` concentration (INC-20260714-001 class). Cited older IDs (INC-20260902-001 and earlier) also have no body here.
- Suggestion: Pointer only. Keep narrative in `docs/incidents/` and product lessons in `reviews/lessons.md`.
- Lesson: L-EXPOSE-01
- Status: open

### Issue 6 -- Severity: nit
- File: `docs/incidents/README.md:5`
- Description: Folder README still says genesis-template **Zero** `incident-*.md` (dated 2026-07-13). True before this review; must be updated when a body is filed.
- Suggestion: Inventory = disk after INC-20260910-001.
- Status: closed (README updated in the same change)

## Non-findings (explicitly OK)

| Check | Result |
|-------|--------|
| `AGENTS.md` tracked on product git | Not tracked (`git check-ignore` → `.gitignore:95`) |
| `docs/incidents/` tracked | Ignored (Pattern A). Correct. Do not force-add. |
| Five Termux runtime defects as current ship bugs | Out of scope for this map review. Lessons remain **open watch**; code/CHANGELOG claim they were fixed in 1.8.14–1.8.27. |
| Versioned `docs/requirements/**` dumping `docs/incidents/` path catalogs | Not found as a new leak this pass (REQ files cite INC IDs in law history; that is product-local, not a harness tree dump). |

## Priority remediation order

1. **`SK-DEST-SSOT-MAP-REBIND`** on this dest (`AGENTS.md` + `docs/README.md`).
2. Thin AGENTS Incidents row (Issue 1 + 5).
3. Owner decision: reconstruct INC-20260907-* / INC-20260909-001 from CHANGELOG/lessons, or leave them cited-only.
4. Do not commit `AGENTS.md` or `docs/incidents/**`.

## Issue counts by severity

- bugs: 3
- suggestions: 2
- nits: 1 (README; addressed with the incident file)

## Related

| Artifact | Role |
|----------|------|
| `docs/incidents/incident-20260910-001-project-root-agents-inventory-vs-disk.md` | Postmortem |
| `reviews/lessons.md` L-MAP-01 · L-EXPOSE-01 | Re-check |
| `SK-DEST-SSOT-MAP-REBIND` | Fix path |
| `avoid-expose-agents` | AGENTS thickness |

**Verdict:** **Block** (map honesty). Product ship unit not re-tested this turn.

**Written by:** Review (council lenses, single session)
**Review status:** Findings open
