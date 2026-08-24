from pathlib import Path
from datetime import datetime
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

SERVICES = {
    "service-test": "http://127.0.0.1:9094/health",
    "dashboard": "http://127.0.0.1:9095/api/status",
    "log-lab": "http://127.0.0.1:9096/health",
}

LOG = Path("monitor.log")

online = 0
offline = 0

timestamp = datetime.now().isoformat(timespec="seconds")

with LOG.open("a") as log:
    log.write(f"\n=== Check {timestamp} ===\n")

    for name, url in SERVICES.items():
        try:
            with urlopen(url, timeout=3) as response:
                result = f"{name} | ONLINE | HTTP {response.status}"
                online += 1
        except (HTTPError, URLError, OSError):
            result = f"{name} | OFFLINE"
            offline += 1

        print(result)
        log.write(result + "\n")

    overall = "PASS" if offline == 0 else "FAIL"
    print(f"Overall: {overall}")
    log.write(f"Overall: {overall}\n")
