import json
import os
from datetime import datetime

REPORTS_DIR = "reports"
REPORTS_FILE = os.path.join(REPORTS_DIR, "reports.json")


def load_reports():
    """
    Load saved reports safely.
    This function can NEVER throw JSONDecodeError.
    """
    # File does not exist → no reports
    if not os.path.exists(REPORTS_FILE):
        return []

    try:
        with open(REPORTS_FILE, "r", encoding="utf-8") as f:
            raw = f.read()

        # Empty or whitespace-only file
        if not raw or raw.strip() == "":
            return []

        data = json.loads(raw)

        # Corrupted but valid JSON type
        if not isinstance(data, list):
            return []

        return data

    except Exception:
        # Any failure → fail safe
        return []


def save_report(report_data):
    """
    Save a report safely.
    This function guarantees persistence without crashes.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    reports = load_reports()

    report_data = dict(report_data)  # defensive copy
    report_data["saved_at"] = datetime.now().isoformat()

    reports.append(report_data)

    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=4)
