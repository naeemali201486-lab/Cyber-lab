import unittest
from pathlib import Path


class AlertUIHealthTest(unittest.TestCase):

    def test_alert_ui(self):
        html = Path(
            "soc-dashboard/index.html"
        ).read_text(encoding="utf-8")

        expected = [
            'id="alerts"',
            "<h2>Security Alerts</h2>",
            "async function loadAlerts()",
            '"/api/alerts"',
            "loadAlerts(),",
        ]

        for item in expected:
            with self.subTest(item=item):
                self.assertIn(item, html)


if __name__ == "__main__":
    unittest.main()
