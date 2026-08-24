import json
import unittest
from urllib.request import urlopen


BASE = "http://127.0.0.1:9099"


def get(path):
    with urlopen(BASE + path, timeout=3) as response:
        return json.loads(response.read().decode())


class SOCHealthTest(unittest.TestCase):

    def test_dashboard_http(self):
        with urlopen(BASE + "/", timeout=3) as response:
            self.assertEqual(response.status, 200)

    def test_service_health(self):
        status = get("/api/status")

        self.assertEqual(status["online"], 6)
        self.assertEqual(status["total"], 6)
        self.assertEqual(status["online"], status["total"])
        self.assertEqual(status["overall"], "HEALTHY")

    def test_soc_summary(self):
        summary = get("/api/summary")

        self.assertGreaterEqual(
            summary["total_events"],
            0,
        )

    def test_incident_api(self):
        data = get("/api/incidents")

        self.assertIn("incidents", data)
        self.assertIsInstance(data["incidents"], list)

    def test_no_open_incidents(self):
        data = get("/api/incidents")
        incidents = data["incidents"]

        open_incidents = [
            incident
            for incident in incidents
            if incident.get("status") == "OPEN"
        ]

        self.assertEqual(len(open_incidents), 0)

    def test_brute_force_high_resolved(self):
        data = get("/api/incidents")
        incidents = data["incidents"]

        brute_force = [
            incident
            for incident in incidents
            if incident.get("event") == "BRUTE_FORCE"
        ]

        self.assertTrue(brute_force)
        self.assertTrue(
            any(
                incident.get("severity") == "HIGH"
                for incident in brute_force
            )
        )
        self.assertTrue(
            all(
                incident.get("status") == "RESOLVED"
                for incident in brute_force
            )
        )


if __name__ == "__main__":
    unittest.main()
