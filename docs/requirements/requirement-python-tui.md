**file**: docs/requirements/requirement-python-tui.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-tui`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The text menu is the grok-cli main menu drawn with the HelloTui frame. HelloTui features stay: path line, local clock, rounded input box, status line, display columns, thirteen languages, system-log, welcome verb, pip self-management, and Exit.

### 1.1 Human-facing

**In one sentence:** On a terminal, `agent-cli` shows the grok-cli numbered menu inside the HelloTui frame, and choosing a row runs that verb.

| You | Another role | Not this |
|-----|--------------|----------|
| Pick **1** grok-auth or **9** Exit | HelloTui still draws the box, the clock, and system-log | A `Choice:` line, or a media join |

## 2. Core Rules

1. Class `Tui` owns the session. Class `MenuPainter` owns the frame glyphs. The product **MUST NOT** import `py_tui`.
2. Multi-user front rows **MUST** be **1** grok-auth, **5** sudoers, **6** self-management, **7** language, **9** Exit. There is no Back row on the front board. Front **3**, **4**, and **8** are not rows.
3. This-login-only (Termux, Git Bash, Windows cmd) **MUST** show **2** run and **MUST** hide **5** sudoers.
4. A set `PREFIX` counts as Termux unless `AGENT_CLI_HOST_OVERRIDE` is `multiuser`, `gitbash`, or `windows-cmd`. `TERMUX_VERSION` counts as Termux even before that override.
5. grok-auth rows **MUST** keep fixed numbers: **11** backup when signed in on a multi-user host, **12** sync-auth-from-remote when not signed in, **13** sync-auth when not signed in on a multi-user host, **14** add-crontab, **15** setup, **16** reinstall, **0** Back. `sync-auth-to-remote` is not a row. Timeout stays signed-in.
6. self-management rows **MUST** be **64** version-check, **65** self-update, **66** self-uninstall, **68** where-is-me, **0** Back.
7. sudoers rows **MUST** be **51** through **55** plus **0** Back.
8. system-log stays available. Typing `system-log` opens **31** view-log, **32** clear-log, **33** log-folder, and **0** Back. It is not a front number.
9. Choosing a domain row **MUST** run that verb and show the result on the result page. `setup` on an existing grok **MUST** offer keep, reinstall, and Exit. Remote sync **MUST** ask for the SPEC in the input box.
10. The first row **MUST** show the current directory and a local clock `HH:MM:SS` when the row has room.
11. The bottom **MUST** be a three-row rounded input box, then up to three unavailable-feature lines, then the status line `AgentCli <version>`.
12. Unavailable lines **MUST** be: host `backup, sync-auth and sudoers features are not available in {label}.`; logged-out `backup features are not available for logged-out environment.`; logged-in `sync-auth and sync-auth-from-remote features are not available for logged-in environment.`
13. A number that is not on the list **MUST** show an error and let the operator choose again.
14. Esc on a nested board or a result page returns to the front board. It is not row 9 Exit.
15. A window that is too small **MUST** show `The text screen is too small for the menu and the input box.` and **MUST NOT** fall back to a `Choice:` line.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | Front row 1 is grok-auth |
| AC-2 | Language is row 7 with codes 80–92 |
| AC-3 | system-log and hello still exist |
| AC-4 | The input box and the path line still draw |
