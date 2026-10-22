# =============================================================================
# Shell startup files: shared USER_BIN line and the missing-file matrix.
# requirement-shell-startup-files — .zprofile, ZPROFILE, rc-test --file zprofile.
# requirement-shell-zshenv — .zshenv. requirement-shell-path-and-shell-support — bash, fish, profile.
# requirement-shell-alpine — ash PATH on .profile.
# requirement-python-oop — class ShellStartup. No module-level helpers.
# This class writes this login's notes only. It does not delete the files.
# =============================================================================
from __future__ import annotations

import os
import shutil
import sys
import tempfile

from .host import Host


class ShellStartup:
    """Create or append this login's shell startup files. One class, one module.

    A missing .zprofile is created only when the shell basename is zsh or
    ZPROFILE is set. A set ZSHENV is not that permission. An existing body
    is appended, never replaced. .zshrc is not a PATH file.
    """

    APP_NAME = "agent-cli"

    def __init__(self, version="", output=None, environ=None, logger=None, host=None, euid=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="ShellStartup")
        if version:
            self.version = version
        else:
            from . import __version__

            self.version = __version__
        self.output = output
        self.environ = os.environ if environ is None else environ
        self.host = host if host is not None else Host(environ=self.environ)
        self.euid = euid

    def _json(self) -> bool:
        return bool(self.output is not None and self.output.json_mode)

    def _plain(self, text: str) -> None:
        if self._json():
            return
        print(text)

    def _warn(self, text: str) -> None:
        if self._json():
            return
        print("[WARN] {0}".format(text))

    def _home(self) -> str:
        return self.environ.get("HOME") or "/tmp"

    def _user_bin(self) -> str:
        value = self.environ.get("USER_BIN") or ""
        if value:
            return value
        return os.path.join(self._home(), ".local", "bin")

    def _path_line(self) -> str:
        return 'export PATH="{0}:$PATH"'.format(self._user_bin())

    def _fish_line(self) -> str:
        return "set -gx PATH {0} $PATH".format(self._user_bin())

    def _comment(self) -> str:
        return "# Added by {0} installer ({1})".format(self.APP_NAME, self.version)

    def _is_root(self) -> bool:
        if self.euid is not None:
            return int(self.euid) == 0
        geteuid = getattr(os, "geteuid", None)
        if geteuid is None:
            return False
        return geteuid() == 0

    def _shell_is_zsh(self) -> bool:
        return os.path.basename(self.environ.get("SHELL") or "") == "zsh"

    def _target(self, name: str, default: str):
        """Return (explicit, path). Empty or unset uses default and is not stored."""
        explicit = name in self.environ
        value = self.environ.get(name) or ""
        if explicit and value:
            return True, value
        return explicit, default

    def _contains(self, path: str, text: str) -> bool:
        try:
            with open(path, "r", encoding="utf-8", errors="surrogateescape") as handle:
                return text in handle.read()
        except OSError:
            return False

    def _create(self, path: str, header: str) -> bool:
        try:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(header)
                if not header.endswith("\n"):
                    handle.write("\n")
            os.chmod(path, 0o644)
        except OSError:
            return False
        return True

    def _append(self, path: str, lines) -> bool:
        try:
            with open(path, "a", encoding="utf-8") as handle:
                handle.write("\n")
                for line in lines:
                    handle.write(line)
                    handle.write("\n")
        except OSError:
            return False
        return True

    def _note_or_add(self, path: str, added_message: str, noted_message: str, created: bool) -> bool:
        """Append the shared line, or only this product's comment. Never replace."""
        path_line = self._path_line()
        comment = self._comment()
        if not self._contains(path, path_line):
            if not self._append(path, (comment, path_line)):
                return False
            self._plain(added_message)
            return True
        if not self._contains(path, comment):
            if not self._append(path, (comment,)):
                return False
            self._plain(noted_message)
            return True
        return created

    def _create_failure(self, path: str) -> bool:
        self._warn(
            "Could not create {0}. Next: create that file as this login, then re-run {1} install.".format(
                path, self.APP_NAME
            )
        )
        return False

    def path_add_bashrc(self) -> bool:
        """Create .bashrc when missing, then append the shared PATH line."""
        _explicit, path = self._target("BASHRC", os.path.join(self._home(), ".bashrc"))
        created = False
        if not os.path.isfile(path):
            header = "# Interactive rc created by {0} installer ({1})\n".format(self.APP_NAME, self.version)
            if not self._create(path, header):
                return self._create_failure(path)
            created = True
            self._plain("→ Created {0}".format(path))
        return self._note_or_add(
            path,
            "→ Added {0} to PATH for bash".format(self._user_bin()),
            "→ Noted {0} installer on bash PATH".format(self.APP_NAME),
            created,
        )

    def path_add_zshenv(self) -> bool:
        """Create .zshenv when the shell is zsh, ZSHENV is set, or the file exists."""
        explicit, path = self._target("ZSHENV", os.path.join(self._home(), ".zshenv"))
        created = False
        if not os.path.isfile(path):
            if self.host.normal_user_only() and not explicit:
                return False
            if not explicit and not self._shell_is_zsh():
                return False
            header = "# Always-on zsh rc created by {0} installer ({1})\n".format(
                self.APP_NAME, self.version
            )
            if not self._create(path, header):
                return self._create_failure(path)
            created = True
            self._plain("→ Created {0}".format(path))
        return self._note_or_add(
            path,
            "→ Added {0} to PATH for zsh (.zshenv)".format(self._user_bin()),
            "→ Noted {0} installer on zsh PATH".format(self.APP_NAME),
            created,
        )

    def path_add_zprofile(self) -> bool:
        """Create .zprofile when the shell is zsh or ZPROFILE is set. Keep an existing body.

        Setting ZSHENV is not permission to create this file.
        """
        explicit, path = self._target("ZPROFILE", os.path.join(self._home(), ".zprofile"))
        created = False
        if not os.path.isfile(path):
            if self.host.normal_user_only() and not explicit:
                return False
            if not explicit and not self._shell_is_zsh():
                return False
            header = "# Zsh login rc created by {0} installer ({1})\n".format(self.APP_NAME, self.version)
            if not self._create(path, header):
                return self._create_failure(path)
            created = True
            self._plain("→ Created {0}".format(path))
        return self._note_or_add(
            path,
            "→ Added {0} to PATH for zsh (.zprofile)".format(self._user_bin()),
            "→ Noted {0} installer on zsh login PATH".format(self.APP_NAME),
            created,
        )

    def path_add_zshrc(self) -> bool:
        """Do not write PATH to .zshrc."""
        return False

    def path_add_fish(self) -> bool:
        """Create the Fish config directory if needed, then append the Fish PATH line."""
        _explicit, path = self._target(
            "FISH_CONFIG", os.path.join(self._home(), ".config", "fish", "config.fish")
        )
        directory = os.path.dirname(path)
        try:
            if directory and not os.path.isdir(directory):
                os.makedirs(directory)
        except OSError:
            return False
        fish_line = self._fish_line()
        comment = self._comment()
        if os.path.isfile(path) and self._contains(path, fish_line):
            if not self._contains(path, comment):
                return self._append(path, (comment,))
            return False
        if not self._append(path, (comment, fish_line)):
            return False
        self._plain("→ Added {0} to PATH for fish shell".format(self._user_bin()))
        return True

    def path_invoking_is_ash(self) -> bool:
        """True when the invoking name is ash, or sh while an alpine-release file exists."""
        raw = self.environ.get("AGENT_CLI_ARGV0")
        if not raw:
            raw = sys.argv[0] if sys.argv else ""
        base = os.path.basename(raw)
        if base.startswith("-"):
            base = base[1:]
        if base == "ash":
            return True
        if base != "sh":
            return False
        if "AGENT_CLI_ALPINE_RELEASE" in self.environ:
            release = self.environ.get("AGENT_CLI_ALPINE_RELEASE") or ""
        else:
            release = "/etc/alpine-release"
        return bool(release) and os.path.isfile(release)

    def path_add_profile_ash(self) -> bool:
        """Append the shared PATH line on an existing .profile when this run is ash."""
        if not self.path_invoking_is_ash():
            return False
        _explicit, path = self._target("PROFILE", os.path.join(self._home(), ".profile"))
        if not os.path.isfile(path):
            return False
        return self._note_or_add(
            path,
            "→ Added {0} to PATH for ash (.profile)".format(self._user_bin()),
            "→ Noted {0} installer on ash PATH".format(self.APP_NAME),
            False,
        )

    def path_ensure_profile(self) -> bool:
        """Generate a missing .profile that sources .bashrc. Ash also adds PATH.

        Bash, zsh, and fish do not put the PATH export on that new file.
        An existing file is kept. Only ash appends PATH to it.
        """
        _explicit, path = self._target("PROFILE", os.path.join(self._home(), ".profile"))
        if os.path.isfile(path):
            return self.path_add_profile_ash()
        header = (
            "# BEGIN {0} profile source-bashrc\n"
            "# Created so a bash login shell sources interactive rc.\n"
            'if [ -n "${{BASH_VERSION:-}}" ]; then\n'
            '    if [ -f "${{HOME}}/.bashrc" ]; then\n'
            '        . "${{HOME}}/.bashrc"\n'
            "    fi\n"
            "fi\n"
            "# END {0} profile source-bashrc\n"
        ).format(self.APP_NAME)
        if not self._create(path, header):
            self._warn(
                "Could not create {0}. Next: create that file as this login so SSH login reads ~/.bashrc, then re-run {1} install.".format(
                    path, self.APP_NAME
                )
            )
            return False
        if self.path_invoking_is_ash():
            self._plain("→ Created {0}".format(path))
            return self.path_add_profile_ash()
        self._plain("→ Created {0} (login shell sources ~/.bashrc)".format(path))
        return True

    def _remember(self, shell_config: str, path: str) -> str:
        if shell_config == "N/A":
            return path
        return "{0} {1}".format(shell_config, path)

    def path_add_shell(self) -> int:
        """Orchestrator. Calls zshenv, then zprofile, and does not pre-assign either.

        Windows cmd does not receive .profile, .zshenv, or .zprofile.
        Root does not edit this login's startup files.
        """
        if self.host.is_windows_cmd() or self._is_root():
            return 0
        added = False
        shell_config = "N/A"
        home = self._home()
        if self.path_add_bashrc():
            added = True
            _explicit, bashrc = self._target("BASHRC", os.path.join(home, ".bashrc"))
            shell_config = bashrc
        if self.path_add_zshenv():
            added = True
            _explicit, zshenv = self._target("ZSHENV", os.path.join(home, ".zshenv"))
            shell_config = self._remember(shell_config, zshenv)
        if self.path_add_zprofile():
            added = True
            _explicit, zprofile = self._target("ZPROFILE", os.path.join(home, ".zprofile"))
            shell_config = self._remember(shell_config, zprofile)
        if self.path_add_fish():
            added = True
            _explicit, fish = self._target(
                "FISH_CONFIG", os.path.join(home, ".config", "fish", "config.fish")
            )
            shell_config = self._remember(shell_config, fish)
        if self.path_ensure_profile():
            added = True
            _explicit, profile = self._target("PROFILE", os.path.join(home, ".profile"))
            shell_config = self._remember(shell_config, profile)
        if added:
            self._plain("→ Restart your terminal or run: source {0}".format(shell_config))
        return 0

    def _snapshot(self, path: str):
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "rb") as handle:
                return handle.read()
        except OSError:
            return None

    def _under_root(self, root: str, path: str) -> bool:
        root_real = os.path.realpath(root)
        parent = os.path.dirname(path) or root
        if not os.path.isdir(parent):
            return False
        parent_real = os.path.realpath(parent)
        return parent_real == root_real or parent_real.startswith(root_real + os.sep)

    def _die(self, message: str, nxt: str) -> int:
        if self.output is not None:
            return self.output.error(message, nxt)
        print("ERROR: {0}".format(message), file=sys.stderr)
        print("   Next: {0}".format(nxt), file=sys.stderr)
        return 1

    def path_rc_test(self, root: str, file_name: str = "bashrc", case: str = "create", feature: str = "") -> int:
        """Type 0 fixture. Writes under --root. Does not call install. Keeps real HOME."""
        sample = '{0} rc-test --root "$tmpdir" --file zprofile --case create'.format(self.APP_NAME)
        if not root:
            return self._die("rc-test requires --root a tmp/cache folder.", sample)
        allowed = ("bashrc", "zshenv", "zprofile", "profile", "fish", "ash")
        if file_name == "zshrc":
            return self._die(
                "rc-test zshrc is not claimed (zsh PATH is .zshenv and .zprofile).",
                '{0} rc-test --root "$tmpdir" --file zshenv --case create'.format(self.APP_NAME),
            )
        if file_name not in allowed:
            return self._die(
                "rc-test --file must be bashrc, zshenv, zprofile, profile, ash, or fish.",
                sample,
            )
        if case not in ("create", "modify", "noop"):
            return self._die("rc-test --case must be create, modify, or noop.", sample)
        try:
            os.makedirs(root, exist_ok=True)
        except OSError:
            return self._die("rc-test cannot create --root {0}.".format(root), sample)

        home = self._home()
        watched = (
            os.path.join(home, ".bashrc"),
            os.path.join(home, ".profile"),
            os.path.join(home, ".zshenv"),
            os.path.join(home, ".zprofile"),
        )
        before = [self._snapshot(path) for path in watched]
        original = self.environ
        overlay = dict(original)
        overlay["BASHRC"] = os.path.join(root, ".bashrc")
        overlay["ZSHENV"] = os.path.join(root, ".zshenv")
        overlay["ZPROFILE"] = os.path.join(root, ".zprofile")
        overlay["ZSHRC"] = os.path.join(root, ".zshrc")
        overlay["PROFILE"] = os.path.join(root, ".profile")
        overlay["FISH_CONFIG"] = os.path.join(root, "config.fish")
        targets = {
            "bashrc": overlay["BASHRC"],
            "zshenv": overlay["ZSHENV"],
            "zprofile": overlay["ZPROFILE"],
            "profile": overlay["PROFILE"],
            "ash": overlay["PROFILE"],
            "fish": overlay["FISH_CONFIG"],
        }
        target = targets[file_name]
        if not self._under_root(root, target):
            return self._die("rc-test writes the fixture under --root only.", sample)
        self.environ = overlay
        if self.host is not None:
            self.host.environ = overlay
        try:
            self._prepare_case(file_name, case, target)
            self._run_case(file_name)
        finally:
            self.environ = original
            if self.host is not None:
                self.host.environ = original
        after = [self._snapshot(path) for path in watched]
        if after != before:
            return self._die("rc-test wrote this login's real home rc. Fixture --root only.", sample)
        message = "rc-test {0} {1}".format(file_name, case)
        if self._json() and self.output is not None:
            return self.output.ok(
                "rc-test",
                message,
                {"root": root, "file": file_name, "case": case, "status": "ok", "feature": feature},
            )
        self._plain("[OK] {0} under {1}".format(message, root))
        return 0

    def _prepare_case(self, file_name: str, case: str, target: str) -> None:
        path_line = self._path_line()
        comment = self._comment()
        if file_name == "fish":
            directory = os.path.dirname(target)
            if directory:
                os.makedirs(directory, exist_ok=True)
        if case == "create":
            if os.path.isfile(target):
                os.remove(target)
            return
        if file_name == "bashrc":
            if case == "modify":
                self._create(target, "# dongle-bashrc-keep\nalias dongle_probe=true\n")
            else:
                self._create(target, "# dongle-already-good\n{0}\n{1}\n".format(comment, path_line))
            return
        if file_name == "zshenv":
            if case == "modify":
                self._create(target, "# dongle-zshenv-keep\n")
            else:
                self._create(target, "# dongle-already-good\n{0}\n{1}\n".format(comment, path_line))
            return
        if file_name == "zprofile":
            if case == "modify":
                self._create(target, "# dongle-zprofile-keep\n")
            else:
                self._create(target, "# dongle-already-good\n{0}\n{1}\n".format(comment, path_line))
            return
        if file_name == "profile":
            self._create(target, "# keep-existing-profile\n")
            return
        if file_name == "ash":
            if case == "modify":
                self._create(target, "# keep-existing-profile\n")
            else:
                self._create(target, "# keep-existing-profile\n{0}\n{1}\n".format(comment, path_line))
            return
        if file_name == "fish":
            if case == "modify":
                self._create(target, "# dongle-fish-keep\n")
            else:
                self._create(target, "{0}\n{1}\n".format(comment, self._fish_line()))

    def _run_case(self, file_name: str) -> None:
        if file_name == "bashrc":
            self.path_add_bashrc()
        elif file_name == "zshenv":
            self.path_add_zshenv()
        elif file_name == "zprofile":
            self.path_add_zprofile()
        elif file_name == "profile":
            self.path_ensure_profile()
        elif file_name == "ash":
            self.environ["AGENT_CLI_ARGV0"] = "ash"
            self.path_ensure_profile()
            self.path_add_profile_ash()
        elif file_name == "fish":
            self.path_add_fish()

    def _user_bin_has_files(self, user_bin: str) -> bool:
        if not os.path.isdir(user_bin):
            return False
        try:
            return len(os.listdir(user_bin)) > 0
        except OSError:
            return False

    def _rewrite(self, path: str, lines) -> bool:
        directory = os.path.dirname(path) or "."
        mode = 0o644
        try:
            mode = os.stat(path).st_mode & 0o777
        except OSError:
            pass
        fd, tmp = tempfile.mkstemp(prefix=".agent-cli-rc-", dir=directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                for line in lines:
                    handle.write(line)
                    handle.write("\n")
            shutil.move(tmp, path)
            os.chmod(path, mode)
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            return False
        return True

    def cleanup_path(self) -> int:
        """Strip this product's stickers. Do not delete the startup files.

        Root does not edit this login's notes. The shared PATH line stays
        while USER_BIN still contains files.
        """
        if self._is_root():
            return 0
        home = self._home()
        user_bin = self._user_bin()
        names = (
            ("BASHRC", os.path.join(home, ".bashrc")),
            ("ZSHENV", os.path.join(home, ".zshenv")),
            ("ZPROFILE", os.path.join(home, ".zprofile")),
            ("ZSHRC", os.path.join(home, ".zshrc")),
            ("FISH_CONFIG", os.path.join(home, ".config", "fish", "config.fish")),
            ("PROFILE", os.path.join(home, ".profile")),
        )
        drop_path = not self._user_bin_has_files(user_bin)
        if not drop_path:
            self._warn("Keeping {0} in PATH because it still contains files.".format(user_bin))
        prefix = "# Added by {0} installer".format(self.APP_NAME)
        path_line = self._path_line()
        fish_line = self._fish_line()
        for name, default in names:
            _explicit, path = self._target(name, default)
            if not os.path.isfile(path):
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="surrogateescape") as handle:
                    body = handle.read().splitlines()
            except OSError:
                continue
            kept = []
            for line in body:
                if line.startswith(prefix):
                    continue
                if drop_path and (line == path_line or line == fish_line):
                    continue
                kept.append(line)
            self._rewrite(path, kept)
        return 0
