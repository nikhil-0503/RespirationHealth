"""
Train ONE combined multi-output classifier that predicts:
 - HR_Class
 - RR_Class
 - Stress_Class

Creates:
  vitals_classifier.joblib
  vitals_class_metrics.json
"""

import os
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer
import joblib

# ============================================================
# FILE PATHS
# ============================================================
BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"

CSV = os.path.join(BASE_DIR, "final_run_stats.csv")
MODEL_FILE = os.path.join(BASE_DIR, "vitals_classifier.joblib")
METRICS_FILE = os.path.join(BASE_DIR, "vitals_class_metrics.json")

# ============================================================
# 10 FEATURES — MUST match inference script
# ============================================================
FEATURES = [
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD",
    "HR_P2P", "RR_P2P", "SQI", "Range_Slope"
]

TARGETS = ["HR_Class", "RR_Class", "Stress_Class"]


# ============================================================
# LOAD DATA
# ============================================================
def load_data():
    if not os.path.exists(CSV):
        raise FileNotFoundError("❌ final_run_stats.csv not found!")

    df = pd.read_csv(CSV)

    # Drop rows missing any class label
    df = df.dropna(subset=TARGETS)

    # Convert categories to strings (safe)
    for col in TARGETS:
        df[col] = df[col].astype(str)

    # Convert feature columns to numeric
    for f in FEATURES:
        df[f] = pd.to_numeric(df[f], errors="coerce")

    # Remove rows with any missing feature
    df = df.dropna(subset=FEATURES)

    return df


# ============================================================
# TRAIN MODEL
# ============================================================
def train_model():
    df = load_data()

    X = df[FEATURES]
    Y = df[TARGETS]

    # Stratify only by HR_Class (best practice)
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y,
        test_size=0.25,
        random_state=42,
        stratify=Y["HR_Class"]
    )

    # Preprocessing pipeline
    preprocess = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # Base classifier
    base_model = RandomForestClassifier(
        n_estimators=400,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )

    # Wrap inside multi-output classifier
    model = Pipeline([
        ("prep", preprocess),
        ("clf", MultiOutputClassifier(base_model))
    ])

    print("📌 Training multi-output classifier...")
    model.fit(X_train, Y_train)

    print("📌 Evaluating model...")
    Y_pred = model.predict(X_test)

    reports = {}
    for i, label in enumerate(TARGETS):
        reports[label] = classification_report(
            Y_test[label],
            Y_pred[:, i],
            output_dict=True
        )

    # Save model
    joblib.dump(model, MODEL_FILE)
    print(f"✔ Saved model to {MODEL_FILE}")

    # Save evaluation metrics
    with open(METRICS_FILE, "w") as f:
        json.dump(reports, f, indent=2)
    print(f"✔ Saved metrics to {METRICS_FILE}")

    return model, reports


# ============================================================
# PREDICT FUNCTION (same as inference)
# ============================================================
def predict_classes(feature_row: dict):
    """
    Predict HR_Class, RR_Class, Stress_Class
    Input example:

    {
        "Avg_HR_clean": 78,
        "Avg_RR_clean": 13,
        "Avg_Range": 0.65,
        "Range_SD": 0.0021,
        "HR_SD": 0.11,
        "RR_SD": 0.09,
        "HR_P2P": 0.35,
        "RR_P2P": 0.31,
        "SQI": 250,
        "Range_Slope": 0.0001
    }
    """
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError("❌ vitals_classifier.joblib not found. Train first!")

    model = joblib.load(MODEL_FILE)

    df = pd.DataFrame([feature_row], columns=FEATURES)

    pred = model.predict(df)[0]

    return {
        "HR_Class": pred[0],
        "RR_Class": pred[1],
        "Stress_Class": pred[2]
    }


# ============================================================
# RUN TRAINING
# ============================================================
if __name__ == "__main__":
    model, rep = train_model()
    print("\n========== TRAINING SUMMARY ==========")
    print(json.dumps(rep, indent=2))
