import json
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.request import urlopen

BASE = "http://127.0.0.1:9099"
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

INCIDENTS = ROOT / "events" / "incidents.json"
AUDIT = ROOT / "events" / "audit.json"

from incident_manager import create_incident, update_status


def get(path):
    with urlopen(BASE + path, timeout=3) as response:
        return json.loads(response.read().decode())


class CombinedHealthTest(unittest.TestCase):

    def test_combined_soc_and_audit(self):
        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).parent / "soc_health_test.py"),
            ],
            cwd=ROOT,
        )

        self.assertEqual(result.returncode, 0)

        with open(INCIDENTS, encoding="utf-8") as f:
            baseline = json.load(f)

        with open(AUDIT, encoding="utf-8") as f:
            audit_baseline = json.load(f)

        try:
            incident = create_incident(
                "COMBINED_HEALTH_TEST",
                "web-security-lab",
                "Combined SOC and audit lifecycle test",
            )

            self.assertEqual(incident["status"], "OPEN")

            update_status(incident["id"], "ACKNOWLEDGED")
            update_status(incident["id"], "RESOLVED")

            with open(AUDIT, encoding="utf-8") as f:
                audit = json.load(f)

            records = [
                x for x in audit
                if x.get("incident_id") == incident["id"]
            ][-3:]

            self.assertEqual(len(records), 3)

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
                json.dump(baseline, f, indent=2)

            with open(AUDIT, "w", encoding="utf-8") as f:
                json.dump(audit_baseline, f, indent=2)

        data = get("/api/incidents")
        incidents = data["incidents"]

        self.assertEqual(len(incidents), len(baseline))
        self.assertEqual(incidents, baseline)

        open_incidents = [
            i for i in incidents
            if i.get("status") == "OPEN"
        ]

        self.assertFalse(open_incidents)

        audit_api = get("/api/audit")
        self.assertIsInstance(audit_api.get("audit"), list)


if __name__ == "__main__":
    unittest.main()
