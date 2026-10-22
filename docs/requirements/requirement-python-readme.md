**file**: docs/requirements/requirement-python-readme.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-readme`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The root README is the user document for AgentCli. Pictures use absolute URLs.

### 1.1 Human-facing

**In one sentence:** The README tells you how to install AgentCli and shows the text menu.

| You | Another role | Not this |
|-----|--------------|----------|
| Read Features, install, and the pictures | Behavior law stays in requirements | A relative `screenshots/` image, or a join picture |

## 2. Core Rules

1. The version badge **MUST** match `[project].version` and `__version__`.
2. Level-2 headings **MUST** be, in order: Features, Advantages, Quick Installation, Usage, Screenshots, Examples, Platform Compatibility, Related Projects, Contributing, License, Last Update.
3. Every PNG under `screenshots/` **MUST** appear as `https://raw.githubusercontent.com/cloudgen/AgentCli/main/screenshots/<name>`.
4. **MUST NOT** use a relative `screenshots/` image link.
5. **MUST NOT** mention `setup.sh`, `sudo pip`, `curl | sh`, `video.png`, or `join-first.png`.
6. The README **MUST** mention the local clock and `HH:MM:SS`.
7. Related Projects links **MUST** be, in order: the GitHub repository, the PyPI project, grok-cli, ChronicleLogger, ciao, ciao-lite, and safe-rm.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | TP-DOC-01 badge, headings, and picture URLs |
