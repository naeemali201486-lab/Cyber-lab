import unittest
from pathlib import Path
from urllib.request import urlopen


class CorrelationUIHealthTest(unittest.TestCase):

    def setUp(self):
        self.ui = Path("soc-dashboard/index.html").read_text(
            encoding="utf-8"
        )

    def test_correlation_ui(self):
        expected = [
            "Event Correlation",
            'id="correlationGroups"',
            "CORRELATION GROUPS",
            '"/api/correlation"',
            "async function loadCorrelation()",
            "data.groups",
            "loadCorrelation()",
            "loadStatus()",
            "loadSummary()",
            "loadAlerts()",
            "loadIncidents()",
            "loadAudit()",
            "loadEvents()",
        ]

        for item in expected:
            with self.subTest(item=item):
                self.assertIn(item, self.ui)

    def test_live_correlation_api(self):
        with urlopen(
            "http://127.0.0.1:9099/api/correlation",
            timeout=5,
        ) as response:
            self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()
