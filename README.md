# Intelligent Failure Prediction & Self-Healing for Cloud VMs

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Shell](https://img.shields.io/badge/Shell-Bash-green)
![Platform](https://img.shields.io/badge/Platform-Linux-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview
A lightweight, rule-based system that continuously monitors cloud VM metrics
in real time, predicts failures based on configurable thresholds, and
automatically heals services without any manual intervention.

Designed for private and hybrid cloud environments where enterprise solutions
are too expensive or complex.

---

## Features
- Real-time monitoring of CPU, memory, disk, and service status
- Rule-based failure prediction engine with configurable thresholds
- Automated self-healing: service restart with escalation to VM reboot
- Full event logging with timestamps for every action taken
- Daily summary report generation
- Cron-based scheduling — runs automatically every minute
- Compatible with Apache CloudStack and standard Linux VMs

---

## Project Structure
self-healing-cloud/
├── scripts/
│   ├── monitor.py         # Collects CPU, memory, disk, service metrics
│   ├── decision.py        # Rule-based prediction and decision engine
│   ├── heal.sh            # Executes healing actions with escalation
│   ├── run_pipeline.sh    # Main orchestrator — ties all scripts together
│   └── report.py          # Generates daily summary reports
├── config/
│   └── thresholds.conf    # All configurable thresholds in one place
├── logs/
│   ├── events.log         # Full timestamped log of all events
│   └── restart_attempts.txt  # Tracks restart count to prevent loops
├── reports/
│   └── report_YYYY-MM-DD.txt  # Daily report files
└── README.md

---
---

## Requirements
- Ubuntu 22.04 or any Debian-based Linux
- Python 3.x
- python3-psutil (`sudo apt install python3-psutil`)
- Apache2 or any systemd-managed service
- Cron

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/self-healing-cloud-vm.git
cd self-healing-cloud-vm
```

### 2. Install dependencies
```bash
sudo apt install python3-psutil -y
```

### 3. Configure thresholds
```bash
nano config/thresholds.conf
```
Edit the values to match your environment:
CPU_THRESHOLD=90
MEMORY_THRESHOLD=85
DISK_THRESHOLD=90
SERVICE_NAME=apache2
MAX_RESTART_ATTEMPTS=3


### 4. Give execute permission to shell scripts
```bash
chmod +x scripts/heal.sh
chmod +x scripts/run_pipeline.sh
```

### 5. Allow sudo without password for automation
```bash
sudo visudo
# Add this line (replace yourusername):
yourusername ALL=(ALL) NOPASSWD: /bin/systemctl, /sbin/reboot
```

### 6. Run manually to test
```bash
bash scripts/run_pipeline.sh
cat logs/events.log
```

### 7. Schedule with cron for automatic execution
```bash
crontab -e
```
Add:/bin/bash /home/yourusername/self-healing-cloud/scripts/run_pipeline.sh >> /home/yourusername/self-healing-cloud/logs/cron.log 2>&1
0 0 * * * python3 /home/yourusername/self-healing-cloud/scripts/report.py >> /home/yourusername/self-healing-cloud/logs/cron.log 2>&1


---

## How It Works

1. **monitor.py** collects CPU, memory, disk, and service status every cycle
2. **decision.py** compares metrics against thresholds and logs warnings
3. **heal.sh** restarts the service; escalates to VM reboot after max attempts
4. **report.py** counts all events and generates a daily summary

### Prediction Rules
| Condition | Threshold | Action |
|---|---|---|
| CPU usage | > 90% | Restart service |
| Memory usage | > 85% | Restart service |
| Disk usage | > 90% | Log warning |
| Service down | Not active | Restart service |
| Restart fails repeatedly | > 3 attempts | Reboot VM |

---

## Test Results

### Test 1 — Normal Condition
- All metrics within threshold
- Log shows: `OK - All metrics normal`

### Test 2 — Service Crash Recovery
- apache2 stopped manually
- System detected and restarted within one pipeline cycle
- Log shows: `CRITICAL → HEALING → RECOVERED`

### Test 3 — High CPU Detection
- CPU spiked to 97% using stress tool
- Warning logged and healing triggered
- Log shows: `WARNING - HIGH CPU: 97.3% > 90%`

### Test 4 — High Memory Detection
- Memory pushed to 87% using stress-ng
- Warning detected and logged
- Log shows: `WARNING - HIGH MEMORY: 87.4% > 85%`

### Test 5 — Escalation Path
- Service kept crashing beyond max restart attempts
- System escalated to VM reboot automatically
- Log shows: `ESCALATE - Max restart attempts reached`

---

## Author
- **Name**: Mohammad Zareef Saim
- **Reg No**: 12219266

---

## License
This project is licensed under the MIT License.


