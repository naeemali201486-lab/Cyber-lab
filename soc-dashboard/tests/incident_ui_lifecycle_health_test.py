import unittest
from pathlib import Path


class IncidentUILifecycleHealthTest(unittest.TestCase):

    def test_incident_ui_lifecycle(self):
        html = Path(
            "soc-dashboard/index.html"
        ).read_text(encoding="utf-8")

        expected = [
            "function renderIncidents()",
            "changeIncident(${incident.id}, 'ACKNOWLEDGED')",
            "changeIncident(${incident.id}, 'RESOLVED')",
            "async function changeIncident(id, status)",
            "fetch(",
            "/api/incidents/${id}/status",
            'method: "POST"',
            "JSON.stringify({status})",
            "loadIncidents()",
            "loadAudit()",
        ]

        for item in expected:
            with self.subTest(item=item):
                self.assertIn(item, html)


if __name__ == "__main__":
    unittest.main()
