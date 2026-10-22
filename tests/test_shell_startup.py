# TP-LC-43..46 — shell startup files. Primary law: requirement-shell-startup-files.
# Install proofs use a throw-away HOME. rc-test keeps the real HOME and writes --root only.
import io
import os
import stat
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from AgentCli.cli import Cli
from AgentCli.output import Output
from AgentCli.shell_startup import ShellStartup


def _home_notes(home):
    names = (".bashrc", ".profile", ".zshenv", ".zprofile")
    found = {}
    for name in names:
        path = os.path.join(home, name)
        if os.path.isfile(path):
            with open(path, "rb") as handle:
                found[path] = handle.read()
        else:
            found[path] = None
    return found


class TestShellStartup(unittest.TestCase):
    """TP-LC-43 create, TP-LC-44 bash-only, TP-LC-45 keep body, TP-LC-46 rc-test."""

    def _writer(self, home, **env):
        environ = {"HOME": home, "USER": "operator"}
        environ.update(env)
        return ShellStartup(version="1.2.0", output=Output(), environ=environ)

    def _line(self, home):
        return 'export PATH="{0}/.local/bin:$PATH"'.format(home)

    def test_tp_lc_43_zsh_creates_zprofile_and_zshenv_once(self):
        """TP-LC-43: zsh install creates .zprofile and .zshenv, skips .zshrc, no duplicate."""
        with tempfile.TemporaryDirectory() as home:
            writer = self._writer(home, SHELL="/bin/zsh")
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(writer.path_add_shell(), 0)
            zprofile = os.path.join(home, ".zprofile")
            zshenv = os.path.join(home, ".zshenv")
            self.assertTrue(os.path.isfile(zprofile), "TP-LC-43 created HOME/.zprofile")
            self.assertTrue(os.path.isfile(zshenv), "TP-LC-43 created HOME/.zshenv")
            line = self._line(home)
            with open(zprofile, "r", encoding="utf-8") as handle:
                profile = handle.read()
            with open(zshenv, "r", encoding="utf-8") as handle:
                env_body = handle.read()
            self.assertIn(line, profile, "TP-LC-43 zprofile PATH")
            self.assertIn(line, env_body, "TP-LC-43 zshenv PATH")
            self.assertIn("# Zsh login rc created by agent-cli installer (1.2.0)", profile)
            self.assertFalse(os.path.isfile(os.path.join(home, ".zshrc")), "TP-LC-43 did not invent .zshrc")
            mode = stat.S_IMODE(os.stat(zprofile).st_mode)
            self.assertEqual(mode, 0o644)
            with redirect_stdout(io.StringIO()):
                writer.path_add_shell()
            count = profile_count(zprofile, line)
            self.assertEqual(count, 1, "TP-LC-43 second install does not duplicate zprofile PATH")

    def test_tp_lc_44_bash_does_not_invent_zsh_notes(self):
        """TP-LC-44: bash-only install does not invent .zprofile or .zshenv."""
        with tempfile.TemporaryDirectory() as home:
            writer = self._writer(home, SHELL="/bin/bash")
            with redirect_stdout(io.StringIO()):
                writer.path_add_shell()
            self.assertFalse(os.path.isfile(os.path.join(home, ".zprofile")), "TP-LC-44 did not invent HOME/.zprofile")
            self.assertFalse(os.path.isfile(os.path.join(home, ".zshenv")), "TP-LC-44 did not invent HOME/.zshenv")
            profile = os.path.join(home, ".profile")
            self.assertTrue(os.path.isfile(profile))
            with open(profile, "r", encoding="utf-8") as handle:
                body = handle.read()
            self.assertIn('. "${HOME}/.bashrc"', body)
            self.assertNotIn(self._line(home), body)

    def test_tp_lc_45_existing_zprofile_keeps_the_body(self):
        """TP-LC-45: an existing .zprofile keeps its body and gains the PATH line."""
        with tempfile.TemporaryDirectory() as home:
            path = os.path.join(home, ".zprofile")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("# user-kept-zprofile\n")
            writer = self._writer(home, SHELL="/bin/bash")
            with redirect_stdout(io.StringIO()):
                writer.path_add_shell()
            with open(path, "r", encoding="utf-8") as handle:
                body = handle.read()
            self.assertIn("# user-kept-zprofile", body, "TP-LC-45 kept existing body")
            self.assertIn(self._line(home), body, "TP-LC-45 appended PATH")
            self.assertTrue(body.startswith("# user-kept-zprofile"))

    def test_tp_lc_46_rc_test_zprofile_writes_the_fixture_only(self):
        """TP-LC-46: rc-test --file zprofile writes the fixture and leaves the real home still."""
        real_home = os.environ.get("HOME") or "/tmp"
        before = _home_notes(real_home)
        with tempfile.TemporaryDirectory() as root:
            writer = self._writer(real_home, SHELL="/bin/bash")
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = writer.path_rc_test(root, "zprofile", "create")
            self.assertEqual(code, 0, "TP-LC-46 rc-test zprofile exit 0")
            fixture = os.path.join(root, ".zprofile")
            self.assertTrue(os.path.isfile(fixture), "TP-LC-46 created fixture zprofile")
            with open(fixture, "r", encoding="utf-8") as handle:
                body = handle.read()
            self.assertIn("export PATH=", body, "TP-LC-46 fixture PATH")
            self.assertIn("rc-test zprofile create", buf.getvalue(), "TP-LC-46 success text")
            self.assertFalse(os.path.isfile(os.path.join(root, ".zshrc")))
        self.assertEqual(_home_notes(real_home), before, "TP-LC-46 did not write HOME/.zprofile")

    def test_zshenv_alone_does_not_create_zprofile(self):
        """A set ZSHENV is not permission to invent .zprofile."""
        with tempfile.TemporaryDirectory() as home:
            writer = self._writer(
                home,
                SHELL="/bin/bash",
                ZSHENV=os.path.join(home, ".zshenv"),
            )
            with redirect_stdout(io.StringIO()):
                writer.path_add_shell()
            self.assertTrue(os.path.isfile(os.path.join(home, ".zshenv")))
            self.assertFalse(os.path.isfile(os.path.join(home, ".zprofile")))

    def test_rc_test_zshrc_fails_closed(self):
        """--file zshrc is not success. Next names --file zshenv."""
        with tempfile.TemporaryDirectory() as root:
            writer = self._writer(os.environ.get("HOME") or "/tmp", SHELL="/bin/bash")
            err = io.StringIO()
            with redirect_stderr(err), redirect_stdout(io.StringIO()):
                code = writer.path_rc_test(root, "zshrc", "create")
            self.assertEqual(code, 1)
            self.assertIn("--file zshenv", err.getvalue())
            self.assertIn(".zprofile", err.getvalue())
            self.assertFalse(os.path.isfile(os.path.join(root, ".zshrc")))

    def test_windows_cmd_does_not_invent_startup_files(self):
        """Windows cmd does not receive .profile, .zshenv, or .zprofile."""
        with tempfile.TemporaryDirectory() as home:
            writer = self._writer(
                home,
                SHELL="/bin/zsh",
                AGENT_CLI_HOST_OVERRIDE="windows-cmd",
            )
            with redirect_stdout(io.StringIO()):
                writer.path_add_shell()
            self.assertFalse(os.path.isfile(os.path.join(home, ".zprofile")))
            self.assertFalse(os.path.isfile(os.path.join(home, ".zshenv")))
            self.assertFalse(os.path.isfile(os.path.join(home, ".profile")))
            self.assertFalse(os.path.isfile(os.path.join(home, ".bashrc")))

    def test_uninstall_strips_the_sticker_and_keeps_the_file(self):
        """Uninstall may remove this product's sticker and must not delete the file."""
        with tempfile.TemporaryDirectory() as home:
            path = os.path.join(home, ".zprofile")
            line = self._line(home)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("# user-kept-zprofile\n# Added by agent-cli installer (1.2.0)\n{0}\n".format(line))
                handle.write("# Added by grok-cli installer (1.0.0)\n")
            writer = self._writer(home, SHELL="/bin/bash")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(writer.cleanup_path(), 0)
            self.assertTrue(os.path.isfile(path))
            with open(path, "r", encoding="utf-8") as handle:
                body = handle.read()
            self.assertIn("# user-kept-zprofile", body)
            self.assertIn("# Added by grok-cli installer (1.0.0)", body)
            self.assertNotIn("# Added by agent-cli installer", body)
            self.assertNotIn(line, body)

    def test_root_uninstall_does_not_edit_this_login(self):
        """Root uninstall must not edit this login's startup files."""
        with tempfile.TemporaryDirectory() as home:
            path = os.path.join(home, ".zprofile")
            original = "# Added by agent-cli installer (1.2.0)\nexport PATH=\"keep:$PATH\"\n"
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(original)
            writer = self._writer(home)
            writer.euid = 0
            writer.cleanup_path()
            with open(path, "r", encoding="utf-8") as handle:
                self.assertEqual(handle.read(), original)

    def test_cli_rc_test_and_install_use_the_same_helper(self):
        """The typed verbs reach ShellStartup. install uses a throw-away HOME."""
        real_home = os.environ.get("HOME") or "/tmp"
        before = _home_notes(real_home)
        app = Cli()
        with tempfile.TemporaryDirectory() as root:
            out = io.StringIO()
            err = io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = app.run(["rc-test", "--root", root, "--file", "zprofile", "--case", "create"])
            self.assertEqual(code, 0)
            self.assertIn("rc-test zprofile create", out.getvalue())
            self.assertTrue(os.path.isfile(os.path.join(root, ".zprofile")))
        self.assertEqual(_home_notes(real_home), before)
        with tempfile.TemporaryDirectory() as home:
            previous = os.environ.get("HOME")
            previous_shell = os.environ.get("SHELL")
            os.environ["HOME"] = home
            os.environ["SHELL"] = "/bin/zsh"
            try:
                installed = Cli()
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(installed.run(["install"]), 0)
                self.assertTrue(os.path.isfile(os.path.join(home, ".zprofile")))
                self.assertFalse(os.path.isfile(os.path.join(home, ".zshrc")))
            finally:
                if previous is None:
                    os.environ.pop("HOME", None)
                else:
                    os.environ["HOME"] = previous
                if previous_shell is None:
                    os.environ.pop("SHELL", None)
                else:
                    os.environ["SHELL"] = previous_shell
        self.assertEqual(_home_notes(real_home), before)


def profile_count(path, line):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().count(line)


if __name__ == "__main__":
    unittest.main()
