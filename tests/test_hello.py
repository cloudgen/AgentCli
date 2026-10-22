# hello — terminal welcome. Front row 1 is grok-auth.
# The typed verb prints the welcome line and does not draw the menu.
# Menu row 1 shows that same line on the result page.
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from AgentCli.cli import Cli
from AgentCli.menu_model import MenuModel
from AgentCli.menu_painter import MenuPainter
from AgentCli.menu_session import MenuSession
from AgentCli.tui import Tui


class TestHello(unittest.TestCase):
    """Typed hello prints a welcome line. Front row 1 is grok-auth."""

    def test_cli_hello_prints_welcome_and_skips_the_menu(self):
        app = Cli()
        self.assertIn("hello", Cli.PRODUCT_VERBS)
        self.assertNotIn("join", Cli.PRODUCT_VERBS)
        self.assertNotIn("list-videos", Cli.PRODUCT_VERBS)
        self.assertFalse(Cli.opens_text_screen(["hello"]))
        previous = Cli.stdout_is_tty
        Cli.stdout_is_tty = staticmethod(lambda: True)
        try:
            self.assertTrue(Cli.opens_text_screen([]))
            self.assertFalse(Cli.opens_text_screen(["hello"]))
            self.assertTrue(Cli.opens_text_screen(["about"]))
            self.assertFalse(Cli.opens_text_screen(["join"]))
            self.assertFalse(Cli.opens_text_screen(["list-videos"]))
        finally:
            Cli.stdout_is_tty = previous
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = app.run(["hello"])
        self.assertEqual(code, 0)
        welcome = "Welcome to {0} {1}.\n".format(Cli.APP_NAME, Cli.VERSION)
        self.assertEqual(buf.getvalue(), welcome)

    def test_removed_video_verbs_are_unknown(self):
        app = Cli()
        for verb in ("join", "list-videos"):
            err = io.StringIO()
            with redirect_stderr(err):
                code = app.run([verb])
            self.assertEqual(code, 1, verb)
            self.assertIn("Unknown verb '{0}'".format(verb), err.getvalue())
        help_buf = io.StringIO()
        with redirect_stdout(help_buf):
            self.assertEqual(app.run(["help"]), 0)
        text = help_buf.getvalue()
        self.assertNotIn("list-videos", text)
        self.assertNotIn("FFmpeg", text)
        self.assertNotIn("ffmpeg", text)
        self.assertNotIn("concatenate", text)

    def test_front_row_1_is_grok_auth_and_hello_stays_a_verb(self):
        home = tempfile.mkdtemp(prefix="vjhello_", dir="/tmp")
        saved = os.environ.get("AGENT_CLI_LANG")
        os.environ.pop("AGENT_CLI_LANG", None)
        painter = MenuPainter(home=home)
        try:
            self.assertEqual(painter.language.code(), "en")
            rows = painter.display_rows("front")
        finally:
            if saved is None:
                os.environ.pop("AGENT_CLI_LANG", None)
            else:
                os.environ["AGENT_CLI_LANG"] = saved
        self.assertEqual(
            rows[0],
            (1, "grok-auth", "backup, sync, crontab, setup, and reinstall", "grok-auth"),
        )
        tui = Tui()
        session = MenuSession(
            Cli.APP_NAME,
            Cli.VERSION,
            on_version=lambda: "",
            on_about=lambda: "",
            on_kind=lambda kind: tui.hello_text() if kind == "hello" else None,
            painter=painter,
        )
        session.model = MenuModel(painter=painter)
        self.assertEqual(session.take_action("hello"), "stay")
        self.assertEqual(session.model.phase, "result")
        welcome = "Welcome to {0} {1}.".format(Cli.APP_NAME, Cli.VERSION)
        self.assertEqual(session.model.result_text, welcome)
        self.assertEqual(tui.hello_text(), welcome)


if __name__ == "__main__":
    unittest.main()
