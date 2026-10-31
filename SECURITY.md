# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.2.1 (Python package, current) | Yes |
| 1.8.47 (shell reference) | Yes |
| 1.8.46 | Yes |
| 1.8.45 | Yes |
| 1.8.44 | Yes |
| 1.8.43 | Yes |
| 1.8.42 | Yes |
| 1.8.32 | Yes |
| 1.8.31 | Yes |
| 1.8.30 | Yes |
| 1.8.29 | Yes |
| 1.8.28 | Yes |
| 1.8.27 | Yes |
| 1.8.26 | Yes |
| 1.8.25 | Yes |
| 1.8.24 | Yes |
| 1.8.23 | Yes |
| 1.8.22 | Yes |
| 1.8.21 | Yes |
| 1.8.20 | Yes |
| 1.8.19 | Yes |
| 1.8.18 | Yes |
| 1.8.14 | Yes |
| 1.8.13 | Yes |
| 1.8.12 | Yes |
| 1.8.11 | Yes |
| 1.8.10 | Yes |
| 1.8.9 | Yes |
| 1.8.8 | Yes |
| 1.8.7 | Yes |
| 1.8.6 | Yes |
| 1.8.5 | Yes |
| 1.8.4 | Yes |
| 1.8.3 | Yes |
| 1.8.2 | Yes |
| 1.8.1 | Yes |
| 1.8.0 | Yes |
| 1.7.3 | Yes |
| 1.7.2 | Yes |
| 1.7.1 | Yes |
| 1.7.0 | Yes |
| 1.6.0 | Yes |
| 1.5.0 | Yes |
| 1.4.0 | Yes |
| 1.3.0 | Yes |
| 1.2.2 | Yes |
| 1.2.1 | Yes |
| 1.2.0 | Yes |
| 1.1.0 | Yes |
| 1.0.0 | Yes |

## Reporting a Vulnerability

Please **do not** open a public issue for security-sensitive reports when a private channel is available.

**Maintainer contact (email):** `wongcf22@gmail.com`

- Source of contact: product **author-email** SSOT in [`LICENSE.md`](./LICENSE.md) (Copyright line).  
- Prefer email (or private GitHub security advisories when enabled) for vulnerability details, reproduction steps, and impact.  
- Do not include exploit weaponization guides in public channels.

## Security Design Principles (CIAO)

This project follows **[CIAO](https://github.com/cloudgen/ciao)** / **[CIAO-Lite](https://github.com/cloudgen/ciao-lite)** defensive design. Security-relevant intent:

| Letter | Principle | Security application |
|--------|-----------|----------------------|
| **C** | **Caution** | Fail closed unless `grok -p hello` succeeds; fail closed without allowlisted `sudo grok-cli backup` for `/var/grok-cli`. Never print tokens or grok’s prompt answer. |
| **I** | **Intentional** | Session check and `sync-auth` stay the invoking login; only deposit/chown/chmod is elevated. `print-sudoers` never writes `/etc`. |
| **A** | **Anti-fragile** | `GROK_HOME` / `GROK_CLI_ROOT` overrides keep tests off production dest; SUDO_USER home used when re-exec'd as root. |
| **O** | **Over-protect** | Narrow Cmnd only (`NOPASSWD: /usr/local/bin/grok-cli backup`); no `cp`/`chmod`/`chown` sudoers tools; Protection Zones. |

Full principles: [CIAO](https://github.com/cloudgen/ciao) · [CIAO-Lite](https://github.com/cloudgen/ciao-lite).

This section is **design posture**, not a third-party certification claim.

## Scope notes

- Elevation is limited to allowlisted `grok-cli backup` under product law.  
- **Online install** fetches this product’s ship unit from `SCRIPT_URL` (`https://raw.githubusercontent.com/cloudgen/grok-cli/main/src/grok-cli`) as the invoking login. Companion `${SCRIPT_URL}.sha256` is checked when present. This is **not** xAI’s grok installer.  
- **`setup`** fetches xAI’s published **version pointer and `grok` binary** (`https://x.ai/cli/{channel}` and `https://x.ai/cli/grok-{version}-{os}-{arch}`) as the invoking login (no sudo). It does **not** download or execute `install.sh`, does **not** install grok-cli, and does **not** grant extra sudoers. Treat the vendor **binary** as third-party code.  
- Operators must admin-install sudoers fragments after review (`visudo -c`, mode `0440`) **or** have sudoer-adm approve the JSON request.  
- **Install trust tiers for elevation:**
  - **Production:** global managed binary (`/usr/local/bin/grok-cli`, typically root-owned). Prefer `sudo grok-cli install` before durable sudoers.  
  - **Test mode only:** local `~/.local/bin/grok-cli` is **user-rewritable**. Do **not** treat local-only sudoers as production-secure.  
  - `print-sudoers` refuses non-production tiers unless `--allow-test-local` / `ALLOW_TEST_LOCAL_SUDOERS=1`.  
  - **Per-user host paths:** draft `~/.config/grok-cli/sudoers.fragment-<user>` installs to `/etc/sudoers.d/grok-cli-<user>`.  
- **Shared store residual:** `/var/grok-cli/auth.*` are **world-readable** (`0644`) so `sync-auth` needs no sudo. Anyone who can read the host can use those grok credentials. That is intentional for this product (shared login on a host) and is **not** equivalent to keeping tokens `0600` in a private home.  
- Home copies from `sync-auth` return `auth.json` to mode `0600`.  
- **`sync-auth-to-remote`** copies this login’s `~/.grok/auth.*` to the remote SSH login’s `~/.grok` (`ssh` + `scp` BatchMode, no sudo) and sets remote `auth.json` to mode `0600`. It does not write `/var/grok-cli`. The remote login can then use those grok credentials.  
- Related docs: [`README.md`](./README.md), [`LICENSE.md`](./LICENSE.md), `docs/requirements/requirement-three-layer-privilege-model.md`, `docs/requirements/requirement-grok-auth-backup.md`.
