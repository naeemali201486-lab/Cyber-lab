#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/cyber-lab"
LOG_DIR="$BASE/runtime-logs"

mkdir -p "$LOG_DIR"

SERVICES=(
    "hacking-lab:9093"
    "service-test:9094"
    "dashboard:9095"
    "log-lab:9096"
    "master-dashboard:9097"
    "web-security-lab:9098"
    "soc-dashboard:9099"
)

port_in_use() {
    local port="$1"

    case "$port" in
        9093) curl -fsS --max-time 2 "http://127.0.0.1:9093/" >/dev/null 2>&1 ;;
        9094) curl -fsS --max-time 2 "http://127.0.0.1:9094/health" >/dev/null 2>&1 ;;
        9095) curl -fsS --max-time 2 "http://127.0.0.1:9095/api/status" >/dev/null 2>&1 ;;
        9096) curl -fsS --max-time 2 "http://127.0.0.1:9096/health" >/dev/null 2>&1 ;;
        9097) curl -fsS --max-time 2 "http://127.0.0.1:9097/api/status" >/dev/null 2>&1 ;;
        9098) curl -fsS --max-time 2 "http://127.0.0.1:9098/health" >/dev/null 2>&1 ;;
        9099) curl -fsS --max-time 2 "http://127.0.0.1:9099/api/status" >/dev/null 2>&1 ;;
        *) return 1 ;;
    esac
}

start_service() {
    local entry="$1"
    local dir="${entry%%:*}"
    local port="${entry##*:}"

    if port_in_use "$port"; then
        echo "Already running: $dir (port $port)"
        return
    fi

    if [ ! -f "$BASE/$dir/server.py" ]; then
        echo "SKIP: $dir/server.py not found"
        return
    fi

    echo "Starting: $dir (port $port)"

    (
        cd "$BASE/$dir" || exit 1
        nohup python -u server.py \
            > "$LOG_DIR/$dir.log" 2>&1 &
    )

    sleep 1

    if port_in_use "$port"; then
        echo "Started successfully: $dir"
    else
        echo "WARNING: $dir did not start on port $port"
    fi
}

echo "=== CYBER LAB START ==="

for service in "${SERVICES[@]}"; do
    start_service "$service"
done

echo
echo "=== SOC MONITOR ==="

if [ -f "$LOG_DIR/soc-monitor.pid" ]; then
    OLD_PID=$(cat "$LOG_DIR/soc-monitor.pid" 2>/dev/null || true)

    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        echo "SOC monitor already running: PID $OLD_PID"
    else
        rm -f "$LOG_DIR/soc-monitor.pid"
    fi
fi

if [ ! -f "$LOG_DIR/soc-monitor.pid" ]; then
    nohup python -u "$BASE/soc-dashboard/monitor.py" \
        > "$LOG_DIR/soc-monitor.log" 2>&1 &

    echo "$!" > "$LOG_DIR/soc-monitor.pid"
    echo "SOC monitor started: PID $(cat "$LOG_DIR/soc-monitor.pid")"
fi

echo
echo "=== LAB WATCHDOG ==="

if [ -f "$LOG_DIR/lab-watchdog.pid" ]; then
    OLD_PID=$(cat "$LOG_DIR/lab-watchdog.pid" 2>/dev/null || true)

    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Lab watchdog already running: PID $OLD_PID"
    else
        rm -f "$LOG_DIR/lab-watchdog.pid"
    fi
fi

if [ ! -f "$LOG_DIR/lab-watchdog.pid" ]; then
    nohup "$BASE/lab-watchdog.sh" \
        > "$LOG_DIR/lab-watchdog-console.log" 2>&1 &

    echo "$!" > "$LOG_DIR/lab-watchdog.pid"
    echo "Lab watchdog started: PID $(cat "$LOG_DIR/lab-watchdog.pid")"
fi

echo
echo "=== START COMPLETE ==="
echo "Check status:"
echo "python $BASE/lab-status/status.py"
