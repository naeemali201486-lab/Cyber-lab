from urllib.request import urlopen
from urllib.error import HTTPError, URLError

SERVICES = {
    "service-test": "http://127.0.0.1:9094/health",
    "dashboard": "http://127.0.0.1:9095/api/status",
    "log-lab": "http://127.0.0.1:9096/health",
}

for name, url in SERVICES.items():
    try:
        with urlopen(url, timeout=3) as response:
            body = response.read().decode()
            print(f"{name}: OK | HTTP {response.status} | {body}")

    except HTTPError as e:
        print(f"{name}: HTTP ERROR | {e.code}")

    except URLError as e:
        print(f"{name}: OFFLINE | {e.reason}")

    except Exception as e:
        print(f"{name}: ERROR | {e}")
