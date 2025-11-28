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
# SAFE CLEAN FUNCTION -> handles ANY shape
# --------------------------------------------------------
def clean_pred(v):
    """
    Takes ANY output and returns a clean integer.
    Handles:
      - integer
      - array([1])
      - array([[1]])
      - array([0., 1.])  <-- probability vector
      - list [1]
      - list [[1]]
      - list of probas
    """

    # 1️⃣ Direct integer
    if isinstance(v, (int, np.integer)):
        return int(v)

    # 2️⃣ If numpy array:
    if isinstance(v, np.ndarray):
        arr = v.flatten()

        # Probability vector? (example: [0. 1.])
        if arr.dtype.kind == "f" and len(arr) > 1:
            return int(np.argmax(arr))

        # Must be scalar after flatten
        if len(arr) != 1:
            raise ValueError(f"Cannot convert array of size {len(arr)} to scalar: {arr}")

        return int(arr[0])

    # 3️⃣ If list / tuple:
    if isinstance(v, (list, tuple)):
        if len(v) == 1:
            return clean_pred(v[0])

        # Probability list (example [0.1, 0.9])
        if all(isinstance(x, float) for x in v):
            return int(np.argmax(v))

        raise ValueError(f"List has more than 1 element: {v}")

    raise ValueError(f"Unknown prediction type: {type(v)}, value={v}")



# --------------------------------------------------------
# LOAD LABEL ENCODERS
# --------------------------------------------------------
def load_encoders():
    enc = json.load(open(ENCODER_FILE))

    fixed = {}

    for key in ["HR_Class", "RR_Class", "Stress_Class"]:
        mapping = enc[key]["mapping"]
        inv = {}

        # mapping is dict: label -> encoded_int
        for label, idx in mapping.items():
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

    # Regression
    reg_model = joblib.load(HR_MODEL_FILE)
    hr_pred = float(reg_model.predict(X)[0])

    # Encoders
    enc = load_encoders()

    # Classifier models
    hr_model = joblib.load(MODEL_HR)
    rr_model = joblib.load(MODEL_RR)
    st_model = joblib.load(MODEL_ST)

    # Clean predictions
    hr_code = clean_pred(hr_model.predict(X))
    rr_code = clean_pred(rr_model.predict(X))
    st_code = clean_pred(st_model.predict(X))

    # Decode
    hr_label = enc["HR_Class"].get(hr_code, "Unknown")
    rr_label = enc["RR_Class"].get(rr_code, "Unknown")
    st_label = enc["Stress_Class"].get(st_code, "Unknown")

    return {
        "Predicted_HR": round(hr_pred, 2),
        "HR_Class": hr_label,
        "RR_Class": rr_label,
        "Stress_Class": st_label
    }


# --------------------------------------------------------
# RUN
# --------------------------------------------------------
if __name__ == "__main__":
    try:
        out = inference_from_latest_run()
        print(json.dumps(out))
    except Exception as e:
        print("FATAL_ERROR:", str(e))
        raise
