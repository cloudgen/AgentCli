# Debug catalog. requirement-python-cli-debug.
# TP-DBG-01 catalog on. TP-DBG-02 catalog off. TP-DBG-03 text-screen file.
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from ChronicleLogger import ChronicleLogger

from AgentCli import __version__
from AgentCli.cli import Cli, main


ROOT = Path(__file__).resolve().parents[1]


def _main_body():
    source = (ROOT / "src" / "AgentCli" / "cli.py").read_text(encoding="utf-8")
    return source.split("def main(", 1)[1].split("\nif __name__", 1)[0]


def _catalog_marks():
    return (
        "v{0} (".format(__version__),
        "Using {0}".format(ChronicleLogger.class_version()),
        "Base ",
        "debug mode",
    )


class TestDebugCatalog(unittest.TestCase):
    def setUp(self):
        self._saved = {
            "DEBUG": os.environ.get("DEBUG"),
            "debug": os.environ.get("debug"),
        }
        os.environ.pop("DEBUG", None)
        os.environ.pop("debug", None)
        self._tty = Cli.stdout_is_tty
        self._run = Cli.run

    def tearDown(self):
        Cli.stdout_is_tty = self._tty
        Cli.run = self._run
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_tp_dbg_01_main_gate_and_catalog_on(self):
        body = _main_body()
        gate = body.split("if logger.isDebug():", 1)[1].split("app = Cli(logger)", 1)[0]
        self.assertIn("logger.isDebug()", body)
        self.assertNotIn('os.getenv("DEBUG"', body)
        self.assertNotIn("os.getenv('DEBUG'", body)
        self.assertNotIn('os.environ.get("DEBUG"', body)
        self.assertNotIn("os.environ.get('DEBUG'", body)
        self.assertNotIn('os.environ["DEBUG"]', body)
        cursor = 0
        for mark in (
            "v{1}",
            '"Using {0}"',
            "ChronicleLogger.class_version()",
            'level="DEBUG"',
            '"debug mode"',
        ):
            found = gate.find(mark, cursor)
            self.assertGreaterEqual(found, cursor, mark)
            cursor = found + len(mark)
        self.assertEqual(gate.count("log_message("), 4)

        os.environ["DEBUG"] = "1"
        Cli.stdout_is_tty = staticmethod(lambda: False)
        out = StringIO()
        with redirect_stdout(out):
            code = main(["version"], basedir=tempfile.mkdtemp(prefix="agdbg-"), logdir=tempfile.mkdtemp(prefix="aglog-"))
        self.assertEqual(code, 0)
        text = out.getvalue()
        cursor = 0
        for mark in _catalog_marks():
            found = text.find(mark, cursor)
            self.assertGreaterEqual(found, cursor, mark)
            cursor = found + len(mark)

    def test_tp_dbg_02_catalog_off(self):
        Cli.stdout_is_tty = staticmethod(lambda: False)
        out = StringIO()
        with redirect_stdout(out):
            code = main(["version"], basedir=tempfile.mkdtemp(prefix="agoff-"), logdir=tempfile.mkdtemp(prefix="aglog-"))
        self.assertEqual(code, 0)
        text = out.getvalue()
        self.assertNotIn("debug mode", text)
        self.assertNotIn(ChronicleLogger.class_version(), text)
        self.assertIn(__version__, text)

    def test_tp_dbg_03_text_screen_file_keeps_catalog_off_the_console(self):
        os.environ["DEBUG"] = "show"
        logdir = tempfile.mkdtemp(prefix="agscreen-")
        Cli.stdout_is_tty = staticmethod(lambda: True)
        Cli.run = lambda self, argv=None: 0
        out = StringIO()
        with redirect_stdout(out):
            code = main([], basedir=tempfile.mkdtemp(prefix="agbase-"), logdir=logdir)
        self.assertEqual(code, 0)
        text = out.getvalue()
        self.assertNotIn("debug mode", text)
        self.assertNotIn(ChronicleLogger.class_version(), text)
        files = list(Path(logdir).glob("*.log"))
        self.assertTrue(files)
        logged = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in files)
        cursor = 0
        for mark in _catalog_marks():
            found = logged.find(mark, cursor)
            self.assertGreaterEqual(found, cursor, mark)
            cursor = found + len(mark)


if __name__ == "__main__":
    unittest.main()
