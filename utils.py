# utils.py
import pandas as pd
from datetime import datetime
import os

LOG_FILE = "team_logs.csv"

def log_standup(member_name, original_update, summary, tags):
    """
    Save standup update (with summary and tags) to team_logs.csv
    """
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "member": member_name,
        "original_update": original_update,
        "summary": summary,
        "tags": ",".join(tags)
    }

    # If file doesn’t exist, create with headers
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame([log_entry])
        df.to_csv(LOG_FILE, index=False)
    else:
        df = pd.DataFrame([log_entry])
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)


def log_prediction(features, prediction):
    """
    Save sprint prediction to team_logs.csv
    """
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "member": "SPRINT_PREDICTOR",
        "original_update": str(features),
        "summary": f"Predicted story points: {prediction:.2f}",
        "tags": "prediction"
    }

    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame([log_entry])
        df.to_csv(LOG_FILE, index=False)
    else:
        df = pd.DataFrame([log_entry])
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
