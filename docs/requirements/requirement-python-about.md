**file**: docs/requirements/requirement-python-about.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-about`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

The about page names this computer, the cache tiers, and the persistence folder. It stays English.

### 1.1 Human-facing

**In one sentence:** `agent-cli about` shows one English page and does not call pip.

| You | Another role | Not this |
|-----|--------------|----------|
| Read the host check and the star box | Domain sentence from `requirement-domain-grok-cli` | A live FFmpeg probe or a curl installer line |

## 2. Core Rules

1. Class `AboutPage` composes the page. Class `CheckSystem` owns the host-check reads. `AboutPage` **MUST NOT** construct `CheckSystem`.
2. The identity block **MUST** include `AgentCli <version>`, `Domain: Install and run xAI grok, and back up its auth files.`, and `Runtime tools: curl, grok`.
3. The page **MUST** name cache folder used, preferred, 1st fallback, 2nd fallback when present, and persistence storage.
4. The star box **MUST** be one rectangle.
5. The page **MUST NOT** print `curl -fsSL`, `py-tui`, `ffmpeg is on PATH`, or `python -m pip install`.
6. A download URL line appears only when a URL is passed. The product URL stays empty.
7. Install kind **MUST** be uninstalled for a source checkout, local for a home copy, and global for `/usr`.

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | Identity, host-check labels, and the star-box title are present |
| AC-2 | Cache used follows `/dev/shm`, then `/tmp`, then the home fallback |
| AC-3 | The page has no curl installer line |
