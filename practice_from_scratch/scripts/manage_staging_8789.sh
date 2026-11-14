#!/usr/bin/env bash
# Service Management & Healthcheck Wrapper for JUNIOR DEVELOPER Staging Server (Port 8789)
# Strictly isolates port 8789 and never modifies or interrupts production port 8788.
set -euo pipefail

STAGING_ROOT="/Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged"
PYTHON_BIN="/Users/huynguyen/Developer/portfolio/motion-estimator-asic-lab-notebook-2026/.venv/bin/python"
SERVER_SCRIPT="${STAGING_ROOT}/practice_from_scratch/web_console/server.py"
LOG_DIR="${STAGING_ROOT}/evidence/logs"
STDOUT_LOG="${LOG_DIR}/staging_8789_stdout.log"
STDERR_LOG="${LOG_DIR}/staging_8789_stderr.log"
PID_FILE="${LOG_DIR}/staging_8789.pid"
PLIST_PATH="${HOME}/Library/LaunchAgents/com.juniordeveloper.engr852.staging8789.plist"
PORT=8789

mkdir -p "${LOG_DIR}"

get_8789_pid() {
    lsof -ti tcp:${PORT} -sTCP:LISTEN 2>/dev/null | head -n 1 || true
}

start_service() {
    local pid
    pid="$(get_8789_pid)"
    if [[ -n "${pid}" ]]; then
        echo "[staging-8789] Already running (PID ${pid}) on http://127.0.0.1:${PORT}/"
        return 0
    fi
    if [[ -f "${PLIST_PATH}" ]]; then
        # LaunchAgent is the ONLY supervisor when installed; no second fallback server.
        launchctl unload "${PLIST_PATH}" >/dev/null 2>&1 || true
        launchctl load -w "${PLIST_PATH}" >/dev/null 2>&1
        for (( attempt=0; attempt<12; attempt++ )); do
            pid="$(get_8789_pid)"
            [[ -n "${pid}" ]] && break
            sleep 1
        done
        if [[ -z "${pid}" ]]; then
            echo "[staging-8789] LaunchAgent failed to bind; refusing duplicate fallback" >&2
            return 1
        fi
    else
        cd "${STAGING_ROOT}"
        nohup "${PYTHON_BIN}" "${SERVER_SCRIPT}" --port "${PORT}" >>"${STDOUT_LOG}" 2>>"${STDERR_LOG}" &
        echo $! > "${PID_FILE}"
        for (( attempt=0; attempt<8; attempt++ )); do
            pid="$(get_8789_pid)"
            [[ -n "${pid}" ]] && break
            sleep 1
        done
    fi
    if [[ -n "${pid}" ]]; then
        echo "${pid}" > "${PID_FILE}"
        echo "[staging-8789] Started successfully (PID ${pid}) on http://127.0.0.1:${PORT}/"
    else
        echo "[staging-8789] ERROR: Failed to bind port ${PORT}" >&2
        return 1
    fi
}

stop_service() {
    if [[ -f "${PLIST_PATH}" ]]; then
        launchctl unload "${PLIST_PATH}" >/dev/null 2>&1 || true
    fi
    local pid
    pid="$(get_8789_pid)"
    if [[ -n "${pid}" ]]; then
        kill "${pid}" 2>/dev/null || true
        sleep 1
    fi
    rm -f "${PID_FILE}"
    echo "[staging-8789] Stopped port ${PORT} listener (Production 8788 untouched)."
}

status_service() {
    local pid8789 pid8788
    pid8789="$(get_8789_pid)"
    pid8788="$(lsof -ti tcp:8788 -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
    echo "=== JUNIOR DEVELOPER Service Status ==="
    echo "Staging    (127.0.0.1:8789) : ${pid8789:+LISTENING (PID ${pid8789})}${pid8789:-STOPPED}"
    echo "Production (127.0.0.1:8788) : ${pid8788:+LISTENING (PID ${pid8788}, UNTOUCHED)}${pid8788:-NOT_DETECTED}"
    echo "LaunchAgent Plist           : ${PLIST_PATH}"
}

healthcheck_service() {
    status_service
    echo "--- HTTP Healthcheck (http://127.0.0.1:${PORT}/api/v8/build-version) ---"
    curl -fsS --max-time 5 "http://127.0.0.1:${PORT}/api/v8/build-version"
    echo ""
}

logs_service() {
    echo "=== Tail of ${STDOUT_LOG} & ${STDERR_LOG} ==="
    tail -n 40 "${STDOUT_LOG}" "${STDERR_LOG}" 2>/dev/null || true
}

ACTION="${1:-status}"
case "${ACTION}" in
    start)       start_service ;;
    stop)        stop_service ;;
    restart)     stop_service; start_service ;;
    status)      status_service ;;
    healthcheck) healthcheck_service ;;
    logs)        logs_service ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|healthcheck|logs}" >&2
        exit 2
        ;;
esac
