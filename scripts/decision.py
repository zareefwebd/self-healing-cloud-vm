import json
import sys
import os
import datetime

CONFIG_FILE = os.path.expanduser("~/self-healing-cloud/config/thresholds.conf")
LOG_FILE    = os.path.expanduser("~/self-healing-cloud/logs/events.log")

def load_config():
    config = {}
    with open(CONFIG_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip()
    return config

def log_event(message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def analyze(metrics, config):
    cpu_thresh  = float(config.get("CPU_THRESHOLD", 90))
    mem_thresh  = float(config.get("MEMORY_THRESHOLD", 85))
    disk_thresh = float(config.get("DISK_THRESHOLD", 90))

    actions = []

    if metrics["cpu_percent"] > cpu_thresh:
        log_event(f"WARNING - HIGH CPU: {metrics['cpu_percent']}% > {cpu_thresh}%")
        actions.append("restart_service")

    if metrics["memory_percent"] > mem_thresh:
        log_event(f"WARNING - HIGH MEMORY: {metrics['memory_percent']}% > {mem_thresh}%")
        actions.append("restart_service")

    if metrics["disk_percent"] > disk_thresh:
        log_event(f"WARNING - HIGH DISK: {metrics['disk_percent']}% > {disk_thresh}%")
        actions.append("log_only")

    if metrics["service_status"] != "active":
        log_event(f"CRITICAL - SERVICE DOWN: {metrics['service_name']} is {metrics['service_status']}")
        actions.append("restart_service")

    if not actions:
        log_event(f"OK - All metrics normal. CPU:{metrics['cpu_percent']}% MEM:{metrics['memory_percent']}%")

    return list(set(actions))

if __name__ == "__main__":
    raw = sys.stdin.read()
    metrics = json.loads(raw)
    config = load_config()
    actions = analyze(metrics, config)
    # Print ONLY clean JSON — no other text
    result = {"actions": actions, "service": metrics["service_name"]}
    print(json.dumps(result))
