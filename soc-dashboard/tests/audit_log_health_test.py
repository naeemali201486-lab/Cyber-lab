import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from audit_log import AUDIT_LOG, record_audit


class AuditLogHealthTest(unittest.TestCase):

    def setUp(self):
        if AUDIT_LOG.exists():
            self.baseline = AUDIT_LOG.read_text(
                encoding="utf-8",
                errors="replace",
            )
        else:
            self.baseline = None

    def tearDown(self):
        if self.baseline is None:
            if AUDIT_LOG.exists():
                AUDIT_LOG.unlink()
        else:
            AUDIT_LOG.write_text(
                self.baseline,
                encoding="utf-8",
            )

    def test_basic_audit_entry(self):
        entry = record_audit(
            999001,
            "TEST_ACTION",
        )

        self.assertEqual(entry["incident_id"], 999001)
        self.assertEqual(entry["action"], "TEST_ACTION")
        self.assertIn("timestamp", entry)

        self.assertNotIn("old_status", entry)
        self.assertNotIn("new_status", entry)

    def test_status_fields(self):
        entry = record_audit(
            999002,
            "STATUS_CHANGED",
            old_status="OPEN",
            new_status="RESOLVED",
        )

        self.assertEqual(entry["old_status"], "OPEN")
        self.assertEqual(entry["new_status"], "RESOLVED")

    def test_entry_persisted(self):
        before = []

        if AUDIT_LOG.exists():
            try:
                before = json.loads(
                    AUDIT_LOG.read_text(encoding="utf-8")
                )
            except json.JSONDecodeError:
                before = []

        entry = record_audit(
            999003,
            "PERSISTENCE_TEST",
        )

        after = json.loads(
            AUDIT_LOG.read_text(encoding="utf-8")
        )

        self.assertEqual(len(after), len(before) + 1)
        self.assertEqual(after[-1], entry)

    def test_multiple_entries_preserved(self):
        first = record_audit(
            999004,
            "FIRST_TEST",
        )

        second = record_audit(
            999005,
            "SECOND_TEST",
        )

        entries = json.loads(
            AUDIT_LOG.read_text(encoding="utf-8")
        )

        self.assertEqual(entries[-2], first)
        self.assertEqual(entries[-1], second)


if __name__ == "__main__":
    unittest.main()
