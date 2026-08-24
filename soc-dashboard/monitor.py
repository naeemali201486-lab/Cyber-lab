from pathlib import Path
import time
from collections import deque
from datetime import datetime

from event_collector import record_event
from incident_manager import create_incident
from correlation_engine import correlate_events, classify_group


LOG = Path.home() / "cyber-lab" / "logs" / "web-security-lab.log"

position = LOG.stat().st_size if LOG.exists() else 0

auth_failures = deque()

BRUTE_FORCE_THRESHOLD = 5
BRUTE_FORCE_WINDOW = 60

# Correlation engine integration
def correlation_classification(events):
    groups = correlate_events(events)
    if not groups:
        return None
    return classify_group(groups[-1])



def main():
    global position
    print("=== SOC EVENT MONITOR ===")
    print(f"Monitoring: {LOG}")

    while True:
        try:
            if LOG.exists():
                with LOG.open(
                    "r",
                    encoding="utf-8",
                    errors="replace"
                ) as f:

                    f.seek(position)

                    for line in f:

                        if " 429 " in line:
                            event = "RATE_LIMIT"
                            detail = "HTTP 429 observed automatically"

                        elif "SUSPICIOUS_REQUEST" in line:
                            event = "SUSPICIOUS_REQUEST"
                            detail = "Suspicious request observed automatically"

                        elif "AUTH_FAILURE" in line:
                            event = "AUTH_FAILURE"
                            detail = "Failed authentication attempt observed automatically"

                            now = time.time()
                            auth_failures.append(now)

                            while auth_failures and (
                                now - auth_failures[0] > BRUTE_FORCE_WINDOW
                            ):
                                auth_failures.popleft()

                            if len(auth_failures) >= BRUTE_FORCE_THRESHOLD:
                                event = "BRUTE_FORCE"
                                detail = (
                                    f"{len(auth_failures)} failed authentication "
                                    f"attempts within {BRUTE_FORCE_WINDOW} seconds"
                                )

                        else:
                            continue

                        created = record_event(
                            event,
                            "web-security-lab",
                            detail
                        )

                        incident = create_incident(
                            event,
                            "web-security-lab",
                            detail
                        )

                        if created:
                            print(
                                f"Security event: {event}"
                            )

                        if incident:
                            print(
                                f"SOC incident #{incident['id']} "
                                f"status={incident['status']}"
                            )

                    position = f.tell()

        except Exception as e:
            print(f"Monitor error: {e}")

        time.sleep(2)


if __name__ == "__main__":
    main()
