# TP-TUI-09 — path label. Primary law: requirement-python-tui.
# English Path is the default. LANG does not select Traditional Chinese.
# The folder path and the clock are not translated.
# TP-TUI-10 — wide columns. Wide and Fullwidth count as two. Ambiguous stays one.
import os
import tempfile
import unittest

from AgentCli.menu_painter import MenuPainter
from AgentCli.tui import Tui


class TestPathLabel(unittest.TestCase):
    """TP-TUI-09."""

    def test_tp_tui_09_english_label_until_language_requirement(self):
        """TP-TUI-09: missing language file stays Path. LANG does not select 路徑."""
        self.assertEqual(MenuPainter.PATH_LABEL_EN, "Path")
        self.assertEqual(MenuPainter.PATH_LABEL_ZH_HANT, "路徑")
        folder = tempfile.mkdtemp(prefix="vjclips_", dir="/tmp")
        home = tempfile.mkdtemp(prefix="vjhome_", dir="/tmp")
        previous = os.getcwd()
        saved = {
            name: os.environ.get(name)
            for name in (
                "LANG", "LANGUAGE", "LC_ALL", "LC_MESSAGES", "HOME", "AGENT_CLI_LANG",
            )
        }
        os.environ["LANG"] = "zh_TW.UTF-8"
        os.environ["LANGUAGE"] = "zh_TW:zh"
        os.environ["LC_ALL"] = "zh_TW.UTF-8"
        os.environ["LC_MESSAGES"] = "zh_TW.UTF-8"
        os.environ["HOME"] = home
        os.environ.pop("AGENT_CLI_LANG", None)
        os.chdir(folder)
        try:
            painter = MenuPainter(home=home)
            self.assertEqual(painter.path_label(), "Path")
            current = os.path.abspath(folder)
            clock = "14:05:09"
            original = painter.clock_text
            painter.clock_text = lambda: clock
            try:
                logical = "Path: " + current + "  " + clock
                self.assertEqual(painter.path_line(), logical)
                self.assertFalse(logical.startswith("路徑"))
                self.assertNotIn("路徑", logical)
                self.assertIn(current, logical)
                self.assertTrue(logical.endswith(clock))
                narrow = len("Path: ") + 4
                shortened = painter.path_line(narrow)
                self.assertEqual(shortened, "Path: " + current[-4:])
                self.assertNotIn(clock, shortened)
                self.assertFalse(shortened.startswith("路徑"))
            finally:
                painter.clock_text = original

            session = Tui()
            session.painter = MenuPainter(home=home)
            session.painter.clock_text = lambda: clock
            try:
                for line in (
                    session.front_lines()[0],
                    session.self_lines()[0],
                    session.log_lines()[0],
                    session.language_lines()[0],
                ):
                    self.assertEqual(line, "Path: " + current + "  " + clock)
                    self.assertFalse(line.startswith("路徑"))
                    self.assertNotIn("AgentCli", line.split("  ")[0])
            finally:
                session.painter.clock_text = original
        finally:
            os.chdir(previous)
            for name, value in saved.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value


class TestWideColumns(unittest.TestCase):
    """TP-TUI-10. Wide and Fullwidth count as two columns. Ambiguous stays one."""

    def test_tp_tui_10_wide_columns(self):
        """TP-TUI-10: the colon starts after the display width of a wide short."""
        import unicodedata

        from AgentCli.cli import Cli
        from AgentCli.menu_model import MenuModel
        from AgentCli.menu_painter import MenuPainter

        class ColumnScreen:
            """Records each addstr with its column."""

            def __init__(self, size=(24, 80)):
                self.size = size
                self.calls = []

            def getmaxyx(self):
                return self.size

            def erase(self):
                self.calls = []

            def addstr(self, y, x, text, _attr=0):
                self.calls.append((y, x, text))

            def refresh(self):
                return None

            def curs_set(self, _visibility):
                return None

        def occupy(calls):
            rows = {}
            for y, x, text in calls:
                row = rows.setdefault(y, {})
                col = x
                for char in text:
                    if unicodedata.category(char) == "Cf":
                        continue
                    wide = unicodedata.east_asian_width(char) in ("W", "F")
                    width = 2 if wide else 1
                    for offset in range(width):
                        pos = col + offset
                        self.assertNotIn(
                            pos,
                            row,
                            "row {0} column {1} already holds {2!r}".format(
                                y, pos, row.get(pos)
                            ),
                        )
                        row[pos] = char if offset == 0 else ""
                    col += width

        def gap_before(line, clock):
            head = line[: -len(clock)]
            return len(head) - len(head.rstrip(" "))

        home = tempfile.mkdtemp(prefix="vjwide_", dir="/tmp")
        folder = tempfile.mkdtemp(prefix="vjclips_", dir="/tmp")
        previous = os.getcwd()
        saved = {
            name: os.environ.get(name)
            for name in ("HOME", "AGENT_CLI_LANG", "LANG", "LC_ALL")
        }
        os.environ["HOME"] = home
        os.environ.pop("AGENT_CLI_LANG", None)
        os.chdir(folder)
        clock = "14:05:09"
        try:
            self.assertEqual(MenuPainter.display_width("╭─╮"), 3)
            self.assertEqual(MenuPainter.display_width("█"), 1)
            self.assertEqual(MenuPainter.display_width("路径"), MenuPainter.display_width("Path"))
            self.assertEqual(MenuPainter.display_width("路徑"), 4)
            self.assertEqual(MenuPainter.display_width("パス"), 4)
            self.assertEqual(MenuPainter.display_width("경로"), 4)

            painter = MenuPainter(home=home)
            painter.clock_text = lambda: clock
            wide = 79
            english = painter.path_line(wide)
            self.assertEqual(MenuPainter.display_width(english), wide)
            self.assertTrue(english.endswith(clock))
            english_gap = gap_before(english, clock)
            for label, first in (
                ("路径", "路"),
                ("路徑", "路"),
                ("パス", "パ"),
                ("경로", "경"),
            ):
                os.environ["AGENT_CLI_LANG"] = {
                    "路径": "zh-Hans",
                    "路徑": "zh-Hant",
                    "パス": "ja",
                    "경로": "ko",
                }[label]
                labeled = MenuPainter(home=home)
                labeled.clock_text = lambda: clock
                self.assertEqual(labeled.path_label(), label)
                line = labeled.path_line(wide)
                self.assertTrue(line.startswith(label + ": "), line)
                self.assertTrue(line.endswith(clock), line)
                self.assertEqual(MenuPainter.display_width(line), wide)
                self.assertEqual(gap_before(line, clock), english_gap)
                self.assertEqual(labeled.path_line(1), "")
                self.assertEqual(labeled.path_line(2), first)
                self.assertEqual(labeled.path_line(3), first)
                self.assertEqual(labeled.path_line(5), label + ":")

            expected = {
                "zh-Hans": [
                    "1. grok-auth: backup, sync, crontab, setup, and reinstall",
                    "5. sudoers  : grant and drafts",
                    "6. 自我管理 : 检查、更新，或移除此包",
                    "7. 语言     : 此菜单的显示语言",
                    "9. 离开     : 离开",
                ],
                "zh-Hant": [
                    "1. grok-auth: backup, sync, crontab, setup, and reinstall",
                    "5. sudoers  : grant and drafts",
                    "6. 自我管理 : 檢查、更新，或移除此套件",
                    "7. 語言     : 這個選單的顯示語言",
                    "9. 離開     : 離開",
                ],
                "ko": [
                    "1. grok-auth: backup, sync, crontab, setup, and reinstall",
                    "5. sudoers  : grant and drafts",
                    "6. 자기관리 : 확인, 업데이트, 또는 이 패키지 제거",
                    "7. 언어     : 이 메뉴의 표시 언어",
                    "9. 종료     : 종료",
                ],
                "ja": [
                    "1. grok-auth: backup, sync, crontab, setup, and reinstall",
                    "5. sudoers  : grant and drafts",
                    "6. 自己管理 : 確認、更新、またはこのパッケージの削除",
                    "7. 言語     : このメニューの表示言語",
                    "9. 終了     : 終了",
                ],
            }
            shorts = {
                "zh-Hans": ("语言", "自我管理", "离开"),
                "zh-Hant": ("語言", "自我管理", "離開"),
                "ko": ("언어", "자기관리", "종료"),
                "ja": ("言語", "自己管理", "終了"),
            }
            for code, words in shorts.items():
                os.environ["AGENT_CLI_LANG"] = code
                board_painter = MenuPainter(home=home)
                board_painter.clock_text = lambda: clock
                self.assertEqual(board_painter.language.code(), code)
                board = board_painter.display_rows("front")
                self.assertEqual(board_painter.format_rows(board), expected[code])
                model = MenuModel(painter=board_painter)
                screen = ColumnScreen()
                board_painter.paint(screen, model, Cli.APP_NAME, Cli.VERSION)
                occupy(screen.calls)
                placeable = screen.getmaxyx()[1] - 1
                path_text = screen.calls[0][2]
                self.assertEqual(screen.calls[0][0], 0)
                self.assertEqual(screen.calls[0][1], 0)
                self.assertTrue(path_text.startswith(board_painter.path_label() + ": "), path_text)
                self.assertTrue(path_text.endswith(clock), path_text)
                self.assertEqual(MenuPainter.display_width(path_text), placeable)
                framed = [text for _y, _x, text in screen.calls if text[:1] == "╭"]
                self.assertEqual(len(framed), 1)
                self.assertEqual(MenuPainter.display_width(framed[0]), placeable)
                for number_field, short, verb_pad, _explain in board_painter.row_parts(board):
                    if short not in words:
                        continue
                    verb_x = MenuPainter.display_width(number_field)
                    matches = [
                        item for item in screen.calls if item[2] == short and item[1] == verb_x
                    ]
                    self.assertEqual(len(matches), 1, short)
                    y, x, text = matches[0]
                    self.assertEqual(text, short)
                    colon_x = x + MenuPainter.display_width(short)
                    colon = [item for item in screen.calls if item[0] == y and item[1] == colon_x]
                    self.assertEqual(colon, [(y, colon_x, "{0}: ".format(verb_pad))], short)
                    self.assertNotEqual(colon_x, x + len(short), short)

            os.environ.pop("AGENT_CLI_LANG", None)
            english_painter = MenuPainter(home=home)
            english_painter.clock_text = lambda: clock
            self.assertEqual(english_painter.language.code(), "en")
            lang_rows = english_painter.display_rows("lang")
            endonyms = ("简体中文", "繁體中文", "日本語", "한국어")
            joined = "\n".join(english_painter.format_rows(lang_rows))
            for endonym in endonyms:
                self.assertIn(endonym, joined)
            model = MenuModel(painter=english_painter)
            model.layer = "lang"
            screen = ColumnScreen(size=(40, 80))
            english_painter.paint(screen, model, Cli.APP_NAME, Cli.VERSION)
            occupy(screen.calls)
            for number_field, short, verb_pad, _explain in english_painter.row_parts(lang_rows):
                if short not in endonyms:
                    continue
                verb_x = MenuPainter.display_width(number_field)
                matches = [
                    item for item in screen.calls if item[2] == short and item[1] == verb_x
                ]
                self.assertEqual(len(matches), 1, short)
                y, x, text = matches[0]
                colon_x = x + MenuPainter.display_width(short)
                colon = [item for item in screen.calls if item[0] == y and item[1] == colon_x]
                self.assertEqual(colon, [(y, colon_x, "{0}: ".format(verb_pad))], short)
                self.assertNotEqual(colon_x, x + len(short), short)
        finally:
            os.chdir(previous)
            for name, value in saved.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value


class TestUnavailableBand(unittest.TestCase):
    """TP-TUI-11. Light lines under the box. The status line is the last row."""

    def _painter(self, override, word):
        from AgentCli.host import Host

        painter = MenuPainter()
        painter.host = Host(environ={"AGENT_CLI_HOST_OVERRIDE": override})
        painter.session_word = word
        painter.clock_text = lambda: "12:00:00"
        return painter

    def test_tp_tui_11_band_under_the_box(self):
        """TP-TUI-11: sentences, chrome height, last-row status, no result-page band."""
        from AgentCli.menu_model import MenuModel

        logged_out = MenuPainter.LOGGED_OUT_UNAVAILABLE
        logged_in = MenuPainter.LOGGED_IN_UNAVAILABLE
        host_termux = MenuPainter.HOST_UNAVAILABLE.format(label="termux")
        host_gitbash = MenuPainter.HOST_UNAVAILABLE.format(label="gitbash")
        host_windows = MenuPainter.HOST_UNAVAILABLE.format(label="windows-cmd")

        multi = self._painter("multiuser", "missing")
        self.assertEqual(MenuPainter.NOTICE_ROWS, 3)
        self.assertEqual(multi.unavailable_lines(), (logged_out,))
        self.assertEqual(
            multi.chrome_rows(),
            MenuPainter.FRAME_ROWS + MenuPainter.NOTICE_ROWS + MenuPainter.FOOTER_ROWS,
        )
        self.assertEqual(self._painter("termux", "missing").chrome_rows(), multi.chrome_rows())
        self.assertEqual(self._painter("multiuser", "timeout").unavailable_lines(), (logged_out,))
        self.assertEqual(self._painter("multiuser", "").unavailable_lines(), (logged_out,))
        self.assertEqual(self._painter("multiuser", "valid").unavailable_lines(), (logged_in,))
        self.assertEqual(
            self._painter("termux", "missing").unavailable_lines(),
            (host_termux, logged_out),
        )
        self.assertEqual(
            self._painter("termux", "valid").unavailable_lines(),
            (host_termux, logged_in),
        )
        self.assertEqual(
            self._painter("gitbash", "timeout").unavailable_lines(),
            (host_gitbash, logged_out),
        )
        self.assertEqual(
            self._painter("windows-cmd", "valid").unavailable_lines(),
            (host_windows, logged_in),
        )

        termux = self._painter("termux", "missing")
        fit_multi = MenuPainter.MIN_MENU_ABOVE + multi.chrome_rows()
        self.assertTrue(multi.screen_can_hold(fit_multi, 40))
        self.assertFalse(multi.screen_can_hold(fit_multi - 1, 40))
        self.assertTrue(termux.screen_can_hold(fit_multi, 40))

        class BandScreen:
            def __init__(self, size):
                self.size = size
                self.calls = []

            def getmaxyx(self):
                return self.size

            def erase(self):
                self.calls = []

            def addstr(self, y, x, text, attr=0):
                self.calls.append((y, x, text, attr))

            def refresh(self):
                return None

            def curs_set(self, _visibility):
                return None

            def move(self, _y, _x):
                return None

        height, width = 24, 80
        model = MenuModel(painter=multi)
        screen = BandScreen((height, width))
        multi.paint(screen, model, "AgentCli", "1.0.0")
        box_top = height - multi.chrome_rows()
        band_y = box_top + MenuPainter.FRAME_ROWS
        status_y = band_y + MenuPainter.NOTICE_ROWS
        self.assertEqual(status_y, height - 1)
        band_rows = []
        for offset in range(MenuPainter.NOTICE_ROWS):
            row = [
                item for item in screen.calls
                if item[0] == band_y + offset and item[1] == 0
            ]
            self.assertEqual(len(row), 1)
            self.assertNotEqual(row[0][3], 0)
            self.assertEqual(MenuPainter.display_width(row[0][2]), width - 1)
            band_rows.append(row[0][2])
        self.assertIn(logged_out, band_rows[0])
        self.assertEqual(band_rows[1].strip(), "")
        self.assertEqual(band_rows[2].strip(), "")
        termux_model = MenuModel(painter=termux)
        termux_screen = BandScreen((height, width))
        termux.paint(termux_screen, termux_model, "AgentCli", "1.0.0")
        termux_rows = []
        for offset in range(MenuPainter.NOTICE_ROWS):
            row = [
                item for item in termux_screen.calls
                if item[0] == band_y + offset and item[1] == 0
            ]
            self.assertEqual(len(row), 1, offset)
            termux_rows.append(row[0][2])
        self.assertIn(host_termux, termux_rows[0])
        self.assertIn(logged_out, termux_rows[1])
        self.assertEqual(termux_rows[2].strip(), "")
        status = [item for item in screen.calls if item[0] == status_y and "Up/Down" in item[2]]
        self.assertEqual(len(status), 1)
        self.assertEqual(status[0][1], 0)
        self.assertIn("AgentCli 1.0.0", status[0][2])
        self.assertFalse(any(item[0] > status_y for item in screen.calls))

        narrow = BandScreen((height, 41))
        multi.paint(narrow, model, "AgentCli", "1.0.0")
        narrow_rows = []
        for offset in range(MenuPainter.NOTICE_ROWS):
            row = [
                item for item in narrow.calls
                if item[0] == band_y + offset and item[1] == 0
            ]
            self.assertEqual(len(row), 1, offset)
            self.assertEqual(MenuPainter.display_width(row[0][2]), 40)
            narrow_rows.append(row[0][2].rstrip())
        self.assertEqual(narrow_rows[0], "backup features are not available for")
        self.assertEqual(narrow_rows[1], "logged-out environment.")
        self.assertEqual(narrow_rows[2], "")
        self.assertNotEqual(narrow_rows[0], MenuPainter.clip_columns(logged_out, 40))
        self.assertFalse(any(item[0] > status_y for item in narrow.calls))
        packed = termux.notice_display_lines(40)
        self.assertEqual(
            packed,
            (
                "backup, sync-auth and sudoers features",
                "are not available in termux.",
                "backup features are not available for",
            ),
        )

        model.show_result("done")
        result = BandScreen((height, width))
        multi.paint(result, model, "AgentCli", "1.0.0")
        self.assertFalse(any(logged_out in item[2] for item in result.calls))
        self.assertFalse(any(logged_in in item[2] for item in result.calls))


class TestWindowResize(unittest.TestCase):
    """TP-TUI-12. A window-size change redraws and wraps inside the three light rows."""

    def _painter(self):
        from AgentCli.host import Host

        painter = MenuPainter()
        painter.host = Host(environ={"AGENT_CLI_HOST_OVERRIDE": "multiuser"})
        painter.session_word = "missing"
        painter.clock_text = lambda: "12:00:00"
        return painter

    def test_tp_tui_12_resize_redraws_and_wraps(self):
        """TP-TUI-12: resize is not a choice. Narrow text continues. Too small waits."""
        import curses

        from AgentCli.menu_model import MenuModel
        from AgentCli.menu_session import MenuSession
        from AgentCli.tui import MenuScreenError, Tui

        logged_out = MenuPainter.LOGGED_OUT_UNAVAILABLE
        painter = self._painter()
        self.assertEqual(painter.wrap_columns("abcdefghij", 4), ["abcd", "efgh", "ij"])
        self.assertEqual(painter.wrap_columns("漢" * 3, 3), ["漢", "漢", "漢"])
        self.assertEqual(painter.wrap_columns("漢", 1), [])
        self.assertEqual(painter.wrap_columns("", 10), [])

        model = MenuModel(painter=painter)
        model.notice = "Language saved."
        model.index = 1
        self.assertIsNone(model.apply_key(curses.KEY_RESIZE, 24))
        self.assertEqual(model.notice, "Language saved.")
        self.assertEqual(model.index, 1)
        self.assertEqual(model.error, "")

        class ResizeScreen:
            def __init__(self, size, keys):
                self.size = size
                self.keys = list(keys)
                self.calls = []
                self.paints = []

            def getmaxyx(self):
                return self.size

            def keypad(self, _flag):
                return None

            def erase(self):
                self.calls = []

            def addstr(self, y, x, text, attr=0):
                self.calls.append((y, x, text, attr))

            def refresh(self):
                self.paints.append((self.size, list(self.calls)))

            def curs_set(self, _visibility):
                return None

            def move(self, _y, _x):
                return None

            def getch(self):
                key, new_size = self.keys.pop(0)
                if new_size is not None:
                    self.size = new_size
                return key

        session = MenuSession(
            "AgentCli",
            "1.0.0",
            on_version=lambda: "1.0.0",
            on_about=lambda: "about",
            on_kind=lambda _kind: None,
            painter=painter,
        )
        session.model.notice = "Language saved."
        session.model.index = 1
        wide_then_narrow = ResizeScreen(
            (24, 80),
            [(curses.KEY_RESIZE, (24, 41)), (-1, None)],
        )
        self.assertEqual(session.run(wide_then_narrow), 0)
        self.assertEqual(session.model.error, "")
        self.assertEqual(session.model.index, 1)
        self.assertEqual(len(wide_then_narrow.paints), 2)
        wide_paint, narrow_paint = wide_then_narrow.paints
        self.assertEqual(wide_paint[0], (24, 80))
        self.assertTrue(any(logged_out in text for _y, _x, text, _attr in wide_paint[1]))
        self.assertTrue(any("Language saved." in text for _y, _x, text, _attr in wide_paint[1]))
        self.assertEqual(narrow_paint[0], (24, 41))
        narrow_text = [text for _y, _x, text, _attr in narrow_paint[1]]
        self.assertTrue(any(text.startswith("backup features are not available for") for text in narrow_text))
        self.assertTrue(any(text.startswith("logged-out environment.") for text in narrow_text))
        self.assertFalse(any(logged_out in text for text in narrow_text))
        self.assertTrue(any("Language saved." in text for text in narrow_text))

        shrink = ResizeScreen(
            (24, 80),
            [
                (curses.KEY_RESIZE, (4, 40)),
                (curses.KEY_RESIZE, (24, 80)),
                (-1, None),
            ],
        )
        session.model.notice = ""
        self.assertEqual(session.run(shrink), 0)
        self.assertEqual(len(shrink.paints), 3)
        too_small = " ".join(text for _y, _x, text, _attr in shrink.paints[1][1])
        self.assertIn("too small", too_small)
        self.assertNotIn(logged_out, too_small)
        restored = " ".join(text for _y, _x, text, _attr in shrink.paints[2][1])
        self.assertIn(logged_out, restored)

        opened_small = ResizeScreen((4, 40), [])
        with self.assertRaises(MenuScreenError):
            session.run(opened_small)
        self.assertEqual(opened_small.paints, [])

        class NoticeScreen:
            def __init__(self):
                self.size = (24, 80)
                self.keys = [curses.KEY_RESIZE, ord("x")]
                self.calls = []
                self.paints = []

            def getmaxyx(self):
                return self.size

            def timeout(self, _ms):
                return None

            def erase(self):
                self.calls = []

            def addstr(self, y, x, text, attr=0):
                self.calls.append((y, x, text, attr))

            def refresh(self):
                self.paints.append((self.size, list(self.calls)))

            def curs_set(self, _visibility):
                return None

            def move(self, _y, _x):
                return None

            def getch(self):
                key = self.keys.pop(0)
                if key == curses.KEY_RESIZE:
                    self.size = (24, 41)
                return key

        notice_screen = NoticeScreen()
        notice_model = MenuModel(painter=painter)
        tui = Tui(app_name="AgentCli", version="1.0.0")
        tui.painter = painter
        tui.notice(notice_screen, notice_model, ["done"], title="result")
        self.assertEqual(len(notice_screen.paints), 2)
        self.assertEqual(notice_screen.paints[0][0], (24, 80))
        self.assertEqual(notice_screen.paints[1][0], (24, 41))
        second = [text for _y, _x, text, _attr in notice_screen.paints[1][1]]
        self.assertTrue(any(text.startswith("logged-out environment.") for text in second))
        self.assertTrue(any("done" in text for text in second))


if __name__ == "__main__":
    unittest.main()
