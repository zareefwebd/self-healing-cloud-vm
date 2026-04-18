import psutil
import subprocess
import json
import datetime
import os

CONFIG_FILE = os.path.expanduser("~/self-healing-cloud/config/thresholds.conf")

def load_config():
    config = {}
    with open(CONFIG_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip()
    return config

def collect_metrics(config):
    service = config.get("SERVICE_NAME", "apache2")
    
    # CPU usage over 1 second
    cpu = psutil.cpu_percent(interval=1)
    
    # Memory usage
    mem = psutil.virtual_memory()
    memory_percent = mem.percent
    
    # Disk usage
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    
    # Service status
    result = subprocess.run(
        ["systemctl", "is-active", service],
        capture_output=True, text=True
    )
    service_status = result.stdout.strip()  # "active" or "inactive"
    
    metrics = {
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu_percent": cpu,
        "memory_percent": memory_percent,
        "disk_percent": disk_percent,
        "service_name": service,
        "service_status": service_status
    }
    return metrics

if __name__ == "__main__":
    config = load_config()
    metrics = collect_metrics(config)
    print(json.dumps(metrics))
