**file**: docs/requirements/requirement-python-error-handling.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-error-handling`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Errors say what happened and the next command. Source auth files are not deleted by a failed sync.

### 1.1 Human-facing

**In one sentence:** A failed backup or sync tells you the next command and leaves the other copy where it was.

| You | Another role | Not this |
|-----|--------------|----------|
| Read `ERROR:` and `Next:` | `Output.error` writes both | A silent `pass` on a failed deposit |

## 2. Core Rules

1. Human errors **MUST** go to stderr as `ERROR:` plus `Next:`.
2. `--json` errors **MUST** be one JSON object on stderr with `type` `out_error`.
3. Missing grok on `run` or `update-grok` **MUST** name `agent-cli setup`.
4. `sync-auth` **MUST** skip when the session is valid or timeout, and **MUST** say `No sync-auth for logged-in environment.`
5. `sync-auth-to-remote` **MUST** still run when the session is valid.
6. A bad remote SPEC **MUST** be refused. Accepted forms are `user@IPv4`, IPv4, domain, and `user@domain`.
7. `reinstall` **MUST NOT** delete `auth.*`.
8. Unknown verbs **MUST** be non-zero. `restore` is unknown.
9. `Output.info` **MUST** stay silent when quiet or `--json`. `Output.error` **MUST** write `ERROR:` and `Next:` on stderr, or one stderr object with `type` `out_error` when `--json`. `Output.ok` **MUST** write one JSON object on stdout when `--json`.

## Sample code

`output.py` is this writer. Domain code calls these methods.

```python
class Output:
    def __init__(self, json_mode=False, quiet=False):
        self.json_mode = bool(json_mode)
        self.quiet = bool(quiet)

    def info(self, message):
        if self.quiet or self.json_mode:
            return
        print("[INFO] {0}".format(message))

    def error(self, message, nxt):
        if self.json_mode:
            body = {
                "type": "out_error",
                "message": message,
                "code": "error",
                "next": nxt,
            }
            print(json.dumps(body, ensure_ascii=False), file=sys.stderr)
        else:
            print("ERROR: {0}".format(message), file=sys.stderr)
            print("   Next: {0}".format(nxt), file=sys.stderr)
        return 1

    def ok(self, kind, message, fields=None):
        if self.json_mode:
            body = {"type": kind, "message": message}
            if fields:
                body.update(fields)
            print(json.dumps(body, ensure_ascii=False))
        elif not self.quiet:
            print("[INFO] {0}".format(message))
        return 0
```

## 3. Acceptance

| AC | Statement |
|----|-----------|
| AC-1 | Logged-in `sync-auth` skips |
| AC-2 | `restore` is unknown |
| AC-3 | A bad SPEC is refused |
| AC-4 | `Output.error` names `ERROR:` and `Next:`, and `--json` uses `out_error` |

## Terminologies

### Operator-readable error

**Definition:** An operator-readable error is a product failure message a person at the prompt can act on without decoding maintainer jargon. It states what happened in one concrete sentence, what it means in plain words, and what to do next (a command or who to ask).

**Human daily-life explanation:** An operator-readable error is a failure message a person at the prompt can act on: what happened, what it means, what to do next, without maintainer slang.

**Daily-life example:** “The oven is off; turn the knob to 180 and press Start” beats “E_THERM_NULL in module 7.”

## 4. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-22 | Active 1.2.0 | Sample is `Output.info`, `error`, and `ok` |
