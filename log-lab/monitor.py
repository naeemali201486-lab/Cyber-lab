import time
from urllib.request import urlopen
from datetime import datetime

URL = "http://127.0.0.1:9094/health"
LOG_FILE = "monitor.log"

for attempt in range(5):
    timestamp = datetime.now().isoformat(timespec="seconds")

    try:
        start = time.perf_counter()

        with urlopen(URL, timeout=3) as response:
            response.read()
            elapsed = (time.perf_counter() - start) * 1000

        line = (
            f"{timestamp} | CHECK {attempt + 1} | "
            f"OK | HTTP {response.status} | "
            f"{elapsed:.2f} ms\n"
        )

    except Exception as e:
        line = (
            f"{timestamp} | CHECK {attempt + 1} | "
            f"FAILED | {e}\n"
        )

    print(line, end="")

    with open(LOG_FILE, "a") as log:
        log.write(line)

    time.sleep(1)
