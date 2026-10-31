# Tests — AgentCli

## Python ship unit

```sh
./tests/run_python.sh
# or
PYTHONPATH=src python3 -m unittest discover -s tests
```

Exit **0** when the unittest modules pass. Ship unit: `src/AgentCli` (package **1.2.1**, console `agent-cli`).

| File | Focus |
|------|--------|
| `test_docs.py` | README badge, headings, absolute screenshot URLs |
| `test_about.py` | About page, host check, cache tiers, star box |
| `test_tui.py` | Path label, wide columns, unavailable band, resize |
| `test_language.py` | Front row 7, codes 80–92, save, this-login-only |
| `test_hello.py` | Welcome line, unknown `join` / `restore`, front row 1 |
| `test_entry.py` | `main(argv, basedir, logdir)`, `opens_text_screen`, `Output` lines |
| `test_debug.py` | Debug catalog on, off, and the text-screen file |
| `test_actor.py` | Actor, Role, Subject. No Approver column |
| `test_idempotency.py` | Second backup overwrite. Second `self-install` |
| `test_domain.py` | Session, backup, sync, setup, crontab, sudoer handoff, `run` |
| `test_shell_startup.py` | `.zprofile` / `.zshenv`, rc-test |
| `test_storage.py` | Cache tiers, one resolver, silent preferred skip |

## POSIX reference

```sh
./tests/run.sh
# or
sh tests/run.sh
```

Exit **0** when all assertions pass; **1** on failure; **2** if ship unit missing.

## Layout

| File | Focus | TP families |
|------|--------|-------------|
| `run.sh` | Entrypoint | — |
| `helpers.sh` | Asserts + isolated HOME | — |
| `test_cli.sh` | CLI surface, empty argv (TTY menu / off-TTY Type O; overlay `--debug` / `--quiet` follow 0-argv), this-login-only menu hide, logged-out lists **12** `sync-auth-from-remote` and **13** `sync-auth` and hides **11**; logged-in lists **11** `backup` and hides **12** and **13**; `sync-auth-to-remote` is not a numbered row, Termux menu does not freeze on hanging grok, reprint does not re-probe, probe always bounded, `--debug` menu elapsed of each paint step, invalid pick retries this menu layer, front **7** menu language (**80–92**) | **TP-CLI-*** |
| `test_local_lifecycle.sh` | install / uninstall / where-is-me | **TP-LC-*** |
| `test_domain_grok_cli.sh` | live `grok -p hello` session gate (incl. elevated `SUDO_USER` home; SIGTERM-ignoring hang bound; `proot` on PATH → reaper else simple `-p`) + backup/sync-auth + sync-auth-from-remote (incl. TTY menu row 3 SPEC prompt + preferred-remote default) + sync-auth-to-remote + add-crontab + sudoers print + JSON grant + submit inbound | **TP-GROK-CLI-*** |
| `test_grok_setup.sh` | `setup` / `update-grok` / `reinstall` fetch xAI channel + artifact (fake curl; no public net; no `install.sh`); TTY keep / reinstall / Exit; Android wrapper `--kill-on-exit` / `proot-exit-reaper` / `-p` SIGKILL; heal stale wrapper on skip | **TP-VCLI-*** |
| `test_online_install.sh` | Channel `curl|sh` ensure, checksum mismatch, version-check, version-aware self-update start line, self-uninstall (fake curl) | **TP-ONL-*** |

## Isolation

- Temp `HOME` + `USER_BIN` for install tests  
- **No** public network  
- **No** write to `/etc/sudoers.d` (suite never installs sudoers)  
- Auth fixtures are synthetic (no live tokens); session tests inject a fake `GROK_BIN` (never `grok -p hello` against xAI)  
- Backup **success** uses writable `GROK_CLI_ROOT` override (not `/var/grok-cli`)

## Ship unit under test

Python: `src/AgentCli`. POSIX reference: `src/grok-cli`.

## Maps

Product TP map: `reviews/test-plan.md`  
RTM: `reviews/requirement-test-matrix.md`
