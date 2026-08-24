SEVERITY_SCORE = {
    "HIGH": 90,
    "MEDIUM": 50,
    "LOW": 20,
}


def evaluate_alert(event, severity):
    severity = severity.upper()

    if severity not in SEVERITY_SCORE:
        severity = "LOW"

    return {
        "event": event,
        "severity": severity,
        "score": SEVERITY_SCORE[severity],
        "alert": severity in {"HIGH", "MEDIUM"},
    }
