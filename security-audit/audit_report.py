from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime

SERVICES = {
    "service-test": "http://127.0.0.1:9094/health",
    "dashboard": "http://127.0.0.1:9095/api/status",
    "log-lab": "http://127.0.0.1:9096/health",
}

with open("audit.log", "a") as log:
    log.write(f"\n=== Audit {datetime.now().isoformat(timespec='seconds')} ===\n")

    for name, url in SERVICES.items():
        try:
            with urlopen(url, timeout=3) as response:
                result = f"{name} | OK | HTTP {response.status}"
        except HTTPError as e:
            result = f"{name} | HTTP ERROR | {e.code}"
        except URLError:
            result = f"{name} | OFFLINE"
        except Exception as e:
            result = f"{name} | ERROR | {e}"

        print(result)
        log.write(result + "\n")
