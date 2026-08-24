#!/data/data/com.termux/files/usr/bin/bash

echo "================================"
echo "       CYBER LAB CONTROL"
echo "================================"
echo

echo "[1] Final system status"
cd ~/cyber-lab/lab-status
python status.py

SYSTEM_OK=$?

echo
echo "[2] Backup status"
cd ~/cyber-lab/backup-lab
python status.py

BACKUP_OK=$?

echo
echo "================================"

if [ "$SYSTEM_OK" -eq 0 ] && [ "$BACKUP_OK" -eq 0 ]; then
    echo "       CONTROL: PASS"
    echo "================================"
    exit 0
else
    echo "       CONTROL: CHECK REQUIRED"
    echo "================================"
    exit 1
fi
