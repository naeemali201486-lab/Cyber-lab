from pathlib import Path
from collections import Counter

events = Path("events.log").read_text().splitlines()
alerts = Path("alerts.log").read_text().splitlines()

types = Counter()

for alert in alerts:
    if alert.startswith("Authentication failure"):
        types["Authentication failures"] += 1
    elif alert.startswith("Access denied"):
        types["Access denied"] += 1
    elif alert.startswith("Application error"):
        types["Application errors"] += 1

print("=== Incident Summary ===")
print(f"Total events: {len(events)}")
print(f"Total alerts: {len(alerts)}")

for name, count in types.items():
    print(f"{name}: {count}")

print("Overall:", "ALERTS PRESENT" if alerts else "CLEAR")
