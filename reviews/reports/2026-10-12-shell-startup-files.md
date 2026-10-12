# Review: shell startup files — grok-cli 1.8.47

**Date:** 2026-10-12  
**Scope:** Shell startup files across Linux bash, Alpine ash, zsh, Fish, Termux, Git Bash, and Windows cmd / PowerShell. Missing `.profile`, `.zprofile`, and `.zshenv`. PATH on `.zprofile`.  
**Law:** `requirement-shell-startup-files` **1.0.0**. Peers point: cli-interface **2.15.8**, path **1.2.1**, zshenv **1.0.1**, alpine **1.0.1**, modular **1.1.2**, class **1.3.7**.  
**Proof:** **TP-LC-43** · **TP-LC-44** · **TP-LC-45** · **TP-LC-46**  
**Checklist:** `CL-SHELL-STARTUP-FILES` (filled local run)  
**Suite:** `tests/test_local_lifecycle.sh` PASS=129 FAIL=0 SKIP=0. Full `tests/run.sh` was not re-run.

## Verdict

**Pass.** The ship unit creates a missing `.zprofile` when the shell is zsh, appends an existing file without replacing it, and does not invent zsh notes for a bash-only login. `rc-test --file zprofile` is named on the CLI interface requirement and on the family owner.

## What was checked

| Check | Result |
|-------|--------|
| Shared line `export PATH="<USER_BIN>:$PATH"` on `.zshenv` and `.zprofile` | Pass |
| Missing `.profile` still generates a source-bashrc note; PATH on that new file only for ash | Pass (unchanged; **TP-LC-41** / **TP-LC-42**) |
| `ZSHENV` alone does not create `.zprofile` | Pass (create gate is `SHELL` basename `zsh` or an explicit `ZPROFILE`) |
| `.zshrc` is not a PATH file | Pass (`path_add_zshrc` still returns without writing) |
| Real home snapshot includes `.zprofile` | Pass |
| Section **Under command line for normal user only** on the new requirement | Pass |
| Published requirements omit harness path maps | Pass (spot check) |

## Strengths

- One family owner. `.zshenv` and ash `.profile` stay on their files and point here.
- Login zsh writes the same `USER_BIN` line after `path_helper` can reorder PATH.
- The test verb refuses a change to this login’s real notes.

## Follow-ups

None that block this release. Lifecycle cleanup may print safe-rm refusals for throw-away homes. Those lines are not assertion failures. The full suite was not re-run after this change.

## Remediation order

None.
