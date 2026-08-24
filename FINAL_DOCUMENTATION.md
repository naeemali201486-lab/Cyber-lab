# CYBER LAB — FINAL DOCUMENTATION

## 1. Project Overview

Cyber Lab is a local security and monitoring environment built with Python and
Termux. It contains service testing, dashboards, log monitoring, security
auditing, incident detection, backup/recovery, centralized monitoring, and
system health control.

---

## 2. Services

| Component | Port | Function |
|---|---:|---|
| Service Test | 9094 | Health/API testing |
| Dashboard | 9095 | Service dashboard |
| Log Lab | 9096 | Logging and monitoring |
| Master Dashboard | 9097 | Central dashboard |

All services use localhost (`127.0.0.1`).

---

## 3. Security Audit

Location:

    ~/cyber-lab/security-audit

Files:

- `audit.py`
- `audit_report.py`
- `summary.py`
- `audit.log`

Purpose:

- Check service availability
- Record HTTP status
- Maintain audit history
- Generate security audit summaries

---

## 4. Incident Lab

Location:

    ~/cyber-lab/incident-lab

Files:

- `events.log`
- `detector.py`
- `alerts.log`
- `summary.py`
- `report.py`
- `incident_report.txt`

The detector identifies:

- FAILED_LOGIN
- DENIED
- ERROR

Current incident state:

    Alerts present

An incident report is generated from detected events.

---

## 5. Backup and Recovery

Location:

    ~/cyber-lab/backup-lab

Files:

- `backup.py`
- `verify.py`
- `restore_test.py`
- `status.py`
- `backups/`

Latest verified backup:

    20260813_172118

Backup contents:

    29 files

Verification:

    PASS

Restore test:

    PASS

Backup and restore are tested before considering the backup valid.

---

## 6. Central Monitoring

Location:

    ~/cyber-lab/central-monitor

Files:

- `history.py`
- `monitor.log`
- `report.py`

Purpose:

- Monitor all primary services
- Record online/offline checks
- Maintain monitoring history
- Generate monitoring reports

---

## 7. Master Dashboard

Location:

    ~/cyber-lab/master-dashboard

Port:

    9097

Files:

- `index.html`
- `server.py`

Purpose:

- Provide a central dashboard
- Display lab status
- Provide a live `/api/status` endpoint

---

## 8. Final Lab Status

Location:

    ~/cyber-lab/lab-status

File:

    status.py

Checks:

- Service Test
- Dashboard
- Log Lab
- Master Dashboard
- Backup availability
- Incident alerts

Healthy condition:

    4/4 services online

Expected result:

    Overall: LAB HEALTHY

---

## 9. Control System

Location:

    ~/cyber-lab/control

File:

    status.sh

The control script runs:

1. Final system health check
2. Backup status check
3. Combined PASS/FAIL decision

Successful result:

    CONTROL: PASS
    Exit code: 0

If a service is offline:

    CONTROL: CHECK REQUIRED
    Exit code: 1

This makes the control script suitable for automated health checking.

---

## 10. Documentation

Main documentation:

- `README.md`
- `FINAL_REPORT.txt`
- `FINAL_DOCUMENTATION.md`

`FINAL_REPORT.txt` contains the final project status.

---

## 11. Quick Start

### Start Service Test

    cd ~/cyber-lab/service-test
    python server.py

### Start Dashboard

    cd ~/cyber-lab/dashboard
    python server.py

### Start Log Lab

    cd ~/cyber-lab/log-lab
    python server.py

### Start Master Dashboard

    cd ~/cyber-lab/master-dashboard
    python server.py

Keep the four server sessions running.

---

## 12. Final Health Check

Run from another Termux session:

    cd ~/cyber-lab/control
    ./status.sh

Successful result:

    Services online: 4/4
    Overall: LAB HEALTHY
    CONTROL: PASS
    Exit code: 0

---

## 13. Backup Procedure

Run:

    cd ~/cyber-lab/backup-lab
    python backup.py
    python verify.py
    python restore_test.py

Expected:

    Backup verification: PASS
    Restore test: PASS

---

## 14. Project Structure

    cyber-lab/
    ├── web/
    ├── service-test/
    ├── dashboard/
    ├── log-lab/
    ├── security-audit/
    ├── incident-lab/
    ├── backup-lab/
    ├── central-monitor/
    ├── master-dashboard/
    ├── lab-status/
    ├── control/
    ├── README.md
    ├── FINAL_REPORT.txt
    └── FINAL_DOCUMENTATION.md

---

## 15. Final Assessment

System architecture: COMPLETE

Monitoring: COMPLETE

Security audit: COMPLETE

Incident detection: COMPLETE

Backup: COMPLETE

Restore testing: COMPLETE

Central monitoring: COMPLETE

Master dashboard: COMPLETE

Control system: COMPLETE

Documentation: COMPLETE

Latest backup: 29 files

Latest backup verification: PASS

Latest restore test: PASS

Final project state:

    CYBER LAB — COMPLETE
