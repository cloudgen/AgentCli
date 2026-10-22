# =============================================================================
# xAI grok install, session, and auth deposit.
# requirement-domain-grok-cli — verbs, deposit, sudoer JSON, setup channel.
# requirement-grok-auth-backup — session words and sync skip.
# requirement-shell-cli-storage — scratch files go through class Storage.
# requirement-python-oop — class GrokDomain. No module-level helpers.
# Peer binary stays grok. Auth files stay under ~/.grok.
# This module does not run a vendor shell installer.
# =============================================================================
from __future__ import annotations

import datetime
import glob
import io
import json
import os
import platform
import re
import shutil
import subprocess
from contextlib import redirect_stderr, redirect_stdout

from .host import Host
from .output import Output
from .shell_startup import ShellStartup
from .storage import Storage


class GrokDomain:
    """Install and run the peer grok binary, and back up its auth files."""

    APP_NAME = "agent-cli"
    DEPOSIT = "/var/agent-cli"
    GLOBAL_BIN = "/usr/local/bin"
    VENDOR_BASE = "https://x.ai/cli"
    VENDOR_FALLBACK = "https://storage.googleapis.com/grok-build-public-artifacts/cli"
    CHANNEL = "stable"
    PROMPT_TIMEOUT = 14
    SESSION_WORDS = ("valid", "timeout", "invalid", "missing")

    def __init__(
        self,
        output=None,
        storage=None,
        host=None,
        session_override=None,
        deposit_root=None,
        environ=None,
        runner=None,
        grok_home=None,
        logger=None,
        version="",
    ):
        self.environ = os.environ if environ is None else environ
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="GrokDomain")
        self.output = output if output is not None else Output()
        self.storage = storage if storage is not None else Storage(
            app_name=self.APP_NAME, environ=self.environ
        )
        self.host = host if host is not None else Host(environ=self.environ)
        self.session_override = session_override
        self.deposit_root = deposit_root or self.environ.get("AGENT_CLI_DEPOSIT") or self.DEPOSIT
        self.runner = runner
        self.grok_home = grok_home
        self.startup = ShellStartup(
            version=version,
            output=self.output,
            environ=self.environ,
            logger=logger,
            host=self.host,
        )
        self._last_stdout = ""
        self._last_stderr = ""

    def global_bin(self) -> str:
        root = self.environ.get("AGENT_CLI_GLOBAL_BIN", self.GLOBAL_BIN)
        return os.path.join(root, self.APP_NAME)

    def invoking_home(self) -> str:
        sudo_user = self.environ.get("SUDO_USER", "")
        if hasattr(os, "geteuid") and os.geteuid() == 0 and sudo_user:
            try:
                import pwd
                return pwd.getpwnam(sudo_user).pw_dir
            except (ImportError, KeyError):
                pass
        return self.environ.get("HOME") or "/tmp"

    def auth_home(self) -> str:
        if self.grok_home:
            return self.grok_home
        if os.geteuid() == 0 and self.environ.get("SUDO_USER"):
            return os.path.join(self.invoking_home(), ".grok")
        return os.path.join(self.environ.get("HOME") or "/tmp", ".grok")

    def peer_path(self) -> str:
        override = self.environ.get("AGENT_CLI_GROK_BIN", "")
        if override:
            return override
        found = shutil.which("grok")
        if found:
            return found
        return os.path.join(self.auth_home(), "bin", "grok")

    def session_word(self) -> str:
        """valid, timeout, invalid, or missing. Timeout is not logged-out."""
        if self.session_override in self.SESSION_WORDS:
            return self.session_override
        forced = self.environ.get("AGENT_CLI_SESSION", "")
        if forced in self.SESSION_WORDS:
            return forced
        if self._uses_local_auth():
            return self._session_from_local_auth()
        return self._session_from_probe()

    def logged_in(self) -> bool:
        """A timeout is still treated as signed-in. Invalid and missing are not."""
        return self.session_word() in ("valid", "timeout")

    def _uses_local_auth(self) -> bool:
        """Termux and a host with proot read cookies. They do not run grok -p hello."""
        if self.host.is_termux():
            return True
        if self.host.override() in ("multiuser", "gitbash", "windows-cmd"):
            return False
        return shutil.which("proot", path=self.environ.get("PATH")) is not None

    def _session_from_local_auth(self) -> str:
        """Absent cookies are invalid. This path does not report missing or timeout."""
        path = os.path.join(self.auth_home(), "auth.json")
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            return "invalid"
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, ValueError):
            return "invalid"
        if self._cookies_still_good(data):
            return "valid"
        return "invalid"

    def _cookies_still_good(self, data) -> bool:
        if not isinstance(data, dict) or not data:
            return False
        if self._secret_still_good(data):
            return True
        for value in data.values():
            if isinstance(value, dict) and self._secret_still_good(value):
                return True
        return False

    def _secret_still_good(self, node) -> bool:
        refresh = node.get("refresh_token")
        if isinstance(refresh, str) and refresh:
            return True
        key = node.get("key")
        if not isinstance(key, str) or not key:
            return False
        expires = node.get("expires_at")
        if not expires:
            return True
        return self._expires_in_future(expires)

    def _expires_in_future(self, value) -> bool:
        text = str(value).replace("Z", "+00:00")
        try:
            stamp = datetime.datetime.fromisoformat(text)
        except ValueError:
            return False
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=datetime.timezone.utc)
        return stamp > datetime.datetime.now(datetime.timezone.utc)

    def _session_from_probe(self) -> str:
        peer = self.peer_path()
        if not peer or not os.path.isfile(peer) or not os.access(peer, os.X_OK):
            return "missing"
        if self.runner is not None:
            code = self.runner(["probe", peer])
            if code == 0:
                return "valid"
            if code in (124, 137):
                return "timeout"
            return "invalid"
        try:
            proc = subprocess.run(
                [peer, "-p", "hello"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.PROMPT_TIMEOUT,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return "timeout"
        except OSError:
            return "missing"
        if proc.returncode == 0:
            return "valid"
        if proc.returncode in (124, 137):
            return "timeout"
        return "invalid"

    def check_session(self) -> int:
        word = self.session_word()
        if word == "valid":
            if self._uses_local_auth():
                message = "Grok is logged in (local auth cookies)."
            else:
                message = "Grok is logged in (grok -p hello succeeded)."
            return self.output.ok("check-session", message, {"session": word})
        if word == "missing":
            return self.output.error(
                "Grok is not installed (no grok on PATH or under {0}/bin).".format(self.auth_home()),
                "agent-cli setup, then grok login, then agent-cli check-session",
            )
        if word == "timeout":
            return self.output.ok("check-session", "timeout", {"session": "timeout"})
        return self.output.error(
            "Grok is not logged in.",
            "grok login, then agent-cli check-session",
        )

    def backup(self) -> int:
        """Re-enter as root when this process is not root. Tests call _deposit."""
        if os.geteuid() != 0 and self.environ.get("AGENT_CLI_BACKUP_AS_ROOT") != "1":
            binary = self.global_bin()
            if self.environ.get("AGENT_CLI_BACKUP_NO_SUDO") == "1":
                return self._deposit()
            return self.output.error(
                "backup deposits auth files as root.",
                "sudo -n {0} backup".format(binary),
            )
        return self._deposit()

    def _deposit(self) -> int:
        source = self.auth_home()
        names = sorted(glob.glob(os.path.join(source, "auth.*")))
        if not names:
            return self.output.error(
                "No auth files under {0}.".format(source),
                "agent-cli setup",
            )
        try:
            os.makedirs(self.deposit_root, mode=0o755, exist_ok=True)
        except OSError as exc:
            return self.output.error(
                "Cannot create deposit {0}.".format(self.deposit_root),
                "sudo -n {0} backup".format(self.global_bin()),
            )
        copied = []
        for path in names:
            base = os.path.basename(path)
            dest = os.path.join(self.deposit_root, base)
            try:
                shutil.copy2(path, dest)
                os.chmod(dest, 0o644)
            except OSError:
                return self.output.error(
                    "Cannot write {0}.".format(dest),
                    "sudo -n {0} backup".format(self.global_bin()),
                )
            copied.append(base)
        return self.output.ok(
            "backup",
            "Deposited {0}.".format(", ".join(copied)),
            {"deposit": self.deposit_root, "files": copied},
        )

    def sync_auth(self) -> int:
        if self.logged_in():
            return self.output.ok(
                "sync-auth",
                "No sync-auth for logged-in environment.",
                {"reason": "logged-in"},
            )
        return self._copy_deposit_to_home()

    def _copy_deposit_to_home(self) -> int:
        names = sorted(glob.glob(os.path.join(self.deposit_root, "auth.*")))
        if not names:
            return self.output.error(
                "Deposit {0} has no auth files.".format(self.deposit_root),
                "agent-cli backup",
            )
        dest_root = self.auth_home()
        try:
            os.makedirs(dest_root, mode=0o700, exist_ok=True)
        except OSError:
            return self.output.error(
                "Cannot create {0}.".format(dest_root),
                "agent-cli sync-auth",
            )
        for path in names:
            dest = os.path.join(dest_root, os.path.basename(path))
            shutil.copy2(path, dest)
            if os.path.basename(path) == "auth.json":
                os.chmod(dest, 0o600)
        return self.output.ok("sync-auth", "Restored auth files into {0}.".format(dest_root))

    def _tool(self, env_keys, fallback: str) -> str:
        for key in env_keys:
            value = self.environ.get(key, "")
            if value:
                return value
        found = shutil.which(fallback)
        return found or ""

    def _spawn(self, argv) -> int:
        if self.runner is not None:
            code = self.runner(list(argv))
            return int(code) if isinstance(code, int) else (0 if code else 1)
        try:
            proc = subprocess.run(
                list(argv),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                check=False,
                universal_newlines=True,
            )
        except (OSError, subprocess.TimeoutExpired):
            return 1
        self._last_stdout = proc.stdout or ""
        self._last_stderr = proc.stderr or ""
        return int(proc.returncode)

    def parse_remote_spec(self, spec: str):
        """user@IPv4, IPv4, domain, or user@domain. None when the form is refused."""
        if not spec or spec.startswith("-"):
            return None
        if re.search(r"[;&|$`()<>\\/ \t*\[\]]", spec):
            return None
        if spec.count("@") > 1:
            return None
        user = ""
        host = spec
        if "@" in spec:
            user, host = spec.split("@", 1)
            if not user or not host:
                return None
            if not re.match(r"^[A-Za-z0-9_.-]+$", user):
                return None
            if not re.match(r"^[A-Za-z_0-9]", user):
                return None
        if self._host_is_ipv4(host) or self._host_is_dns(host):
            return user, host
        return None

    def _host_is_ipv4(self, host: str) -> bool:
        parts = host.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            number = int(part)
            if number < 0 or number > 255:
                return False
        return True

    def _host_is_dns(self, host: str) -> bool:
        if not host or host.startswith(".") or host.endswith(".") or ".." in host:
            return False
        if host.startswith("-") or host.endswith("-"):
            return False
        if re.search(r"[^A-Za-z0-9.-]", host):
            return False
        return bool(re.search(r"[A-Za-z]", host))

    def _preferred_remote_path(self) -> str:
        return os.path.join(self.storage.persistent_dir(), "preferred-remote")

    def preferred_remote_load(self) -> str:
        path = self._preferred_remote_path()
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read().strip()
        except OSError:
            return ""

    def preferred_remote_save(self, spec: str) -> None:
        folder = self.storage.resolve_persistent()
        path = os.path.join(folder, "preferred-remote")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(spec + "\n")
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass

    def _remote_root(self) -> str:
        return self.environ.get("AGENT_CLI_REMOTE_ROOT") or self.deposit_root

    def _remote_target(self, user: str, host: str) -> str:
        if user:
            return "{0}@{1}".format(user, host)
        return host

    def sync_from_remote(self, spec: str) -> int:
        if self.logged_in():
            return self.output.ok(
                "sync-auth-from-remote",
                "No sync-auth for logged-in environment.",
                {"reason": "logged-in"},
            )
        if not spec:
            spec = self.preferred_remote_load()
        parsed = self.parse_remote_spec(spec)
        if parsed is None:
            return self.output.error(
                "Cannot sync-auth-from-remote: remote '{0}' is not user@host, IPv4, domain, or user@domain.".format(spec),
                "agent-cli sync-auth-from-remote USER@HOST",
            )
        user, host = parsed
        scp = self._tool(("AGENT_CLI_SCP", "GROK_CLI_SCP"), "scp")
        if not scp or not os.access(scp, os.X_OK):
            return self.output.error(
                "Cannot sync-auth-from-remote: scp not found.",
                "install openssh-client, then agent-cli sync-auth-from-remote {0}".format(spec),
            )
        dest_root = self.auth_home()
        try:
            os.makedirs(dest_root, mode=0o700, exist_ok=True)
        except OSError:
            return self.output.error(
                "Cannot create {0}.".format(dest_root),
                "agent-cli sync-auth-from-remote {0}".format(spec),
            )
        label = self._remote_target(user, host)
        remote_root = self._remote_root()
        remote = "{0}:{1}/auth.json".format(label, remote_root)
        try:
            tmp = self.storage.mktemp("authjson")
        except OSError:
            return self.output.error(
                "Cannot create a scratch file for auth.json.",
                "agent-cli sync-auth-from-remote {0}".format(spec),
            )
        self.output.info("Fetching auth.json from {0}".format(label))
        code = self._spawn([
            scp, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", remote, tmp,
        ])
        if code != 0 or not os.path.isfile(tmp) or os.path.getsize(tmp) == 0:
            try:
                os.remove(tmp)
            except OSError:
                pass
            return self.output.error(
                "Cannot sync-auth-from-remote: scp from {0} failed.".format(label),
                "ssh {0}, then agent-cli sync-auth-from-remote {1}".format(label, spec),
            )
        dest = os.path.join(dest_root, "auth.json")
        shutil.copy2(tmp, dest)
        os.chmod(dest, 0o600)
        os.remove(tmp)
        copied = ["auth.json"]
        lock_remote = "{0}:{1}/auth.json.lock".format(label, remote_root)
        try:
            lock_tmp = self.storage.mktemp("authlock")
        except OSError:
            lock_tmp = ""
        if lock_tmp:
            if self._spawn([
                scp, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", lock_remote, lock_tmp,
            ]) == 0 and os.path.isfile(lock_tmp) and os.path.getsize(lock_tmp) > 0:
                lock_dest = os.path.join(dest_root, "auth.json.lock")
                shutil.copy2(lock_tmp, lock_dest)
                os.chmod(lock_dest, 0o600)
                copied.append("auth.json.lock")
            try:
                os.remove(lock_tmp)
            except OSError:
                pass
        try:
            self.preferred_remote_save(spec)
        except OSError:
            pass
        message = "sync-auth-from-remote complete: {0}:{1} → {2} ({3} file(s): {4})".format(
            label, remote_root, dest_root, len(copied), " ".join(copied),
        )
        return self.output.ok(
            "sync-auth-from-remote",
            message,
            {"remote": label, "files": copied, "count": len(copied)},
        )

    def sync_to_remote(self, spec: str) -> int:
        if not spec:
            spec = self.preferred_remote_load()
        parsed = self.parse_remote_spec(spec)
        if parsed is None:
            return self.output.error(
                "Cannot sync-auth-to-remote: remote '{0}' is not user@host, IPv4, domain, or user@domain.".format(spec),
                "agent-cli sync-auth-to-remote USER@HOST",
            )
        user, host = parsed
        source = self.auth_home()
        auth = os.path.join(source, "auth.json")
        if not os.path.isfile(auth) or os.path.islink(auth) or os.path.getsize(auth) == 0:
            return self.output.error(
                "Cannot sync-auth-to-remote: no auth.json under {0}.".format(source),
                "grok login, then agent-cli sync-auth-to-remote USER@HOST",
            )
        scp = self._tool(("AGENT_CLI_SCP", "GROK_CLI_SCP"), "scp")
        ssh = self._tool(("AGENT_CLI_SSH", "GROK_CLI_SSH"), "ssh")
        if not scp or not os.access(scp, os.X_OK):
            return self.output.error(
                "Cannot sync-auth-to-remote: scp not found.",
                "install openssh-client, then agent-cli sync-auth-to-remote {0}".format(spec),
            )
        if not ssh or not os.access(ssh, os.X_OK):
            return self.output.error(
                "Cannot sync-auth-to-remote: ssh not found.",
                "install openssh-client, then agent-cli sync-auth-to-remote {0}".format(spec),
            )
        target = self._remote_target(user, host)
        self.output.info("Sending auth.json to {0}".format(target))
        if self._spawn([
            ssh, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", target,
            "mkdir -p .grok && chmod 0700 .grok",
        ]) != 0:
            return self.output.error(
                "Cannot sync-auth-to-remote: cannot prepare ~/.grok on {0}.".format(target),
                "ssh {0}, then agent-cli sync-auth-to-remote {1}".format(target, spec),
            )
        if self._spawn([
            scp, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15",
            auth, "{0}:.grok/auth.json".format(target),
        ]) != 0:
            return self.output.error(
                "Cannot sync-auth-to-remote: scp to {0} failed.".format(target),
                "ssh {0}, then agent-cli sync-auth-to-remote {1}".format(target, spec),
            )
        if self._spawn([
            ssh, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", target,
            "chmod 0600 .grok/auth.json",
        ]) != 0:
            return self.output.error(
                "Cannot sync-auth-to-remote: cannot set mode 0600 on {0}:.grok/auth.json.".format(target),
                "ssh {0}, then agent-cli sync-auth-to-remote {1}".format(target, spec),
            )
        copied = ["auth.json"]
        lock = os.path.join(source, "auth.json.lock")
        if os.path.isfile(lock) and not os.path.islink(lock) and os.path.getsize(lock) > 0:
            if self._spawn([
                scp, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15",
                lock, "{0}:.grok/auth.json.lock".format(target),
            ]) == 0 and self._spawn([
                ssh, "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", target,
                "chmod 0600 .grok/auth.json.lock",
            ]) == 0:
                copied.append("auth.json.lock")
        try:
            self.preferred_remote_save(spec)
        except OSError:
            pass
        message = "sync-auth-to-remote complete: {0} → {1}:.grok ({2} file(s): {3})".format(
            source, target, len(copied), " ".join(copied),
        )
        return self.output.ok(
            "sync-auth-to-remote",
            message,
            {"remote": target, "files": copied, "count": len(copied)},
        )

    def detect_platform(self) -> str:
        forced = self.environ.get("AGENT_CLI_PLATFORM", "")
        if forced:
            return forced
        system = platform.system()
        if system == "Darwin":
            os_name = "macos"
        elif system == "Linux":
            os_name = "linux"
        elif system.startswith("MINGW") or system.startswith("MSYS") or system.startswith("CYGWIN"):
            os_name = "windows"
        else:
            return ""
        machine = platform.machine().lower()
        if machine in ("x86_64", "amd64"):
            arch = "x86_64"
        elif machine in ("arm64", "aarch64"):
            arch = "aarch64"
        else:
            return ""
        return "{0}-{1}".format(os_name, arch)

    def setup(self, force=False, interactive=False) -> int:
        """Point at the vendor channel, then the public fallback. Do not run a shell installer."""
        token = self.detect_platform()
        if not token:
            return self.output.error(
                "This host is not linux, macos, or windows on x86_64 or aarch64.",
                "agent-cli about",
            )
        peer = self.peer_path()
        installed = os.path.isfile(peer) and os.access(peer, os.X_OK)
        if installed and not force:
            if interactive:
                return self.output.ok(
                    "setup",
                    "grok is already installed. Choose keep, reinstall, or exit.",
                    {"choices": ["keep", "reinstall", "exit"], "peer": peer},
                )
            return self.output.ok(
                "setup",
                "grok is already installed at {0}.".format(peer),
                {"peer": peer, "skipped": True},
            )
        if shutil.which("curl") is None and self.runner is None:
            return self.output.error(
                "curl is required to download grok.",
                "Install curl, then agent-cli setup",
            )
        version = self._read_pointer(self.VENDOR_BASE) or self._read_pointer(self.VENDOR_FALLBACK)
        if not version:
            return self.output.error(
                "The grok version pointer could not be read.",
                "agent-cli setup --force",
            )
        dest_dir = os.path.join(self.auth_home(), "downloads")
        try:
            os.makedirs(dest_dir, mode=0o700, exist_ok=True)
        except OSError:
            return self.output.error(
                "Cannot create {0}.".format(dest_dir),
                "agent-cli setup",
            )
        artifact = "grok-{0}-{1}".format(version, token)
        saved = self._fetch_artifact(version, artifact, dest_dir)
        if not saved:
            return self.output.error(
                "The grok artifact could not be downloaded.",
                "agent-cli setup --force",
            )
        if not self._smoke(saved):
            return self.output.error(
                "The downloaded grok binary did not run.",
                "agent-cli setup --force",
            )
        bin_dir = os.path.join(self.auth_home(), "bin")
        os.makedirs(bin_dir, mode=0o700, exist_ok=True)
        vendor = os.path.join(dest_dir, "grok-{0}".format(token))
        if os.path.abspath(saved) != os.path.abspath(vendor):
            shutil.copy2(saved, vendor)
        os.chmod(vendor, 0o755)
        link = os.path.join(bin_dir, "grok")
        if self.host.is_termux() or self._is_android():
            if not self.write_exec_wrapper(link, vendor):
                return self.output.error(
                    "The Android grok wrapper could not be written.",
                    "agent-cli setup --force",
                )
        else:
            if os.path.lexists(link):
                os.remove(link)
            shutil.copy2(vendor, link)
            os.chmod(link, 0o755)
        return self.output.ok("setup", "Installed grok {0}.".format(version), {"peer": link})

    def _read_pointer(self, base: str) -> str:
        url = "{0}/{1}".format(base.rstrip("/"), self.CHANNEL)
        if self.runner is not None:
            text = self.runner(["pointer", url])
            if not isinstance(text, str) or not text.strip():
                return ""
            return text.splitlines()[0].strip()
        try:
            proc = subprocess.run(
                ["curl", "-fsSL", url],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=30,
                check=False,
                universal_newlines=True,
            )
        except (OSError, subprocess.TimeoutExpired):
            return ""
        if proc.returncode != 0 or not proc.stdout:
            return ""
        return proc.stdout.splitlines()[0].strip()

    def _fetch_artifact(self, version: str, artifact: str, dest_dir: str) -> str:
        for suffix in (".zst", ".gz", ""):
            name = artifact + suffix
            for base in (self.VENDOR_BASE, self.VENDOR_FALLBACK):
                url = "{0}/{1}/{2}".format(base.rstrip("/"), version, name)
                dest = os.path.join(dest_dir, name)
                if self.runner is not None:
                    body = self.runner(["fetch", url, dest])
                    if body:
                        return dest
                    continue
                try:
                    proc = subprocess.run(
                        ["curl", "-fsSL", "-o", dest, url],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=120,
                        check=False,
                    )
                except (OSError, subprocess.TimeoutExpired):
                    continue
                if proc.returncode == 0 and os.path.isfile(dest) and os.path.getsize(dest) > 0:
                    return dest
        return ""

    def _smoke(self, path: str) -> bool:
        if self.runner is not None:
            return bool(self.runner(["smoke", path]))
        try:
            proc = subprocess.run(
                [path, "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        return proc.returncode == 0

    def _is_android(self) -> bool:
        try:
            blob = " ".join(str(part) for part in platform.uname())
        except Exception:
            blob = platform.platform()
        return "Android" in blob

    def write_exec_wrapper(self, path: str, vendor: str, resolv: str = "") -> bool:
        """Write bin/grok. Does not edit the vendor file.

        The wrapper unsets LD_PRELOAD, sets TERMUX_EXEC_OPTOUT, binds a no-op
        over start-services.sh, and uses proot --kill-on-exit plus the
        proot-exit-reaper when grok is started with -p.
        """
        if not path or not vendor:
            return False
        quoted = "'" + vendor.replace("'", "'\\''") + "'"
        bind = ""
        if resolv:
            quoted_resolv = "'" + resolv.replace("'", "'\\''") + "'"
            bind = "-b {0}:/etc/resolv.conf ".format(quoted_resolv)
        body = """#!/bin/sh
unset LD_PRELOAD
TERMUX_EXEC_OPTOUT=1
export TERMUX_EXEC_OPTOUT
_g={quoted}
_p=$(command -v proot 2>/dev/null || true)
if [ -z "${{_p}}" ]; then
  printf '%s\\n' "proot is not on PATH, so grok cannot run on this Android host. Next: pkg install proot" >&2
  exit 127
fi
_k=""
if command -v grep >/dev/null 2>&1; then
  if "${{_p}}" --help 2>&1 | grep -q kill-on-exit; then
    _k="--kill-on-exit"
  fi
fi
_svc=""
if [ -n "${{PREFIX:-}}" ] && [ -f "${{PREFIX}}/etc/profile.d/start-services.sh" ]; then
  _svc="-b /dev/null:${{PREFIX}}/etc/profile.d/start-services.sh"
fi
_pflag=0
_nau=""
for _a in "$@"; do
  case "${{_a}}" in
    -p|--single|--prompt-file|--prompt-json) _pflag=1 ;;
    --no-auto-update) _nau="have" ;;
  esac
done
if [ "${{_pflag}}" -eq 1 ] && [ "${{_nau}}" != "have" ]; then
  _nau="--no-auto-update"
else
  _nau=""
fi
if [ "${{_pflag}}" -eq 1 ]; then
  # grok-cli proot-exit-reaper
  # grok-linux _exit()s; leftover runsvdir (bash -lc → start-services.sh)
  # stay PRoot tracees. Match args/exe, not truncated comm. Reap NEW only.
  _tmp="${{TMPDIR:-${{TMP:-/tmp}}}}"
  _out=$(mktemp "${{_tmp}}/grok-p-out.XXXXXX") || exit 1
  _err=$(mktemp "${{_tmp}}/grok-p-err.XXXXXX") || exit 1
  _before=$(mktemp "${{_tmp}}/grok-p-rsv.XXXXXX") || exit 1
  ps -eo pid= -o args= 2>/dev/null | awk '
    $2 ~ /\\/runsvdir$/ || $2 == "runsvdir" {{ print $1 }}
  ' | sort >"${{_before}}" 2>/dev/null || :
  trap '
    if [ -n "${{_pid:-}}" ]; then
      kill -TERM "${{_pid}}" 2>/dev/null || true
      sleep 1
      kill -KILL "${{_pid}}" 2>/dev/null || true
    fi
    rm -f "${{_out}}" "${{_err}}" "${{_before}}"
    exit 130
  ' INT TERM TSTP
  "${{_p}}" ${{_k}} ${{_svc}} {bind}"${{_g}}" ${{_nau}} "$@" >"${{_out}}" 2>"${{_err}}" &
  _pid=$!
  (
    trap '' TSTP INT
    _seen=0
    _osize=0
    _idle_since=0
    _start=$(date +%s)
    while :; do
      _now=$(date +%s)
      if [ $((_now - _start)) -ge 180 ]; then
        break
      fi
      if ! kill -0 "${{_pid}}" 2>/dev/null; then
        exit 0
      fi
      _child=$(ps -eo pid= -o ppid= -o args= 2>/dev/null | awk -v col="${{_pid}}" '
        {{
          pid=$1; ppid=$2; arg=$3
          p[pid]=ppid
          a[pid]=arg
        }}
        END {{
          for (i in a) {{
            if (a[i] !~ /grok-linux/) continue
            c=i
            for (n=0; n<32; n++) {{
              if (c == col) {{ print i; exit }}
              if (!(c in p)) break
              if (p[c] == c || p[c] + 0 == 0) break
              c=p[c]
            }}
          }}
        }}
      ')
      if [ -n "${{_child}}" ]; then
        _seen=1
      elif [ "${{_seen}}" -eq 1 ]; then
        break
      fi
      _sz=$(wc -c <"${{_out}}" 2>/dev/null | tr -d ' \\t\\n')
      _sz=${{_sz:-0}}
      if [ "${{_sz}}" -gt 0 ]; then
        if [ "${{_sz}}" -ne "${{_osize}}" ]; then
          _osize=${{_sz}}
          _idle_since=${{_now}}
        elif [ "${{_idle_since}}" -gt 0 ] && [ $((_now - _idle_since)) -ge 1 ]; then
          break
        fi
      fi
      sleep 1
    done
    ps -eo pid= -o args= 2>/dev/null | awk '
      $2 ~ /\\/runsvdir$/ || $2 == "runsvdir" {{ print $1 }}
    ' | sort | while read -r _rpid; do
      [ -n "${{_rpid}}" ] || continue
      if ! grep -qx "${{_rpid}}" "${{_before}}" 2>/dev/null; then
        kill "${{_rpid}}" 2>/dev/null || :
      fi
    done
    kill "${{_pid}}" 2>/dev/null || :
    kill -KILL "${{_pid}}" 2>/dev/null || :
    exit 0
  ) &
  _reaper=$!
  wait "${{_reaper}}" 2>/dev/null || :
  wait "${{_pid}}" 2>/dev/null || :
  trap - INT TERM TSTP
  if [ -s "${{_err}}" ]; then
    cat "${{_err}}" >&2
  fi
  if [ -s "${{_out}}" ]; then
    cat "${{_out}}"
    rm -f "${{_out}}" "${{_err}}" "${{_before}}"
    exit 0
  fi
  rm -f "${{_out}}" "${{_err}}" "${{_before}}"
  exit 1
fi
exec "${{_p}}" ${{_k}} ${{_svc}} {bind}"${{_g}}" "$@"
""".format(quoted=quoted, bind=bind)
        try:
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, mode=0o700, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(body)
            os.chmod(path, 0o755)
        except OSError:
            return False
        return os.path.isfile(path) and os.path.getsize(path) > 0

    def update_grok(self) -> int:
        peer = self.peer_path()
        if not peer or not os.path.isfile(peer) or not os.access(peer, os.X_OK):
            return self.output.error(
                "grok is not installed, so agent-cli cannot update it.",
                "agent-cli setup",
            )
        return self.setup(force=True, interactive=False)

    def reinstall(self) -> int:
        peer = self.peer_path()
        link = os.path.join(self.auth_home(), "bin", "grok")
        for path in (peer, link):
            if path and os.path.lexists(path) and not os.path.basename(path).startswith("auth."):
                try:
                    os.remove(path)
                except OSError:
                    return self.output.error(
                        "Cannot remove {0}.".format(path),
                        "agent-cli reinstall",
                    )
        return self.setup(force=True, interactive=False)

    def run(self, args=None) -> int:
        if self.output.json_mode:
            return self.output.error(
                "run starts grok in the terminal, so --json cannot be used.",
                "agent-cli run",
            )
        peer = self.peer_path()
        if not peer or not os.path.isfile(peer) or not os.access(peer, os.X_OK):
            return self.output.error(
                "grok is not installed, so agent-cli cannot start it.",
                "agent-cli setup",
            )
        extra = list(args or [])
        if "--no-auto-update" in extra:
            argv = [peer] + extra
        else:
            argv = [peer, "--no-auto-update"] + extra
        if self.runner is not None:
            code = self.runner(argv)
            return int(code) if isinstance(code, int) else 0
        try:
            proc = subprocess.run(argv, check=False)
        except OSError:
            return self.output.error(
                "Could not start grok at {0}.".format(peer),
                "agent-cli setup",
            )
        return int(proc.returncode)

    def crontab_lines(self) -> tuple:
        binary = self.global_bin()
        backup = self.environ.get(
            "AGENT_CLI_CRON_BACKUP",
            "*/30 * * * * sudo {0} backup".format(binary),
        )
        sync = self.environ.get(
            "AGENT_CLI_CRON_SYNC",
            "45 * * * * {0} sync-auth".format(binary),
        )
        return backup, sync

    def _grant_present(self) -> bool:
        if self.environ.get("AGENT_CLI_SUDO_GRANT") == "1":
            return True
        user = self.environ.get("USER") or self.environ.get("USERNAME") or "unknown"
        path = self.environ.get("AGENT_CLI_SUDOERS_FILE") or os.path.join(
            "/etc/sudoers.d", "{0}-{1}".format(self.APP_NAME, user)
        )
        needle = "NOPASSWD: {0} backup".format(self.global_bin())
        try:
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            return False
        return needle in text

    def add_crontab(self) -> int:
        binary = self.global_bin()
        user = self.environ.get("USER") or self.environ.get("USERNAME") or "unknown"
        if not os.path.isfile(binary) or not os.access(binary, os.X_OK):
            if self.environ.get("AGENT_CLI_ASSUME_BIN") != "1":
                return self.output.error(
                    "Cannot add crontab: need the global binary {0}.".format(binary),
                    "pip install AgentCli, then agent-cli add-crontab",
                )
        if not self._grant_present():
            return self.output.error(
                "Cannot add crontab: no passwordless sudo {0} backup grant for this login ({1}).".format(binary, user),
                "agent-cli generate-sudoer-request",
            )
        cron = self._tool(("AGENT_CLI_CRONTAB", "GROK_CLI_CRONTAB"), "crontab")
        if not cron or not os.access(cron, os.X_OK):
            return self.output.error(
                "Cannot add crontab: crontab command not found.",
                "install cron, then agent-cli add-crontab",
            )
        backup, sync = self.crontab_lines()
        listed = ""
        if self.runner is not None:
            loaded = self.runner(["crontab-list", cron])
            listed = loaded if isinstance(loaded, str) else ""
        else:
            try:
                proc = subprocess.run(
                    [cron, "-l"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    timeout=15,
                    check=False,
                    universal_newlines=True,
                )
                if proc.returncode == 0:
                    listed = proc.stdout or ""
            except (OSError, subprocess.TimeoutExpired):
                listed = ""
        if listed.startswith("no crontab"):
            listed = ""
        have_backup = binary + " backup" in listed or "sudo {0} backup".format(binary) in listed
        have_sync = binary + " sync-auth" in listed
        if have_backup and have_sync:
            return self.output.ok(
                "add-crontab",
                "add-crontab: backup and sync-auth jobs already present for {0}".format(user),
                {"already_present": True, "backup": backup, "sync": sync},
            )
        lines = [line for line in listed.splitlines() if line.strip()]
        if not have_backup:
            lines.append(backup)
        if not have_sync:
            lines.append(sync)
        try:
            tmp = self.storage.mktemp("crontab")
        except OSError:
            return self.output.error(
                "Cannot add crontab: scratch file failed.",
                "agent-cli add-crontab",
            )
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
        if self.runner is not None:
            code = self.runner(["crontab-install", cron, tmp])
            code = int(code) if isinstance(code, int) else 0
        else:
            try:
                proc = subprocess.run([cron, tmp], check=False, timeout=15)
                code = int(proc.returncode)
            except (OSError, subprocess.TimeoutExpired):
                code = 1
        try:
            os.remove(tmp)
        except OSError:
            pass
        if code != 0:
            return self.output.error(
                "Cannot add crontab: crontab install failed.",
                "check crontab -l, then agent-cli add-crontab",
            )
        return self.output.ok(
            "add-crontab",
            "add-crontab complete for {0}: backup every 30 minutes; sync-auth at minute 45".format(user),
            {"backup": backup, "sync": sync, "already_present": False},
        )

    def sudoer_document(self, action="add", username=None) -> dict:
        user = username or self.environ.get("USER") or self.environ.get("USERNAME") or "unknown"
        if action not in ("add", "update"):
            action = "add"
        purpose = "Allow {0} to run {1} backup as root.".format(user, self.APP_NAME)
        return {
            "schema_version": 1,
            "purpose": purpose,
            "username": user,
            "service": self.APP_NAME,
            "action": action,
            "commands": [
                {
                    "runas": "root",
                    "tags": ["NOPASSWD"],
                    "path": self.global_bin(),
                    "args": ["backup"],
                }
            ],
        }

    def sudoer_text(self, username=None) -> str:
        doc = self.sudoer_document(username=username)
        return "\n".join([
            "# Purpose: {0}".format(doc["purpose"]),
            "{0} ALL=(root) NOPASSWD: {1} backup".format(doc["username"], doc["commands"][0]["path"]),
            "",
        ])

    def print_sudoers(self) -> int:
        text = self.sudoer_text()
        if self.output.json_mode:
            return self.output.ok("print-sudoers", text.strip())
        print(text, end="")
        return 0

    def _login_user(self) -> str:
        return self.environ.get("USER") or self.environ.get("USERNAME") or "unknown"

    def _sudoers_d(self) -> str:
        return self.environ.get("AGENT_CLI_SUDOERS_D") or "/etc/sudoers.d"

    def _installed_sudoers_path(self) -> str:
        return os.path.join(self._sudoers_d(), "{0}-{1}".format(self.APP_NAME, self._login_user()))

    def _config_dir(self) -> str:
        return os.path.join(self.environ.get("HOME") or "/tmp", ".config", self.APP_NAME)

    def _draft_path(self) -> str:
        return os.path.join(self._config_dir(), "sudoers.fragment-{0}".format(self._login_user()))

    def _list_drafts(self):
        folder = self._config_dir()
        found = []
        legacy = os.path.join(folder, "sudoers.fragment")
        if os.path.isfile(legacy) and not os.path.islink(legacy):
            found.append(legacy)
        if os.path.isdir(folder):
            for name in sorted(os.listdir(folder)):
                if not name.startswith("sudoers.fragment-") or name.endswith(".json"):
                    continue
                path = os.path.join(folder, name)
                if os.path.isfile(path) and not os.path.islink(path):
                    found.append(path)
        return found

    def _grant_allows_backup(self, path: str) -> bool:
        """The grant may name backup only. Extra arguments are refused."""
        try:
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            return False
        stripped = text.lstrip()
        if stripped.startswith("{"):
            try:
                data = json.loads(text)
            except ValueError:
                return False
            commands = data.get("commands") if isinstance(data, dict) else None
            if not isinstance(commands, list) or not commands:
                return False
            for command in commands:
                if not isinstance(command, dict):
                    return False
                args = command.get("args")
                target = str(command.get("path") or "")
                if args != ["backup"]:
                    return False
                if not target.endswith("/" + self.APP_NAME) and target != self.APP_NAME:
                    return False
            return True
        lines = [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
        if len(lines) != 1:
            return False
        return lines[0].endswith(" NOPASSWD: {0} backup".format(self.global_bin())) or lines[0].endswith(
            " NOPASSWD: {0} backup".format(self.APP_NAME)
        )

    def _request_id(self, text: str) -> str:
        match = re.search(r'"request_id"\s*:\s*"([^"]+)"', text or "")
        if match:
            return match.group(1)
        match = re.search(r"request_id=(\S+)", text or "")
        return match.group(1) if match else ""

    def _admin_script_text(self, user, draft, installed, legacy, deposit) -> str:
        """Admin handoff. This process does not run the script and does not write /etc."""
        return """#!/bin/sh
# {app} admin sudoers install / uninstall script
# Generated by: {app} print-sudoers-install-script
# Draft: {draft}
# Installed path: {installed}
# RUN AS ROOT: sudo sh "$0" install|uninstall|replace|status
set -u
APP_NAME="{app}"
PROJECT_SUDOERS_FILE="{draft}"
INSTALLED_SUDOERS="{installed}"
LEGACY_INSTALLED_SUDOERS="{legacy}"
DEPOSIT_DIR="{deposit}"
GEN_USER="{user}"
die() {{ printf '%s\\n' "ERROR: $*" >&2; exit 1; }}
info() {{ printf '%s\\n' "$*"; }}
require_root() {{
    if [ "$(id -u 2>/dev/null || echo 1)" -ne 0 ]; then
        die "Must run as root (e.g. sudo sh $0 install)."
    fi
}}
cmd_install() {{
    require_root
    [ -f "$PROJECT_SUDOERS_FILE" ] || die "Missing project sudoers file: $PROJECT_SUDOERS_FILE"
    if command -v visudo >/dev/null 2>&1; then
        visudo -c -f "$PROJECT_SUDOERS_FILE" || die "visudo -c failed on draft"
    fi
    install -m 0440 -o root -g root "$PROJECT_SUDOERS_FILE" "$INSTALLED_SUDOERS" \\
        || die "install to $INSTALLED_SUDOERS failed"
    if command -v visudo >/dev/null 2>&1; then
        visudo -c -f "$INSTALLED_SUDOERS" || die "visudo -c failed on installed file"
    fi
    mkdir -p "$DEPOSIT_DIR" 2>/dev/null || true
    chmod 0755 "$DEPOSIT_DIR" 2>/dev/null || true
    info "OK: installed $INSTALLED_SUDOERS (mode 0440) from $PROJECT_SUDOERS_FILE"
}}
cmd_uninstall() {{
    require_root
    if [ ! -e "$INSTALLED_SUDOERS" ]; then
        info "OK: $INSTALLED_SUDOERS already absent"
    else
        rm -f "$INSTALLED_SUDOERS" || die "Failed to remove $INSTALLED_SUDOERS"
        info "OK: removed $INSTALLED_SUDOERS"
    fi
    info "Note: does not remove {app} binaries or auth files"
}}
cmd_replace() {{
    cmd_uninstall
    cmd_install
}}
cmd_status() {{
    if [ -f "$INSTALLED_SUDOERS" ]; then
        info "installed: $INSTALLED_SUDOERS"
    else
        info "installed: (absent) $INSTALLED_SUDOERS"
    fi
    if [ -f "$PROJECT_SUDOERS_FILE" ]; then
        info "draft: $PROJECT_SUDOERS_FILE"
    else
        info "draft: (absent) $PROJECT_SUDOERS_FILE"
    fi
    if [ -e "$LEGACY_INSTALLED_SUDOERS" ] && [ "$LEGACY_INSTALLED_SUDOERS" != "$INSTALLED_SUDOERS" ]; then
        info "legacy_installed: $LEGACY_INSTALLED_SUDOERS"
    fi
    info "generated_for_user=$GEN_USER"
}}
usage() {{
    printf '%s\\n' "Usage: sudo sh $0 {{install|uninstall|replace|status}}"
}}
action="${{1:-}}"
case "$action" in
    install) cmd_install ;;
    uninstall) cmd_uninstall ;;
    replace) cmd_replace ;;
    status) cmd_status ;;
    -h|--help|help|"") usage; [ -n "$action" ] || exit 1 ;;
    *) die "Unknown action: $action" ;;
esac
exit 0
""".format(
            app=self.APP_NAME,
            user=user,
            draft=draft,
            installed=installed,
            legacy=legacy,
            deposit=deposit,
        )

    def print_sudoers_install_script(self, script_out="") -> int:
        """Write the user draft and an admin script. Do not write /etc."""
        if script_out.startswith("/etc"):
            return self.output.error(
                "Refusing to write admin script under /etc (Type 0).",
                "agent-cli print-sudoers-install-script",
            )
        user = self._login_user()
        draft = self._draft_path()
        try:
            os.makedirs(self._config_dir(), mode=0o700, exist_ok=True)
            with open(draft, "w", encoding="utf-8") as handle:
                handle.write(self.sudoer_text(username=user))
            os.chmod(draft, 0o600)
        except OSError:
            return self.output.error(
                "Cannot write the project sudoers draft.",
                "agent-cli print-sudoers",
            )
        if not script_out:
            try:
                script_out = self.storage.mktemp("sudoers-admin")
            except OSError:
                return self.output.error(
                    "Cannot create the admin script.",
                    "agent-cli print-sudoers-install-script",
                )
        else:
            parent = os.path.dirname(os.path.abspath(script_out)) or "."
            try:
                os.makedirs(parent, mode=0o700, exist_ok=True)
            except OSError:
                return self.output.error(
                    "Cannot create {0}.".format(parent),
                    "agent-cli print-sudoers-install-script",
                )
        installed = self._installed_sudoers_path()
        legacy = os.path.join(self._sudoers_d(), self.APP_NAME)
        body = self._admin_script_text(user, draft, installed, legacy, self.deposit_root)
        try:
            with open(script_out, "w", encoding="utf-8") as handle:
                handle.write(body)
            os.chmod(script_out, 0o750)
        except OSError:
            return self.output.error(
                "Cannot write {0}.".format(script_out),
                "agent-cli print-sudoers-install-script",
            )
        message = (
            "Wrote admin sudoers script: {0}\n"
            "Project sudoers file (draft): {1}\n"
            "Installed path (admin only, per-user): {2}\n"
            "sudo sh {0} install\n"
            "sudo sh {0} uninstall\n"
            "sudo sh {0} replace\n"
            "sudo sh {0} status"
        ).format(script_out, draft, installed)
        return self.output.ok(
            "print-sudoers-install-script",
            message,
            {"script_path": script_out, "project_sudoers_file": draft, "installed_path": installed, "user": user},
        )

    def generate_sudoer_request(self, directory=None, action="add") -> int:
        doc = self.sudoer_document(action=action)
        folder = directory or os.getcwd()
        stamp = datetime.date.today().strftime("%Y%m%d")
        number = 1
        while True:
            base = "sudoer-{0}-{1}-{2}-{3}-{4}.json".format(
                stamp, self.APP_NAME, doc["username"], doc["action"], number
            )
            path = os.path.join(folder, base)
            if not os.path.exists(path):
                break
            number += 1
        try:
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(doc, handle, indent=2)
                handle.write("\n")
        except OSError:
            return self.output.error(
                "Cannot write the sudoer request.",
                "agent-cli generate-sudoer-request",
            )
        return self.output.ok("generate-sudoer-request", path, {"path": path})

    def submit_sudoer_request(self, path="") -> int:
        """Queue a backup-only grant. This command does not write /etc."""
        user = self._login_user()
        cli = self._tool(("AGENT_CLI_SUDOER_CLI", "SUDOER_CLI"), "sudoer-cli")
        if not cli or not os.path.isfile(cli) or not os.access(cli, os.X_OK):
            return self.output.error(
                "sudoer-cli not found (set SUDOER_CLI or install sudoer-cli). Submit does not write /etc.",
                "agent-cli print-sudoers-install-script",
            )
        inbound = self.environ.get("AGENT_CLI_SUDOER_INBOUND") or self.environ.get("SUDOER_QUEUE_INBOUND") or ""
        if not inbound:
            preferred = "/var/sudoer-cli/sudoer-request"
            if os.path.isdir(preferred):
                inbound = preferred
        if not inbound or not os.path.isdir(inbound):
            return self.output.error(
                "sudoer inbound queue not found (preferred /var/sudoer-cli/sudoer-request).",
                "Ask an admin to run: sudo sudoer-cli setup",
            )
        if not os.access(inbound, os.W_OK):
            return self.output.error(
                "sudoer inbound not writable: {0}.".format(inbound),
                "Check mode 3773 on public inbound.",
            )
        host_path = self._installed_sudoers_path()
        host_present = os.path.isfile(host_path)
        action = self.environ.get("AGENT_CLI_SUBMIT_ACTION") or ("update" if host_present else "add")
        if action not in ("add", "update"):
            return self.output.error(
                "submit-sudoer-request action must be add or update (got {0}).".format(action),
                "agent-cli submit-sudoer-request",
            )
        cleanup = False
        source = path
        if source:
            if os.path.islink(source):
                return self.output.error(
                    "refusing symlink sudoers input: {0}".format(source),
                    "agent-cli generate-sudoer-request",
                )
            if not os.path.isfile(source):
                return self.output.error(
                    "sudoers file not found: {0}".format(source),
                    "agent-cli generate-sudoer-request",
                )
        else:
            try:
                source = self.storage.mktemp("sudoer-json")
            except OSError:
                return self.output.error(
                    "Cannot write temp sudoer JSON.",
                    "agent-cli generate-sudoer-request",
                )
            cleanup = True
            document = self.sudoer_document(action=action, username=user)
            try:
                with open(source, "w", encoding="utf-8") as handle:
                    json.dump(document, handle)
                    handle.write("\n")
            except OSError:
                return self.output.error(
                    "Cannot write temp sudoer JSON.",
                    "agent-cli generate-sudoer-request",
                )
        if not self._grant_allows_backup(source):
            if cleanup:
                try:
                    os.remove(source)
                except OSError:
                    pass
            return self.output.error(
                "Queued sudo request is incomplete: it does not allow backup.",
                "agent-cli generate-sudoer-request && agent-cli submit-sudoer-request <path>",
            )
        verb = "update-sudoer-request" if action == "update" else "add-sudoer-request"
        purpose = "Allow {0} to run {1} backup as root.".format(user, self.APP_NAME)
        argv = [cli, verb, "--file", source, "--purpose", purpose, "--service", self.APP_NAME]
        if self.output.json_mode:
            argv.insert(1, "--json")
        code = self._spawn(argv)
        stdout = self._last_stdout
        stderr = self._last_stderr
        if cleanup:
            try:
                os.remove(source)
            except OSError:
                pass
        if code != 0:
            detail = (stderr or stdout or "exit {0}".format(code)).strip()
            return self.output.error(
                "sudoer-cli {0} failed: {1}".format(verb, detail),
                "agent-cli generate-sudoer-request",
            )
        request_id = self._request_id(stdout)
        if request_id:
            queued = os.path.join(inbound, request_id)
            if os.path.isfile(queued) and not self._grant_allows_backup(queued):
                return self.output.error(
                    "Queued sudo request is incomplete: it does not allow backup. Do not approve {0}.".format(
                        request_id
                    ),
                    "agent-cli generate-sudoer-request && agent-cli submit-sudoer-request <path>",
                )
        message = "Submitted {0} request via {1}".format(action, cli)
        if request_id:
            message = "{0}\nrequest_id={1}".format(message, request_id)
        if host_present:
            message = "{0}\nhost_fragment={1}".format(message, host_path)
        message = (
            "{0}\ninbound={1}\nThis CLI did not write /etc. Approver must approve the request."
        ).format(message, inbound)
        return self.output.ok(
            "submit-sudoer-request",
            message,
            {
                "request_id": request_id,
                "action": action,
                "inbound": inbound,
                "host_fragment_present": host_present,
            },
        )

    def remove_project_sudoers(self, path="", force=False) -> int:
        """Delete the user draft only. Never delete a file under /etc."""
        if path == "/etc" or path.startswith("/etc/"):
            return self.output.error(
                "Refusing to remove paths under /etc as Type 0. This command only deletes the user draft.",
                "agent-cli print-sudoers-install-script",
            )
        drafts = self._list_drafts()
        if not path:
            if len(drafts) > 1:
                return self.output.error(
                    "remove-project-sudoers: multiple drafts present; specify path argument (non-interactive).\n{0}".format(
                        "\n".join(drafts)
                    ),
                    "agent-cli remove-project-sudoers --force <path>",
                )
            path = drafts[0] if drafts else self._draft_path()
        installed = self._installed_sudoers_path()
        if not os.path.lexists(path):
            message = "Project sudoers draft not present (nothing to remove): {0}".format(path)
            if os.path.isfile(installed):
                message += "\nHost elevation STILL ACTIVE (separate from draft): {0}".format(installed)
            return self.output.ok(
                "remove-project-sudoers",
                message,
                {"path": path, "status": "already_absent", "installed_path": installed},
            )
        if not force:
            return self.output.error(
                "remove-project-sudoers requires confirmation.",
                "agent-cli remove-project-sudoers --force",
            )
        try:
            os.remove(path)
        except OSError:
            return self.output.error(
                "Failed to remove {0}".format(path),
                "agent-cli remove-project-sudoers --force {0}".format(path),
            )
        message = "Removed project-sudoers-file draft: {0}".format(path)
        if os.path.isfile(installed):
            message += "\nHost elevation STILL ACTIVE (separate from draft): {0}".format(installed)
            message += "\nremove-project-sudoers only deletes the user draft."
        return self.output.ok(
            "remove-project-sudoers",
            message,
            {"path": path, "status": "removed", "installed_path": installed},
        )

    def install_startup(self) -> int:
        """User-bin companion. Writes this login's startup files. Does not call pip."""
        self.startup.path_add_shell()
        return 0

    def uninstall_startup(self, force=False) -> int:
        """Strip this product's stickers when --force is set. Does not delete the files."""
        if not force:
            return self.output.error(
                "uninstall edits this login's startup-file stickers.",
                "agent-cli uninstall --force",
            )
        self.startup.cleanup_path()
        return self.output.ok(
            "uninstall",
            "Removed this product's startup-file stickers. Type: agent-cli self-uninstall --force",
        )

    def rc_test(self, root, file_name="bashrc", case="create", feature="") -> int:
        """Fixture writer. Does not call install or setup."""
        return self.startup.path_rc_test(root, file_name or "bashrc", case or "create", feature)

    def where_is_me(self) -> int:
        binary = self.global_bin()
        peer = self.peer_path()
        message = "agent-cli: {0}\ngrok: {1}".format(binary, peer)
        return self.output.ok("where-is-me", message, {"agent_cli": binary, "grok": peer})

    def menu_text(self, kind: str) -> str:
        """Result page for a menu row. Remote and setup choices stay on the terminal."""
        if kind in ("sync-auth-from-remote", "sync-auth-to-remote"):
            return "Type: agent-cli {0} user@host".format(kind)
        if kind == "setup":
            peer = self.peer_path()
            if os.path.isfile(peer):
                return "grok is already installed. Choose keep, reinstall, or exit.\nType: agent-cli setup"
            return "Type: agent-cli setup"
        if kind == "run":
            return "Type: agent-cli run"
        if kind == "backup":
            return "Type: sudo -n agent-cli backup"
        if kind == "add-crontab":
            backup, sync = self.crontab_lines()
            return "{0}\n{1}".format(backup, sync)
        if kind in ("version-check", "self-update", "self-uninstall", "self-install"):
            return kind
        if kind == "where-is-me":
            return "agent-cli: {0}\ngrok: {1}".format(self.global_bin(), self.peer_path())
        if kind == "check-session":
            return self.session_word()
        if kind == "reinstall":
            return "Type: agent-cli reinstall"
        if kind == "update-grok":
            return "Type: agent-cli update-grok"
        return "Type: agent-cli {0}".format(kind)

    def captured(self, verb: str, args=None, force=False) -> str:
        """Run one verb and return the lines the menu result page shows."""
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = self.dispatch(verb, args, force=force)
        parts = []
        if out.getvalue().strip():
            parts.append(out.getvalue().strip())
        if err.getvalue().strip():
            parts.append(err.getvalue().strip())
        text = "\n".join(parts).strip()
        if text:
            return text
        return "ok" if code == 0 else "failed"

    def dispatch(self, verb: str, args=None, force=False) -> int:
        args = list(args or [])
        if verb == "check-session":
            return self.check_session()
        if verb == "backup":
            return self.backup()
        if verb == "sync-auth":
            return self.sync_auth()
        if verb == "sync-auth-from-remote":
            return self.sync_from_remote(args[0] if args else "")
        if verb == "sync-auth-to-remote":
            return self.sync_to_remote(args[0] if args else "")
        if verb == "setup":
            return self.setup(force=force, interactive=False)
        if verb == "update-grok":
            return self.update_grok()
        if verb == "reinstall":
            return self.reinstall()
        if verb == "run":
            return self.run(args)
        if verb == "add-crontab":
            return self.add_crontab()
        if verb == "print-sudoers":
            return self.print_sudoers()
        if verb == "print-sudoers-install-script":
            return self.print_sudoers_install_script(args[0] if args else "")
        if verb == "remove-project-sudoers":
            return self.remove_project_sudoers(args[0] if args else "", force=force)
        if verb == "generate-sudoer-request":
            return self.generate_sudoer_request()
        if verb == "submit-sudoer-request":
            return self.submit_sudoer_request(args[0] if args else "")
        if verb == "where-is-me":
            return self.where_is_me()
        if verb == "ensure":
            return self.output.ok(verb, "Type: agent-cli self-install")
        if verb == "install":
            return self.install_startup()
        if verb == "uninstall":
            return self.uninstall_startup(force=force)
        if verb == "rc-test":
            return self.output.error(
                "rc-test requires --root a tmp/cache folder.",
                'agent-cli rc-test --root "$tmpdir" --file zprofile --case create',
            )
        return self.output.error(
            "Unknown verb '{0}'.".format(verb),
            "agent-cli help",
        )
