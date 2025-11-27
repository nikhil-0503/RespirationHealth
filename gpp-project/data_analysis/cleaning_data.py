import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import os

# =======================================================
# PATHS
# =======================================================
RAW_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\backend\vital_signs_data_new.csv"
CLEAN_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\cleaned_vital_signs_new.csv"

print("Loading raw data...")

if not os.path.exists(RAW_FILE):
    print("❌ Raw input file not found.")
    exit()

raw_df = pd.read_csv(RAW_FILE)

# Rename Configuration → ConfigurationFile
if "Configuration" in raw_df.columns:
    raw_df = raw_df.rename(columns={"Configuration": "ConfigurationFile"})

required_cols = [
    "Timestamp", "User", "SessionTime",
    "HeartRate_BPM", "RespirationRate_BPM", "Range_m",
    "HeartWaveform", "BreathWaveform",
    "HeartRate_FFT", "BreathRate_FFT",
    "ConfigurationFile"
]

for col in required_cols:
    if col not in raw_df.columns:
        print(f"❌ Missing column: {col}")
        exit()

raw_df["Timestamp"] = raw_df["Timestamp"].astype(str).str.strip()

# =======================================================
# SORT — very important for calibration run detection
# =======================================================
raw_df = raw_df.sort_values(by=["Timestamp", "SessionTime"]).reset_index(drop=True)

# =======================================================
# TYPE CAST
# =======================================================
num_cols = ["HeartRate_BPM", "RespirationRate_BPM", "Range_m"]
for col in num_cols:
    raw_df[col] = pd.to_numeric(raw_df[col], errors="coerce")

# =======================================================
# REMOVE IMPOSSIBLE SAMPLE OUTLIERS
# =======================================================
clean = raw_df[
    raw_df["HeartRate_BPM"].between(40,180) &
    raw_df["RespirationRate_BPM"].between(5,40) &
    raw_df["Range_m"].between(0.1,2.0)
].reset_index(drop=True)

if clean.empty:
    print("⚠ All samples filtered as impossible.")
    exit()

# =======================================================
# DETECT STUCK HR SAMPLES (NOT RUNS)
# =======================================================
# We detect stuck HR *locally*, NOT by timestamp group

def mark_stuck(hr):
    return hr.mode().iloc[0] if len(hr.mode()) > 0 else None

mode_hr = clean["HeartRate_BPM"].mode()
if len(mode_hr) > 0:
    most_common = mode_hr.iloc[0]
    # If the heart rate repeats too many times → stuck sensor
    stuck_mask = clean["HeartRate_BPM"].value_counts().max() > 0.6 * len(clean)
    if stuck_mask and most_common > 110:
        print("⚠ Detected stuck HR values. Removing them…")
        clean = clean[clean["HeartRate_BPM"] != most_common]

if clean.empty:
    print("⚠ All stuck HR removed, no data left.")
    exit()

# =======================================================
# MEDIAN + LOW PASS FILTER
# =======================================================
def lowpass(arr, cutoff=0.3, fs=10):
    arr = arr.ffill().bfill()
    if len(arr) < 12:
        return arr.rolling(3, min_periods=1, center=True).mean()
    b, a = butter(4, cutoff/(fs/2), btype='low')
    return filtfilt(b, a, arr)

window = min(5, len(clean))
clean["Heart_med"] = clean["HeartRate_BPM"].rolling(window, center=True, min_periods=1).median()
clean["Resp_med"] = clean["RespirationRate_BPM"].rolling(window, center=True, min_periods=1).median()
clean["Range_med"] = clean["Range_m"].rolling(window, center=True, min_periods=1).median()

clean["Heart_clean"] = lowpass(clean["Heart_med"])
clean["Resp_clean"] = lowpass(clean["Resp_med"])
clean["Range_clean"] = lowpass(clean["Range_med"])

# Final sanity limits
clean.loc[~clean["Heart_clean"].between(40,180), "Heart_clean"] = np.nan
clean.loc[~clean["Resp_clean"].between(5,40), "Resp_clean"] = np.nan
clean.loc[~clean["Range_clean"].between(0.1,2.0), "Range_clean"] = np.nan

clean = clean.ffill().bfill()

# =======================================================
# OUTPUT FORMAT — EXACTLY WHAT calibration.py EXPECTS
# =======================================================
final_df = clean[
    [
        "Timestamp","User","SessionTime",
        "HeartRate_BPM","RespirationRate_BPM","Range_m",
        "HeartWaveform","BreathWaveform","HeartRate_FFT","BreathRate_FFT",
        "ConfigurationFile",
        "Heart_clean","Resp_clean","Range_clean"
    ]
]

# =======================================================
# APPEND MODE
# =======================================================
write_header = not os.path.exists(CLEAN_FILE)
final_df.to_csv(CLEAN_FILE, mode="a", index=False, header=write_header)

print(f"✔ Saved {len(final_df)} cleaned rows.")
print("✔ Cleaning completed successfully.")
