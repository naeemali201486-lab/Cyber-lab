import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from incident_manager import get_severity


class RiskScoringHealthTest(unittest.TestCase):

    EXPECTED = {
        "BRUTE_FORCE": "HIGH",
        "SUSPICIOUS_REQUEST": "MEDIUM",
        "AUTH_FAILURE": "MEDIUM",
        "RATE_LIMIT": "MEDIUM",
        "UNKNOWN_EVENT": "LOW",
    }

    def test_risk_scoring(self):
        for event, expected in self.EXPECTED.items():
            with self.subTest(event=event):
                actual = get_severity(event)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
