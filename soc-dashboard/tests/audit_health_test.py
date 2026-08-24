import json
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from incident_manager import create_incident, update_status

INCIDENTS = BASE / "events" / "incidents.json"
AUDIT = BASE / "events" / "audit.json"


class AuditHealthTest(unittest.TestCase):

    def test_audit_lifecycle(self):
        with open(INCIDENTS, encoding="utf-8") as f:
            baseline = json.load(f)

        try:
            incident = create_incident(
                "AUDIT_HEALTH_TEST",
                "web-security-lab",
                "Automated audit lifecycle test",
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


if __name__ == "__main__":
    unittest.main()
