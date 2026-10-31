# Cache tiers and silent preferred skip.
# requirement-python-cli-storage. POSIX shapes stay on requirement-shell-cli-storage.
# TP-CLI-12 tiers. TP-STO-01 one resolver. TP-IDEM-03 mktemp refuses $$.
import ast
import os
import stat
import tempfile
import unittest
from pathlib import Path

from AgentCli.storage import Storage


ROOT = Path(__file__).resolve().parents[1]


class TestStorage(unittest.TestCase):
    def test_linux_gitbash_and_mac_leaves(self):
        home = tempfile.mkdtemp(prefix="agcache-")
        linux = Storage(home=home, login="ada", pid=9, environ={"AGENT_CLI_CACHE_HOST": "linux"})
        self.assertEqual(linux.preferred_dir(), "/dev/shm/cache/cache-agent-cli-ada-9")
        self.assertEqual(linux.fallback_dir(), "/tmp/cache/cache-agent-cli-ada-9")
        self.assertTrue(linux.fallback2_dir().endswith("/.cache/cache-agent-cli-9"))
        gitbash = Storage(home=home, login="ada", pid=9, environ={"AGENT_CLI_CACHE_HOST": "gitbash"})
        self.assertTrue(gitbash.preferred_dir().startswith("/tmp/cache/"))
        self.assertIn("AppData", gitbash.fallback_dir())
        self.assertEqual(gitbash.fallback2_dir(), "")
        mac = Storage(home=home, login="ada", pid=9, environ={"AGENT_CLI_CACHE_HOST": "mac"})
        self.assertIn("Library/Caches", mac.fallback_dir())
        self.assertTrue(mac.fallback2_dir().endswith("/cache/cache-agent-cli-9"))
        self.assertEqual(linux.persistent_dir(), os.path.join(home, ".local", "agent-cli"))

    def test_skip_preferred_is_silent_and_mktemp_refuses_pid_template(self):
        home = tempfile.mkdtemp(prefix="agskip-")
        env = {"AGENT_CLI_CACHE_HOST": "linux", "AGENT_CLI_CACHE_SKIP": "preferred", "HOME": home}
        store = Storage(home=home, login="ada", pid=9, environ=env)
        used = store.resolve()
        self.assertTrue(used.startswith("/tmp/cache/"))
        self.assertFalse(os.path.isdir(store.preferred_dir()))
        mode = stat.S_IMODE(os.stat(used).st_mode)
        self.assertEqual(mode, 0o700)
        with self.assertRaises(OSError):
            store.mktemp("$$")
        path = store.mktemp("note")
        self.assertTrue(path.startswith(used))
        self.assertNotIn("$$", os.path.basename(path))

    def test_tp_sto_01_one_resolver_and_about_lines(self):
        source = (ROOT / "src" / "AgentCli" / "storage.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
        self.assertEqual(classes, ["Storage"])
        self.assertEqual(functions, [])
        home = tempfile.mkdtemp(prefix="agabout-")
        store = Storage(home=home, login="ada", pid=91031, environ={"AGENT_CLI_CACHE_HOST": "linux", "HOME": home})
        lines = "\n".join(store.about_lines())
        self.assertIn("Cache folder used:", lines)
        self.assertIn("/dev/shm/cache/cache-agent-cli-", lines)
        self.assertIn("Persistence storage:", lines)
        self.assertIn(os.path.join(home, ".local", "agent-cli"), lines)
        self.assertNotIn("/dev/shm/agent-cli", store.preferred_dir())
        leaf = store.preferred_dir()
        if os.path.isdir(leaf):
            os.rmdir(leaf)


if __name__ == "__main__":
    unittest.main()
