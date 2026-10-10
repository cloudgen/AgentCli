# Reviews — grok-cli

Public product review surface (peer of `tests/`).

| File | Role |
|------|------|
| `what-to-review.md` | Living review plan / checklist |
| `test-plan.md` | TP-* status map |
| `requirement-test-matrix.md` | Requirement → TP families |
| `lessons.md` | Durable failure modes to re-check |
| `index.md` | Report index |
| `cli-routed-verb-table.md` | Kept live-command list: name, function, who may run, comment date, help one-liner (**`SK-CLI-ROUTED-VERB-TABLE`**) |
| `reports/` | Dated review run reports |

**Ship unit:** `src/grok-cli` (**VERSION 1.8.43**)  
**Suite:** `./tests/run.sh`  
**Last suite baseline:** see `test-plan.md` and `reports/`  

**Privilege review focus (1.1.0):** session gate, `/var/grok-cli` deposit (`backup` only), unprivileged `sync-auth`, trust tier **S13**, project-sudoers-file, **independent generate** (`generate-sudoer-request`), `submit-sudoer-request` public inbound, inbound fidelity, **operator-readable errors**, `print-sudoers-install-script`, `remove-project-sudoers` (draft only).
