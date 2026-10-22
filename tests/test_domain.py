# Domain verbs stay off the text screen. Primary law: requirement-domain-grok-cli.
import io
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from AgentCli.cli import Cli
from AgentCli.grok_domain import GrokDomain
from AgentCli.output import Output


class TestDomain(unittest.TestCase):
    def test_typed_domain_verbs_do_not_open_the_menu(self):
        previous = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: True)
        try:
            self.assertFalse(Cli.opens_text_screen(["backup"]))
            self.assertFalse(Cli.opens_text_screen(["setup"]))
            self.assertFalse(Cli.opens_text_screen(["--json"]))
            self.assertFalse(Cli.opens_text_screen(["hello"]))
            self.assertTrue(Cli.opens_text_screen([]))
            self.assertTrue(Cli.opens_text_screen(["about"]))
        finally:
            Cli.stdout_is_tty = previous

    def test_unknown_join_and_restore(self):
        app = Cli()
        for verb in ("join", "list-videos", "restore"):
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run([verb])
            self.assertEqual(code, 1, verb)
            self.assertIn("Unknown verb", err.getvalue())

    def test_sudoer_json_shape(self):
        home = tempfile.mkdtemp(prefix="agsudo-")
        domain = GrokDomain(output=Output(), environ={"USER": "ada"})
        with redirect_stdout(io.StringIO()):
            code = domain.generate_sudoer_request(directory=home, action="add")
        self.assertEqual(code, 0)
        files = os.listdir(home)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].startswith("sudoer-"))
        self.assertIn("-agent-cli-ada-add-", files[0])
        with open(os.path.join(home, files[0]), "r", encoding="utf-8") as handle:
            doc = json.load(handle)
        self.assertEqual(doc["schema_version"], 1)
        self.assertEqual(doc["service"], "agent-cli")
        self.assertEqual(doc["commands"][0]["args"], ["backup"])
        self.assertEqual(doc["commands"][0]["path"], "/usr/local/bin/agent-cli")
        self.assertEqual(doc["commands"][0]["tags"], ["NOPASSWD"])
        text = domain.sudoer_text(username="ada")
        self.assertIn("# Purpose: Allow ada to run agent-cli backup as root.", text)
        self.assertIn("ada ALL=(root) NOPASSWD: /usr/local/bin/agent-cli backup", text)

    def test_sync_auth_skips_when_logged_in(self):
        domain = GrokDomain(output=Output(), session_override="valid")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = domain.sync_auth()
        self.assertEqual(code, 0)
        self.assertIn("No sync-auth for logged-in environment.", buf.getvalue())
        domain.session_override = "timeout"
        with redirect_stdout(io.StringIO()):
            self.assertEqual(domain.sync_auth(), 0)

    def test_setup_platform_and_source_has_no_shell_installer(self):
        domain = GrokDomain(environ={"AGENT_CLI_PLATFORM": "linux-x86_64"})
        self.assertEqual(domain.detect_platform(), "linux-x86_64")
        mac = GrokDomain(environ={"AGENT_CLI_PLATFORM": "macos-aarch64"})
        self.assertEqual(mac.detect_platform(), "macos-aarch64")
        path = os.path.join(os.path.dirname(__file__), "..", "src", "AgentCli", "grok_domain.py")
        with open(path, encoding="utf-8") as handle:
            source = handle.read()
        self.assertNotIn("install.sh", source)

    def test_deposit_copies_auth_files(self):
        home = tempfile.mkdtemp(prefix="agauth-")
        deposit = tempfile.mkdtemp(prefix="agdep-")
        grok = os.path.join(home, ".grok")
        os.makedirs(grok)
        with open(os.path.join(grok, "auth.json"), "w", encoding="utf-8") as handle:
            handle.write('{"key":"x"}\n')
        domain = GrokDomain(
            output=Output(),
            deposit_root=deposit,
            grok_home=grok,
            environ={"AGENT_CLI_BACKUP_NO_SUDO": "1", "HOME": home},
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(domain._deposit(), 0)
        stored = os.path.join(deposit, "auth.json")
        self.assertTrue(os.path.isfile(stored))
        self.assertEqual(os.stat(stored).st_mode & 0o777, 0o644)

    def test_remote_spec_four_forms(self):
        domain = GrokDomain(environ={"HOME": "/tmp", "USER": "ada"})
        self.assertEqual(domain.parse_remote_spec("ada@192.0.2.10"), ("ada", "192.0.2.10"))
        self.assertEqual(domain.parse_remote_spec("192.0.2.10"), ("", "192.0.2.10"))
        self.assertEqual(domain.parse_remote_spec("backup.example"), ("", "backup.example"))
        self.assertEqual(domain.parse_remote_spec("ada@backup.example"), ("ada", "backup.example"))
        self.assertIsNone(domain.parse_remote_spec("ada@"))
        self.assertIsNone(domain.parse_remote_spec("-host"))
        self.assertIsNone(domain.parse_remote_spec("a b@host"))

    def test_sync_from_remote_uses_scp_and_saves_preferred(self):
        home = tempfile.mkdtemp(prefix="agrem-")
        bin_dir = tempfile.mkdtemp(prefix="agscp-")
        store = os.path.join(home, "remote-store")
        os.makedirs(store)
        with open(os.path.join(store, "auth.json"), "w", encoding="utf-8") as handle:
            handle.write('{"key":"remote"}\n')
        scp = os.path.join(bin_dir, "scp")
        with open(scp, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/bin/sh\n"
                "set -eu\n"
                "dest=\"\"\n"
                "src=\"\"\n"
                "skip=0\n"
                "for arg in \"$@\"; do\n"
                "  if [ \"$skip\" -eq 1 ]; then skip=0; continue; fi\n"
                "  case \"$arg\" in\n"
                "    -o) skip=1 ;;\n"
                "    *) if [ -z \"$src\" ]; then src=\"$arg\"; else dest=\"$arg\"; fi ;;\n"
                "  esac\n"
                "done\n"
                "case \"$src\" in\n"
                "  *:*) cp \"${src#*:}\" \"$dest\" ;;\n"
                "  *) cp \"$src\" \"$dest\" ;;\n"
                "esac\n"
            )
        os.chmod(scp, 0o755)
        domain = GrokDomain(
            output=Output(),
            grok_home=os.path.join(home, ".grok"),
            session_override="missing",
            environ={
                "HOME": home,
                "USER": "ada",
                "AGENT_CLI_SCP": scp,
                "AGENT_CLI_REMOTE_ROOT": store,
                "AGENT_CLI_CACHE_SKIP": "preferred",
            },
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = domain.sync_from_remote("ada@192.0.2.10")
        self.assertEqual(code, 0, buf.getvalue())
        copied = os.path.join(home, ".grok", "auth.json")
        self.assertTrue(os.path.isfile(copied))
        self.assertEqual(os.stat(copied).st_mode & 0o777, 0o600)
        self.assertEqual(domain.preferred_remote_load(), "ada@192.0.2.10")
        self.assertIn("sync-auth-from-remote complete", buf.getvalue())

    def test_sync_to_remote_runs_when_logged_in(self):
        home = tempfile.mkdtemp(prefix="agto-")
        remote_home = os.path.join(home, "remote-login")
        os.makedirs(remote_home)
        grok = os.path.join(home, ".grok")
        os.makedirs(grok)
        with open(os.path.join(grok, "auth.json"), "w", encoding="utf-8") as handle:
            handle.write('{"key":"local"}\n')
        bin_dir = tempfile.mkdtemp(prefix="agssh-")
        ssh = os.path.join(bin_dir, "ssh")
        scp = os.path.join(bin_dir, "scp")
        with open(ssh, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/bin/sh\n"
                "set -eu\n"
                "target=\"\"\n"
                "skip=0\n"
                "for arg in \"$@\"; do\n"
                "  if [ \"$skip\" -eq 1 ]; then skip=0; continue; fi\n"
                "  case \"$arg\" in\n"
                "    -o) skip=1 ;;\n"
                "    *) if [ -z \"$target\" ]; then target=\"$arg\"; else cmd=\"$arg\"; fi ;;\n"
                "  esac\n"
                "done\n"
                "cd \"$REMOTE_HOME\"\n"
                "eval \"$cmd\"\n"
            )
        with open(scp, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/bin/sh\n"
                "set -eu\n"
                "src=\"\"\n"
                "dest=\"\"\n"
                "skip=0\n"
                "for arg in \"$@\"; do\n"
                "  if [ \"$skip\" -eq 1 ]; then skip=0; continue; fi\n"
                "  case \"$arg\" in\n"
                "    -o) skip=1 ;;\n"
                "    *) if [ -z \"$src\" ]; then src=\"$arg\"; else dest=\"$arg\"; fi ;;\n"
                "  esac\n"
                "done\n"
                "case \"$dest\" in\n"
                "  *:*) cp \"$src\" \"$REMOTE_HOME/${dest#*:}\" ;;\n"
                "  *) cp \"$src\" \"$dest\" ;;\n"
                "esac\n"
            )
        os.chmod(ssh, 0o755)
        os.chmod(scp, 0o755)
        env = {
            "HOME": home,
            "USER": "ada",
            "AGENT_CLI_SSH": ssh,
            "AGENT_CLI_SCP": scp,
            "AGENT_CLI_CACHE_SKIP": "preferred",
            "REMOTE_HOME": remote_home,
        }
        domain = GrokDomain(
            output=Output(),
            grok_home=grok,
            session_override="valid",
            environ=env,
        )
        # The fake ssh/scp read REMOTE_HOME from the process environment.
        os.environ["REMOTE_HOME"] = remote_home
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = domain.sync_to_remote("ada@backup.example")
        finally:
            os.environ.pop("REMOTE_HOME", None)
        self.assertEqual(code, 0, buf.getvalue())
        stored = os.path.join(remote_home, ".grok", "auth.json")
        self.assertTrue(os.path.isfile(stored))
        self.assertEqual(os.stat(stored).st_mode & 0o777, 0o600)
        self.assertIn("sync-auth-to-remote complete", buf.getvalue())

    def test_from_remote_skips_when_logged_in(self):
        domain = GrokDomain(output=Output(), session_override="valid", environ={"HOME": "/tmp"})
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(domain.sync_from_remote("ada@192.0.2.10"), 0)
        self.assertIn("No sync-auth for logged-in environment.", buf.getvalue())

    def test_add_crontab_installs_both_lines_once(self):
        home = tempfile.mkdtemp(prefix="agcron-")
        cron_file = os.path.join(home, "crontab.txt")
        with open(cron_file, "w", encoding="utf-8") as handle:
            handle.write("")
        cron = os.path.join(home, "crontab")
        with open(cron, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/bin/sh\n"
                "set -eu\n"
                "if [ \"$1\" = \"-l\" ]; then\n"
                "  cat \"$CRON_FILE\"\n"
                "  exit 0\n"
                "fi\n"
                "cp \"$1\" \"$CRON_FILE\"\n"
            )
        os.chmod(cron, 0o755)
        os.environ["CRON_FILE"] = cron_file
        try:
            domain = GrokDomain(
                output=Output(),
                environ={
                    "HOME": home,
                    "USER": "ada",
                    "AGENT_CLI_CRONTAB": cron,
                    "AGENT_CLI_SUDO_GRANT": "1",
                    "AGENT_CLI_ASSUME_BIN": "1",
                    "AGENT_CLI_GLOBAL_BIN": "/usr/local/bin",
                    "AGENT_CLI_CACHE_SKIP": "preferred",
                },
            )
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(domain.add_crontab(), 0)
            with open(cron_file, encoding="utf-8") as handle:
                text = handle.read()
            self.assertIn("sudo /usr/local/bin/agent-cli backup", text)
            self.assertIn("/usr/local/bin/agent-cli sync-auth", text)
            again = io.StringIO()
            with redirect_stdout(again):
                self.assertEqual(domain.add_crontab(), 0)
            self.assertIn("already present", again.getvalue())
        finally:
            os.environ.pop("CRON_FILE", None)
        with open(cron_file, encoding="utf-8") as handle:
            again = handle.read().count("agent-cli backup")
        self.assertEqual(again, 1)

    def test_run_inserts_no_auto_update_and_update_needs_grok(self):
        seen = {}

        def runner(argv):
            seen["argv"] = list(argv)
            return 0

        peer = tempfile.mkdtemp(prefix="agpeer-")
        binary = os.path.join(peer, "grok")
        with open(binary, "w", encoding="utf-8") as handle:
            handle.write("#!/bin/sh\nexit 0\n")
        os.chmod(binary, 0o755)
        domain = GrokDomain(
            output=Output(),
            runner=runner,
            environ={"HOME": "/tmp", "AGENT_CLI_GROK_BIN": binary},
        )
        self.assertEqual(domain.run(["-p", "hello"]), 0)
        self.assertEqual(seen["argv"][0], binary)
        self.assertEqual(seen["argv"][1], "--no-auto-update")
        self.assertIn("-p", seen["argv"])
        missing = GrokDomain(
            output=Output(),
            environ={"HOME": "/tmp", "AGENT_CLI_GROK_BIN": os.path.join(peer, "missing")},
        )
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(missing.update_grok(), 1)
        self.assertIn("not installed", err.getvalue())

    def test_prefix_counts_as_termux_until_override(self):
        from AgentCli.host import Host

        termux = Host(environ={"PREFIX": "/data/data/com.termux/files/usr"})
        self.assertTrue(termux.is_termux())
        self.assertTrue(termux.normal_user_only())
        forced = Host(environ={"PREFIX": "/opt/local", "AGENT_CLI_HOST_OVERRIDE": "multiuser"})
        self.assertFalse(forced.is_termux())
        self.assertFalse(forced.normal_user_only())

    def test_android_wrapper_keeps_reaper_markers(self):
        folder = tempfile.mkdtemp(prefix="agwrap-")
        domain = GrokDomain(environ={"HOME": folder, "USER": "ada"})
        path = os.path.join(folder, "grok")
        self.assertTrue(domain.write_exec_wrapper(path, os.path.join(folder, "vendor")))
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        self.assertIn("proot-exit-reaper", text)
        self.assertIn("--kill-on-exit", text)
        self.assertIn("start-services.sh", text)
        self.assertIn("unset LD_PRELOAD", text)
        self.assertNotIn("install.sh", text)

    def test_proot_reads_nested_cookies_and_skips_the_live_probe(self):
        home = tempfile.mkdtemp(prefix="agcookie-")
        bindir = os.path.join(home, "bin")
        os.makedirs(bindir)
        proot = os.path.join(bindir, "proot")
        with open(proot, "w", encoding="utf-8") as handle:
            handle.write("#!/bin/sh\nexit 0\n")
        os.chmod(proot, 0o755)
        grok_home = os.path.join(home, ".grok")
        os.makedirs(grok_home)
        with open(os.path.join(grok_home, "auth.json"), "w", encoding="utf-8") as handle:
            json.dump({"one": {"refresh_token": "cookie-value"}}, handle)
        called = {"n": 0}

        def runner(argv):
            called["n"] += 1
            return 1

        domain = GrokDomain(
            output=Output(),
            runner=runner,
            grok_home=grok_home,
            environ={"HOME": home, "PATH": bindir, "USER": "ada"},
        )
        self.assertEqual(domain.session_word(), "valid")
        self.assertEqual(called["n"], 0)
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(domain.check_session(), 0)
        self.assertIn("local auth cookies", buf.getvalue())

    def test_submit_queues_backup_and_refuses_a_wider_grant(self):
        home = tempfile.mkdtemp(prefix="agsub-")
        inbound = os.path.join(home, "inbound")
        os.makedirs(inbound)
        cli = os.path.join(home, "sudoer-cli")
        with open(cli, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/bin/sh\n"
                "file=\n"
                "prev=\n"
                "for arg in \"$@\"; do\n"
                "  if [ \"$prev\" = \"--file\" ]; then file=$arg; fi\n"
                "  prev=$arg\n"
                "done\n"
                "cp \"$file\" \"{0}/req-1\"\n"
                "printf '%s\\n' 'request_id=req-1'\n".format(inbound)
            )
        os.chmod(cli, 0o755)
        domain = GrokDomain(
            output=Output(),
            environ={
                "HOME": home,
                "USER": "ada",
                "PATH": "/usr/bin:/bin",
                "AGENT_CLI_SUDOER_CLI": cli,
                "AGENT_CLI_SUDOER_INBOUND": inbound,
                "AGENT_CLI_CACHE_SKIP": "preferred",
                "AGENT_CLI_GLOBAL_BIN": "/usr/local/bin",
            },
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(domain.submit_sudoer_request(""), 0)
        queued = os.path.join(inbound, "req-1")
        with open(queued, encoding="utf-8") as handle:
            body = json.load(handle)
        self.assertEqual(body["commands"][0]["args"], ["backup"])
        self.assertIn("did not write /etc", buf.getvalue())
        self.assertIn("request_id=req-1", buf.getvalue())
        wider = os.path.join(home, "wider.json")
        with open(wider, "w", encoding="utf-8") as handle:
            json.dump(
                {"commands": [{"path": "/usr/local/bin/agent-cli", "args": ["backup", "restore"]}]},
                handle,
            )
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(domain.submit_sudoer_request(wider), 1)
        self.assertIn("does not allow backup", err.getvalue())
        missing = GrokDomain(
            output=Output(),
            environ={"HOME": home, "USER": "ada", "AGENT_CLI_SUDOER_CLI": os.path.join(home, "missing")},
        )
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(missing.submit_sudoer_request(""), 1)
        self.assertIn("sudoer-cli not found", err.getvalue())

    def test_remove_draft_needs_force_and_refuses_etc(self):
        home = tempfile.mkdtemp(prefix="agrm-")
        draft_dir = os.path.join(home, ".config", "agent-cli")
        os.makedirs(draft_dir)
        draft = os.path.join(draft_dir, "sudoers.fragment-ada")
        with open(draft, "w", encoding="utf-8") as handle:
            handle.write("ada ALL=(root) NOPASSWD: /usr/local/bin/agent-cli backup\n")
        domain = GrokDomain(output=Output(), environ={"HOME": home, "USER": "ada"})
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(domain.remove_project_sudoers(), 1)
        self.assertTrue(os.path.isfile(draft))
        self.assertIn("--force", err.getvalue())
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(domain.remove_project_sudoers(force=True), 0)
        self.assertFalse(os.path.exists(draft))
        self.assertIn("Removed project-sudoers-file draft", buf.getvalue())
        etc = io.StringIO()
        with redirect_stderr(etc):
            self.assertEqual(domain.remove_project_sudoers("/etc/sudoers.d/agent-cli-ada", force=True), 1)
        self.assertIn("Refusing to remove paths under /etc", etc.getvalue())

    def test_install_script_writes_draft_and_checks_with_sh(self):
        home = tempfile.mkdtemp(prefix="agscript-")
        script = os.path.join(home, "admin-sudoers")
        domain = GrokDomain(
            output=Output(),
            environ={
                "HOME": home,
                "USER": "ada",
                "AGENT_CLI_CACHE_SKIP": "preferred",
                "AGENT_CLI_GLOBAL_BIN": "/usr/local/bin",
            },
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(domain.print_sudoers_install_script(script), 0)
        draft = os.path.join(home, ".config", "agent-cli", "sudoers.fragment-ada")
        self.assertTrue(os.path.isfile(draft))
        self.assertTrue(os.path.isfile(script))
        with open(script, encoding="utf-8") as handle:
            body = handle.read()
        self.assertIn("cmd_install", body)
        self.assertIn("cmd_uninstall", body)
        self.assertIn("0440", body)
        self.assertIn("/etc/sudoers.d/agent-cli-ada", body)
        proc = subprocess.run(["sh", "-n", script], check=False)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("sudo sh {0} install".format(script), buf.getvalue())

    def test_cli_accepts_force_on_remove_project_sudoers(self):
        from AgentCli.cli import Cli

        home = tempfile.mkdtemp(prefix="agcli-")
        cli = Cli()
        cli.domain.environ = {"HOME": home, "USER": "ada", "AGENT_CLI_CACHE_SKIP": "preferred"}
        parsed = {
            "verb": "remove-project-sudoers",
            "force": True,
            "json": False,
            "root": "",
            "file": "",
            "case": "",
            "feature": "",
            "extra": [],
            "help": False,
            "version": False,
            "error": "",
        }
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(cli._dispatch(parsed), 0)
        self.assertIn("nothing to remove", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
