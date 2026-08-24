#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/cyber-lab"
LOG="$BASE/runtime-logs/lab-watchdog.log"

mkdir -p "$BASE/runtime-logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

check_url() {
    curl -fsS \
        --connect-timeout 2 \
        --max-time 3 \
        "$1" >/dev/null 2>&1
}

while true; do

    HEALTHY=true

    # Core lab services
    check_url "http://127.0.0.1:9093/" || {
        log "Hacking Lab unhealthy"
        HEALTHY=false
    }

    check_url "http://127.0.0.1:9094/health" || {
        log "Service Test unhealthy"
        HEALTHY=false
    }

    check_url "http://127.0.0.1:9095/api/status" || {
        log "Dashboard unhealthy"
        HEALTHY=false
    }

    check_url "http://127.0.0.1:9096/health" || {
        log "Log Lab unhealthy"
        HEALTHY=false
    }

    check_url "http://127.0.0.1:9097/api/status" || {
        log "Master Dashboard unhealthy"
        HEALTHY=false
    }

    check_url "http://127.0.0.1:9098/health" || {
        log "Web Security Lab unhealthy"
        HEALTHY=false
    }

    # SOC Dashboard
    check_url "http://127.0.0.1:9099/" || {
        log "SOC Dashboard unhealthy"
        HEALTHY=false
    }

    # Recover all lab servers if any service is unhealthy
    if [ "$HEALTHY" = false ]; then
        log "Service failure detected - restarting lab"

        "$BASE/start-lab.sh" \
            >> "$BASE/runtime-logs/watchdog-start.log" 2>&1

        sleep 5
    fi

    # SOC monitor process check
    MONITOR_OK=false

    if [ -f "$BASE/runtime-logs/soc-monitor.pid" ]; then
        PID=$(cat "$BASE/runtime-logs/soc-monitor.pid" 2>/dev/null || true)

        if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
            MONITOR_OK=true
        fi
    fi

    if [ "$MONITOR_OK" = false ]; then
        log "SOC monitor missing - restarting monitor"

        nohup python -u "$BASE/soc-dashboard/monitor.py" \
            >> "$BASE/runtime-logs/soc-monitor.log" 2>&1 &

        echo "$!" > "$BASE/runtime-logs/soc-monitor.pid"
    fi

    if [ "$HEALTHY" = true ] && [ "$MONITOR_OK" = true ]; then
        log "All services healthy; SOC monitor healthy"
    fi

    sleep 10
done
