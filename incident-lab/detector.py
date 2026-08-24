from pathlib import Path

LOG_FILE = Path("events.log")
ALERT_FILE = Path("alerts.log")

KEYWORDS = {
    "FAILED_LOGIN": "Authentication failure",
    "ERROR": "Application error",
    "DENIED": "Access denied",
}

events = LOG_FILE.read_text().splitlines()
alerts = []

for line in events:
    for keyword, description in KEYWORDS.items():
        if keyword in line:
            alerts.append(f"{description} | {line}")
            break

with ALERT_FILE.open("w") as log:
    for alert in alerts:
        log.write(alert + "\n")

print("=== Incident Detector ===")

for alert in alerts:
    print(f"[ALERT] {alert}")

print()
print(f"Events: {len(events)}")
print(f"Alerts: {len(alerts)}")
print(f"Alert log: {ALERT_FILE}")
