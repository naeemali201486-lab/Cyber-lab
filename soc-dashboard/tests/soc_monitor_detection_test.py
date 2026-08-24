import json
import time
import unittest
from pathlib import Path


ROOT = Path.home() / "cyber-lab"

LOG = ROOT / "logs" / "web-security-lab.log"
INCIDENTS = ROOT / "soc-dashboard" / "events" / "incidents.json"
AUDIT = ROOT / "soc-dashboard" / "events" / "audit.json"


class SOCMonitorDetectionTest(unittest.TestCase):

    def test_brute_force_detection(self):
        baseline_incidents = json.loads(
            INCIDENTS.read_text(encoding="utf-8")
        )

        baseline_audit = json.loads(
            AUDIT.read_text(encoding="utf-8")
        )

        baseline_ids = {
            incident.get("id")
            for incident in baseline_incidents
        }

        try:
            marker = "PHASE8_AUTOMATED_TEST"

            with LOG.open("a", encoding="utf-8") as f:
                for i in range(5):
                    f.write(
                        f"AUTH_FAILURE {marker} attempt={i + 1}\n"
                    )

            detected = None

            for _ in range(10):
                time.sleep(1)

                current = json.loads(
                    INCIDENTS.read_text(encoding="utf-8")
                )

                new_incidents = [
                    incident
                    for incident in current
                    if incident.get("id") not in baseline_ids
                ]

                matches = [
                    incident
                    for incident in new_incidents
                    if incident.get("event") == "BRUTE_FORCE"
                ]

                if matches:
                    detected = matches[-1]
                    break

            self.assertIsNotNone(
                detected,
                "BRUTE_FORCE incident not detected",
            )

            self.assertEqual(
                detected.get("severity"),
                "HIGH",
            )

            self.assertEqual(
                detected.get("status"),
                "OPEN",
            )

        finally:
            INCIDENTS.write_text(
                json.dumps(
                    baseline_incidents,
                    indent=2,
                ),
                encoding="utf-8",
            )

            AUDIT.write_text(
                json.dumps(
                    baseline_audit,
                    indent=2,
                ),
                encoding="utf-8",
            )


if __name__ == "__main__":
    unittest.main()
