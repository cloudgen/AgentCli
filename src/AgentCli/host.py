# =============================================================================
# This-login-only host detect.
# requirement-shell-cli-default-interaction — Termux, Git Bash, Windows cmd.
# requirement-python-oop — class Host.
# =============================================================================
from __future__ import annotations

import os
import platform


class Host:
    """Whether this host is command-line for a normal user only.

    AGENT_CLI_HOST_OVERRIDE is multiuser, termux, gitbash, or windows-cmd.
    A set TERMUX_VERSION is Termux even when the override says multiuser is
    not the case: multiuser and gitbash and windows-cmd suppress Termux.
    """

    def __init__(self, environ=None):
        self.environ = os.environ if environ is None else environ

    def override(self) -> str:
        return self.environ.get("AGENT_CLI_HOST_OVERRIDE", "")

    def is_termux(self) -> bool:
        """TERMUX_VERSION wins. Then the host override. Then a set PREFIX.

        A bare PREFIX is Termux, matching the shell host helper. An explicit
        multiuser, gitbash, or windows-cmd override still wins over PREFIX.
        """
        if self.environ.get("TERMUX_VERSION"):
            return True
        forced = self.override()
        if forced in ("multiuser", "gitbash", "windows-cmd"):
            return False
        if forced == "termux":
            return True
        if self.environ.get("PREFIX"):
            return True
        return self._uname_says_android()

    def _uname_says_android(self) -> bool:
        try:
            blob = " ".join(str(part) for part in platform.uname())
        except Exception:
            blob = platform.platform()
        return "Android" in blob

    def is_git_bash(self) -> bool:
        if self.override() == "gitbash":
            return True
        if self.override() in ("multiuser", "termux", "windows-cmd"):
            return False
        if self.environ.get("MSYSTEM"):
            return True
        system = platform.system()
        return system.startswith("MINGW") or system.startswith("MSYS")

    def is_windows_cmd(self) -> bool:
        if self.override() == "windows-cmd":
            return True
        if self.override() in ("multiuser", "termux", "gitbash"):
            return False
        if self.environ.get("OS") != "Windows_NT":
            return False
        if self.is_git_bash():
            return False
        system = platform.system()
        if system.startswith("CYGWIN") or system.startswith("MINGW") or system.startswith("MSYS"):
            return False
        if self.environ.get("WSL_DISTRO_NAME") or self.environ.get("WSL_INTEROP"):
            return False
        return True

    def normal_user_only(self) -> bool:
        if self.override() == "multiuser":
            return False
        return self.is_termux() or self.is_git_bash() or self.is_windows_cmd()

    def label(self) -> str:
        if self.is_termux():
            return "termux"
        if self.is_git_bash():
            return "gitbash"
        if self.is_windows_cmd():
            return "windows-cmd"
        return ""
