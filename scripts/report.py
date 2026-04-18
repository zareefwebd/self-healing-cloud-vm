import os
import datetime

LOG_FILE    = os.path.expanduser("~/self-healing-cloud/logs/events.log")
REPORT_DIR  = os.path.expanduser("~/self-healing-cloud/reports/")

def generate_report():
    os.makedirs(REPORT_DIR, exist_ok=True)
    today = datetime.date.today().isoformat()
    report_path = os.path.join(REPORT_DIR, f"report_{today}.txt")

    counts = {"OK": 0, "WARNING": 0, "CRITICAL": 0, "RECOVERED": 0, "FAILED": 0, "ESCALATE": 0}

    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return

    with open(LOG_FILE) as f:
        for line in f:
            for key in counts:
                if key in line:
                    counts[key] += 1

    with open(report_path, "w") as r:
        r.write(f"Daily Report - {today}\n")
        r.write("=" * 40 + "\n")
        for k, v in counts.items():
            r.write(f"{k}: {v}\n")
        r.write("=" * 40 + "\n")
        r.write("See logs/events.log for full details.\n")

    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    generate_report()
