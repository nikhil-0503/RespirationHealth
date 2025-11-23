import os
import pandas as pd
import numpy as np
import joblib
import json

BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"

FINAL_STATS_FILE = os.path.join(BASE_DIR, "final_run_stats.csv")
HR_MODEL_FILE = os.path.join(BASE_DIR, "hr_model.joblib")
CLASSIFIER_MODEL_FILE = os.path.join(BASE_DIR, "vitals_classifier.joblib")

REGRESSION_FEATURES = [
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD",
    "HR_P2P", "RR_P2P", "SQI", "Range_Slope"
]

CLASS_FEATURES = [
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD",
    "HR_P2P", "RR_P2P", "Range_Slope", "SQI"
]


def inference_from_latest_run():
    df = pd.read_csv(FINAL_STATS_FILE)
    latest = df.iloc[-1]

    # ---- HR Regression ----
    X_reg = latest[REGRESSION_FEATURES].astype(float).values.reshape(1, -1)
    hr_model = joblib.load(HR_MODEL_FILE)
    hr_pred = float(hr_model.predict(X_reg)[0])

    # ---- Multi Classification ----
    X_class = latest[CLASS_FEATURES].astype(float).values.reshape(1, -1)
    class_model = joblib.load(CLASSIFIER_MODEL_FILE)
    class_pred = class_model.predict(X_class)[0]

    hr_class, rr_class, stress_class = class_pred

    return {
        "Predicted_HR": round(hr_pred, 2),
        "HR_Class": hr_class,
        "RR_Class": rr_class,
        "Stress_Class": stress_class
    }


if __name__ == "__main__":
    output = inference_from_latest_run()
    print(json.dumps(output))   # <-- IMPORTANT: print ONLY JSON
