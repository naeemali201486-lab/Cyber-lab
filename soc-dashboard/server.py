from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
import json
from incident_manager import load_incidents, update_status
from correlation_engine import correlate_events, classify_group

BASE = Path(__file__).parent
EVENT_LOG = BASE / "events" / "security.log"
AUDIT_LOG = BASE / "events" / "audit.json"

SERVICES = {
    "Hacking Lab": "http://127.0.0.1:9093/",
    "Service Test": "http://127.0.0.1:9094/health",
    "Dashboard": "http://127.0.0.1:9095/api/status",
    "Log Lab": "http://127.0.0.1:9096/health",
    "Master Dashboard": "http://127.0.0.1:9097/api/status",
    "Web Security Lab": "http://127.0.0.1:9098/health",
}


def get_events(limit=20):
    if not EVENT_LOG.exists():
        return []

    lines = EVENT_LOG.read_text(
        encoding="utf-8",
        errors="replace"
    ).splitlines()

    return lines[-limit:]


def get_correlation(limit=100):
    events = []

    for line in get_events(limit=limit):
        parts = line.split(" | ", 3)

        if len(parts) != 4:
            continue

        timestamp, event, service, detail = parts

        if service.startswith("service="):
            service = service[len("service="):]

        events.append({
            "timestamp": timestamp,
            "event": event,
            "service": service,
            "detail": detail
        })

    groups = correlate_events(events)

    result = []

    for group in groups:
        result.append({
            "classification": classify_group(group),
            "count": len(group),
            "events": group
        })

    return {
        "window_seconds": 60,
        "groups": result
    }


def get_summary():
    events = get_events(limit=1000)

    counts = {}

    for line in events:
        parts = line.split(" | ", 3)

        if len(parts) >= 2:
            event_type = parts[1]
            counts[event_type] = counts.get(event_type, 0) + 1

    latest = events[-1] if events else None

    if latest and "BRUTE_FORCE" in latest:
        severity = "HIGH"
    elif events:
        severity = "MEDIUM"
    else:
        severity = "NONE"

    return {
        "total_events": len(events),
        "event_types": counts,
        "latest_event": latest,
        "severity": severity,
        "affected_service": "web-security-lab" if events else None
    }


def get_risk_summary():
    incidents = load_incidents()

    counts = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    open_counts = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for incident in incidents:
        severity = incident.get("severity", "LOW")

        if severity not in counts:
            severity = "LOW"

        counts[severity] += 1

        if incident.get("status") == "OPEN":
            open_counts[severity] += 1

    return {
        "total": len(incidents),
        "by_severity": counts,
        "open_by_severity": open_counts,
    }


def get_alerts():
    incidents = load_incidents()

    alerts = []

    for incident in incidents:
        severity = incident.get("severity", "LOW")

        if severity in {"HIGH", "MEDIUM"}:
            alerts.append({
                "id": incident.get("id"),
                "event": incident.get("event"),
                "service": incident.get("service"),
                "severity": severity,
                "status": incident.get("status"),
                "detail": incident.get("detail"),
                "created": incident.get("created"),
            })

    return {
        "total": len(alerts),
        "alerts": alerts,
    }


def get_alert_summary():
    incidents = load_incidents()

    summary = {
        "total": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for incident in incidents:
        severity = incident.get("severity", "LOW").upper()

        if severity not in summary:
            severity = "LOW"

        summary[severity] += 1
        summary["total"] += 1

    return summary


def get_status():
    results = {}

    for name, url in SERVICES.items():
        try:
            with urlopen(url, timeout=2) as response:
                results[name] = {
                    "status": "online",
                    "http": response.status
                }
        except (HTTPError, URLError, OSError):
            results[name] = {
                "status": "offline"
            }

    online = sum(
        1 for item in results.values()
        if item["status"] == "online"
    )

    return {
        "services": results,
        "online": online,
        "total": len(results),
        "overall": "HEALTHY"
        if online == len(results)
        else "CHECK REQUIRED"
    }


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.startswith("/api/incidents/") and self.path.endswith("/status"):
            try:
                incident_id = int(
                    self.path.split("/")[3]
                )

                length = int(
                    self.headers.get("Content-Length", 0)
                )

                raw = self.rfile.read(length)
                data = json.loads(raw.decode("utf-8"))

                status = data.get("status")
                incident = update_status(
                    incident_id,
                    status
                )

                if incident is None:
                    body = json.dumps({
                        "error": "Invalid incident or status"
                    }).encode()

                    self.send_response(400)
                else:
                    body = json.dumps({
                        "incident": incident
                    }).encode()

                    self.send_response(200)

                self.send_header(
                    "Content-Type",
                    "application/json"
                )
                self.send_header(
                    "Content-Length",
                    str(len(body))
                )
                self.end_headers()
                self.wfile.write(body)

            except (ValueError, json.JSONDecodeError):
                body = json.dumps({
                    "error": "Invalid request"
                }).encode()

                self.send_response(400)
                self.send_header(
                    "Content-Type",
                    "application/json"
                )
                self.send_header(
                    "Content-Length",
                    str(len(body))
                )
                self.end_headers()
                self.wfile.write(body)

        else:
            self.send_response(404)
            self.end_headers()


    def do_GET(self):
        if self.path == "/api/status":
            body = json.dumps(get_status()).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/summary":
            body = json.dumps(get_summary()).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/risk-summary":
            body = json.dumps(
                get_risk_summary()
            ).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header(
                "Content-Length",
                str(len(body))
            )
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/alert-summary":
            body = json.dumps(get_alert_summary()).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/alerts":
            body = json.dumps(get_alerts()).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/correlation":
            body = json.dumps(
                get_correlation()
            ).encode()

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.send_header(
                "Content-Length",
                str(len(body))
            )
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/incidents":
            body = json.dumps({
                "incidents": load_incidents()
            }).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/audit":
            try:
                if AUDIT_LOG.exists():
                    audit = json.loads(
                        AUDIT_LOG.read_text(
                            encoding="utf-8",
                            errors="replace"
                        )
                    )
                else:
                    audit = []

                body = json.dumps({
                    "audit": audit
                }).encode()

                self.send_response(200)

            except (json.JSONDecodeError, OSError):
                body = json.dumps({
                    "error": "Audit log unavailable"
                }).encode()

                self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/api/events":
            body = json.dumps({
                "events": get_events()
            }).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/":
            body = (BASE / "index.html").read_bytes()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_response(404)
            self.end_headers()


server = HTTPServer(("127.0.0.1", 9099), Handler)

print("SOC Dashboard running on 127.0.0.1:9099")
server.serve_forever()
