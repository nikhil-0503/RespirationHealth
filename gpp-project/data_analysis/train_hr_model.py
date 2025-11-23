"""
Train a machine learning model to predict Heart Rate (HR)
from final_run_stats.csv using XGBoost.

Usage:
  python train_hr_model.py
"""

import os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
import warnings

warnings.filterwarnings("ignore")

# ----------------------------------------------------
# CONFIG
# ----------------------------------------------------
BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"
FINAL_STATS_FILE = os.path.join(BASE_DIR, "final_run_stats.csv")
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, "hr_model.joblib")
METRICS_OUTPUT_PATH = os.path.join(BASE_DIR, "hr_model_metrics.json")

FEATURES = [
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD",
    "HR_P2P", "RR_P2P", "SQI", "Range_Slope"
]

TARGET = "Final_Accurate_HR"
RANDOM_STATE = 42

# ----------------------------------------------------
# TRAINING FUNCTION
# ----------------------------------------------------
def train_hr_model():
    print("📌 Loading:", FINAL_STATS_FILE)
    df = pd.read_csv(FINAL_STATS_FILE)

    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df = df.dropna(subset=[TARGET])

    X = df[FEATURES]
    y = df[TARGET]

    if len(X) < 5:
        print("⚠ WARNING: Very small dataset. Training may be unstable.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="reg:squarederror",
            random_state=RANDOM_STATE
        ))
    ])

    print("🚀 Training XGBoost model...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "features": FEATURES
    }

    print("\n📊 MODEL PERFORMANCE:")
    print(json.dumps(metrics, indent=2))

    joblib.dump(pipeline, MODEL_OUTPUT_PATH)
    print("✔ Model saved at:", MODEL_OUTPUT_PATH)

    with open(METRICS_OUTPUT_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("✔ Metrics saved at:", METRICS_OUTPUT_PATH)

    return pipeline


if __name__ == "__main__":
    train_hr_model()
