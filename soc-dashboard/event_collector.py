from pathlib import Path
from datetime import datetime

LOG = Path(__file__).parent / "events" / "security.log"


def record_event(event, service, detail):
    LOG.parent.mkdir(parents=True, exist_ok=True)

    # Prevent duplicate identical events within 30 seconds
    if LOG.exists():
        lines = LOG.read_text(
            encoding="utf-8",
            errors="replace"
        ).splitlines()

        for line in reversed(lines[-20:]):
            parts = line.split(" | ", 3)

            if len(parts) == 4:
                old_event = parts[1]
                old_service = parts[2]
                old_detail = parts[3]

                if (
                    event != "AUTH_FAILURE"
                    and old_event == event
                    and old_service == f"service={service}"
                    and old_detail == detail
                ):
                    try:
                        old_time = datetime.fromisoformat(parts[0])
                        now = datetime.now().astimezone()

                        if (now - old_time).total_seconds() < 30:
                            return False
                    except ValueError:
                        pass

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    line = (
        f"{timestamp} | {event} | "
        f"service={service} | {detail}\n"
    )

    with LOG.open("a", encoding="utf-8") as f:
        f.write(line)

    return True


if __name__ == "__main__":
    if record_event(
        "RATE_LIMIT",
        "web-security-lab",
        "HTTP 429 observed during local test"
    ):
        print("Security event recorded.")
    else:
        print("Duplicate event ignored.")
