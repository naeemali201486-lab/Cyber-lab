from datetime import datetime, timedelta
import json
import sys
import unittest
from urllib.request import urlopen

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from correlation_engine import correlate_events, classify_group


BASE = "http://127.0.0.1:9099/api/correlation"


def make_event(event, timestamp):
    return {
        "event": event,
        "service": "web-security-lab",
        "timestamp": timestamp.isoformat(),
    }


class CorrelationAPIHealthTest(unittest.TestCase):

    def setUp(self):
        self.base = datetime.now().astimezone()

    def test_five_auth_failures_brute_force(self):
        events = [
            make_event(
                "AUTH_FAILURE",
                self.base + timedelta(seconds=i * 5),
            )
            for i in range(5)
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 1)
        self.assertEqual(
            classify_group(groups[0]),
            "BRUTE_FORCE",
        )

    def test_four_auth_failures_related(self):
        events = [
            make_event(
                "AUTH_FAILURE",
                self.base + timedelta(seconds=i * 5),
            )
            for i in range(4)
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 1)
        self.assertEqual(
            classify_group(groups[0]),
            "RELATED_EVENTS",
        )

    def test_sixty_second_window(self):
        events = [
            make_event("AUTH_FAILURE", self.base),
            make_event(
                "AUTH_FAILURE",
                self.base + timedelta(seconds=61),
            ),
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 2)

    def test_suspicious_request(self):
        events = [
            make_event("SUSPICIOUS_REQUEST", self.base)
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 1)
        self.assertEqual(
            classify_group(groups[0]),
            "SUSPICIOUS_ACTIVITY",
        )

    def test_rate_limit(self):
        events = [
            make_event("RATE_LIMIT", self.base)
        ]

        groups = correlate_events(events)

        self.assertEqual(len(groups), 1)
        self.assertEqual(
            classify_group(groups[0]),
            "RATE_LIMIT_ACTIVITY",
        )

    def test_live_api(self):
        with urlopen(BASE, timeout=5) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(
                response.read().decode("utf-8")
            )

        self.assertEqual(data["window_seconds"], 60)
        self.assertIsInstance(data["groups"], list)


if __name__ == "__main__":
    unittest.main()
