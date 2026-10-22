# =============================================================================
# Menu language for the text menu.
# requirement-python-cli-language — codes, the language leaf, and menu copy.
# requirement-python-oop — class MenuLanguage.
# =============================================================================
from __future__ import annotations

import os


class MenuLanguage:
    """The thirteen menu languages, the saved code, and the words the menu prints.

    English is the default when the leaf is missing, empty, or not one of the
    codes. LANG is not read. AGENT_CLI_LANG wins at startup and does not write
    the leaf. A menu pick writes the leaf and updates this process.
    """

    CODES = (
        ("en", "English", 80),
        ("zh-Hans", "简体中文", 81),
        ("zh-Hant", "繁體中文", 82),
        ("es", "Español", 83),
        ("ar", "العربية", 84),
        ("fr", "Français", 85),
        ("pt", "Português", 86),
        ("ru", "Русский", 87),
        ("de", "Deutsch", 88),
        ("ja", "日本語", 89),
        ("ko", "한국어", 90),
        ("nl", "Nederlands", 91),
        ("el", "Ελληνικά", 92),
    )
    # Assigned 80–92. Reserved and not printed: 70–79 and 93–98.
    BLOCK_FIRST = 70
    BLOCK_LAST = 98
    APP_DIR = "agent-cli"
    LEAF_NAME = "language"

    def __init__(self, logger=None, home=None) -> None:
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MenuLanguage")
        if home is None:
            home = os.environ.get("HOME", "")
        self.home = home
        self._code = "en"
        self.load()

    def codes(self) -> tuple:
        return tuple(code for code, _name, _number in self.CODES)

    def endonym(self, code: str) -> str:
        for item, name, _number in self.CODES:
            if item == code:
                return name
        return ""

    def number_for(self, code: str) -> int | None:
        for item, _name, number in self.CODES:
            if item == code:
                return number
        return None

    def code_for_number(self, number: int) -> str | None:
        for code, _name, item in self.CODES:
            if item == number:
                return code
        return None

    def leaf_path(self) -> str:
        """The language leaf. Empty when this process has no home directory."""
        if not self.home:
            return ""
        return os.path.join(self.home, ".local", self.APP_DIR, self.LEAF_NAME)

    def code(self) -> str:
        return self._code

    def load(self) -> None:
        """Pick the code for this process. Does not write the leaf.

        AGENT_CLI_LANG wins when it is one of the thirteen codes. Otherwise the
        first line of the leaf is used. A missing, empty, or other line is English.
        An other line is not rewritten.
        """
        forced = os.environ.get("AGENT_CLI_LANG", "")
        if forced in self.codes():
            self._code = forced
            return
        self._code = self._read_leaf()

    def _read_leaf(self) -> str:
        path = self.leaf_path()
        if not path or not os.path.isfile(path):
            return "en"
        try:
            with open(path, "r", encoding="utf-8") as handle:
                line = handle.readline()
        except OSError:
            return "en"
        line = line.replace("\r", "").strip()
        if line in self.codes():
            return line
        return "en"

    def save(self, code: str) -> str:
        """Write one code and switch this process. A failed write keeps the old code.

        The message is in the language that is current after a success, and in
        the language that was current before a failed write.
        """
        if code not in self.codes():
            return self.text("save_failed")
        path = self.leaf_path()
        if not path:
            return self.text("save_failed")
        previous = self._code
        try:
            folder = os.path.dirname(path)
            os.makedirs(folder, mode=0o700, exist_ok=True)
            os.chmod(folder, 0o700)
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            try:
                os.write(descriptor, (code + "\n").encode("utf-8"))
            finally:
                os.close(descriptor)
            os.chmod(path, 0o600)
        except OSError:
            self._code = previous
            return self.text("save_failed")
        self._code = code
        return self.text("saved")

    def text(self, key: str) -> str:
        block = _TEXTS.get(self._code) or _TEXTS["en"]
        found = block.get(key)
        if found is None:
            found = _TEXTS["en"].get(key, "")
        return found

    def path_label(self) -> str:
        """The path-line word for the selected code. The directory is not translated."""
        return self.text("path")

    def lang_long(self, endonym: str) -> str:
        return self.text("lang_long").format(name=endonym)

    def row_short(self, kind: str, english: str) -> str:
        key = _SHORT_KEY.get(kind)
        if key is None:
            return english
        return self.text(key)

    def row_long(self, kind: str, english: str) -> str:
        key = _LONG_KEY.get(kind)
        if key is None:
            return english
        return self.text(key)

    def token_kind(self, token: str, layer: str) -> str | None:
        """A typed word that is not the row currently on screen.

        The language board accepts the code tokens. The front board accepts
        every category short. Leaf verbs stay the English token on the row.
        """
        if layer == "lang":
            code = _LANG_TOKENS.get(token)
            if code is not None:
                return "set-" + code
            return None
        if layer == "front":
            return _FRONT_TOKENS.get(token)
        return None


_SHORT_KEY = {
    "language": "language_short",
    "system-log": "system_log_short",
    "self-management": "self_short",
    "exit": "exit_short",
    "back": "back_short",
}

_LONG_KEY = {
    "hello": "hello_long",
    "language": "language_long",
    "system-log": "system_log_long",
    "self-management": "self_long",
    "exit": "exit_long",
    "back": "back_long",
    "view-log": "view_long",
    "clear-log": "clear_long",
    "log-folder": "folder_long",
    "version": "version_long",
    "about": "about_long",
    "version-check": "version_check_long",
    "self-update": "self_update_long",
    "self-uninstall": "self_uninstall_long",
    "self-install": "self_install_long",
    "where-is-me": "where_is_me_long",
}

_LANG_TOKENS = {
    "english": "en",
    "en": "en",
    "English": "en",
    "simplified-chinese": "zh-Hans",
    "zh-hans": "zh-Hans",
    "zh-Hans": "zh-Hans",
    "简体中文": "zh-Hans",
    "traditional-chinese": "zh-Hant",
    "zh-hant": "zh-Hant",
    "zh-Hant": "zh-Hant",
    "繁體中文": "zh-Hant",
    "spanish": "es",
    "es": "es",
    "Español": "es",
    "español": "es",
    "arabic": "ar",
    "ar": "ar",
    "العربية": "ar",
    "عربي": "ar",
    "french": "fr",
    "fr": "fr",
    "Français": "fr",
    "français": "fr",
    "portuguese": "pt",
    "pt": "pt",
    "Português": "pt",
    "português": "pt",
    "portugues": "pt",
    "russian": "ru",
    "ru": "ru",
    "Русский": "ru",
    "русский": "ru",
    "german": "de",
    "de": "de",
    "Deutsch": "de",
    "deutsch": "de",
    "japanese": "ja",
    "ja": "ja",
    "日本語": "ja",
    "korean": "ko",
    "ko": "ko",
    "한국어": "ko",
    "dutch": "nl",
    "nl": "nl",
    "Nederlands": "nl",
    "nederlands": "nl",
    "greek": "el",
    "el": "el",
    "Ελληνικά": "el",
    "ελληνικά": "el",
}

_FRONT_TOKENS = {
    "grok-auth": "grok-auth",
    "sudoers": "sudoers",
    "run": "run",
    "language": "language",
    "語言": "language",
    "语言": "language",
    "idioma": "language",
    "langue": "language",
    "Sprache": "language",
    "sprache": "language",
    "言語": "language",
    "언어": "language",
    "لغة": "language",
    "язык": "language",
    "taal": "language",
    "γλώσσα": "language",
    "system-log": "system-log",
    "系统日志": "system-log",
    "系統日誌": "system-log",
    "registro": "system-log",
    "journal": "system-log",
    "Systemprotokoll": "system-log",
    "システムログ": "system-log",
    "시스템 로그": "system-log",
    "registo": "system-log",
    "системный журнал": "system-log",
    "systeemlog": "system-log",
    "αρχείο καταγραφής": "system-log",
    "سجل النظام": "system-log",
    "self-management": "self-management",
    "自我管理": "self-management",
    "autogestión": "self-management",
    "autogestion": "self-management",
    "autogestão": "self-management",
    "Selbstverwaltung": "self-management",
    "selbstverwaltung": "self-management",
    "自己管理": "self-management",
    "자기관리": "self-management",
    "إدارة ذاتية": "self-management",
    "самоуправление": "self-management",
    "zelfbeheer": "self-management",
    "αυτοδιαχείριση": "self-management",
    "hello": "hello",
    "Exit": "exit",
    "离开": "exit",
    "離開": "exit",
    "Salir": "exit",
    "خروج": "exit",
    "Quitter": "exit",
    "Sair": "exit",
    "Выход": "exit",
    "Beenden": "exit",
    "終了": "exit",
    "종료": "exit",
    "Afsluiten": "exit",
    "Έξοδος": "exit",
}

_TEXTS = {
    "en": {
        "path": "Path",
        "language_short": "language",
        "language_long": "display language for this menu",
        "system_log_short": "system-log",
        "system_log_long": "view, clear, and the log folder",
        "self_short": "self-management",
        "self_long": "check, update, or remove this package",
        "where_is_me_long": "show running and install paths",
        "exit_short": "Exit",
        "exit_long": "leave",
        "back_short": "Back",
        "back_long": "return to the main menu",
        "hello_long": "show a welcome message",
        "view_long": "list a log file and show it",
        "clear_long": "empty one log file",
        "folder_long": "show the log folder",
        "version_long": "show the installed version",
        "about_long": "version and this computer",
        "version_check_long": "compare this install with pip",
        "self_update_long": "upgrade this package with pip",
        "self_uninstall_long": "remove this package with pip",
        "self_install_long": "install this package with pip",
        "title_main": "main menu",
        "title_language": "language",
        "title_log": "system-log",
        "title_self": "self-management",
        "invalid": "That choice is not on this list. Pick a listed number.",
        "saved": "Menu language is English",
        "save_failed": "Could not save the menu language",
        "lang_long": "use {name} for this menu",
    },
    "zh-Hans": {
        "path": "路径",
        "language_short": "语言",
        "language_long": "此菜单的显示语言",
        "system_log_short": "系统日志",
        "system_log_long": "查看、清空，以及日志文件夹",
        "self_short": "自我管理",
        "self_long": "检查、更新，或移除此包",
        "where_is_me_long": "显示运行路径和安装路径",
        "exit_short": "离开",
        "exit_long": "离开",
        "back_short": "返回",
        "back_long": "返回主菜单",
        "hello_long": "显示一条欢迎消息",
        "view_long": "列出日志文件并显示",
        "clear_long": "清空一个日志文件",
        "folder_long": "显示日志文件夹",
        "version_long": "显示已安装的版本",
        "about_long": "版本，以及这台计算机",
        "version_check_long": "用 pip 比较此安装",
        "self_update_long": "用 pip 升级此包",
        "self_uninstall_long": "用 pip 移除此包",
        "self_install_long": "用 pip 安装此包",
        "title_main": "主菜单",
        "title_language": "语言",
        "title_log": "系统日志",
        "title_self": "自我管理",
        "invalid": "这个选择不在列表上。请挑选列出的号码。",
        "saved": "菜单语言是简体中文",
        "save_failed": "无法保存菜单语言",
        "lang_long": "此菜单使用{name}",
    },
    "zh-Hant": {
        "path": "路徑",
        "language_short": "語言",
        "language_long": "這個選單的顯示語言",
        "system_log_short": "系統日誌",
        "system_log_long": "查看、清空，以及日誌資料夾",
        "self_short": "自我管理",
        "self_long": "檢查、更新，或移除此套件",
        "where_is_me_long": "顯示執行路徑和安裝路徑",
        "exit_short": "離開",
        "exit_long": "離開",
        "back_short": "返回",
        "back_long": "返回主選單",
        "hello_long": "顯示一則歡迎訊息",
        "view_long": "列出日誌檔並顯示",
        "clear_long": "清空一個日誌檔",
        "folder_long": "顯示日誌資料夾",
        "version_long": "顯示已安裝的版本",
        "about_long": "版本，以及這台電腦",
        "version_check_long": "用 pip 比較此安裝",
        "self_update_long": "用 pip 升級此套件",
        "self_uninstall_long": "用 pip 移除此套件",
        "self_install_long": "用 pip 安裝此套件",
        "title_main": "主選單",
        "title_language": "語言",
        "title_log": "系統日誌",
        "title_self": "自我管理",
        "invalid": "這個選擇不在清單上。請挑選列出的號碼。",
        "saved": "選單語言是繁體中文",
        "save_failed": "無法儲存選單語言",
        "lang_long": "這個選單使用{name}",
    },
    "es": {
        "path": "Ruta",
        "language_short": "idioma",
        "language_long": "idioma de este menú",
        "system_log_short": "registro",
        "system_log_long": "ver, vaciar y la carpeta de registro",
        "self_short": "autogestión",
        "self_long": "comprobar, actualizar o quitar este paquete",
        "where_is_me_long": "mostrar las rutas de ejecución e instalación",
        "exit_short": "Salir",
        "exit_long": "salir",
        "back_short": "Atrás",
        "back_long": "volver al menú principal",
        "hello_long": "muestra un mensaje de bienvenida",
        "view_long": "listar un archivo de registro y mostrarlo",
        "clear_long": "vaciar un archivo de registro",
        "folder_long": "mostrar la carpeta de registro",
        "version_long": "mostrar la versión instalada",
        "about_long": "versión y este equipo",
        "version_check_long": "comparar esta instalación con pip",
        "self_update_long": "actualizar este paquete con pip",
        "self_uninstall_long": "quitar este paquete con pip",
        "self_install_long": "instalar este paquete con pip",
        "title_main": "menú principal",
        "title_language": "idioma",
        "title_log": "registro",
        "title_self": "autogestión",
        "invalid": "Esa opción no está en la lista. Elija un número de la lista.",
        "saved": "El idioma del menú es español",
        "save_failed": "No se pudo guardar el idioma del menú",
        "lang_long": "usar {name} en este menú",
    },
    "ar": {
        "path": "المسار",
        "language_short": "لغة",
        "language_long": "لغة العرض لهذه القائمة",
        "system_log_short": "سجل النظام",
        "system_log_long": "عرض ومسح ومجلد السجل",
        "self_short": "إدارة ذاتية",
        "self_long": "فحص أو تحديث أو إزالة هذه الحزمة",
        "where_is_me_long": "عرض مساري التشغيل والتثبيت",
        "exit_short": "خروج",
        "exit_long": "خروج",
        "back_short": "رجوع",
        "back_long": "العودة إلى القائمة الرئيسية",
        "hello_long": "اعرض رسالة ترحيب",
        "view_long": "سرد ملف سجل وعرضه",
        "clear_long": "إفراغ ملف سجل واحد",
        "folder_long": "عرض مجلد السجل",
        "version_long": "عرض الإصدار المثبّت",
        "about_long": "الإصدار وهذا الجهاز",
        "version_check_long": "قارن هذا التثبيت مع pip",
        "self_update_long": "ترقية هذه الحزمة بـ pip",
        "self_uninstall_long": "إزالة هذه الحزمة بـ pip",
        "self_install_long": "تثبيت هذه الحزمة بـ pip",
        "title_main": "القائمة الرئيسية",
        "title_language": "لغة",
        "title_log": "سجل النظام",
        "title_self": "إدارة ذاتية",
        "invalid": "هذا الاختيار ليس في القائمة. اختر رقماً معروضاً.",
        "saved": "لغة القائمة هي العربية",
        "save_failed": "تعذر حفظ لغة القائمة",
        "lang_long": "استخدام {name} لهذه القائمة",
    },
    "fr": {
        "path": "Chemin",
        "language_short": "langue",
        "language_long": "langue d'affichage de ce menu",
        "system_log_short": "journal",
        "system_log_long": "voir, vider et le dossier du journal",
        "self_short": "autogestion",
        "self_long": "vérifier, mettre à jour ou retirer ce paquet",
        "where_is_me_long": "afficher les chemins d'exécution et d'installation",
        "exit_short": "Quitter",
        "exit_long": "quitter",
        "back_short": "Retour",
        "back_long": "revenir au menu principal",
        "hello_long": "afficher un message de bienvenue",
        "view_long": "lister un fichier journal et l'afficher",
        "clear_long": "vider un fichier journal",
        "folder_long": "afficher le dossier du journal",
        "version_long": "afficher la version installée",
        "about_long": "version et cet ordinateur",
        "version_check_long": "comparer cette installation avec pip",
        "self_update_long": "mettre à jour ce paquet avec pip",
        "self_uninstall_long": "retirer ce paquet avec pip",
        "self_install_long": "installer ce paquet avec pip",
        "title_main": "menu principal",
        "title_language": "langue",
        "title_log": "journal",
        "title_self": "autogestion",
        "invalid": "Ce choix n'est pas dans la liste. Choisissez un numéro affiché.",
        "saved": "La langue du menu est le français",
        "save_failed": "Impossible d'enregistrer la langue du menu",
        "lang_long": "utiliser {name} pour ce menu",
    },
    "pt": {
        "path": "Caminho",
        "language_short": "idioma",
        "language_long": "idioma deste menu",
        "system_log_short": "registo",
        "system_log_long": "ver, esvaziar e a pasta de registo",
        "self_short": "autogestão",
        "self_long": "verificar, atualizar ou remover este pacote",
        "where_is_me_long": "mostrar os caminhos de execução e de instalação",
        "exit_short": "Sair",
        "exit_long": "sair",
        "back_short": "Voltar",
        "back_long": "voltar ao menu principal",
        "hello_long": "mostra uma mensagem de boas-vindas",
        "view_long": "listar um ficheiro de registo e mostrá-lo",
        "clear_long": "esvaziar um ficheiro de registo",
        "folder_long": "mostrar a pasta de registo",
        "version_long": "mostrar a versão instalada",
        "about_long": "versão e este computador",
        "version_check_long": "comparar esta instalação com o pip",
        "self_update_long": "atualizar este pacote com o pip",
        "self_uninstall_long": "remover este pacote com o pip",
        "self_install_long": "instalar este pacote com o pip",
        "title_main": "menu principal",
        "title_language": "idioma",
        "title_log": "registo",
        "title_self": "autogestão",
        "invalid": "Essa escolha não está na lista. Escolha um número da lista.",
        "saved": "O idioma do menu é português",
        "save_failed": "Não foi possível guardar o idioma do menu",
        "lang_long": "usar {name} neste menu",
    },
    "ru": {
        "path": "Путь",
        "language_short": "язык",
        "language_long": "язык этого меню",
        "system_log_short": "системный журнал",
        "system_log_long": "просмотр, очистка и папка журнала",
        "self_short": "самоуправление",
        "self_long": "проверить, обновить или удалить этот пакет",
        "where_is_me_long": "показать пути запуска и установки",
        "exit_short": "Выход",
        "exit_long": "выход",
        "back_short": "Назад",
        "back_long": "вернуться в главное меню",
        "hello_long": "показать приветствие",
        "view_long": "показать список файлов журнала и открыть один",
        "clear_long": "очистить один файл журнала",
        "folder_long": "показать папку журнала",
        "version_long": "показать установленную версию",
        "about_long": "версия и этот компьютер",
        "version_check_long": "сравнить эту установку с pip",
        "self_update_long": "обновить этот пакет через pip",
        "self_uninstall_long": "удалить этот пакет через pip",
        "self_install_long": "установить этот пакет через pip",
        "title_main": "главное меню",
        "title_language": "язык",
        "title_log": "системный журнал",
        "title_self": "самоуправление",
        "invalid": "Этого пункта нет в списке. Выберите номер из списка.",
        "saved": "Язык меню — русский",
        "save_failed": "Не удалось сохранить язык меню",
        "lang_long": "использовать {name} для этого меню",
    },
    "de": {
        "path": "Pfad",
        "language_short": "Sprache",
        "language_long": "Anzeigesprache für dieses Menü",
        "system_log_short": "Systemprotokoll",
        "system_log_long": "ansehen, leeren und der Protokollordner",
        "self_short": "Selbstverwaltung",
        "self_long": "prüfen, aktualisieren oder dieses Paket entfernen",
        "where_is_me_long": "Lauf- und Installationspfade anzeigen",
        "exit_short": "Beenden",
        "exit_long": "beenden",
        "back_short": "Zurück",
        "back_long": "zurück zum Hauptmenü",
        "hello_long": "eine Willkommensnachricht anzeigen",
        "view_long": "eine Protokolldatei auflisten und anzeigen",
        "clear_long": "eine Protokolldatei leeren",
        "folder_long": "den Protokollordner anzeigen",
        "version_long": "die installierte Version anzeigen",
        "about_long": "Version und dieser Computer",
        "version_check_long": "diese Installation mit pip vergleichen",
        "self_update_long": "dieses Paket mit pip aktualisieren",
        "self_uninstall_long": "dieses Paket mit pip entfernen",
        "self_install_long": "dieses Paket mit pip installieren",
        "title_main": "Hauptmenü",
        "title_language": "Sprache",
        "title_log": "Systemprotokoll",
        "title_self": "Selbstverwaltung",
        "invalid": "Diese Wahl steht nicht auf der Liste. Wählen Sie eine angezeigte Nummer.",
        "saved": "Die Menüsprache ist Deutsch",
        "save_failed": "Die Menüsprache konnte nicht gespeichert werden",
        "lang_long": "{name} für dieses Menü verwenden",
    },
    "ja": {
        "path": "パス",
        "language_short": "言語",
        "language_long": "このメニューの表示言語",
        "system_log_short": "システムログ",
        "system_log_long": "表示、消去、ログフォルダ",
        "self_short": "自己管理",
        "self_long": "確認、更新、またはこのパッケージの削除",
        "where_is_me_long": "実行中のパスとインストール先を表示する",
        "exit_short": "終了",
        "exit_long": "終了",
        "back_short": "戻る",
        "back_long": "メインメニューに戻る",
        "hello_long": "歓迎のメッセージを表示する",
        "view_long": "ログファイルを一覧して表示する",
        "clear_long": "ログファイルを1つ空にする",
        "folder_long": "ログフォルダを表示する",
        "version_long": "インストール済みのバージョンを表示する",
        "about_long": "バージョンとこのコンピュータ",
        "version_check_long": "このインストールを pip と比較する",
        "self_update_long": "pip でこのパッケージを更新する",
        "self_uninstall_long": "pip でこのパッケージを削除する",
        "self_install_long": "pip でこのパッケージをインストールする",
        "title_main": "メインメニュー",
        "title_language": "言語",
        "title_log": "システムログ",
        "title_self": "自己管理",
        "invalid": "その選択は一覧にありません。表示された番号を選んでください。",
        "saved": "メニューの言語は日本語",
        "save_failed": "メニューの言語を保存できませんでした",
        "lang_long": "このメニューで{name}を使う",
    },
    "ko": {
        "path": "경로",
        "language_short": "언어",
        "language_long": "이 메뉴의 표시 언어",
        "system_log_short": "시스템 로그",
        "system_log_long": "보기, 비우기, 로그 폴더",
        "self_short": "자기관리",
        "self_long": "확인, 업데이트, 또는 이 패키지 제거",
        "where_is_me_long": "실행 경로와 설치 경로를 표시합니다",
        "exit_short": "종료",
        "exit_long": "종료",
        "back_short": "뒤로",
        "back_long": "주 메뉴로 돌아가기",
        "hello_long": "환영 메시지를 보여 줍니다",
        "view_long": "로그 파일을 나열하고 표시합니다",
        "clear_long": "로그 파일 하나를 비웁니다",
        "folder_long": "로그 폴더를 표시합니다",
        "version_long": "설치된 버전을 표시합니다",
        "about_long": "버전과 이 컴퓨터",
        "version_check_long": "이 설치를 pip과 비교합니다",
        "self_update_long": "pip으로 이 패키지를 업그레이드합니다",
        "self_uninstall_long": "pip으로 이 패키지를 제거합니다",
        "self_install_long": "pip으로 이 패키지를 설치합니다",
        "title_main": "주 메뉴",
        "title_language": "언어",
        "title_log": "시스템 로그",
        "title_self": "자기관리",
        "invalid": "그 선택은 목록에 없습니다. 표시된 번호를 고르세요.",
        "saved": "메뉴 언어는 한국어",
        "save_failed": "메뉴 언어를 저장하지 못했습니다",
        "lang_long": "이 메뉴에서 {name} 사용",
    },
    "nl": {
        "path": "Pad",
        "language_short": "taal",
        "language_long": "weergavetaal voor dit menu",
        "system_log_short": "systeemlog",
        "system_log_long": "bekijken, legen en de logmap",
        "self_short": "zelfbeheer",
        "self_long": "controleren, bijwerken of dit pakket verwijderen",
        "where_is_me_long": "toon de actieve en installatiepaden",
        "exit_short": "Afsluiten",
        "exit_long": "afsluiten",
        "back_short": "Terug",
        "back_long": "terug naar het hoofdmenu",
        "hello_long": "toon een welkomstbericht",
        "view_long": "een logbestand tonen en weergeven",
        "clear_long": "één logbestand legen",
        "folder_long": "de logmap tonen",
        "version_long": "de geïnstalleerde versie tonen",
        "about_long": "versie en deze computer",
        "version_check_long": "deze installatie met pip vergelijken",
        "self_update_long": "dit pakket met pip bijwerken",
        "self_uninstall_long": "dit pakket met pip verwijderen",
        "self_install_long": "dit pakket met pip installeren",
        "title_main": "hoofdmenu",
        "title_language": "taal",
        "title_log": "systeemlog",
        "title_self": "zelfbeheer",
        "invalid": "Die keuze staat niet op de lijst. Kies een nummer van de lijst.",
        "saved": "De menutaal is Nederlands",
        "save_failed": "De menutaal kon niet worden opgeslagen",
        "lang_long": "{name} voor dit menu gebruiken",
    },
    "el": {
        "path": "Διαδρομή",
        "language_short": "γλώσσα",
        "language_long": "γλώσσα εμφάνισης για αυτό το μενού",
        "system_log_short": "αρχείο καταγραφής",
        "system_log_long": "προβολή, εκκαθάριση και ο φάκελος καταγραφής",
        "self_short": "αυτοδιαχείριση",
        "self_long": "έλεγχος, ενημέρωση ή αφαίρεση αυτού του πακέτου",
        "where_is_me_long": "εμφάνιση διαδρομών εκτέλεσης και εγκατάστασης",
        "exit_short": "Έξοδος",
        "exit_long": "έξοδος",
        "back_short": "Πίσω",
        "back_long": "επιστροφή στο κύριο μενού",
        "hello_long": "δείξε ένα μήνυμα καλωσορίσματος",
        "view_long": "λίστα αρχείων καταγραφής και εμφάνιση",
        "clear_long": "εκκένωση ενός αρχείου καταγραφής",
        "folder_long": "εμφάνιση του φακέλου καταγραφής",
        "version_long": "εμφάνιση της εγκατεστημένης έκδοσης",
        "about_long": "έκδοση και αυτός ο υπολογιστής",
        "version_check_long": "σύγκριση αυτής της εγκατάστασης με το pip",
        "self_update_long": "αναβάθμιση αυτού του πακέτου με το pip",
        "self_uninstall_long": "αφαίρεση αυτού του πακέτου με το pip",
        "self_install_long": "εγκατάσταση αυτού του πακέτου με το pip",
        "title_main": "κύριο μενού",
        "title_language": "γλώσσα",
        "title_log": "αρχείο καταγραφής",
        "title_self": "αυτοδιαχείριση",
        "invalid": "Αυτή η επιλογή δεν είναι στη λίστα. Διάλεξε έναν αριθμό της λίστας.",
        "saved": "Η γλώσσα του μενού είναι ελληνικά",
        "save_failed": "Δεν ήταν δυνατή η αποθήκευση της γλώσσας του μενού",
        "lang_long": "χρήση της {name} για αυτό το μενού",
    },
}
