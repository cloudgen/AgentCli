# TP-LANG-01 — menu language. Primary law: requirement-python-cli-language.
# Front row 7 is language. Codes 80–92. Reserved 70–79 and 93–98. LANG does not select a code.
import os
import stat
import tempfile
import unittest

from AgentCli.cli import Cli
from AgentCli.menu_language import MenuLanguage
from AgentCli.menu_model import MenuModel
from AgentCli.menu_painter import MenuPainter
from AgentCli.menu_session import MenuSession


def _commit(model, token):
    model.buffer = token
    model.cursor = len(token)
    model.focus = "input"
    return model.apply_key(10)


class TestMenuLanguage(unittest.TestCase):
    """TP-LANG-01."""

    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="vjlang_", dir="/tmp")
        self.saved = {
            name: os.environ.get(name)
            for name in ("HOME", "AGENT_CLI_LANG", "LANG", "LC_ALL")
        }
        os.environ["HOME"] = self.home
        os.environ.pop("AGENT_CLI_LANG", None)
        os.environ["LANG"] = "zh_TW.UTF-8"
        os.environ["LC_ALL"] = "zh_TW.UTF-8"
        self.painter = MenuPainter(home=self.home)
        self.model = MenuModel(painter=self.painter)

    def tearDown(self):
        for name, value in self.saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

    def test_tp_lang_01_front_row_and_blocks(self):
        """TP-LANG-01: row 7 is language. 80–92 print. 70–79 and 93–98 do not."""
        front = self.painter.display_rows("front")
        numbers = [row[0] for row in front]
        self.assertEqual(numbers, [1, 5, 6, 7, 9])
        self.assertEqual(front[0][3], "grok-auth")
        self.assertEqual(front[1][3], "sudoers")
        self.assertEqual(front[2][3], "self-management")
        self.assertEqual(front[3][1], "language")
        self.assertEqual(front[3][3], "language")
        self.assertNotIn(2, numbers)
        self.assertNotIn(3, numbers)
        self.assertNotIn(4, numbers)
        self.assertNotIn(8, numbers)
        self.assertEqual([row[0] for row in self.painter.display_rows("self")], [64, 65, 66, 68, 0])
        self.assertEqual([row[0] for row in self.painter.display_rows("sudo")], [51, 52, 53, 54, 55, 0])
        log_rows = self.painter.display_rows("log")
        self.assertEqual([row[0] for row in log_rows], [31, 32, 33, 0])
        self.assertEqual([row[1] for row in log_rows[:3]], ["view-log", "clear-log", "log-folder"])
        self.assertIsNone(_commit(self.model, "system-log"))
        self.assertEqual(self.model.layer, "log")
        self.model.layer = "front"
        for unused in ("3", "4", "8"):
            self.assertIsNone(_commit(self.model, unused))
            self.assertEqual(self.model.layer, "front")
            self.assertIn("not on this list", self.model.error)
        lang_rows = self.painter.display_rows("lang")
        printed = [row[0] for row in lang_rows]
        self.assertEqual(printed[:13], list(range(80, 93)))
        self.assertEqual(printed[-1], 0)
        for reserved in (70, 79, 93, 98):
            self.assertNotIn(reserved, printed)
        endonyms = [row[1] for row in lang_rows[:-1]]
        self.assertEqual(endonyms[0], "English")
        self.assertEqual(endonyms[2], "繁體中文")
        self.assertEqual(endonyms[-1], "Ελληνικά")
        self.assertIsNone(_commit(self.model, "7"))
        self.assertEqual(self.model.layer, "lang")

    def test_tp_lang_01_save_back_reserved_and_env(self):
        """TP-LANG-01: save writes mode 0600. Back and reserved numbers do not write."""
        leaf = self.painter.language.leaf_path()
        self.assertFalse(os.path.exists(os.path.join(self.home, ".local")))
        self.assertIsNone(_commit(self.model, "7"))
        self.assertIsNone(_commit(self.model, "0"))
        self.assertEqual(self.model.layer, "front")
        self.assertFalse(os.path.exists(leaf))
        self.assertIsNone(_commit(self.model, "7"))
        for reserved in ("70", "79", "93", "98"):
            self.assertIsNone(_commit(self.model, reserved))
            self.assertEqual(self.model.layer, "lang")
            self.assertIn("not on this list", self.model.error)
            self.assertFalse(os.path.exists(leaf))
        action = _commit(self.model, "82")
        self.assertEqual(action, "set-zh-Hant")
        session = MenuSession(
            "AgentCli",
            "1.0.4",
            on_version=lambda: "1.0.4",
            on_about=lambda: "about",
            painter=self.painter,
        )
        session.model = self.model
        self.assertEqual(session.take_action(action), "stay")
        self.assertEqual(self.model.layer, "front")
        self.assertEqual(self.model.notice, "選單語言是繁體中文")
        self.assertEqual(self.painter.path_label(), "路徑")
        self.assertEqual(self.painter.language.code(), "zh-Hant")
        self.assertTrue(leaf.startswith(self.home))
        with open(leaf, "r", encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "zh-Hant\n")
        self.assertEqual(stat.S_IMODE(os.stat(leaf).st_mode), 0o600)
        folder = os.path.dirname(leaf)
        self.assertEqual(stat.S_IMODE(os.stat(folder).st_mode), 0o700)
        front = self.painter.display_rows("front")
        self.assertEqual(front[3][1], "語言")
        self.assertEqual(front[0][1], "grok-auth")
        self.assertEqual(front[0][3], "grok-auth")
        self.assertEqual(self.painter.display_rows("log")[0][1], "view-log")
        self.assertEqual(self.painter.display_rows("lang")[0][1], "English")
        self.assertNotIn("language", Cli.PRODUCT_VERBS)

    def test_tp_lang_01_this_login_only_hides_sudoers(self):
        """TP-LANG-01: this-login-only lists 2 run and omits 5. Choosing 5 stays on the front."""
        os.environ["AGENT_CLI_HOST_OVERRIDE"] = "termux"
        try:
            painter = MenuPainter(home=self.home)
            model = MenuModel(painter=painter)
            numbers = [row[0] for row in painter.display_rows("front")]
            self.assertEqual(numbers, [1, 2, 6, 7, 9])
            self.assertIsNone(_commit(model, "5"))
            self.assertEqual(model.layer, "front")
            self.assertIn("not on this list", model.error)
            self.assertIsNone(_commit(model, "7"))
            self.assertEqual(model.layer, "lang")
            self.assertIsNone(_commit(model, "8"))
            self.assertEqual(model.layer, "lang")
        finally:
            os.environ.pop("AGENT_CLI_HOST_OVERRIDE", None)

    def test_tp_lang_01_invalid_leaf_and_env_override(self):
        """TP-LANG-01: a bad first line stays English. AGENT_CLI_LANG wins and does not write."""
        leaf = self.painter.language.leaf_path()
        os.makedirs(os.path.dirname(leaf), mode=0o700)
        with open(leaf, "w", encoding="utf-8") as handle:
            handle.write("nope\nzh-Hant\n")
        loaded = MenuLanguage(home=self.home)
        self.assertEqual(loaded.code(), "en")
        self.assertEqual(loaded.path_label(), "Path")
        with open(leaf, "r", encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "nope\nzh-Hant\n")
        os.environ["AGENT_CLI_LANG"] = "zh-Hant"
        forced = MenuLanguage(home=self.home)
        self.assertEqual(forced.code(), "zh-Hant")
        self.assertEqual(forced.path_label(), MenuPainter.PATH_LABEL_ZH_HANT)
        with open(leaf, "r", encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "nope\nzh-Hant\n")
        os.environ.pop("AGENT_CLI_LANG", None)
        cr = MenuLanguage(home=self.home)
        with open(leaf, "w", encoding="utf-8") as handle:
            handle.write("es\r\n")
        cr.load()
        self.assertEqual(cr.code(), "es")
        self.assertEqual(cr.path_label(), "Ruta")

    def test_tp_lang_01_failed_write_keeps_the_code(self):
        """TP-LANG-01: a failed write keeps the previous code and warns in that language."""
        empty = MenuLanguage(home="")
        self.assertEqual(empty.save("es"), "Could not save the menu language")
        self.assertEqual(empty.code(), "en")
        self.painter.language.save("zh-Hant")
        local = os.path.join(self.home, ".local")
        os.rename(local, local + ".kept")
        with open(local, "w", encoding="utf-8") as handle:
            handle.write("x")
        message = self.painter.language.save("es")
        self.assertEqual(self.painter.language.code(), "zh-Hant")
        self.assertEqual(message, "無法儲存選單語言")


if __name__ == "__main__":
    unittest.main()
