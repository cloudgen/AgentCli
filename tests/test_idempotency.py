# Re-run safety. requirement-python-idempotency.
# TP-IDEM-01 backup overwrite. TP-IDEM-02 self-install when the console script exists.
import os
import stat
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

from AgentCli.grok_domain import GrokDomain
from AgentCli.output import Output
from AgentCli.self_management import SelfManage


class TestPythonIdempotency(unittest.TestCase):
    def test_tp_idem_01_second_backup_replaces_the_same_names(self):
        home = tempfile.mkdtemp(prefix="agidem-")
        deposit = tempfile.mkdtemp(prefix="agdep-")
        grok = os.path.join(home, ".grok")
        os.makedirs(grok)
        auth = os.path.join(grok, "auth.json")
        with open(auth, "w", encoding="utf-8") as handle:
            handle.write('{"key":"first"}\n')
        domain = GrokDomain(
            output=Output(),
            deposit_root=deposit,
            grok_home=grok,
            environ={"AGENT_CLI_BACKUP_NO_SUDO": "1", "HOME": home},
        )
        buf = StringIO()
        with redirect_stdout(buf):
            self.assertEqual(domain._deposit(), 0)
            with open(auth, "w", encoding="utf-8") as handle:
                handle.write('{"key":"second"}\n')
            self.assertEqual(domain._deposit(), 0)
        stored = os.path.join(deposit, "auth.json")
        with open(stored, encoding="utf-8") as handle:
            self.assertEqual(handle.read(), '{"key":"second"}\n')
        names = sorted(os.listdir(deposit))
        self.assertEqual(names, ["auth.json"])
        self.assertFalse(any(name.endswith(".tar") or name.endswith(".tar.gz") for name in names))

    def test_tp_idem_02_self_install_succeeds_when_console_script_is_present(self):
        bin_dir = tempfile.mkdtemp(prefix="agbin-")
        script = os.path.join(bin_dir, "agent-cli")
        with open(script, "w", encoding="utf-8") as handle:
            handle.write("#!/bin/sh\nexit 0\n")
        os.chmod(script, stat.S_IRWXU)
        calls = []

        def runner(argv):
            calls.append(list(argv))
            return 1, "", "pip should not run"

        previous = os.environ.get("PATH")
        os.environ["PATH"] = bin_dir
        try:
            manager = SelfManage("AgentCli", "0.0.0", runner=runner)
            code, text = manager.run_pip("self-install")
            again, again_text = manager.run_pip("self-install")
        finally:
            if previous is None:
                os.environ.pop("PATH", None)
            else:
                os.environ["PATH"] = previous
        self.assertEqual(code, 0)
        self.assertEqual(again, 0)
        self.assertIn("already present", text)
        self.assertIn("already present", again_text)
        self.assertEqual(calls, [])

    def test_self_install_calls_pip_when_the_console_script_is_absent(self):
        calls = []

        def runner(argv):
            calls.append(list(argv))
            return 0, "installed", ""

        previous = os.environ.get("PATH")
        os.environ["PATH"] = tempfile.mkdtemp(prefix="agnopath-")
        try:
            manager = SelfManage("AgentCli", "0.0.0", runner=runner)
            code, text = manager.run_pip("self-install")
        finally:
            if previous is None:
                os.environ.pop("PATH", None)
            else:
                os.environ["PATH"] = previous
        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 1)
        self.assertIn("install", calls[0])
        self.assertIn("AgentCli", calls[0])
        self.assertIn("installed", text)


if __name__ == "__main__":
    unittest.main()
