import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import numpy as np
import os

# -----------------------------------------
# 1. INIT FIREBASE
# -----------------------------------------
cred = credentials.Certificate(
    r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\backend\serviceAccountKey.json"
)
firebase_admin.initialize_app(cred)

db = firestore.client()

# -----------------------------------------
# 2. FETCH CLEANED DATA
# -----------------------------------------
docs = db.collection("CleanedVitalSignsData").stream()

rows = []
for d in docs:
    rows.append(d.to_dict())

df = pd.DataFrame(rows)

# -----------------------------------------
# 3. FIX DATA TYPES
# -----------------------------------------
df["Heart_clean"] = pd.to_numeric(df["Heart_clean"], errors="coerce")
df["Resp_clean"] = pd.to_numeric(df["Resp_clean"], errors="coerce")
df["Range_clean"] = pd.to_numeric(df["Range_clean"], errors="coerce")

# -----------------------------------------
# 4. GROUP BY RUN (Timestamp)
# -----------------------------------------
run_stats = df.groupby("Timestamp").agg(
    Rows=("Heart_clean", "count"),
    Avg_HR_clean=("Heart_clean", "mean"),
    Avg_RR_clean=("Resp_clean", "mean"),
    Avg_Range=("Range_clean", "mean"),
    Range_SD=("Range_clean", "std"),
).reset_index()

# ---------------------------------------------------
# 5. EXTRA FEATURE EXTRACTION (per run)
# ---------------------------------------------------

# HR, RR variability + peak-to-peak amplitude
extra_features = df.groupby("Timestamp").agg(
    HR_SD=("Heart_clean", "std"),
    RR_SD=("Resp_clean", "std"),
    HR_P2P=("Heart_clean", lambda x: float(x.max() - x.min())),
    RR_P2P=("Resp_clean", lambda x: float(x.max() - x.min())),
).reset_index()

# Range slope (movement trend)
def compute_range_slope(values):
    if len(values) < 2:
        return 0.0
    t = np.arange(len(values))
    slope = np.polyfit(t, values, 1)[0]
    return float(slope)

range_slopes = df.groupby("Timestamp")["Range_clean"].apply(compute_range_slope).reset_index()
range_slopes.columns = ["Timestamp", "Range_Slope"]

# Signal quality index (lower movement = higher SQI)
SQI = df.groupby("Timestamp").apply(
    lambda g: float(1 / (g["Range_clean"].std() + 1e-6))
).reset_index()
SQI.columns = ["Timestamp", "SQI"]

# Merge all features into run_stats
run_stats = (
    run_stats
    .merge(extra_features, on="Timestamp")
    .merge(range_slopes, on="Timestamp")
    .merge(SQI, on="Timestamp")
)

# -----------------------------------------
# 6. APPLY CALIBRATION MODEL (for HR only)
# -----------------------------------------
OFFSET = 10.5
run_stats["Final_Accurate_HR"] = run_stats["Avg_HR_clean"] + OFFSET

# -----------------------------------------
# 7. ASSIGN RUN NUMBERS
# -----------------------------------------
run_stats = run_stats.sort_values("Timestamp").reset_index(drop=True)
run_stats["Run"] = run_stats.index + 1

# -----------------------------------------
# 8. SAVE AS CSV LOCALLY
# -----------------------------------------
OUTPUT_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"
os.makedirs(OUTPUT_DIR, exist_ok=True)

csv_path = os.path.join(OUTPUT_DIR, "final_run_stats.csv")
run_stats.to_csv(csv_path, index=False)

print(f"✔ CSV saved at: {csv_path}")

# -----------------------------------------
# 9. SAVE RUN STATS BACK TO FIRESTORE
# -----------------------------------------
run_stats_ref = db.collection("FinalStats")

count = 0

for _, row in run_stats.iterrows():
    run_stats_ref.document(f"Run_{row['Run']}").set({
        "Run": int(row["Run"]),
        "Timestamp": row["Timestamp"],
        "Rows": int(row["Rows"]),
        "Avg_HR_clean": float(row["Avg_HR_clean"]),
        "Avg_RR_clean": float(row["Avg_RR_clean"]),
        "Avg_Range": float(row["Avg_Range"]),
        "Range_SD": float(row["Range_SD"]),
        "HR_SD": float(row["HR_SD"]),
        "RR_SD": float(row["RR_SD"]),
        "HR_P2P": float(row["HR_P2P"]),
        "RR_P2P": float(row["RR_P2P"]),
        "Range_Slope": float(row["Range_Slope"]),
        "SQI": float(row["SQI"]),
        "Final_Accurate_HR": float(row["Final_Accurate_HR"])
    })
    count += 1

print(f"✔ Uploaded {count} run summaries to Firestore (FinalStats collection).")
