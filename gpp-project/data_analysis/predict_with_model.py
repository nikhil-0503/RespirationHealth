import os
import pandas as pd
import numpy as np
import joblib
import json
import sys

BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"

FINAL_STATS_FILE = os.path.join(BASE_DIR, "final_run_stats_new.csv")

HR_MODEL_FILE = os.path.join(BASE_DIR, "hr_model.joblib")   # regression model
MODEL_HR = os.path.join(BASE_DIR, "hr_class_model.joblib")
MODEL_RR = os.path.join(BASE_DIR, "rr_class_model.joblib")
MODEL_ST = os.path.join(BASE_DIR, "stress_class_model.joblib")

ENCODER_FILE = os.path.join(BASE_DIR, "class_label_encodings.json")

FEATURES = [
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD",
    "HR_P2P", "RR_P2P", "SQI", "Range_Slope"
]


# --------------------------------------------------------
# LOAD LABEL ENCODERS PROPERLY BASED ON YOUR JSON FORMAT
# --------------------------------------------------------
def load_encoders():
    enc = json.load(open(ENCODER_FILE))

    fixed = {}

    for key in ["HR_Class", "RR_Class", "Stress_Class"]:
        mapping = enc[key]["mapping"]       # <-- THIS is correct

        inv = {}
        for label, idx in mapping.items():

            # convert numpy / list types to clean int
            if isinstance(idx, list) and len(idx) == 1:
                idx = idx[0]
            if hasattr(idx, "item"):
                idx = int(idx.item())

            inv[int(idx)] = label

        fixed[key] = inv

    return fixed


# --------------------------------------------------------
# MAIN INFERENCE
# --------------------------------------------------------
def inference_from_latest_run():

    df = pd.read_csv(FINAL_STATS_FILE).drop_duplicates()
    df = df.sort_values("Timestamp")
    latest = df.iloc[-1]

    X = latest[FEATURES].astype(float).values.reshape(1, -1)

    # Load regression
    reg_model = joblib.load(HR_MODEL_FILE)
    hr_pred = float(reg_model.predict(X)[0])

    # Load encoders
    enc = load_encoders()

    # Load classification models
    hr_model = joblib.load(MODEL_HR)
    rr_model = joblib.load(MODEL_RR)
    st_model = joblib.load(MODEL_ST)

    # Predict encoded classes
    hr_encoded = int(hr_model.predict(X)[0])
    rr_encoded = int(rr_model.predict(X)[0])
    st_encoded = int(st_model.predict(X)[0])

    # Decode back to labels
    hr_label = enc["HR_Class"][hr_encoded]
    rr_label = enc["RR_Class"][rr_encoded]
    st_label = enc["Stress_Class"][st_encoded]

    return {
        "Predicted_HR": round(hr_pred, 2),
        "HR_Class": hr_label,
        "RR_Class": rr_label,
        "Stress_Class": st_label
    }


# --------------------------------------------------------
if __name__ == "__main__":
    try:
        out = inference_from_latest_run()
        print(json.dumps(out))
    except Exception as e:
        print("FATAL_ERROR:", str(e))
        raise
