from pathlib import Path
from datetime import datetime
import json

AUDIT_LOG = Path(__file__).parent / "events" / "audit.json"


def record_audit(incident_id, action, old_status=None, new_status=None):
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)

    entries = []

    if AUDIT_LOG.exists():
        try:
            entries = json.loads(
                AUDIT_LOG.read_text(
                    encoding="utf-8",
                    errors="replace"
                )
            )
        except (json.JSONDecodeError, OSError):
            entries = []

    entry = {
        "timestamp": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "incident_id": incident_id,
        "action": action
    }

    if old_status is not None:
        entry["old_status"] = old_status

    if new_status is not None:
        entry["new_status"] = new_status

    entries.append(entry)

    AUDIT_LOG.write_text(
        json.dumps(entries, indent=2),
        encoding="utf-8"
    )

    return entry
