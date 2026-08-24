import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from event_collector import LOG, record_event


class EventCollectorHealthTest(unittest.TestCase):

    def setUp(self):
        if LOG.exists():
            self.baseline = LOG.read_text(
                encoding="utf-8",
                errors="replace",
            )
        else:
            self.baseline = None

    def tearDown(self):
        if self.baseline is None:
            if LOG.exists():
                LOG.unlink()
        else:
            LOG.write_text(
                self.baseline,
                encoding="utf-8",
            )

    def test_event_recorded(self):
        result = record_event(
            "TEST_EVENT",
            "test-service",
            "event collector health test",
        )

        self.assertTrue(result)
        self.assertTrue(LOG.exists())

        content = LOG.read_text(
            encoding="utf-8",
            errors="replace",
        )

        self.assertIn("TEST_EVENT", content)
        self.assertIn("service=test-service", content)
        self.assertIn(
            "event collector health test",
            content,
        )

    def test_log_format(self):
        record_event(
            "FORMAT_TEST",
            "test-service",
            "format validation",
        )

        line = LOG.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines()[-1]

        parts = line.split(" | ", 3)

        self.assertEqual(len(parts), 4)
        self.assertEqual(parts[1], "FORMAT_TEST")
        self.assertEqual(
            parts[2],
            "service=test-service",
        )
        self.assertEqual(
            parts[3],
            "format validation",
        )

    def test_duplicate_non_auth_failure_ignored(self):
        first = record_event(
            "RATE_LIMIT",
            "test-service",
            "duplicate test",
        )

        second = record_event(
            "RATE_LIMIT",
            "test-service",
            "duplicate test",
        )

        self.assertTrue(first)
        self.assertFalse(second)

    def test_auth_failure_not_suppressed(self):
        first = record_event(
            "AUTH_FAILURE",
            "test-service",
            "authentication failed",
        )

        second = record_event(
            "AUTH_FAILURE",
            "test-service",
            "authentication failed",
        )

        self.assertTrue(first)
        self.assertTrue(second)


if __name__ == "__main__":
    unittest.main()
