from urllib.request import urlopen
from urllib.error import HTTPError, URLError

SERVICES = {
    "Service Test": "http://127.0.0.1:9094/health",
    "Dashboard": "http://127.0.0.1:9095/api/status",
    "Log Lab": "http://127.0.0.1:9096/health",
}

online = 0
offline = 0

print("=== Cyber Lab Central Monitor ===")

for name, url in SERVICES.items():
    try:
        with urlopen(url, timeout=3) as response:
            print(f"[ONLINE]  {name} | HTTP {response.status}")
            online += 1
    except (HTTPError, URLError, OSError):
        print(f"[OFFLINE] {name}")
        offline += 1

print()
print(f"Online : {online}")
print(f"Offline: {offline}")
print("Status :", "ALL SYSTEMS OK" if offline == 0 else "ATTENTION REQUIRED")
