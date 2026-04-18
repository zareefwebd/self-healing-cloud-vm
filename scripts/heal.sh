#!/bin/bash

ACTION=$1
SERVICE=$2
LOG_FILE=~/self-healing-cloud/logs/events.log
TIMESTAMP=$(date -Iseconds)
MAX_ATTEMPTS=3
ATTEMPT_FILE=~/self-healing-cloud/logs/restart_attempts.txt

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Track restart attempts to avoid infinite loops
get_attempts() {
    if [ -f "$ATTEMPT_FILE" ]; then
        cat "$ATTEMPT_FILE"
    else
        echo 0
    fi
}

reset_attempts() {
    echo 0 > "$ATTEMPT_FILE"
}

increment_attempts() {
    current=$(get_attempts)
    echo $((current + 1)) > "$ATTEMPT_FILE"
}

if [ "$ACTION" == "restart_service" ]; then
    ATTEMPTS=$(get_attempts)

    if [ "$ATTEMPTS" -ge "$MAX_ATTEMPTS" ]; then
        log "ESCALATE - Max restart attempts ($MAX_ATTEMPTS) reached for $SERVICE. Rebooting VM."
        reset_attempts
        sudo reboot
    else
        log "HEALING - Attempting to restart $SERVICE (attempt $((ATTEMPTS+1)))"
        sudo systemctl restart "$SERVICE"
        sleep 5

        STATUS=$(systemctl is-active "$SERVICE")
        if [ "$STATUS" == "active" ]; then
            log "RECOVERED - $SERVICE restarted successfully."
            reset_attempts
        else
            log "FAILED - $SERVICE restart failed. Incrementing counter."
            increment_attempts
        fi
    fi

elif [ "$ACTION" == "log_only" ]; then
    log "LOGGED - High disk usage detected. No automated action taken. Manual review required."

else
    log "INFO - No healing action required."
fi
