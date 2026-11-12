import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "vuln_report_check.py"
GOOD = ROOT / "samples" / "good-report.md"
BAD = ROOT / "samples" / "bad-report.md"


def run(path):
    return subprocess.run(
        [sys.executable, str(CLI), str(path)],
        capture_output=True,
        text=True,
    )


class ValidatorTests(unittest.TestCase):
    def test_good_report_passes(self):
        r = run(GOOD)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("RESULT: PASS", r.stdout)

    def test_bad_report_fails(self):
        r = run(BAD)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("RESULT: FAIL", r.stdout)

    def test_bad_report_names_the_missing_elements(self):
        r = run(BAD)
        for label in ("Boundary", "Benign control", "Deduplication"):
            self.assertIn(f"FAIL  {label}", r.stdout)

    def test_missing_dedup_alone_fails(self):
        text = GOOD.read_text()
        cut = text.index("## Deduplication")
        end = text.index("## Suggested fix")
        broken = text[:cut] + text[end:]
        tmp = ROOT / "tests" / "_tmp_broken.md"
        tmp.write_text(broken)
        try:
            r = run(tmp)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("FAIL  Deduplication note", r.stdout)
        finally:
            tmp.unlink(missing_ok=True)

    def test_missing_file_is_a_clean_error(self):
        r = run(ROOT / "samples" / "does-not-exist.md")
        self.assertEqual(r.returncode, 2)
        self.assertIn("cannot read", r.stderr)


if __name__ == "__main__":
    unittest.main()
