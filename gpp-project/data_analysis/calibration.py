import pandas as pd
import numpy as np
import os
import json

# ==========================================================
# PATHS
# ==========================================================
CLEAN_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\cleaned_vital_signs_new.csv"
COMPARISON_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\VariousData.csv"
OFFSET_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\calibration_offsets.json"
FINAL_STATS_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\final_run_stats_new.csv"

os.makedirs(os.path.dirname(FINAL_STATS_FILE), exist_ok=True)

# ==========================================================
# 1. LOAD CLEANED SENSOR DATA
# ==========================================================
if not os.path.exists(CLEAN_FILE):
    print("❌ cleaned_vital_signs_new.csv not found.")
    exit()

df = pd.read_csv(CLEAN_FILE)
df["Timestamp"] = df["Timestamp"].astype(str).str.strip()

# Sort to maintain true order
df = df.sort_values(by=["Timestamp", "SessionTime"]).reset_index(drop=True)

# Remove invalid timestamps
INVALID_TS = ["", "nan", "None", "NaT", "null", "[]"]
df = df[~df["Timestamp"].isin(INVALID_TS)]

if df.empty:
    print("❌ No usable cleaned rows.")
    exit()

# ==========================================================
# 2. LEARN OR LOAD CONFIG-BASED HR OFFSETS
# ==========================================================
def learn_offsets():
    print("📘 Learning HR offsets by configuration...")

    comp = pd.read_csv(COMPARISON_FILE)

    comp = comp.rename(columns={
        "Average Heart Rate": "Sensor_HR",
        "Unnamed: 2": "Smartwatch_HR",
        "Unnamed: 3": "Finger_HR",
        "Configuration": "Config",
        "ConfigurationFile": "Config"   # support both column names
    })

    # Force numeric conversion
    numeric_cols = ["Sensor_HR", "Smartwatch_HR", "Finger_HR", "Config"]
    for col in numeric_cols:
        comp[col] = pd.to_numeric(comp[col], errors="coerce")

    # Drop invalid rows
    comp = comp.dropna(subset=["Sensor_HR", "Smartwatch_HR", "Finger_HR", "Config"])

    if comp.empty:
        print("❌ No valid calibration rows! Using default offsets.")
        return {"offset_0": 10.5, "offset_1": 10.5}

    # Compute real HR
    comp["Real_HR"] = (comp["Smartwatch_HR"] + comp["Finger_HR"]) / 2
    comp["Offset"] = comp["Real_HR"] - comp["Sensor_HR"]

    # Two configurations
    offset_0 = comp[comp["Config"] == 0]["Offset"].mean()
    offset_1 = comp[comp["Config"] == 1]["Offset"].mean()

    offsets = {
        "offset_0": float(offset_0) if not np.isnan(offset_0) else 10.5,
        "offset_1": float(offset_1) if not np.isnan(offset_1) else 10.5
    }

    with open(OFFSET_FILE, "w") as f:
        json.dump(offsets, f, indent=2)

    print("✔ Saved calibration:", offsets)
    return offsets
# ==========================================================
# 2B. LOAD OR LEARN OFFSETS
# ==========================================================
if os.path.exists(OFFSET_FILE):
    offsets = json.load(open(OFFSET_FILE))
    print("✔ Loaded calibration offsets:", offsets)

elif os.path.exists(COMPARISON_FILE):
    offsets = learn_offsets()

else:
    print("⚠ No calibration available. Using default 10.5 for both configs.")
    offsets = {"offset_0": 10.5, "offset_1": 10.5}

# ==========================================================
# 3. LOAD EXISTING final_run_stats_new TO CONTINUE RUN NUMBERS
# ==========================================================
if os.path.exists(FINAL_STATS_FILE):
    prev = pd.read_csv(FINAL_STATS_FILE)
    last_run = int(prev["Run"].max()) if "Run" in prev.columns else 0
else:
    prev = pd.DataFrame()
    last_run = 0
    print("ℹ Starting fresh final_run_stats_new.csv")

# ==========================================================
# 4. DETECT RUNS USING SessionTime RESET
# ==========================================================
df["Run"] = 0
run_num = last_run + 1

df.loc[0, "Run"] = run_num

for i in range(1, len(df)):
    if df.loc[i, "SessionTime"] < df.loc[i - 1, "SessionTime"]:
        run_num += 1
    df.loc[i, "Run"] = run_num

# ==========================================================
# 5. FILTER RUNS WITH < 5 SAMPLES
# ==========================================================
valid_runs = [(rn, g) for rn, g in df.groupby("Run") if len(g) >= 5]

if not valid_runs:
    print("⚠ All runs too short.")
    exit()

# ==========================================================
# 6. COMPUTE RUN-LEVEL STATISTICS
# ==========================================================
final_rows = []

for rn, g in valid_runs:

    timestamp = g["Timestamp"].iloc[0]

    avg_hr = g["Heart_clean"].mean()
    avg_rr = g["Resp_clean"].mean()
    avg_range = g["Range_clean"].mean()

    range_sd = g["Range_clean"].std()
    hr_sd = g["Heart_clean"].std()
    rr_sd = g["Resp_clean"].std()

    hr_p2p = g["Heart_clean"].max() - g["Heart_clean"].min()
    rr_p2p = g["Resp_clean"].max() - g["Resp_clean"].min()

    arr = g["Range_clean"].dropna().values
    t = np.arange(len(arr))
    range_slope = float(np.polyfit(t, arr, 1)[0]) if len(arr) > 1 else 0.0

    sqi = 0 if range_sd in [0, np.nan] else float(1 / range_sd)

    # 🔥 Apply configuration-specific offset
    config = int(g["ConfigurationFile"].iloc[0])
    OFFSET = offsets["offset_0"] if config == 0 else offsets["offset_1"]

    final_hr = avg_hr + OFFSET

    # CLASSIFICATIONS
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

    def classify_stress(hsd):
        if hsd < 0.05: return "Relaxed"
        elif hsd < 0.15: return "Mild Stress"
        elif hsd < 0.25: return "High Stress"
        else: return "Very High Stress"

    final_rows.append([
        timestamp, rn, len(g),
        avg_hr, avg_rr, avg_range,
        range_sd, hr_sd, rr_sd,
        hr_p2p, rr_p2p,
        range_slope, sqi,
        final_hr,
        classify_hr(final_hr),
        classify_rr(avg_rr),
        classify_stress(hr_sd)
    ])

# ==========================================================
# 7. SAVE OUTPUT
# ==========================================================
cols = [
    "Timestamp", "Run", "Rows",
    "Avg_HR_clean", "Avg_RR_clean", "Avg_Range",
    "Range_SD", "HR_SD", "RR_SD",
    "HR_P2P", "RR_P2P",
    "Range_Slope", "SQI",
    "Final_Accurate_HR",
    "HR_Class", "RR_Class", "Stress_Class"
]

final_df = pd.DataFrame(final_rows, columns=cols)
write_header = not os.path.exists(FINAL_STATS_FILE)
final_df.to_csv(FINAL_STATS_FILE, mode="a", index=False, header=write_header)

print("===============================================")
print("✔ NEW FINAL RUN STATS GENERATED")
print(f"✔ Runs added: {len(final_df)}")
print(f"✔ Saved → {FINAL_STATS_FILE}")
print("===============================================")
