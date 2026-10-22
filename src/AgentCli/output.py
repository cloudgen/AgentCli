# =============================================================================
# Human lines and JSON objects.
# requirement-shell-output-requirements — success on stdout, errors on stderr.
# requirement-python-oop — class Output.
# =============================================================================
from __future__ import annotations

import json
import sys


class Output:
    """One writer for human lines and for --json objects."""

    def __init__(self, json_mode=False, quiet=False):
        self.json_mode = bool(json_mode)
        self.quiet = bool(quiet)

    def escape(self, value) -> str:
        return json.dumps("" if value is None else str(value), ensure_ascii=False)[1:-1]

    def info(self, message: str) -> None:
        if self.quiet or self.json_mode:
            return
        print("[INFO] {0}".format(message))

    def error(self, message: str, nxt: str) -> int:
        """Human error on stderr. JSON error object on stderr when --json."""
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

    def ok(self, kind: str, message: str, fields=None) -> int:
        if self.json_mode:
            body = {"type": kind, "message": message}
            if fields:
                body.update(fields)
            print(json.dumps(body, ensure_ascii=False))
        elif not self.quiet:
            print("[INFO] {0}".format(message))
        return 0
