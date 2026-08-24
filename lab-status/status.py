from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
import sys

SERVICES = {
    "Hacking Lab": "http://127.0.0.1:9093/",
    "Service Test": "http://127.0.0.1:9094/health",
    "Dashboard": "http://127.0.0.1:9095/api/status",
    "Log Lab": "http://127.0.0.1:9096/health",
    "Master Dashboard": "http://127.0.0.1:9097/api/status",
    "Web Security Lab": "http://127.0.0.1:9098/health",
}

print("=== CYBER LAB FINAL STATUS ===")

online = 0

for name, url in SERVICES.items():
    try:
        with urlopen(url, timeout=3) as response:
            print(f"[ONLINE]  {name} | HTTP {response.status}")
            online += 1
    except (HTTPError, URLError, OSError):
        print(f"[OFFLINE] {name}")

print()
print(f"Services online: {online}/{len(SERVICES)}")

backup = Path.home() / "cyber-lab" / "backup-lab" / "backups"
incident = Path.home() / "cyber-lab" / "incident-lab" / "alerts.log"

print(
    f"Backup available: "
    f"{'YES' if backup.exists() and any(backup.iterdir()) else 'NO'}"
)

print(
    f"Incident alerts: "
    f"{'PRESENT' if incident.exists() and incident.stat().st_size > 0 else 'NONE'}"
)

print()

if online == len(SERVICES):
    print("Overall: LAB HEALTHY")
    sys.exit(0)
else:
    print("Overall: CHECK REQUIRED")
    sys.exit(1)
