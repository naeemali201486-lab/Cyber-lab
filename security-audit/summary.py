from urllib.request import urlopen
from urllib.error import HTTPError, URLError

SERVICES = {
    "service-test": "http://127.0.0.1:9094/health",
    "dashboard": "http://127.0.0.1:9095/api/status",
    "log-lab": "http://127.0.0.1:9096/health",
}

online = 0
offline = 0

print("=== Cyber Lab Security Audit ===")

for name, url in SERVICES.items():
    try:
        with urlopen(url, timeout=3) as response:
            print(f"[OK] {name} - HTTP {response.status}")
            online += 1
    except (HTTPError, URLError, OSError):
        print(f"[OFFLINE] {name}")
        offline += 1

print()
print(f"Online: {online}")
print(f"Offline: {offline}")

if offline == 0:
    print("Overall: PASS")
else:
    print("Overall: FAIL")
