import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import incident_manager
from incident_manager import (
    INCIDENTS,
    create_incident,
    get_severity,
    load_incidents,
    save_incidents,
    update_status,
)

AUDIT = ROOT / "events" / "audit.json"


class IncidentManagerHealthTest(unittest.TestCase):

    def setUp(self):
        self.incidents_baseline = (
            INCIDENTS.read_text(encoding="utf-8")
            if INCIDENTS.exists()
            else None
        )

        self.audit_baseline = (
            AUDIT.read_text(encoding="utf-8")
            if AUDIT.exists()
            else None
        )

        save_incidents([])

        AUDIT.parent.mkdir(parents=True, exist_ok=True)
        AUDIT.write_text("[]", encoding="utf-8")

    def tearDown(self):
        if self.incidents_baseline is None:
            if INCIDENTS.exists():
                INCIDENTS.unlink()
        else:
            INCIDENTS.write_text(
                self.incidents_baseline,
                encoding="utf-8",
            )

        if self.audit_baseline is None:
            if AUDIT.exists():
                AUDIT.unlink()
        else:
            AUDIT.write_text(
                self.audit_baseline,
                encoding="utf-8",
            )

    def test_severity_mapping(self):
        self.assertEqual(
            get_severity("BRUTE_FORCE"),
            "HIGH",
        )

        self.assertEqual(
            get_severity("SUSPICIOUS_REQUEST"),
            "MEDIUM",
        )

        self.assertEqual(
            get_severity("AUTH_FAILURE"),
            "MEDIUM",
        )

        self.assertEqual(
            get_severity("RATE_LIMIT"),
            "MEDIUM",
        )

        self.assertEqual(
            get_severity("UNKNOWN_EVENT"),
            "LOW",
        )

    def test_save_and_load_incidents(self):
        expected = [
            {
                "id": 1,
                "event": "TEST",
                "status": "OPEN",
            }
        ]

        save_incidents(expected)

        self.assertEqual(
            load_incidents(),
            expected,
        )

    def test_create_incident_assigns_sequential_ids(self):
        first = create_incident(
            "AUTH_FAILURE",
            "service-a",
            "first",
        )

        second = create_incident(
            "RATE_LIMIT",
            "service-a",
            "second",
        )

        self.assertEqual(first["id"], 1)
        self.assertEqual(second["id"], 2)

    def test_duplicate_unresolved_incident_suppressed(self):
        first = create_incident(
            "RATE_LIMIT",
            "service-a",
            "first detail",
        )

        second = create_incident(
            "RATE_LIMIT",
            "service-a",
            "different detail",
        )

        self.assertEqual(
            first["id"],
            second["id"],
        )

        incidents = load_incidents()

        self.assertEqual(
            len(incidents),
            1,
        )

    def test_resolved_incident_allows_new_incident(self):
        first = create_incident(
            "RATE_LIMIT",
            "service-a",
            "first",
        )

        update_status(
            first["id"],
            "RESOLVED",
        )

        second = create_incident(
            "RATE_LIMIT",
            "service-a",
            "second",
        )

        self.assertNotEqual(
            first["id"],
            second["id"],
        )

        self.assertEqual(
            second["status"],
            "OPEN",
        )

    def test_invalid_status_rejected(self):
        incident = create_incident(
            "AUTH_FAILURE",
            "service-a",
            "test",
        )

        result = update_status(
            incident["id"],
            "INVALID_STATUS",
        )

        self.assertIsNone(result)

        current = load_incidents()[0]

        self.assertEqual(
            current["status"],
            "OPEN",
        )

    def test_missing_incident_returns_none(self):
        self.assertIsNone(
            update_status(
                999999,
                "RESOLVED",
            )
        )

    def test_brute_force_resolves_auth_failures(self):
        auth = create_incident(
            "AUTH_FAILURE",
            "service-a",
            "failed login",
        )

        brute_force = create_incident(
            "BRUTE_FORCE",
            "service-a",
            "five failures",
        )

        incidents = load_incidents()

        auth_after = next(
            incident
            for incident in incidents
            if incident["id"] == auth["id"]
        )

        self.assertEqual(
            auth_after["status"],
            "RESOLVED",
        )

        self.assertEqual(
            auth_after["correlated_to"],
            "BRUTE_FORCE",
        )

        self.assertEqual(
            brute_force["severity"],
            "HIGH",
        )

        self.assertEqual(
            brute_force["status"],
            "OPEN",
        )


if __name__ == "__main__":
    unittest.main()
