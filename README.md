# AgentCli - Install and run xAI grok, and back up its auth files

[![Version](https://img.shields.io/badge/Version-1.2.0-blue?style=flat-square)](https://github.com/cloudgen/AgentCli)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE.md)
[![CIAO](https://img.shields.io/badge/CIAO-Defensive%20Programming-orange?style=flat-square)](https://github.com/cloudgen/ciao)
[![Stars](https://img.shields.io/github/stars/cloudgen/AgentCli?style=flat-square)](https://github.com/cloudgen/AgentCli)
[![Python](https://img.shields.io/badge/Python-2.7%2B%20(3.x%20recommended)-blue?style=flat-square)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/AgentCli?style=flat-square)](https://pypi.org/project/AgentCli/)

AgentCli installs and runs the peer binary `grok`, and it backs up `~/.grok` auth files. Typed verbs do that work in the terminal. The text menu uses the same tokens. `hello` prints one welcome line and does not draw the menu. **Exit** is menu-only.

## Features

- Console script `agent-cli` and module entry `python -m AgentCli`.
- On a terminal with no arguments, the text menu opens. The first row names the current directory on the left and a local clock (`HH:MM:SS`) on the right when the row has room.
- Multi-user front rows are **1 grok-auth**, **5 sudoers**, **6 self-management**, **7 language**, and **9 Exit**. A this-login-only host shows **2 run** and hides **5**. **3**, **4**, and **8** are not rows. Typing `system-log` opens view, clear, and the log folder.
- **grok-auth** covers session, backup, sync, crontab, setup, and reinstall. **sudoers** covers the backup grant only.
- Thirteen menu languages, codes **80**–**92**. **70**–**79** and **93**–**98** stay unprinted so a later language can be added. The saved leaf is `~/.local/agent-cli/language`. `AGENT_CLI_LANG` overrides one process and does not write the file. `language` is not a typed verb.
- **about** stays in English. It prints the domain line, the runtime tools, a host check, the cache tiers, and the persistence folder.
- Pip lifecycle: `version-check`, `self-update`, `self-install`, and `self-uninstall`. Those verbs do not use sudo. `self-uninstall` on the command line needs `--force`.
- Empty arguments on a terminal do not run pip and do not download `grok`. With no terminal and no verb, the program prints help and returns 0.

## Advantages

1. **Two ways to do the work.** A menu number and the same typed verb share one action. `agent-cli hello` prints `Welcome to AgentCli 1.2.0.` and does not draw the menu. With no arguments on a terminal, the text menu opens and waits. With no terminal and no verb, the program prints help and returns 0.
2. **Built-in languages.** Row **7** lists thirteen languages. The numbers are **80** through **92**. **70** through **79** and **93** through **98** stay unprinted so a later language can be added. The choice is saved for the next run. Leaf shorts stay English.
3. **Cache and persistence.** Linux prefers `/dev/shm/cache`, then `/tmp/cache`, then a leaf under the home cache directory. A missed tier is silent. Persistence is `~/.local/agent-cli`. The about page names the tier this process selected.
4. **A narrow root path.** The only elevated action is `agent-cli backup`, and only after an administrator installs a sudoers fragment whose argument is `backup`. Other verbs stay this login. Peer `grok` is fetched by `setup` from the vendor channel, then the public fallback. This package does not run a vendor shell installer.

| Feature | Typed verb | Text menu |
|---------|------------|-----------|
| Daily start on a terminal | `agent-cli menu` | empty argv |
| Welcome line | `agent-cli hello` | not a front row |
| Peer binary | `agent-cli setup` | grok-auth row **15** |
| Auth deposit | `agent-cli backup` | grok-auth row **11** when signed in |
| Menu language | not a verb | row **7**, codes **80**–**92** |
| This computer | `agent-cli about` | typed `about`, not a numbered row |
| Pip lifecycle | `version-check`, `self-update`, `self-install`, `self-uninstall` | rows **64**, **65**, and **66**. `self-install` is typed. **68** is `where-is-me` |

## Quick Installation

**Python:** 2.7 or newer, excluding 3.0 through 3.4. 3.x is recommended.

**Python dependency:** `ChronicleLogger>=1.3.1` (required). Pip installs it with AgentCli. `setup` needs `curl` when it downloads peer `grok`.

```bash
pip install AgentCli
```

This installs the console entry **`agent-cli`** and the package **`AgentCli`**. Packaging name SSOT is `pyproject.toml` `[project].name` = `AgentCli`. This tree is **1.2.0**. The PyPI badge above shows the live index. Nothing in this tree uploads a release by itself.

From a checkout:

```bash
git clone https://github.com/cloudgen/AgentCli.git
cd AgentCli
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

After install, on a terminal, `agent-cli` with no arguments prints this screen. The verb is the short token. The note after the colon is the explanation. `9` leaves. `0` on a submenu goes back. A number that is not on the list prints an error and lets you choose again. The path row is the current directory and a local clock (`HH:MM:SS`).

```text
$ agent-cli
Path: <current directory>                                          HH:MM:SS
1. grok-auth      : backup, sync, crontab, setup, and reinstall
5. sudoers        : grant and drafts
6. self-management: check, update, or remove this package
7. language       : display language for this menu
9. Exit           : leave
```

## Usage

```bash
agent-cli
python -m AgentCli
```

**hello** prints the welcome line in the terminal and does not draw the menu:

```bash
agent-cli hello
```

```bash
agent-cli help
agent-cli version
agent-cli about
agent-cli hello
agent-cli setup
agent-cli check-session
agent-cli backup
agent-cli where-is-me
agent-cli version-check
agent-cli self-update
agent-cli self-install
agent-cli self-uninstall --force
```

`version` prints `AgentCli 1.2.0` and does not call pip. `about` shows one English page: the product identity, a host check of this computer, the cache tiers, the persistence folder, and a star box. It does not call pip. `hello` prints `Welcome to AgentCli 1.2.0.` and does not draw the menu. `help` prints usage.

`setup` downloads peer `grok` for this platform and links `~/.grok/bin/grok`. `backup` copies `auth.*` into `/var/agent-cli` when this login may run that one command as root. `sync-auth` copies the deposit back and skips that copy when grok is already signed in. `add-crontab` stays closed until the backup grant is present.

`version-check` runs `python -m pip index versions AgentCli`. `self-update` runs `python -m pip install --upgrade AgentCli`. `self-install` runs `python -m pip install AgentCli`. `self-uninstall` runs `python -m pip uninstall -y AgentCli` and needs `--force` on the command line. Those pip verbs do not use sudo. Empty arguments do not install or update.

`agent-cli install` writes this login's shell startup files so `~/.local/bin` is on PATH. A zsh login gets that line on `.zshenv` and again on `.zprofile`. A bash-only login does not invent those zsh files. `.zshrc` is not a PATH file. `agent-cli rc-test` is test-purpose: it writes only under `--root` and leaves this login's real notes still. `agent-cli uninstall --force` may remove this product's installer stickers and does not delete the files.

```python
from AgentCli import main
main()
```

## Screenshots

Each heading is the file name. The paragraph is what that picture shows. Package **1.2.0**. On these captures the path is `/tmp/agent-cli-shots` and the clock is `12:06:45`. Under the rounded input box, three light rows show the logged-out sentence `backup features are not available for logged-out environment.` The status line starts with `AgentCli 1.2.0`. Leaf shorts stay English. **1 grok-auth** is highlighted on each main menu.

### `language-menu.png`

Row **7** has opened the language list. **80 English** is highlighted, with the note "use English for this menu." The other rows are **81 简体中文**, **82 繁體中文**, **83 Español**, **84 العربية**, **85 Français**, **86 Português**, **87 Русский**, **88 Deutsch**, **89 日本語**, **90 한국어**, **91 Nederlands**, and **92 Ελληνικά**. Each note says to use that language for this menu. **0 Back** says "return to the main menu." The path label is `Path`. The status line says `language`.

![Language list, 80 English highlighted](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/language-menu.png)

### `main-menu-en.png`

English main menu. There is no saved-language line above the box. The path label is `Path`. **1 grok-auth** is "backup, sync, crontab, setup, and reinstall." Then **5 sudoers** "grant and drafts," **6 self-management** "check, update, or remove this package," **7 language** "display language for this menu," and **9 Exit** "leave." The status line says `main menu`.

![English main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-en.png)

### `main-menu-zh-hans.png`

Simplified Chinese main menu. The line above the box says `菜单语言是简体中文`. The path label is `路径`. **1 grok-auth** stays the English token. **5** stays `sudoers`. **6** is `自我管理`, **7** is `语言`, and **9** is `离开`. The status line says `主菜单`.

![Simplified Chinese main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-zh-hans.png)

### `main-menu-zh-hant.png`

Traditional Chinese main menu. The line above the box says `選單語言是繁體中文`. The path label is `路徑`. **5** stays `sudoers`. **6** is `自我管理`, **7** is `語言`, and **9** is `離開`. The status line says `主選單`.

![Traditional Chinese main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-zh-hant.png)

### `main-menu-es.png`

Spanish main menu. The line above the box says `El idioma del menú es español`. The path label is `Ruta`. **6** is `autogestión`, **7** is `idioma`, and **9** is `Salir`. The status line says `menú principal`.

![Spanish main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-es.png)

### `main-menu-ar.png`

Arabic main menu. The line above the box says `لغة القائمة هي العربية`. The path label is `المسار`. The numbers stay on the left. **6** is `إدارة ذاتية`, **7** is `لغة`, and **9** is `خروج`. The status line says `القائمة الرئيسية`.

![Arabic main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-ar.png)

### `main-menu-fr.png`

French main menu. The line above the box says `La langue du menu est le français`. The path label is `Chemin`. **6** is `autogestion`, **7** is `langue`, and **9** is `Quitter`. The status line says `menu principal`.

![French main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-fr.png)

### `main-menu-pt.png`

Portuguese main menu. The line above the box says `O idioma do menu é português`. The path label is `Caminho`. **6** is `autogestão`, **7** is `idioma`, and **9** is `Sair`. The status line says `menu principal`.

![Portuguese main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-pt.png)

### `main-menu-ru.png`

Russian main menu. The line above the box says `Язык меню — русский`. The path label is `Путь`. **6** is `самоуправление`, **7** is `язык`, and **9** is `Выход`. The status line says `главное меню`.

![Russian main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-ru.png)

### `main-menu-de.png`

German main menu. The line above the box says `Die Menüsprache ist Deutsch`. The path label is `Pfad`. **6** is `Selbstverwaltung`, **7** is `Sprache`, and **9** is `Beenden`. The status line says `Hauptmenü`.

![German main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-de.png)

### `main-menu-ja.png`

Japanese main menu. The line above the box says `メニューの言語は日本語`. The path label is `パス`. **6** is `自己管理`, **7** is `言語`, and **9** is `終了`. The status line says `メインメニュー`.

![Japanese main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-ja.png)

### `main-menu-ko.png`

Korean main menu. The line above the box says `메뉴 언어는 한국어`. The path label is `경로`. **6** is `자기관리`, **7** is `언어`, and **9** is `종료`. The status line says `주 메뉴`.

![Korean main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-ko.png)

### `main-menu-nl.png`

Dutch main menu. The line above the box says `De menutaal is Nederlands`. The path label is `Pad`. **6** is `zelfbeheer`, **7** is `taal`, and **9** is `Afsluiten`. The status line says `hoofdmenu`.

![Dutch main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-nl.png)

### `main-menu-el.png`

Greek main menu. The line above the box says `Η γλώσσα του μενού είναι ελληνικά`. The path label is `Διαδρομή`. **6** is `αυτοδιαχείριση`, **7** is `γλώσσα`, and **9** is `Έξοδος`. The status line says `κύριο μενού`.

![Greek main menu](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/main-menu-el.png)

### `system-log.png`

Typing `system-log` has opened that board. **31 view-log** is highlighted: "list a log file and show it." Then **32 clear-log**, **33 log-folder**, and **0 Back**. The path label is `Path`. The status line says `system-log`. **3** is not a front row.

![System log, 31 view-log](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/system-log.png)

### `self-management.png`

Row **6** has opened self-management. **64 version-check** is highlighted: "compare this install with pip." Then **65 self-update**, **66 self-uninstall**, **68 where-is-me**, and **0 Back**. The path label is `Path`. The status line says `self-management`.

![Self-management, 64 version-check](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/self-management.png)

### `grok-auth.png`

**1 grok-auth** on a multi-user host while the session word is missing. The board shows **12 sync-auth-from-remote**, **13 sync-auth**, **14 add-crontab**, **15 setup**, **16 reinstall**, and **0 Back**. A signed-in session shows **11 backup** instead of the sync rows. The status line says `grok-auth`.

![Logged-out grok-auth board](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/grok-auth.png)

### `sudoers.png`

Row **5** has opened sudoers. The rows are **51 generate-sudoer-request**, **52 submit-sudoer-request**, **53 print-sudoers**, **54 print-sudoers-install-script**, **55 remove-project-sudoers**, and **0 Back**. The grant argument is `backup` only. The status line says `sudoers`.

![Sudoers board, backup grant only](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/sudoers.png)

### `tui-about.png`

**about** on the result page. The title is `AgentCli (1.2.0) — result`. The page prints `AgentCli 1.2.0`, `Domain: Install and run xAI grok, and back up its auth files.`, `Runtime tools: curl, grok`, and `Entry points: agent-cli, python -m AgentCli`. The host check is headed `[CHECK SYSTEM]:` and includes the cache lines. The footer says `Up/Down scrolls this page.` and `Press a key to return to the main menu.` There is no input box and no clock. The page stays in English.

![About page with cache lines](https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/tui-about.png)

## Examples

```bash
agent-cli
agent-cli version
agent-cli hello
agent-cli about
agent-cli setup
```

`version` prints `AgentCli 1.2.0` and does not call pip. A run that is not the text menu can also print ChronicleLogger status lines above that. The text menu keeps those lines off the screen.

```bash
agent-cli hello
```

That prints `Welcome to AgentCli 1.2.0.` and does not draw the menu.

## Platform Compatibility

Linux is the primary host. macOS and Windows work when Python is present. `setup` selects `linux`, `macos`, or `windows`, and `x86_64` or `aarch64`. The text menu needs a terminal. Git Bash and Windows cmd are this-login-only: they show **run** and hide **sudoers**. Termux is detected from `TERMUX_VERSION` or `AGENT_CLI_HOST_OVERRIDE=termux`.

## Related Projects

- [AgentCli on GitHub](https://github.com/cloudgen/AgentCli) — this program’s source
- [AgentCli on PyPI](https://pypi.org/project/AgentCli/) — this program on PyPI
- [grok-cli](https://github.com/cloudgen/grok-cli) — shell sibling this Python package specializes beside
- [ChronicleLogger](https://github.com/Wilgat/ChronicleLogger) — status logger this program depends on (`ChronicleLogger>=1.3.1`)
- [CIAO](https://github.com/cloudgen/ciao) — Caution, Intentional, Anti-fragile, Over-engineered
- [CIAO-Lite](https://github.com/cloudgen/ciao-lite) — short agent contract
- [safe-rm](https://github.com/cloudgen/safe-rm) — guarded `rm`

## Contributing

1. Keep product law in `docs/requirements/` aligned with this document when behavior changes.
2. Do not add `join`, `list-videos`, or an encoder. Those verbs stay unknown.
3. Version dual SSOT: bump **`pyproject.toml`** and **`src/AgentCli/__init__.py`** `__version__` together.
4. Do not widen the root path past `agent-cli backup`.
5. Empty argv on a terminal opens the menu. Empty argv off a terminal prints help and returns 0.

## License

MIT. See [LICENSE.md](LICENSE.md).

Copyright (c) 2026 cloudgen.

## Last Update

2026-10-22 — **1.2.0**. `submit-sudoer-request` queues a backup-only grant when sudoer-cli and the inbound directory are present, and it does not write `/etc`. `remove-project-sudoers --force` deletes the user draft. `print-sudoers-install-script` writes that draft and an admin script. A host with `proot` on `PATH` reads local auth cookies. 2026-10-12 — **1.2.0**. `agent-cli install` writes this login's shell startup files. A zsh login gets `~/.local/bin` on `.zshenv` and on `.zprofile`. A bash-only login does not invent those files. `rc-test --file zprofile` writes a fixture under `--root`. Front rows are **1 grok-auth**, **5 sudoers**, **6 self-management**, **7 language**, and **9 Exit**. Language codes are **80**–**92**, with **70**–**79** and **93**–**98** left unprinted. Self-management lists **64**, **65**, **66**, and **68**. Typing `system-log` opens **31**–**33**. Under the input box, three light rows name features that are not available. The path line, the local clock (`HH:MM:SS`), and the status line stay. Pictures in `screenshots/` match this menu.
