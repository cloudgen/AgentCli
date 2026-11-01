**file**: docs/requirements/requirement-python-about.md
**Status**: Active (Version 1.3.0)
**Area**: python
**Key**: `requirement-python-about`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The about page names this computer, the cache tiers, the persistence folder, and the Cython shared-object name. It stays English.

### 1.1 Human-facing

**In one sentence:** `agent-cli about` shows one English page, records the Cython `.so` name, and does not call pip.

| You | Another role | Not this |
|-----|--------------|----------|
| Read the host check and the star box | Domain sentence from `requirement-domain-grok-cli` | A live FFmpeg probe or a curl installer line |
| Read `Cython .so` | The same name on `agent-cli about --json` as `cython_so` | A compile step, or a claim that the file is already on disk |

## 2. Core Rules

1. Class `AboutPage` composes the page. Class `CheckSystem` owns the host-check reads. `AboutPage` **MUST NOT** construct `CheckSystem`.
2. The identity block **MUST** include `AgentCli <version>`, `Domain: Install and run xAI grok, and back up its auth files.`, and `Runtime tools: curl, grok`.
3. The page **MUST** name cache folder used, preferred, 1st fallback, 2nd fallback when present, and persistence storage.
4. The star box **MUST** be one rectangle.
5. The page **MUST NOT** print `curl -fsSL`, `py-tui`, `ffmpeg is on PATH`, or `python -m pip install`.
6. A download URL line appears only when a URL is passed. The product URL stays empty.
7. Install kind **MUST** be uninstalled for a source checkout, local for a home copy, and global for `/usr`.
8. The host check **MUST** record the Cython shared-object name on the line `Cython .so`, immediately after `Cython String`. `Cython String` stays `sysconfig.get_config_var("SOABI")`, or empty. The shared-object name is `AgentCli.` plus that SOABI plus `.so` when the SOABI is non-empty. An empty SOABI leaves `Cython .so` empty. Both lines stay. The page does not compile an extension and does not require that file to exist.
9. `agent-cli about --json` **MUST** record the same name as the string field `cython_so`. An empty SOABI records `""`. Domain fields stay on `requirement-domain-grok-cli`. Storage fields stay on `requirement-python-cli-storage`.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | Identity, host-check labels, and the star-box title are present |
| AC-2 | Cache used follows `/dev/shm`, then `/tmp`, then the home fallback |
| AC-3 | The page has no curl installer line |
| AC-4 | `Cython .so` is `AgentCli.` plus the SOABI plus `.so` when the SOABI is non-empty, and empty when the SOABI is empty. `Cython String` stays the SOABI |
| AC-5 | `agent-cli about --json` field `cython_so` is that same string |

## Terminologies

### CLI about

**Definition:** CLI about is the operator page of the verb `about`. It prints live facts for this run: which program this is, what this computer is, and where the program is running from. The page is three blocks in this order: identity, host check, install location. A missing host-check value stays a blank on a line that remains. The check reads the environment and path existence. It does not spawn `python2`, `python3`, `conda`, or `pyenv`, and it does not freeze a login, a home path, or a display id into the page. When the menu claims the row, the number is 83 under self-management. A specialized product requirement owns extra identity lines and the live reads.

**Human daily-life explanation:** CLI about is the card the tool shows when you ask what it is and which machine it is on. It names the program, the computer, and the drawer it is running from. It does not install itself, and it does not start other programs to look those facts up.

**Daily-life example:** You ask the kitchen timer about. It says which model it is, that it is on the counter, and which drawer it came from. It does not start the oven to answer.

### CLI about Python example

**Definition:** CLI about Python example is the picture of CLI about for a Python CLI. It shows the host-check labels in a fixed order, including `python2 location`, `python3 location`, `conda location`, `pyenv location`, then `PID`, the cache folder chain, persistence storage, and `TTY / Interactive`. `Cython String` on that picture is the SOABI text, or blank. Values are read at print time. When the picture is under conda, `python2` and `python3` are inside the active prefix, and `conda location` is that prefix root's `bin/conda`. When the picture is under pyenv and not under conda, those interpreters stay inside the pyenv root, and `pyenv location` is that root's `bin/pyenv`. When both qualify, conda owns the two interpreter lines and pyenv still owns `pyenv location`. A missing interpreter is a blank value. The line stays. The check does not spawn those programs. A specialized product requirement owns domain sentences and the live reads.

**Human daily-life explanation:** CLI about Python example is the sample card for a Python tool's about answer. It names the Python that is in use, and it points at the conda or pyenv drawer when that drawer is the one in charge. It does not start those programs to ask them.

**Daily-life example:** The card says the whisk in the blue jar, and when a labeled jar is on the counter it names that jar's whisk, not a different whisk that happens to be first in the drawer.

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-22 | Active 1.2.0 | Host check, cache lines, star box, English page |
| 2026-11-01 | Active 1.3.0 | `about` records the Cython `.so` name on `Cython .so` and as JSON `cython_so` |
