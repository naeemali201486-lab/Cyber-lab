from pathlib import Path
from datetime import datetime
import json

from audit_log import record_audit

INCIDENTS = Path(__file__).parent / "events" / "incidents.json"


SEVERITY_MAP = {
    "BRUTE_FORCE": "HIGH",
    "SUSPICIOUS_REQUEST": "MEDIUM",
    "AUTH_FAILURE": "MEDIUM",
    "RATE_LIMIT": "MEDIUM",
}


def get_severity(event):
    return SEVERITY_MAP.get(event, "LOW")


def load_incidents():
    if not INCIDENTS.exists():
        return []

    try:
        return json.loads(
            INCIDENTS.read_text(
                encoding="utf-8",
                errors="replace"
            )
        )
    except (json.JSONDecodeError, OSError):
        return []


def save_incidents(incidents):
    INCIDENTS.parent.mkdir(parents=True, exist_ok=True)

    INCIDENTS.write_text(
        json.dumps(incidents, indent=2),
        encoding="utf-8"
    )


def create_incident(event, service, detail):
    incidents = load_incidents()

    # Correlate previous authentication failures into the
    # higher-level brute-force incident.
    if event == "BRUTE_FORCE":
        now = datetime.now().astimezone().isoformat(timespec="seconds")

        for incident in incidents:
            if (
                incident.get("event") == "AUTH_FAILURE"
                and incident.get("service") == service
                and incident.get("status") == "OPEN"
            ):
                incident["status"] = "RESOLVED"
                incident["resolved"] = now
                incident["correlated_to"] = "BRUTE_FORCE"

                record_audit(
                    incident.get("id"),
                    "CORRELATED_AND_RESOLVED",
                    old_status="OPEN",
                    new_status="RESOLVED"
                )

        save_incidents(incidents)

    # Don't create duplicate unresolved incidents.
    # BRUTE_FORCE detail changes as the failure count increases,
    # so matching the detail would incorrectly create multiple
    # HIGH incidents for the same active brute-force condition.
    for incident in incidents:
        if (
            incident.get("event") == event
            and incident.get("service") == service
            and incident.get("status") != "RESOLVED"
        ):
            return incident

    next_id = max(
        [item.get("id", 0) for item in incidents],
        default=0
    ) + 1

    incident = {
        "id": next_id,
        "created": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "event": event,
        "service": service,
        "detail": detail,
        "severity": get_severity(event),
        "status": "OPEN"
    }

    incidents.append(incident)
    save_incidents(incidents)

    record_audit(
        incident["id"],
        "CREATED",
        old_status=None,
        new_status="OPEN"
    )

    return incident


def update_status(incident_id, status):
    allowed = {
        "OPEN",
        "ACKNOWLEDGED",
        "RESOLVED"
    }

    if status not in allowed:
        return None

    incidents = load_incidents()

    for incident in incidents:
        if incident.get("id") == incident_id:
            old_status = incident.get("status")

            incident["status"] = status

            if status == "RESOLVED":
                incident["resolved"] = (
                    datetime.now()
                    .astimezone()
                    .isoformat(timespec="seconds")
                )

            save_incidents(incidents)

            if old_status != status:
                record_audit(
                    incident_id,
                    "STATUS_CHANGED",
                    old_status=old_status,
                    new_status=status
                )

            return incident

    return None
