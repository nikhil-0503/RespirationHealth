import pandas as pd
import joblib
import os

BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"
FINAL_STATS = os.path.join(BASE_DIR, "final_run_stats.csv")
MODEL_FILE = os.path.join(BASE_DIR, "calibration_model.pkl")

def inference_from_latest_run():
    df = pd.read_csv(FINAL_STATS)
    last = df.iloc[-1]   # last appended run

    feature_cols = [
        "Avg_HR_clean","Avg_RR_clean","Avg_Range",
        "Range_SD","HR_SD","RR_SD","HR_P2P","RR_P2P",
        "Range_Slope","SQI"
    ]

    X = last[feature_cols].values.reshape(1,-1)

    model = joblib.load(MODEL_FILE)
    prediction = model.predict(X)[0]

    return prediction

if __name__ == "__main__":
    print(inference_from_latest_run())
