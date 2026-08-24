<<<<<<< HEAD
# Cyber-lab
=======
# Cyber Lab

## Services

| Component | Port | Purpose |
|---|---:|---|
| Service Test | 9094 | Health/API testing |
| Dashboard | 9095 | Dashboard service |
| Log Lab | 9096 | Logging and monitoring |
| Master Dashboard | 9097 | Central dashboard |

## Monitoring

- `central-monitor/history.py` — health check history
- `central-monitor/report.py` — monitoring report
- `lab-status/status.py` — final health check
- `control/status.sh` — combined control check

## Security

- `security-audit/` — service security audit
- `incident-lab/` — event detection and incident reports

## Backup

- `backup-lab/backup.py` — create backup
- `backup-lab/verify.py` — verify backup
- `backup-lab/restore_test.py` — test restoration
- `backup-lab/status.py` — backup status

## Quick Checks

### Final system status

    cd ~/cyber-lab/lab-status
    python status.py

### Control check

    cd ~/cyber-lab/control
    ./status.sh

### Backup

    cd ~/cyber-lab/backup-lab
    python backup.py
    python verify.py
    python restore_test.py

## Current Backup

Latest verified backup contains 28 files.

Backup verification: PASS  
Restore test: PASS
>>>>>>> 065f4e4 (Complete SOC dashboard monitoring and health checks)
