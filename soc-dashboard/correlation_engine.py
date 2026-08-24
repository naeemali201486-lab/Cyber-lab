from datetime import datetime, timedelta


CORRELATION_WINDOW = 60


def correlate_events(events):
    """
    Group related security events occurring within a short time window.

    Expected event format:
    {
        "event": "AUTH_FAILURE",
        "service": "web-security-lab",
        "timestamp": "2026-08-21T17:00:00+05:00"
    }
    """

    if not events:
        return []

    parsed = []

    for event in events:
        try:
            timestamp = datetime.fromisoformat(event["timestamp"])
        except (KeyError, ValueError, TypeError):
            continue

        parsed.append((timestamp, event))

    parsed.sort(key=lambda item: item[0])

    groups = []
    current = []
    current_start = None

    for timestamp, event in parsed:
        if not current:
            current = [event]
            current_start = timestamp
            continue

        elapsed = (timestamp - current_start).total_seconds()

        if elapsed <= CORRELATION_WINDOW:
            current.append(event)
        else:
            groups.append(current)
            current = [event]
            current_start = timestamp

    if current:
        groups.append(current)

    return groups


def classify_group(events):
    """
    Return a simple correlation classification.
    """

    event_types = {event.get("event") for event in events}

    if "AUTH_FAILURE" in event_types and len(
        [e for e in events if e.get("event") == "AUTH_FAILURE"]
    ) >= 5:
        return "BRUTE_FORCE"

    if "SUSPICIOUS_REQUEST" in event_types:
        return "SUSPICIOUS_ACTIVITY"

    if "RATE_LIMIT" in event_types:
        return "RATE_LIMIT_ACTIVITY"

    return "RELATED_EVENTS"
