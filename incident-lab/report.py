from pathlib import Path
from datetime import datetime

events = Path("events.log").read_text().splitlines()
alerts = Path("alerts.log").read_text().splitlines()

report = [
    "=== Cyber Lab Incident Report ===",
    f"Generated: {datetime.now().isoformat(timespec='seconds')}",
    "",
    f"Total events: {len(events)}",
    f"Total alerts: {len(alerts)}",
    "",
    "Alerts:",
]

report.extend(f"- {alert}" for alert in alerts)

report.extend([
    "",
    "Assessment: ALERTS PRESENT" if alerts else "Assessment: CLEAR",
])

Path("incident_report.txt").write_text("\n".join(report) + "\n")

print("\n".join(report))
print()
print("Saved: incident_report.txt")
