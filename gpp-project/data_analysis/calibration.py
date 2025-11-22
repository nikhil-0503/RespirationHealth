import pandas as pd
import numpy as np
import os
import re

# -----------------------------------------------------
# 1. PATHS
# -----------------------------------------------------
CLEAN_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\cleaned_vital_signs.csv"
OUTPUT_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis"
FINAL_STATS_FILE = os.path.join(OUTPUT_DIR, "final_run_stats.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------
# 2. LOAD CLEANED SAMPLE DATA
# -----------------------------------------------------
if not os.path.exists(CLEAN_FILE):
    print("❌ cleaned_vital_signs.csv not found!")
    exit()

df = pd.read_csv(CLEAN_FILE)

# -----------------------------------------------------
# 3. CLEAN TIMESTAMP COLUMN
# -----------------------------------------------------
df["Timestamp"] = (
    df["Timestamp"]
    .astype(str)
    .str.strip()
)

# Remove invalid timestamp values
INVALID_TS = ["", "nan", "None", "NaT", "null", "[]"]
df = df[~df["Timestamp"].isin(INVALID_TS)]

# Keep only valid dd-mm-yyyy timestamps
df = df[df["Timestamp"].str.contains(r"\d{2}-\d{2}-\d{4}", regex=True, na=False)]

if df.empty:
    print("❌ No valid timestamps in cleaned_vital_signs.csv")
    exit()

# Convert numeric columns
for col in ["Heart_clean", "Resp_clean", "Range_clean"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows where all vital signs are missing
df = df.dropna(subset=["Heart_clean", "Resp_clean", "Range_clean"], how="all")

# -----------------------------------------------------
# 4. LOAD EXISTING FINAL_RUN_STATS TO DETECT NEW RUNS
# -----------------------------------------------------
if os.path.exists(FINAL_STATS_FILE):
    prev = pd.read_csv(FINAL_STATS_FILE)
    old_timestamps = set(prev["Timestamp"].astype(str))
else:
    prev = pd.DataFrame()
    old_timestamps = set()

# Filter only NEW timestamps
new_df = df[~df["Timestamp"].isin(old_timestamps)].copy()

if len(new_df) == 0:
    print("✔ No new runs detected.")
    exit()

print(f"✔ New samples detected: {len(new_df)}")

# -----------------------------------------------------
# 5. REMOVE RUNS WITH < 5 SAMPLES (invalid runs)
# -----------------------------------------------------
new_df = new_df.groupby("Timestamp").filter(lambda g: len(g) >= 5)

if len(new_df) == 0:
    print("⚠ All new timestamps had <5 samples. No valid runs.")
    exit()

print(f"✔ Valid new samples after filtering short runs: {len(new_df)}")

# -----------------------------------------------------
# 6. GROUP INTO RUNS
# -----------------------------------------------------
run_stats = new_df.groupby("Timestamp").agg(
    Rows=("Heart_clean", "count"),
    Avg_HR_clean=("Heart_clean", "mean"),
    Avg_RR_clean=("Resp_clean", "mean"),
    Avg_Range=("Range_clean", "mean"),
    Range_SD=("Range_clean", "std")
).reset_index()

# -----------------------------------------------------
# 7. EXTRA FEATURES (Safe)
# -----------------------------------------------------
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

# Merge all
run_stats = (
    run_stats.merge(extra, on="Timestamp")
             .merge(range_slopes, on="Timestamp")
             .merge(SQI, on="Timestamp")
)

# -----------------------------------------------------
# 8. CLEAN ANY NaNs
# -----------------------------------------------------
fill_zero = ["Range_SD", "HR_SD", "RR_SD", "HR_P2P", "RR_P2P", "Range_Slope", "SQI"]
for c in fill_zero:
    run_stats[c] = run_stats[c].fillna(0.0)

run_stats["Avg_HR_clean"] = run_stats["Avg_HR_clean"].fillna(0.0)
run_stats["Avg_RR_clean"] = run_stats["Avg_RR_clean"].fillna(0.0)
run_stats["Avg_Range"] = run_stats["Avg_Range"].fillna(0.0)

# -----------------------------------------------------
# 9. HR CALIBRATION (OFFSET)
# -----------------------------------------------------
OFFSET = 10.5
run_stats["Final_Accurate_HR"] = run_stats["Avg_HR_clean"] + OFFSET

# -----------------------------------------------------
# 10. ASSIGN RUN NUMBERS
# -----------------------------------------------------
last_run = prev["Run"].max() if len(prev) > 0 else 0

run_stats = run_stats.sort_values("Timestamp").reset_index(drop=True)
run_stats["Run"] = run_stats.index + 1 + last_run

# -----------------------------------------------------
# 11. APPEND TO FINAL_RUN_STATS
# -----------------------------------------------------
write_header = not os.path.exists(FINAL_STATS_FILE)

run_stats.to_csv(
    FINAL_STATS_FILE,
    mode="a",
    index=False,
    header=write_header
)

print("==============================================")
print("✔ FINAL RUN STATS UPDATED SUCCESSFULLY")
print(f"✔ New runs added: {len(run_stats)}")
print(f"✔ Saved to: {FINAL_STATS_FILE}")
print("==============================================")
