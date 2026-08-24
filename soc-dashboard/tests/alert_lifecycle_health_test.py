import json
import sys
import unittest
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:9099"
ROOT = Path(__file__).resolve().parent.parent

INCIDENTS = ROOT / "events" / "incidents.json"
AUDIT = ROOT / "events" / "audit.json"

sys.path.insert(0, str(ROOT))

from incident_manager import create_incident


def get(path):
    with urlopen(BASE + path, timeout=5) as response:
        return response.status, json.loads(response.read().decode())


def post_status(incident_id, status):
    data = json.dumps({"status": status}).encode()

    request = Request(
        f"{BASE}/api/incidents/{incident_id}/status",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode())
    except Exception as exc:
        if hasattr(exc, "code"):
            body = exc.read().decode()
            return exc.code, json.loads(body)
        raise


class AlertLifecycleHealthTest(unittest.TestCase):

    def test_alert_lifecycle(self):
        with open(INCIDENTS, encoding="utf-8") as f:
            incident_baseline = json.load(f)

        with open(AUDIT, encoding="utf-8") as f:
            audit_baseline = json.load(f)

        try:
            before_ids = {x.get("id") for x in incident_baseline}

            incident = create_incident(
                "ALERT_LIFECYCLE_TEST",
                "web-security-lab",
                "Temporary lifecycle health test",
            )

            incident_id = incident["id"]

            self.assertNotIn(incident_id, before_ids)
            self.assertEqual(incident["status"], "OPEN")

            status, data = get("/api/incidents")
            self.assertEqual(status, 200)

            api_incident = next(
                x for x in data["incidents"]
                if x["id"] == incident_id
            )
            self.assertEqual(api_incident["status"], "OPEN")

            status, data = post_status(incident_id, "ACKNOWLEDGED")
            self.assertEqual(status, 200)
            self.assertEqual(
                data["incident"]["status"],
                "ACKNOWLEDGED",
            )

            status, data = post_status(incident_id, "RESOLVED")
            self.assertEqual(status, 200)
            self.assertEqual(
                data["incident"]["status"],
                "RESOLVED",
            )
            self.assertTrue(data["incident"].get("resolved"))

            status, data = post_status(incident_id, "INVALID_STATUS")
            self.assertEqual(status, 400)
            self.assertIn("error", data)

            with open(AUDIT, encoding="utf-8") as f:
                audit = json.load(f)

            records = [
                x for x in audit
                if x.get("incident_id") == incident_id
            ][-3:]

            self.assertEqual(records[0]["action"], "CREATED")
            self.assertEqual(records[0]["new_status"], "OPEN")

            self.assertEqual(records[1]["action"], "STATUS_CHANGED")
            self.assertEqual(records[1]["old_status"], "OPEN")
            self.assertEqual(records[1]["new_status"], "ACKNOWLEDGED")

            self.assertEqual(records[2]["action"], "STATUS_CHANGED")
            self.assertEqual(records[2]["old_status"], "ACKNOWLEDGED")
            self.assertEqual(records[2]["new_status"], "RESOLVED")

        finally:
            with open(INCIDENTS, "w", encoding="utf-8") as f:
                json.dump(incident_baseline, f, indent=2)

            with open(AUDIT, "w", encoding="utf-8") as f:
                json.dump(audit_baseline, f, indent=2)


if __name__ == "__main__":
    unittest.main()
