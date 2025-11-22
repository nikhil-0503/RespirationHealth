"""
Train a calibration model to predict Final_Accurate_HR from run-level features.

Usage:
  python train_calibration_model.py         # trains on final_run_stats.csv and saves model
  # or import inference function from this file in your pipeline to predict new runs
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, RepeatedKFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
import joblib
import json
import warnings

warnings.filterwarnings("ignore")

# -----------------------
# CONFIG - change paths if needed
# -----------------------
FINAL_STATS_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\final_run_stats.csv"   # path to run-level CSV
MODEL_OUTPUT_PATH = os.path.join(os.path.dirname(FINAL_STATS_FILE), "calibration_model.joblib")
METRICS_OUTPUT_PATH = os.path.join(os.path.dirname(FINAL_STATS_FILE), "calibration_metrics.json")

# Features to use (these are present in your final_run_stats.csv)
FEATURE_COLS = [
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD", "HR_P2P", "RR_P2P",
    "Range_Slope", "SQI"
]
TARGET_COL = "Final_Accurate_HR"

RANDOM_STATE = 42

# -----------------------
# HELPERS
# -----------------------
def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found.")
    df = pd.read_csv(path)
    # ensure Timestamp string presence
    if "Timestamp" in df.columns:
        df["Timestamp"] = df["Timestamp"].astype(str)
    return df

def prepare_features(df, feature_cols, target_col):
    # keep only rows with target present
    df = df.copy()
    df[target_col] = pd.to_numeric(df[target_col], errors="coerce")
    df = df.dropna(subset=[target_col])
    # ensure features exist, if missing create with zeros
    for c in feature_cols:
        if c not in df.columns:
            df[c] = 0.0
    X = df[feature_cols].replace([np.inf, -np.inf], np.nan)
    y = df[target_col].astype(float)
    return X, y, df

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)

    # FIX HERE
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5

    r2 = r2_score(y_test, y_pred)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

# -----------------------
# MAIN training routine
# -----------------------
def train_and_save():
    print("Loading data:", FINAL_STATS_FILE)
    df = load_data(FINAL_STATS_FILE)

    print("Preparing features...")
    X, y, df_filtered = prepare_features(df, FEATURE_COLS, TARGET_COL)

    if X.shape[0] < 5:
        print("⚠️ Warning: Very small dataset (n < 5). Model will still run but results are unstable.")

    # Split into train/test (stratify not applicable for regression)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    # Pipeline: imputer -> scaler -> model
    base_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # 1) RandomForest
    rf = Pipeline([
        ("prep", base_pipeline),
        ("model", RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1))
    ])

    # 2) GradientBoosting
    gb = Pipeline([
        ("prep", base_pipeline),
        ("model", GradientBoostingRegressor(n_estimators=500, learning_rate=0.05,
                                            max_depth=3, random_state=RANDOM_STATE))
    ])

    # Quick cross-validated scoring
    cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=RANDOM_STATE)

    print("Cross-validating RandomForest...")
    rf_scores = cross_val_score(rf, X_train, y_train, scoring="neg_mean_absolute_error", cv=cv, n_jobs=-1)
    print(f"RF CV MAE (neg): {np.mean(rf_scores):.4f} (std {np.std(rf_scores):.4f})")

    print("Cross-validating GradientBoosting...")
    gb_scores = cross_val_score(gb, X_train, y_train, scoring="neg_mean_absolute_error", cv=cv, n_jobs=-1)
    print(f"GB CV MAE (neg): {np.mean(gb_scores):.4f} (std {np.std(gb_scores):.4f})")

    # Fit both on full training set
    print("Fitting models on training set...")
    rf.fit(X_train, y_train)
    gb.fit(X_train, y_train)

    # Evaluate on test set
    print("Evaluating on test set...")
    rf_metrics = evaluate_model(rf, X_test, y_test)
    gb_metrics = evaluate_model(gb, X_test, y_test)

    print("RF test metrics:", rf_metrics)
    print("GB test metrics:", gb_metrics)

    # Choose best by RMSE then MAE
    if rf_metrics["RMSE"] <= gb_metrics["RMSE"]:
        best_model = rf
        best_metrics = rf_metrics
        chosen = "RandomForest"
    else:
        best_model = gb
        best_metrics = gb_metrics
        chosen = "GradientBoosting"

    print(f"Chosen model: {chosen}. Saving to {MODEL_OUTPUT_PATH}")
    joblib.dump(best_model, MODEL_OUTPUT_PATH)

    # Save metrics + feature importances if possible
    metrics_out = {
        "chosen_model": chosen,
        "rf_metrics": rf_metrics,
        "gb_metrics": gb_metrics,
        "n_train": int(X_train.shape[0]),
        "n_test": int(X_test.shape[0]),
        "features": FEATURE_COLS
    }

    # Try to extract feature importances
    try:
        final_model = best_model.named_steps["model"]
        if hasattr(final_model, "feature_importances_"):
            importances = final_model.feature_importances_.tolist()
            metrics_out["feature_importances"] = dict(zip(FEATURE_COLS, importances))
    except Exception:
        pass

    with open(METRICS_OUTPUT_PATH, "w") as f:
        json.dump(metrics_out, f, indent=2)

    print("✔ Model training completed. Metrics saved at:", METRICS_OUTPUT_PATH)
    print("✔ Model saved at:", MODEL_OUTPUT_PATH)
    return best_model, metrics_out

# -----------------------
# Inference helper for pipeline integration
# -----------------------
def inference(run_row):
    """
    Given a dict-like or pandas Series with columns = FEATURE_COLS,
    return predicted Final_Accurate_HR using the saved model.
    Example:
      run_row = {
        "Avg_HR_clean": 78.2, "Avg_RR_clean": 13.7, ...
      }
    """
    if not os.path.exists(MODEL_OUTPUT_PATH):
        raise FileNotFoundError("Model not found. Run training first.")

    model = joblib.load(MODEL_OUTPUT_PATH)

    # Build DataFrame from single row
    row_df = pd.DataFrame([run_row], columns=FEATURE_COLS)
    # same preprocessing pipeline inside model handles NaNs
    pred = model.predict(row_df)[0]
    return float(pred)

# -----------------------
# If run as script, train
# -----------------------
if __name__ == "__main__":
    model, metrics = train_and_save()
    # print short summary
    print("\nSUMMARY:")
    print(json.dumps(metrics, indent=2))
