**file**: docs/requirements/requirement-shell-cli-language.md
**Status**: Active (Version 1.1.2)
**Area**: shell
**Key**: `requirement-shell-cli-language`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the product law for **menu language** on grok-cli. The thirteen codes and the order **51–63** match sshd-cli: English, Simplified Chinese, Traditional Chinese, Spanish, Arabic, French, Portuguese, Russian, German, Japanese, Korean, Dutch, and Greek. It owns the language codes, the saved file, which boards follow the code, and the words those boards print.

Which row is **5**, and how Back and Exit behave on the numbered tree, stays owned by `requirement-shell-cli-default-interaction`. The persistence directory stays owned by `requirement-shell-cli-storage`. This file owns the `language` leaf and the copy.

### 1.1 Human-facing

**In one sentence:** Menu **5** chooses one of thirteen languages, **51** English through **63** Ελληνικά, for the numbered menu, for human `help`, and for human `about`, and the next run opens in that language.

| Includes | Excludes |
|----------|----------|
| Codes `en`, `zh-Hans`, `zh-Hant`, `es`, `ar`, `fr`, `pt`, `ru`, `de`, `ja`, `ko`, `nl`, and `el`; front **5** / block **50–69** (assigned **51–63**); human `help` and human `about` | Translating command output, argv `version`, JSON about fields, or the setup keep / reinstall list |
| File `${HOME}/.local/${APP_NAME}/language` | Putting that file in the cache folder or under `/var/grok-cli` |

## 2. Core Rules / Requirements (Mandatory)

**Claimed:** yes. Default language is English so an existing menu test keeps matching English words.

### 2.1 Languages

| Code | Name on the language board | Number | Default |
|------|----------------------------|--------|---------|
| `en` | English | **51** | yes |
| `zh-Hans` | 简体中文 | **52** | no |
| `zh-Hant` | 繁體中文 | **53** | no |
| `es` | Español | **54** | no |
| `ar` | العربية | **55** | no |
| `fr` | Français | **56** | no |
| `pt` | Português | **57** | no |
| `ru` | Русский | **58** | no |
| `de` | Deutsch | **59** | no |
| `ja` | 日本語 | **60** | no |
| `ko` | 한국어 | **61** | no |
| `nl` | Nederlands | **62** | no |
| `el` | Ελληνικά | **63** | no |

**MUST** accept only these thirteen codes in this version. **MUST** treat a missing file, an empty file, or any other first line as English for this process. **MUST NOT** rewrite a file whose first line is not one of these codes. **MUST NOT** add a fourteenth code without a new revision of this file. Numbers **50** through **69** are the only language rows (not more than 20 languages). **50** and **64** through **69** are reserved and are not printed.

The short names **English**, **简体中文**, **繁體中文**, **Español**, **العربية**, **Français**, **Português**, **Русский**, **Deutsch**, **日本語**, **한국어**, **Nederlands**, and **Ελληνικά** are the same words in every language (each language’s own name).

### 2.2 Where the choice is stored

1. The leaf is `${HOME}/.local/${APP_NAME}/language`, inside the persistence directory from `requirement-shell-cli-storage`. **MUST NOT** put it in the cache folder. **MUST NOT** put it under `/var/grok-cli`.
2. The file is one line, one of the thirteen codes, then a newline. Mode **0600**. A trailing CR is ignored. Only the first line is read.
3. `app_lang_load` sets `APP_LANG` once, at the start of `app_main`, after persistence is resolved and before argv dispatch. Human `help`, human `about`, and the menu all see that value. **MUST NOT** call it again in that same process. A later call would let `GROK_CLI_LANG` cover a pick just saved.
4. When `GROK_CLI_LANG` is one of those thirteen codes, that value wins over the file at process start. It does not write the file. A menu pick still writes the file and sets `APP_LANG` for the rest of that process.
5. `app_lang_save` writes the line and sets `APP_LANG` only after the write succeeds. A code outside the thirteen returns failure and leaves `APP_LANG` unchanged.

### 2.3 Menu numbers

Front **5** opens the language board on every host, including Termux, Git Bash, and Windows cmd. It is not a hide cause. Front **6** is not a row. Choosing **6** warns and does not open the language board and does not write the file. **51** saves `en`. **52** saves `zh-Hans`. **53** saves `zh-Hant`. **54** saves `es`. **55** saves `ar`. **56** saves `fr`. **57** saves `pt`. **58** saves `ru`. **59** saves `de`. **60** saves `ja`. **61** saves `ko`. **62** saves `nl`. **63** saves `el`. Each is a valid leaf: an info line names the language, then the front board redisplays in that language.

**0** / `q` / empty / `back` is Back and does not write the file. **9** / `exit` / `quit` leaves the program, the same as the other grok submenus. EOF leaves the program. An invalid choice, including **50** and **64** through **69**, `out_error` and reprints this board. **MUST NOT** `out_die`.

`language` is not an argv verb. Typed `language`, `語言`, `语言`, `idioma`, `langue`, `Sprache`, `sprache`, `言語`, `언어`, `لغة`, `язык`, `taal`, and `γλώσσα` on the front board open it when row **5** is listed (it always is).

The language board also accepts:

| Row | Typed tokens |
|-----|----------------|
| **51** | `english`, `en`, `English` |
| **52** | `simplified-chinese`, `zh-hans`, `zh-Hans`, `简体中文` |
| **53** | `traditional-chinese`, `zh-hant`, `zh-Hant`, `繁體中文` |
| **54** | `spanish`, `es`, `Español`, `español` |
| **55** | `arabic`, `ar`, `العربية`, `عربي` |
| **56** | `french`, `fr`, `Français`, `français` |
| **57** | `portuguese`, `pt`, `Português`, `português`, `portugues` |
| **58** | `russian`, `ru`, `Русский`, `русский` |
| **59** | `german`, `de`, `Deutsch`, `deutsch` |
| **60** | `japanese`, `ja`, `日本語` |
| **61** | `korean`, `ko`, `한국어` |
| **62** | `dutch`, `nl`, `Nederlands`, `nederlands` |
| **63** | `greek`, `el`, `Ελληνικά`, `ελληνικά` |

The front board also accepts the displayed category short: `grok-auth`, `grok 認證`, `grok 认证`, `autenticación grok`, `authentification grok`, `grok-Anmeldung`, `grok 認証`, `grok 인증`, `مصادقة grok`, `autenticação grok`, `вход grok`, `grok-aanmelding`, `σύνδεση grok`; `self-management`, `自我管理`, `autogestión`, `autogestion`, `Selbstverwaltung`, `selbstverwaltung`, `自己管理`, `자기관리`, `إدارة-ذاتية`, `autogestão`, `самоуправление`, `zelfbeheer`, `αυτοδιαχείριση`. The sudoers short stays `sudoers` in every language.

### 2.4 What follows the saved language

**MUST** follow `APP_LANG` on these boards: front, grok-auth, language, self-management, and sudoers. That covers the layer title, the category shorts, every long description, Back, Exit, the choose-prompt, the unknown-choice line, and the three menu-hidden sentences.

**MUST** keep each leaf short as the English verb in every language (`backup`, `run`, `setup`, `reinstall`, `generate-sudoer-request`, and the other leaf tokens). The sudoers category short stays `sudoers` in every language.

English (`APP_LANG=en`, or unset) **MUST** keep these literals so the existing menu tests still match: `logged in`, `timeout`, `logged out`, `Choice: `, `Not a menu choice`, `9. Exit`, `0. Back`, `Alternative online installer for xAI grok`, and the three hide sentences `backup, sync-auth and sudoers features are not available in {{label}}.`, `sync-auth and sync-auth-from-remote features are not available for logged-in environment.`, and `backup features are not available for logged-out environment.` The English choose-prompt stays `Choice: ` (trailing space). The English unknown line stays `Not a menu choice`.

Category shorts:

| Token | en | zh-Hans | zh-Hant | es | ar | fr | pt |
|-------|----|---------|---------|----|----|----|-----|
| grok-auth | grok-auth | grok 认证 | grok 認證 | autenticación grok | مصادقة grok | authentification grok | autenticação grok |
| language | language | 语言 | 語言 | idioma | لغة | langue | idioma |
| self-management | self-management | 自我管理 | 自我管理 | autogestión | إدارة-ذاتية | autogestion | autogestão |
| sudoers | sudoers | sudoers | sudoers | sudoers | sudoers | sudoers | sudoers |

| Token | ru | de | ja | ko | nl | el |
|-------|----|----|----|----|----|-----|
| grok-auth | вход grok | grok-Anmeldung | grok 認証 | grok 인증 | grok-aanmelding | σύνδεση grok |
| language | язык | Sprache | 言語 | 언어 | taal | γλώσσα |
| self-management | самоуправление | Selbstverwaltung | 自己管理 | 자기관리 | zelfbeheer | αυτοδιαχείριση |
| sudoers | sudoers | sudoers | sudoers | sudoers | sudoers | sudoers |

English front longs: grok-auth `Backup, sync, crontab, setup, and reinstall`; language `display language for this menu`; sudoers `Grant and drafts`; self-management `Check, update, or remove grok-cli`; run `Start grok without auto-update`. The other twelve languages use the same meaning through `app_menu_text`.

Language-board longs (English): `use English for this menu`, `use Simplified Chinese for this menu`, `use Traditional Chinese for this menu`, `use Spanish for this menu`, `use Arabic for this menu`, `use French for this menu`, `use Portuguese for this menu`, `use Russian for this menu`, `use German for this menu`, `use Japanese for this menu`, `use Korean for this menu`, `use Dutch for this menu`, `use Greek for this menu`.

Back / Exit: en `Back` / `Exit`; zh-Hans `返回` / `离开`; zh-Hant `返回` / `離開`; es `Atrás` / `Salir`; ar `رجوع` / `خروج`; fr `Retour` / `Quitter`; pt `Voltar` / `Sair`; ru `Назад` / `Выход`; de `Zurück` / `Beenden`; ja `戻る` / `終了`; ko `뒤로` / `종료`; nl `Terug` / `Afsluiten`; el `Πίσω` / `Έξοδος`.

After a successful save the info line is printed in the new language:

| Code | Saved |
|------|--------|
| `en` | `Menu language is English` |
| `zh-Hans` | `菜单语言是简体中文` |
| `zh-Hant` | `選單語言是繁體中文` |
| `es` | `El idioma del menú es español` |
| `ar` | `لغة القائمة هي العربية` |
| `fr` | `La langue du menu est le français` |
| `pt` | `O idioma do menu é português` |
| `ru` | `Язык меню — русский` |
| `de` | `Die Menüsprache ist Deutsch` |
| `ja` | `メニューの言語は日本語` |
| `ko` | `메뉴 언어는 한국어` |
| `nl` | `Menutaal is Nederlands` |
| `el` | `Η γλώσσα του μενού είναι ελληνικά` |

A failed write warns in the language that was current before the failed write, leaves `APP_LANG` unchanged, and still returns to the front board. English failure text is `Could not save the menu language`.

**MUST** follow `APP_LANG` on human `help` and human `about`. Section headings follow the code. The command token, the flag, the path, and the env name stay the Latin spelling (`install`, `setup`, `--json`, `SCRIPT_URL`, `GROK_CLI_LANG`). English `help` still prints `Usage:` and `Test-purpose`. English `about` still prints `About / Diagnostics` and `Cache folder used:`. Japanese about prints `概要 / 診断` and `使用中のキャッシュフォルダ:`. Korean about prints `개요 / 진단` and `사용 중인 캐시 폴더:`. Greek help prints `Χρήση:`.

**Stays English in this version:** argv `version`, operational command output, JSON about keys and JSON values, JSON help, and the setup keep / reinstall list.

`app_menu_text` prints the chosen string on stdout. The caller passes that string to `out_*`. The operator sees `out_*`. `app_menu_text` is pure data: it **MUST NOT** call `read`.

## 3. Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-CLI-32** | `tests/test_cli.sh` | have (front **5** / block **50–69**, assigned **51–63**, **50** and **64–69** unprinted, front **6** does not open the board, save mode 0600, `GROK_CLI_LANG` override, Back does not write, next run uses the file, help and about follow the code) |
| **TP-CLI-13** · **TP-CLI-19** · **TP-CLI-20** · **TP-CLI-30** | `tests/test_cli.sh` | have (English front still matches; **5** opens language; unused front integer is **4**; on Termux the unused integer that replaced **5** is **6**) |

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`

---

**Last Updated**: 2026-10-10 (1.1.2 — logged-out hide sentence names `backup`. 1.1.1 also named `sync-auth-to-remote`.)
**Owner**: product
**Alignment**: `requirement-shell-cli-default-interaction` · `requirement-shell-cli-storage` · `requirement-shell-cli-interface` · CIAO / CIAO-Lite
