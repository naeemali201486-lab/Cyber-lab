import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from alert_rules import evaluate_alert
from incident_manager import get_severity


class AlertIntegrationHealthTest(unittest.TestCase):

    EVENTS = [
        "BRUTE_FORCE",
        "SUSPICIOUS_REQUEST",
        "AUTH_FAILURE",
        "RATE_LIMIT",
    ]

    def test_alert_incident_integration(self):
        for event in self.EVENTS:
            with self.subTest(event=event):
                severity = get_severity(event)
                result = evaluate_alert(event, severity)

                self.assertEqual(result["event"], event)
                self.assertEqual(result["severity"], severity)
                self.assertGreater(result["score"], 0)


if __name__ == "__main__":
    unittest.main()
