import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from alert_rules import evaluate_alert


class AlertRulesHealthTest(unittest.TestCase):

    EXPECTED = {
        ("BRUTE_FORCE", "HIGH"): (90, True),
        ("SUSPICIOUS_REQUEST", "MEDIUM"): (50, True),
        ("AUTH_FAILURE", "MEDIUM"): (50, True),
        ("UNKNOWN_EVENT", "LOW"): (20, False),
    }

    def test_alert_rules(self):
        for (event, severity), (score, should_alert) in self.EXPECTED.items():
            with self.subTest(event=event, severity=severity):
                result = evaluate_alert(event, severity)

                self.assertEqual(result["event"], event)
                self.assertEqual(result["severity"], severity)
                self.assertEqual(result["score"], score)
                self.assertIs(result["alert"], should_alert)


if __name__ == "__main__":
    unittest.main()
