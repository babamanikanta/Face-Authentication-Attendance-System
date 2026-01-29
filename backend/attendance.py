import pandas as pd
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTENDANCE_CSV = os.path.join(BASE_DIR, "attendance.csv")


def mark_attendance(emp_id, name, action):
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    emp_id = str(emp_id)
    df = pd.read_csv(ATTENDANCE_CSV)

    today_logs = df[
        (df["employee_id"].astype(str) == emp_id) &
        (df["date"] == today)
    ]

    if action == "in":
        if not today_logs.empty and today_logs.iloc[-1]["action"] == "in":
            return "Already Checked In"

        df.loc[len(df)] = [emp_id, name, today, now, "in"]
        df.to_csv(ATTENDANCE_CSV, index=False)
        return "Checked In Successfully"

    if action == "out":
        if today_logs.empty or today_logs.iloc[-1]["action"] != "in":
            return "No Check-in Found"

        df.loc[len(df)] = [emp_id, name, today, now, "out"]
        df.to_csv(ATTENDANCE_CSV, index=False)
        return "Checked Out Successfully"
