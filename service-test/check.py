import time
from urllib.request import urlopen

URL = "http://127.0.0.1:9094/health"

for attempt in range(5):
    start = time.perf_counter()

    try:
        with urlopen(URL, timeout=3) as response:
            body = response.read().decode()
            elapsed = (time.perf_counter() - start) * 1000

            print(
                f"Check {attempt + 1}: "
                f"OK | HTTP {response.status} | "
                f"{elapsed:.2f} ms | {body}"
            )

    except Exception as e:
        print(f"Check {attempt + 1}: FAILED | {e}")

    time.sleep(1)
