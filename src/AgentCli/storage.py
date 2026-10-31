# =============================================================================
# Cache folder and persistence storage.
# requirement-python-cli-storage — class Storage is the only resolver.
# requirement-shell-cli-storage — POSIX tier shapes. This class does not copy them.
# requirement-python-oop — class Storage. No module-level helpers.
# A missed tier is silent. The preferred leaf is not /dev/shm/${APP_NAME}.
# =============================================================================
from __future__ import annotations

import os
import platform
import tempfile


class Storage:
    """Scratch cache and the durable per-login directory.

    Linux preferred leaf is /dev/shm/cache/cache-${APP_NAME}-${login}-$$.
    Git Bash preferred leaf is /tmp/cache/cache-${APP_NAME}-${login}-$$.
    Mac preferred leaf is the same /tmp/cache shape.
    Home leaves omit the login segment. Persistence is ${HOME}/.local/${APP_NAME}.
    """

    APP_NAME = "agent-cli"

    def __init__(self, app_name=None, home=None, login=None, pid=None, environ=None):
        self.app_name = app_name or self.APP_NAME
        self.environ = os.environ if environ is None else environ
        if home is None:
            home = self.environ.get("HOME", "")
        self.home = home or "/tmp"
        self.login_name = login
        self.pid = os.getpid() if pid is None else pid
        self.used = ""

    def host_kind(self) -> str:
        """linux, gitbash, or mac. AGENT_CLI_CACHE_HOST overrides the probe."""
        forced = self.environ.get("AGENT_CLI_CACHE_HOST", "")
        if forced in ("linux", "gitbash", "mac"):
            return forced
        if self.environ.get("MSYSTEM"):
            return "gitbash"
        system = platform.system()
        if system == "Darwin":
            return "mac"
        uname = platform.uname().system if hasattr(platform, "uname") else system
        if uname.startswith("MINGW") or uname.startswith("MSYS"):
            return "gitbash"
        return "linux"

    def login(self) -> str:
        """Path-safe login. Non-token characters become underscores."""
        if self.login_name:
            raw = self.login_name
        else:
            raw = self.environ.get("USERNAME") or self.environ.get("USER") or "unknown"
        cleaned = []
        for char in raw:
            if char.isalnum() or char in "._-":
                cleaned.append(char)
            else:
                cleaned.append("_")
        text = "".join(cleaned)
        return text or "unknown"

    def volatile_leaf(self) -> str:
        return "cache-{0}-{1}-{2}".format(self.app_name, self.login(), self.pid)

    def home_leaf(self) -> str:
        return "cache-{0}-{1}".format(self.app_name, self.pid)

    def preferred_dir(self) -> str:
        leaf = self.volatile_leaf()
        if self.host_kind() in ("gitbash", "mac"):
            return "/tmp/cache/{0}".format(leaf)
        return "/dev/shm/cache/{0}".format(leaf)

    def fallback_dir(self) -> str:
        kind = self.host_kind()
        if kind == "gitbash":
            return os.path.join(self.home, "AppData", "Local", "Temp", self.home_leaf())
        if kind == "mac":
            return os.path.join(self.home, "Library", "Caches", self.home_leaf())
        return "/tmp/cache/{0}".format(self.volatile_leaf())

    def fallback2_dir(self) -> str:
        kind = self.host_kind()
        if kind == "gitbash":
            return ""
        if kind == "mac":
            return os.path.join(self.home, "cache", self.home_leaf())
        return os.path.join(self.home, ".cache", self.home_leaf())

    def try_dir(self, path: str) -> bool:
        """Create one tier. Silent failure lets the caller try the next tier."""
        if not path:
            return False
        parent = os.path.dirname(path)
        try:
            if parent in ("/dev/shm/cache", "/tmp/cache"):
                os.makedirs(parent, mode=0o1777, exist_ok=True)
                try:
                    os.chmod(parent, 0o1777)
                except OSError:
                    pass
            else:
                os.makedirs(parent, mode=0o700, exist_ok=True)
            os.makedirs(path, mode=0o700, exist_ok=True)
            os.chmod(path, 0o700)
        except OSError:
            return False
        return os.path.isdir(path) and os.access(path, os.W_OK)

    def persistent_dir(self) -> str:
        return os.path.join(self.home, ".local", self.app_name)

    def resolve_persistent(self) -> str:
        """Create persistence storage. Fail closed. Not the install bin directory."""
        path = self.persistent_dir()
        if path.rstrip("/").endswith(os.path.join(".local", "bin")):
            raise OSError("Persistence storage must not be the install bin directory {0}".format(path))
        os.makedirs(path, mode=0o700, exist_ok=True)
        if not os.access(path, os.W_OK):
            raise OSError("Cannot create persistence storage {0}".format(path))
        return path

    def resolve(self) -> str:
        """First writable tier. Silent when a higher tier is skipped."""
        chosen = ""
        if self.environ.get("AGENT_CLI_CACHE_SKIP", "") != "preferred":
            preferred = self.preferred_dir()
            if self.try_dir(preferred):
                chosen = preferred
        if not chosen:
            first = self.fallback_dir()
            if self.try_dir(first):
                chosen = first
        if not chosen:
            second = self.fallback2_dir()
            if second and self.try_dir(second):
                chosen = second
        if not chosen:
            raise OSError("Cannot create cache folder")
        self.used = chosen
        return chosen

    def mktemp(self, suffix: str = "tmp") -> str:
        """Scratch file under the cache root. Refuses a predictable $$ template."""
        if "$$" in suffix:
            raise OSError("refuse predictable $$ name template")
        root = self.used or self.resolve()
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            prefix="{0}.{1}.".format(self.app_name, suffix),
            dir=root,
            delete=False,
        )
        handle.close()
        return handle.name

    def about_fields(self) -> dict:
        """Human labels and the live directories. A skipped tier is not an error."""
        used = self.used or self.resolve()
        second = self.fallback2_dir()
        return {
            "cache_used": used,
            "cache_preferred": self.preferred_dir(),
            "cache_fallback": self.fallback_dir(),
            "cache_fallback_2": second,
            "persistence_storage": self.persistent_dir(),
        }

    def about_lines(self) -> list:
        """Cache folder used, preferred, 1st fallback, 2nd fallback when present."""
        fields = self.about_fields()
        lines = [
            "Cache folder used: {0}".format(fields["cache_used"]),
            "Cache folder (preferred): {0}".format(fields["cache_preferred"]),
            "Cache folder (1st fallback): {0}".format(fields["cache_fallback"]),
        ]
        if fields["cache_fallback_2"]:
            lines.append("Cache folder (2nd fallback): {0}".format(fields["cache_fallback_2"]))
        lines.append("Persistence storage: {0}".format(fields["persistence_storage"]))
        return lines
