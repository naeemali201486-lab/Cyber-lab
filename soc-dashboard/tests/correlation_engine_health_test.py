from datetime import datetime, timedelta
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from correlation_engine import correlate_events, classify_group


class CorrelationEngineHealthTest(unittest.TestCase):

    def setUp(self):
        self.base = datetime.fromisoformat(
            "2026-08-21T17:00:00+05:00"
        )

    def event(self, event_type, seconds):
        return {
            "event": event_type,
            "service": "web-security-lab",
            "timestamp": (
                self.base + timedelta(seconds=seconds)
            ).isoformat(),
        }

    def test_five_auth_failures_brute_force(self):
        events = [
            self.event("AUTH_FAILURE", 0),
            self.event("AUTH_FAILURE", 10),
            self.event("AUTH_FAILURE", 20),
            self.event("AUTH_FAILURE", 30),
            self.event("AUTH_FAILURE", 40),
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 5)
        self.assertEqual(
            classify_group(groups[0]),
            "BRUTE_FORCE",
        )

    def test_correlation_window(self):
        events = [
            self.event("AUTH_FAILURE", 0),
            self.event("AUTH_FAILURE", 30),
            self.event("AUTH_FAILURE", 61),
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups[0]), 2)
        self.assertEqual(len(groups[1]), 1)

    def test_suspicious_request(self):
        events = [
            self.event("SUSPICIOUS_REQUEST", 0),
            self.event("AUTH_FAILURE", 10),
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 1)
        self.assertEqual(
            classify_group(groups[0]),
            "SUSPICIOUS_ACTIVITY",
        )

    def test_rate_limit(self):
        events = [
            self.event("RATE_LIMIT", 0),
            self.event("RATE_LIMIT", 20),
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 1)
        self.assertEqual(
            classify_group(groups[0]),
            "RATE_LIMIT_ACTIVITY",
        )

    def test_empty_event_set(self):
        self.assertEqual(correlate_events([]), [])


if __name__ == "__main__":
    unittest.main()
