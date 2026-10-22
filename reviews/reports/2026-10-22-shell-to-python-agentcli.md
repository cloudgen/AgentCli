# Review: shell grok-cli → Python AgentCli

**Date:** 2026-10-22  
**Verdict:** Pass with residuals  
**Suite:** `./tests/run_python.sh` — 60 tests, OK  
**POSIX reference:** `src/grok-cli` **1.8.47**, suite `tests/run.sh` (not re-run)

## Requirement review

The request is a full conversion. HelloTui supplies the text-menu frame. grok-cli supplies the domain. The product name is AgentCli. Direction is those two sources into this tree only. HelloTui was not edited. The sibling trees were not edited.

| Keep | Convert |
|------|---------|
| Domain verbs, deposit of `auth.*`, privilege Type 0 plus narrow Type 1 `backup` | Shell language law becomes the Active `requirement-python-*` files |
| Peer binary `grok`, auth under `~/.grok` | Console `agent-cli`, package `AgentCli`, deposit `/var/agent-cli` |
| Front numbers 1, 5, 6, 7, 9 and this-login-only row 2 | Numbered shell menu becomes the text menu |
| HelloTui path line, local clock, rounded input, status line, thirteen languages, system-log, pip lifecycle, typed `hello`, about, Exit | Those features stay. They are not replaced by grok-cli row numbers |
| `src/grok-cli` as the behavior reference | Install story is pip. Empty argv off a terminal prints help and returns 0 |

One Active domain file remains: `requirement-domain-grok-cli`. No second domain file was added.

## Feature matrix

| Feature | Python ship unit |
|---------|------------------|
| Empty argv on a terminal | Text menu |
| Empty argv off a terminal | Help, return 0 |
| Front rows | 1 grok-auth, 5 sudoers (51–55), 6 self-management (64, 65, 66, 68), 7 language (80–92), 9 Exit |
| This-login-only | Shows 2 run and hides 5 |
| Auth numbers | 11 backup when signed in; 12 and 13 when logged out; 14–16 stay; `sync-auth-to-remote` is typed |
| Menu row | Runs the verb. Setup can keep, reinstall, or Exit. Remote rows ask for a SPEC |
| Session | valid, timeout, invalid, missing. Timeout stays signed in. Termux and `proot` on PATH read local cookies |
| Sync | From-remote skips when signed in. To-remote still runs. Four SPEC forms |
| Crontab | Both lines, once, after a backup grant |
| `run` | Inserts `--no-auto-update` |
| Sudoer JSON | `args` is `["backup"]` only |
| Submit | Calls sudoer-cli into the inbound queue. Does not write `/etc`. Missing tool fails closed |
| Remove draft | `--force` deletes the user draft. `/etc` is refused |
| Admin script | Draft plus a script with install, uninstall, replace, and status |
| Android wrapper | `proot-exit-reaper`, `--kill-on-exit`, `start-services.sh` bind. No vendor shell installer |

## Residuals

These stay on the POSIX reference. They are not silent stubs in the Python verbs above.

1. Menu `--debug` elapsed lines (TP-CLI-25) are not painted on the text screen.
2. The setup channel matrix for a Windows `.exe`, resolv.conf bind, and heal-on-skip stays in `tests/test_grok_setup.sh`.
3. A non-PRoot live probe is a 14-second subprocess timeout. The shell setsid / `timeout -k` reaper stays in `src/grok-cli`. Termux and `proot` do not start that probe.
4. `tests/run.sh` was not re-run.
5. `docs/skills/skill-shell-to-python-cli.md` is named from `docs/README.md` and is not on disk. This review used the bootstrap-specialize checklist.

## Proof

`PYTHONPATH=src python3 -m unittest discover -s tests` — Ran 60 tests, OK (2026-10-22).
