# Entry sample from cli.py and output.py.
# requirement-python-cli-interface, requirement-python-cli-logging,
# requirement-python-error-handling, requirement-python-project-structure.
import inspect
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from AgentCli.cli import Cli, main
from AgentCli.output import Output


ROOT = Path(__file__).resolve().parents[1]


class TestEntrySample(unittest.TestCase):
    """The live entry matches the specialized sample."""

    def test_tp_py_entry_01_main_signature_and_construct(self):
        params = list(inspect.signature(main).parameters)
        self.assertEqual(params, ["argv", "basedir", "logdir"])
        source = (ROOT / "src" / "AgentCli" / "cli.py").read_text(encoding="utf-8")
        body = source.split("def main(", 1)[1].split("\nif __name__", 1)[0]
        self.assertIn("Cli.opens_text_screen(argv)", body)
        self.assertIn("ChronicleLogger(", body)
        self.assertIn("is_quiet=screen", body)
        self.assertIn("app = Cli(logger)", body)
        self.assertIn("return app.run(argv)", body)
        self.assertNotIn("log_basedir", body)
        self.assertNotIn("_show_log_mirror", body)
        self.assertNotIn("logger=logger", body)
        self.assertNotIn("shutil.move", body)
        module = (ROOT / "src" / "AgentCli" / "__main__.py").read_text(encoding="utf-8")
        self.assertIn("from .cli import main", module)
        self.assertIn("sys.exit(main())", module)
        previous = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: True)
        try:
            self.assertTrue(Cli.opens_text_screen(["--quiet"]))
            self.assertTrue(Cli.opens_text_screen(["--debug"]))
            self.assertFalse(Cli.opens_text_screen(["--json"]))
        finally:
            Cli.stdout_is_tty = previous
        Cli.stdout_is_tty = staticmethod(lambda: False)
        try:
            self.assertFalse(Cli.opens_text_screen(["--quiet"]))
            self.assertFalse(Cli.opens_text_screen([]))
        finally:
            Cli.stdout_is_tty = previous

    def test_tp_py_entry_02_output_error_ok_and_quiet_info(self):
        human_err = io.StringIO()
        with redirect_stderr(human_err):
            code = Output().error("disk full", "agent-cli setup")
        self.assertEqual(code, 1)
        text = human_err.getvalue()
        self.assertIn("ERROR: disk full", text)
        self.assertIn("Next: agent-cli setup", text)

        json_err = io.StringIO()
        json_out = io.StringIO()
        with redirect_stderr(json_err), redirect_stdout(json_out):
            code = Output(json_mode=True).error("disk full", "agent-cli setup")
        self.assertEqual(code, 1)
        self.assertEqual(json_out.getvalue(), "")
        payload = json.loads(json_err.getvalue())
        self.assertEqual(payload["type"], "out_error")
        self.assertEqual(payload["message"], "disk full")
        self.assertEqual(payload["next"], "agent-cli setup")

        ok_out = io.StringIO()
        with redirect_stdout(ok_out):
            code = Output(json_mode=True).ok("session", "ready", {"word": "valid"})
        self.assertEqual(code, 0)
        ok_payload = json.loads(ok_out.getvalue())
        self.assertEqual(ok_payload["type"], "session")
        self.assertEqual(ok_payload["word"], "valid")

        info_out = io.StringIO()
        with redirect_stdout(info_out):
            Output(quiet=True).info("hidden")
            Output(json_mode=True).info("hidden")
            Output().info("shown")
        self.assertEqual(info_out.getvalue(), "[INFO] shown\n")
