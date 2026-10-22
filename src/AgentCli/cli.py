#!/usr/bin/env python
# =============================================================================
# AgentCli CLI — text menu and typed verbs.
# Law keys: requirement-python-cli-interface, requirement-python-cli-logging,
#           requirement-python-tui, requirement-python-oop,
#           requirement-python-about, requirement-domain-grok-cli,
#           requirement-python-error-handling, requirement-python-coding-style,
#           requirement-runtime-prerequisites
# Video join is not part of this program. Peer grok stays a separate binary.
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# def main writes ChronicleLogger(...). This module does not construct it
# at import time and does not re-export it.
# =============================================================================
from __future__ import print_function, unicode_literals

import argparse
import json
import sys

from .about_page import AboutPage
from .check_system import CheckSystem
from .grok_domain import GrokDomain
from .output import Output
from .self_management import SelfManage
from .tui import Tui


class Cli:
    """Parser, dispatch, verbs, and the tty gate. One class in this file.

    Identity, verb lists, and suffix sets are attributes of this class.
    Collaborators arrive through the constructor. def main stays beside this class.
    """

    from . import __version__ as VERSION

    APP_NAME = "AgentCli"
    CONSOLE_NAME = "agent-cli"
    PRODUCT_VERBS = (
        "help",
        "version",
        "about",
        "hello",
        "menu",
        "main",
        "ensure",
        "install",
        "uninstall",
        "rc-test",
        "where-is-me",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
        "setup",
        "update-grok",
        "reinstall",
        "run",
        "check-session",
        "backup",
        "sync-auth",
        "sync-auth-from-remote",
        "sync-auth-to-remote",
        "add-crontab",
        "print-sudoers",
        "print-sudoers-install-script",
        "remove-project-sudoers",
        "generate-sudoer-request",
        "submit-sudoer-request",
    )
    MENU_KINDS = (
        "backup",
        "sync-auth",
        "sync-auth-from-remote",
        "sync-auth-to-remote",
        "add-crontab",
        "setup",
        "reinstall",
        "update-grok",
        "run",
        "check-session",
        "where-is-me",
        "print-sudoers",
        "print-sudoers-install-script",
        "remove-project-sudoers",
        "generate-sudoer-request",
        "submit-sudoer-request",
    )
    SCREEN_VERBS = ("about", "menu", "main")
    LIFECYCLE_VERBS = (
        "version",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    AUTHOR_NAME = "cloudgen"
    AUTHOR_EMAIL = "wongcf22@gmail.com"
    HOMEPAGE = "https://github.com/cloudgen/AgentCli"
    LAST_UPDATE = "2026-10-12"
    DOWNLOAD_URL = ""
    BASIC_USAGE = "agent-cli"

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.app_name = Cli.APP_NAME
        self.version = Cli.VERSION
        self.about = AboutPage(
            CheckSystem(
                logger=logger,
                app_name=Cli.APP_NAME,
                version=Cli.VERSION,
                console_name=Cli.CONSOLE_NAME,
            ),
            Cli.APP_NAME,
            Cli.VERSION,
            Cli.AUTHOR_NAME,
            Cli.LAST_UPDATE,
            Cli.HOMEPAGE,
            Cli.DOWNLOAD_URL,
            Cli.BASIC_USAGE,
            Cli.CONSOLE_NAME,
            logger=logger,
        )
        self.self_manage = SelfManage(Cli.APP_NAME, Cli.VERSION, logger=logger)
        self.output = Output()
        self.domain = GrokDomain(output=self.output, logger=logger, version=Cli.VERSION)
        self.tui = Tui(self, logger=logger)

    @staticmethod
    def stdout_is_tty():
        """General Purpose: Whether the text screen can be drawn on this stdout."""
        try:
            return sys.stdout.isatty()
        except Exception:
            return False

    @staticmethod
    def opens_text_screen(argv):
        """
        General Purpose: Whether this argv draws the text screen.

        The real parser has not run yet. This walk only decides is_quiet.
        Help, version, hello, domain verbs, and the pip verbs do not draw the screen.
        Empty argv and about do, when stdout is a terminal and --json is absent.
        hello prints the welcome line and does not draw the screen.
        """
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        if "--json" in argv or "--help" in argv or "-h" in argv or "--version" in argv:
            return False
        if not Cli.stdout_is_tty():
            return False
        verb = None
        saw_force = False
        for token in argv:
            if token in ("--force", "--debug", "--quiet"):
                if token == "--force":
                    saw_force = True
                continue
            if token.startswith("-"):
                return False
            if verb is None:
                verb = token
                continue
            return False
        if saw_force and verb != "self-uninstall":
            return False
        if verb in Cli.SCREEN_VERBS:
            return True
        return verb is None

    def report_error(self, message, nxt):
        """User-visible failure plus the same fact on the logger when one exists."""
        if self.logger is not None:
            self.logger.log_message(
                "{0} Next: {1}".format(message, nxt),
                level="ERROR",
                component="main",
            )
        print("ERROR: {0}".format(message), file=sys.stderr)
        print("   Next: {0}".format(nxt), file=sys.stderr)
        return 1

    def build_parser(self):
        """
        General Purpose: One optional product verb. No file-operand flags.
        help is also --help. --force belongs only to self-uninstall.
        """
        parser = argparse.ArgumentParser(
            prog=Cli.CONSOLE_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=(
                "{0} — install and run xAI grok, and back up its auth files.\n"
                "With no arguments on a terminal, opens the text menu.\n"
                "With no arguments and no terminal, prints this help and stops.\n"
                "--json with no verb prints JSON help and does not open the menu.\n"
                "hello prints a welcome line and does not draw the menu.\n"
                "Menu row 1 is grok-auth. language is menu row 7 and is not a verb.\n"
                "This program does not join media or list files in this folder.\n"
                "version-check runs: python -m pip index versions {0}\n"
                "self-update runs: python -m pip install --upgrade {0}\n"
                "self-install runs: python -m pip install {0}\n"
                "self-uninstall runs: python -m pip uninstall -y {0}\n"
                "and needs --force. Empty arguments do not install or update.\n"
                "Operational verbs include install, setup, and self-install.\n"
                "Test-purpose, apart from those: rc-test --root DIR "
                "--file bashrc|zshenv|zprofile|profile|fish|ash "
                "--case create|modify|noop.\n"
                "Environment: BASHRC, ZSHENV, ZPROFILE, ZSHRC, PROFILE, FISH_CONFIG, USER_BIN."
                .format(Cli.APP_NAME)
            ),
        )
        parser.add_argument(
            "verb",
            nargs="?",
            default=None,
            metavar="verb",
            help=(
                "Product verb. language and Exit are menu-only."
            ),
        )
        parser.add_argument(
            "--version",
            action="version",
            version="{0} {1}".format(Cli.APP_NAME, Cli.VERSION),
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Confirm self-uninstall. Required on the command line.",
        )
        return parser

    def _page(self, text):
        print(text)
        return 0

    def _verb_hello(self):
        """Welcome on the terminal. Does not draw the menu."""
        print(self.tui.hello_text())
        return 0

    def _unknown_verb(self, token):
        names = ", ".join(Cli.PRODUCT_VERBS)
        return self.report_error(
            "Unknown verb '{0}'.".format(token),
            "{0} help — verbs: {1}".format(Cli.CONSOLE_NAME, names),
        )

    def _walk(self, argv):
        """Flags and one verb. Extra tokens are operands, not a second verb."""
        parsed = {
            "json": False,
            "force": False,
            "verb": None,
            "extra": [],
            "help": False,
            "version": False,
            "error": "",
            "root": "",
            "file": "",
            "case": "",
            "feature": "",
        }
        valued = {
            "--root": "root",
            "--file": "file",
            "--case": "case",
            "--feature": "feature",
        }
        index = 0
        tokens = list(argv)
        while index < len(tokens):
            token = tokens[index]
            if token in valued:
                if index + 1 >= len(tokens) or str(tokens[index + 1]).startswith("-"):
                    parsed["error"] = token
                    return parsed
                parsed[valued[token]] = tokens[index + 1]
                index += 2
                continue
            if token == "--json":
                parsed["json"] = True
            elif token == "--force":
                parsed["force"] = True
            elif token in ("--debug", "--quiet"):
                pass
            elif token in ("-h", "--help"):
                parsed["help"] = True
            elif token == "--version":
                parsed["version"] = True
            elif token.startswith("-"):
                parsed["error"] = token
                return parsed
            elif parsed["verb"] is None:
                parsed["verb"] = token
            else:
                parsed["extra"].append(token)
            index += 1
        return parsed

    def _json_help(self):
        body = {
            "type": "help",
            "message": "agent-cli help",
            "verbs": list(Cli.PRODUCT_VERBS),
        }
        print(json.dumps(body, ensure_ascii=False))
        return 0

    def _json_about(self):
        from .storage import Storage

        store = Storage()
        fields = store.about_fields()
        body = {
            "type": "about",
            "message": "Install and run xAI grok, and back up its auth files.",
            "name": Cli.APP_NAME,
            "version": Cli.VERSION,
        }
        body.update(fields)
        print(json.dumps(body, ensure_ascii=False))
        return 0

    def _dispatch(self, parsed):
        """One product verb, the front board, or a fail-closed stop."""
        verb = parsed["verb"]
        if parsed["json"]:
            self.output.json_mode = True
            self.domain.output = self.output
        if parsed["force"] and verb not in (
            "self-uninstall",
            "uninstall",
            "setup",
            "reinstall",
            "remove-project-sudoers",
        ):
            return self.report_error(
                "--force is only for self-uninstall.",
                "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
            )
        if verb != "rc-test" and (parsed["root"] or parsed["file"] or parsed["case"] or parsed["feature"]):
            return self.report_error(
                "--root, --file, --case, and --feature belong to rc-test.",
                "{0} rc-test --root DIR --file zprofile --case create".format(Cli.CONSOLE_NAME),
            )
        if verb == "about":
            if parsed["json"]:
                return self._json_about()
            result = self.tui.about_on_screen()
            if isinstance(result, int):
                return result
            return self._page(result)
        if verb == "hello":
            return self._verb_hello()
        if verb == "version":
            return self._page(self.self_manage.local_version())
        if verb == "self-uninstall":
            if not parsed["force"]:
                return self.report_error(
                    "self-uninstall removes this package with pip.",
                    "{0} self-uninstall --force".format(Cli.CONSOLE_NAME),
                )
            self.domain.startup.cleanup_path()
            return self.self_manage.emit(verb)
        if verb == "rc-test":
            return self.domain.rc_test(
                parsed["root"],
                parsed["file"] or "bashrc",
                parsed["case"] or "create",
                parsed["feature"],
            )
        if verb in ("version-check", "self-update", "self-install"):
            return self.self_manage.emit(verb)
        if verb in ("menu", "main") or verb is None:
            if parsed["json"] and verb is None:
                return self._json_help()
            if not self.stdout_is_tty():
                if parsed["json"]:
                    return self._json_help()
                self.build_parser().print_help()
                return 0
            action = self.tui.open_text_menu()
            if action == "missing":
                return 1
            return 0
        if verb in Cli.PRODUCT_VERBS:
            return self.domain.dispatch(verb, parsed["extra"], force=parsed["force"])
        return self._unknown_verb(verb)

    def run(self, argv=None):
        """One job. def main already wrote ChronicleLogger(...) and passed it in."""
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        parsed = self._walk(argv)
        if parsed["error"]:
            return self.report_error(
                "Unknown flag '{0}'.".format(parsed["error"]),
                "{0} help".format(Cli.CONSOLE_NAME),
            )
        if parsed["help"] or parsed["verb"] == "help":
            if parsed["json"]:
                return self._json_help()
            self.build_parser().print_help()
            return 0
        if parsed["version"]:
            return self._page("{0} {1}".format(Cli.APP_NAME, Cli.VERSION))
        return self._dispatch(parsed)


def main(argv=None, basedir="", logdir=""):
    """This function instantiates ChronicleLogger. The statement below is the construct."""
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        sys.stderr.write(
            'ChronicleLogger is required. Next step: python -m pip install "ChronicleLogger>=1.3.1"\n'
        )
        return 1

    from AgentCli import __version__

    screen = Cli.opens_text_screen(argv)
    logger = ChronicleLogger(
        logname=Cli.APP_NAME,
        is_quiet=screen,
        basedir=basedir,
        logdir=logdir,
    )
    appname = logger.logName()
    resolved_base = logger.baseDir()
    logger.logDir()

    if logger.isDebug():
        logger.log_message(
            "{0} v{1} ({2})".format(appname, __version__, __file__),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(resolved_base),
            level="DEBUG",
            component="main",
        )
        logger.log_message("debug mode", component="main")

    app = Cli(logger)
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main())
