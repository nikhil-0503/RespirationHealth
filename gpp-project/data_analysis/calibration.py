# calibration.py (updated)
import pandas as pd
import numpy as np
import os

# -----------------------
# PATHS - adjust if needed
# -----------------------
CLEAN_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\cleaned_vital_signs.csv"
OUTPUT_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"
FINAL_STATS_FILE = os.path.join(OUTPUT_DIR, "final_run_stats.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------
# LOAD CLEANED SAMPLE DATA
# -----------------------
if not os.path.exists(CLEAN_FILE):
    print("❌ cleaned_vital_signs.csv not found!")
    exit(1)

df = pd.read_csv(CLEAN_FILE)
df["Timestamp"] = df["Timestamp"].astype(str).str.strip()

INVALID_TS = ["", "nan", "None", "NaT", "null", "[]"]
df = df[~df["Timestamp"].isin(INVALID_TS)]
df = df[df["Timestamp"].str.contains(r"\d{2}-\d{2}-\d{4}", regex=True, na=False)]

if df.empty:
    print("❌ No valid timestamps in cleaned_vital_signs.csv")
    exit(0)

# numeric coercions for essential columns
for col in ["Heart_clean", "Resp_clean", "Range_clean"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# drop rows where all vitals missing
df = df.dropna(subset=["Heart_clean", "Resp_clean", "Range_clean"], how="all")

# -----------------------
# LOAD EXISTING FINAL_RUN_STATS TO DETECT NEW RUNS
# -----------------------
if os.path.exists(FINAL_STATS_FILE):
    prev = pd.read_csv(FINAL_STATS_FILE)
    # treat prev Timestamp as string for comparison
    old_timestamps = set(prev["Timestamp"].astype(str))
else:
    prev = pd.DataFrame()
    old_timestamps = set()

# pick only new rows
new_df = df[~df["Timestamp"].astype(str).isin(old_timestamps)].copy()

if len(new_df) == 0:
    print("✔ No new runs detected.")
    exit(0)

print(f"✔ New samples detected: {len(new_df)}")

# -----------------------
# FILTER RUNS WITH < 5 SAMPLES
# -----------------------
new_df = new_df.groupby("Timestamp").filter(lambda g: len(g) >= 5)

if new_df.empty:
    print("⚠ All new timestamps had <5 samples. No valid runs.")
    exit(0)

print(f"✔ Valid new samples after filtering short runs: {len(new_df)}")

# -----------------------
# GROUP INTO RUNS — basic aggregates
# -----------------------
run_stats = new_df.groupby("Timestamp").agg(
    Rows=("Heart_clean", "count"),
    Avg_HR_clean=("Heart_clean", "mean"),
    Avg_RR_clean=("Resp_clean", "mean"),
    Avg_Range=("Range_clean", "mean"),
    Range_SD=("Range_clean", "std")
).reset_index()

# extra features
extra = new_df.groupby("Timestamp").agg(
    HR_SD=("Heart_clean", "std"),
    RR_SD=("Resp_clean", "std"),
    HR_P2P=("Heart_clean", lambda x: float(x.max() - x.min())),
    RR_P2P=("Resp_clean", lambda x: float(x.max() - x.min()))
).reset_index()

def compute_range_slope(vals):
    vals = vals.dropna()
    if len(vals) < 2:
        return 0.0
    t = np.arange(len(vals))
    return float(np.polyfit(t, vals, 1)[0])

range_slopes = new_df.groupby("Timestamp")["Range_clean"].apply(compute_range_slope).reset_index()
range_slopes.columns = ["Timestamp", "Range_Slope"]

def compute_sqi(group):
    std = group["Range_clean"].std()
    if pd.isna(std) or std == 0:
        return 0.0
    return float(1 / std)

SQI = new_df.groupby("Timestamp").apply(compute_sqi).reset_index()
SQI.columns = ["Timestamp", "SQI"]

# merge all pieces
run_stats = (
    run_stats.merge(extra, on="Timestamp")
             .merge(range_slopes, on="Timestamp")
             .merge(SQI, on="Timestamp")
)

# fill NaNs sensibly
fill_zero = ["Range_SD", "HR_SD", "RR_SD", "HR_P2P", "RR_P2P", "Range_Slope", "SQI"]
for c in fill_zero:
    if c in run_stats.columns:
        run_stats[c] = run_stats[c].fillna(0.0)

for c in ["Avg_HR_clean", "Avg_RR_clean", "Avg_Range"]:
    if c in run_stats.columns:
        run_stats[c] = run_stats[c].fillna(0.0)

# -----------------------
# HR CALIBRATION (OFFSET) - keep as before
# -----------------------
OFFSET = 10.5
run_stats["Final_Accurate_HR"] = run_stats["Avg_HR_clean"] + OFFSET

# -----------------------
# AUTO LABELS (classification columns)
# -----------------------
def classify_hr(hr):
    if hr < 65: return "Low"
    elif hr <= 90: return "Normal"
    elif hr <= 115: return "Elevated"
    else: return "High"

def classify_rr(rr):
    if rr < 12: return "Low"
    elif rr <= 20: return "Normal"
    elif rr <= 25: return "Fast"
    else: return "Very High"

def classify_stress(hr_sd):
    # these thresholds are heuristic — adjust later if needed
    if hr_sd < 0.05: return "Relaxed"
    elif hr_sd < 0.15: return "Mild Stress"
    elif hr_sd < 0.25: return "High Stress"
    else: return "Very High Stress"

run_stats["HR_Class"] = run_stats["Avg_HR_clean"].apply(classify_hr)
run_stats["RR_Class"] = run_stats["Avg_RR_clean"].apply(classify_rr)
run_stats["Stress_Class"] = run_stats["HR_SD"].apply(classify_stress)

# -----------------------
# ASSIGN RUN NUMBERS (continue from prev if present)
# -----------------------
last_run = int(prev["Run"].max()) if ("Run" in prev.columns and len(prev) > 0) else 0

run_stats = run_stats.sort_values("Timestamp").reset_index(drop=True)
run_stats["Run"] = run_stats.index + 1 + last_run

# -----------------------
# ENSURE final column order (helps frontend)
# -----------------------
cols_order = [
    "Timestamp", "Run", "Rows",
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD", "HR_P2P", "RR_P2P",
    "Range_Slope", "SQI",
    "Final_Accurate_HR",
    "HR_Class", "RR_Class", "Stress_Class"
]
# keep only columns that exist and maintain order
cols = [c for c in cols_order if c in run_stats.columns]
run_stats = run_stats[cols]

# -----------------------
# APPEND to final CSV
# -----------------------
write_header = not os.path.exists(FINAL_STATS_FILE)

run_stats.to_csv(FINAL_STATS_FILE, mode="a", index=False, header=write_header)

print("==============================================")
print("✔ FINAL RUN STATS UPDATED SUCCESSFULLY")
print(f"✔ New runs added: {len(run_stats)}")
print(f"✔ Saved to: {FINAL_STATS_FILE}")
print("==============================================")
