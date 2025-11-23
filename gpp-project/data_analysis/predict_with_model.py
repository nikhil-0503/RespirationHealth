"""
Inference script to predict HR for latest run using trained ML model.
"""

import os
import pandas as pd
import numpy as np
import joblib

BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"
FINAL_STATS_FILE = os.path.join(BASE_DIR, "final_run_stats.csv")
MODEL_FILE = os.path.join(BASE_DIR, "hr_model.joblib")

FEATURES = [
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD",
    "HR_P2P", "RR_P2P", "SQI", "Range_Slope"
]


def inference_from_latest_run():
    df = pd.read_csv(FINAL_STATS_FILE)
    latest = df.iloc[-1]

    X = latest[FEATURES].astype(float).values.reshape(1, -1)

    model = joblib.load(MODEL_FILE)

    pred = model.predict(X)[0]

    return round(float(pred), 2)


if __name__ == "__main__":
    print(inference_from_latest_run())
