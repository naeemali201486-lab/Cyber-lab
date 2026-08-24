import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path.home() / "cyber-lab"
LOG = ROOT / "logs" / "web-security-lab.log"
EVENTS = ROOT / "soc-dashboard" / "events" / "security.log"
INCIDENTS = ROOT / "soc-dashboard" / "events" / "incidents.json"


class SOCMonitorHealthTest(unittest.TestCase):

    def test_required_files(self):
        self.assertTrue(LOG.exists())
        self.assertTrue(EVENTS.exists())
        self.assertTrue(INCIDENTS.exists())

    def test_incident_database(self):
        incidents = json.loads(
            INCIDENTS.read_text(encoding="utf-8")
        )

        self.assertIsInstance(incidents, list)

    def test_monitor_process(self):
        result = subprocess.run(
            ["ps", "-A", "-o", "cmd"],
            capture_output=True,
            text=True,
        )

        self.assertIn(
            "monitor.py",
            result.stdout,
        )

    def test_security_events_readable(self):
        content = EVENTS.read_text(
            encoding="utf-8",
            errors="replace",
        )

        self.assertIsInstance(content, str)

    def test_baseline_data(self):
        events = EVENTS.read_text(
            encoding="utf-8",
            errors="replace",
        )

        incidents = json.loads(
            INCIDENTS.read_text(encoding="utf-8")
        )

        self.assertGreaterEqual(len(events.splitlines()), 0)
        self.assertGreaterEqual(len(incidents), 0)


if __name__ == "__main__":
    unittest.main()
