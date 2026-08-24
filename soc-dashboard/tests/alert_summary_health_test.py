import json
import unittest
from urllib.request import urlopen


URL = "http://127.0.0.1:9099/api/alert-summary"


class AlertSummaryHealthTest(unittest.TestCase):

    def test_alert_summary(self):
        with urlopen(URL, timeout=5) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())

        for key in ("total", "HIGH", "MEDIUM", "LOW"):
            self.assertIn(key, data)

        self.assertEqual(
            data["total"],
            data["HIGH"] + data["MEDIUM"] + data["LOW"],
        )

        self.assertGreaterEqual(data["HIGH"], 0)
        self.assertGreaterEqual(data["MEDIUM"], 0)
        self.assertGreaterEqual(data["LOW"], 0)


if __name__ == "__main__":
    unittest.main()
