# Actor catalog. requirement-actor-role-subject.
# TP-ARS-01 columns. TP-ARS-02 help None and install on the placed-files row.
# TP-ARS-03 no Approver column in this tree.
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "docs" / "requirements"


def _catalog_rows(text):
    rows = []
    for line in text.splitlines():
        if not line.startswith("| This login |"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


class TestActorCatalog(unittest.TestCase):
    def test_tp_ars_01_columns_are_actor_role_subject(self):
        text = (REQ / "requirement-actor-role-subject.md").read_text(encoding="utf-8")
        self.assertIn("| Actor | Role | Subject |", text)
        self.assertNotIn("| Approver |", text)
        self.assertNotIn("| Submitter |", text)
        for cells in _catalog_rows(text):
            self.assertEqual(len(cells), 3, cells)

    def test_tp_ars_02_help_is_none_and_install_is_placed_files(self):
        text = (REQ / "requirement-actor-role-subject.md").read_text(encoding="utf-8")
        rows = _catalog_rows(text)
        help_row = [cells for cells in rows if "`help`" in cells[1]]
        self.assertEqual(len(help_row), 1)
        self.assertEqual(help_row[0][2], "None")
        install_row = [cells for cells in rows if "`install`" in cells[1]]
        self.assertEqual(len(install_row), 1)
        self.assertIn("placed files", install_row[0][2])
        self.assertNotEqual(install_row[0][2], "None")

    def test_tp_ars_03_no_approver_column_in_requirements(self):
        offenders = []
        for path in sorted(REQ.glob("requirement-*.md")):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.startswith("|") and "Approver" in line and "Subject" in line:
                    offenders.append(path.name)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
