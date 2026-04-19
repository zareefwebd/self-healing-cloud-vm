import psutil
import subprocess
import json
import os

OUTPUT = os.path.expanduser("~/self-healing-cloud/dashboard/metrics.json")

def export():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    result = subprocess.run(["systemctl", "is-active", "apache2"], capture_output=True, text=True)
    service_status = result.stdout.strip()

    data = {
        "cpu_percent": cpu,
        "memory_percent": mem,
        "disk_percent": disk,
        "service_name": "apache2",
        "service_status": service_status
    }
    with open(OUTPUT, "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    export()
