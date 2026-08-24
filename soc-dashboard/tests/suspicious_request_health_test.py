import json
import time
import unittest
from pathlib import Path
from urllib.request import Request, urlopen


BASE = "http://127.0.0.1:9099"
ROOT = Path(__file__).resolve().parent.parent

INCIDENTS = ROOT / "events" / "incidents.json"
AUDIT = ROOT / "events" / "audit.json"
LOG = Path.home() / "cyber-lab" / "logs" / "web-security-lab.log"


def get(path):
    with urlopen(BASE + path, timeout=3) as response:
        return json.loads(response.read().decode())


def change_status(incident_id, value):
    request = Request(
        f"{BASE}/api/incidents/{incident_id}/status",
        data=json.dumps({"status": value}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=3) as response:
        return json.loads(response.read().decode())


class SuspiciousRequestHealthTest(unittest.TestCase):

    def test_suspicious_request_lifecycle(self):
        with open(INCIDENTS, encoding="utf-8") as f:
            baseline_incidents = json.load(f)

        with open(AUDIT, encoding="utf-8") as f:
            baseline_audit = json.load(f)

        try:
            marker = f"local-controlled-test-{time.time_ns()}"
            LOG.parent.mkdir(parents=True, exist_ok=True)

            with LOG.open("a", encoding="utf-8") as f:
                f.write(
                    f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')} "
                    f"SUSPICIOUS_REQUEST {marker}\n"
                )

            baseline_max_id = max(
                (x.get("id", 0) for x in baseline_incidents),
                default=0,
            )

            deadline = time.time() + 8
            detected = None

            while time.time() < deadline:
                data = get("/api/incidents")

                for incident in data["incidents"]:
                    if (
                        incident.get("event") == "SUSPICIOUS_REQUEST"
                        and incident.get("id", 0) > baseline_max_id
                    ):
                        detected = incident
                        break

                if detected:
                    break

                time.sleep(0.5)

            self.assertIsNotNone(
                detected,
                "SUSPICIOUS_REQUEST was not detected",
            )

            self.assertEqual(
                detected["severity"],
                "MEDIUM",
            )
            self.assertEqual(
                detected["status"],
                "OPEN",
            )

            incident_id = detected["id"]

            updated = change_status(
                incident_id,
                "ACKNOWLEDGED",
            )
            self.assertEqual(
                updated["incident"]["status"],
                "ACKNOWLEDGED",
            )

            updated = change_status(
                incident_id,
                "RESOLVED",
            )
            self.assertEqual(
                updated["incident"]["status"],
                "RESOLVED",
            )

            with open(AUDIT, encoding="utf-8") as f:
                audit = json.load(f)

            records = [
                x for x in audit
                if x.get("incident_id") == incident_id
            ][-3:]

            self.assertEqual(len(records), 3)

            self.assertEqual(
                records[0]["action"],
                "CREATED",
            )
            self.assertEqual(
                records[1]["new_status"],
                "ACKNOWLEDGED",
            )
            self.assertEqual(
                records[2]["new_status"],
                "RESOLVED",
            )

        finally:
            with open(INCIDENTS, "w", encoding="utf-8") as f:
                json.dump(
                    baseline_incidents,
                    f,
                    indent=2,
                )

            with open(AUDIT, "w", encoding="utf-8") as f:
                json.dump(
                    baseline_audit,
                    f,
                    indent=2,
                )


if __name__ == "__main__":
    unittest.main()
