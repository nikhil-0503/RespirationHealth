import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import os

# ==========================================================
# PATHS
# ==========================================================
RAW_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\backend\vital_signs_new_data.csv"
CLEAN_FILE = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\data_analysis\cleaned_vital_signs_new.csv"

# ==========================================================
# 1. LOAD RAW DATA
# ==========================================================
print("Loading raw data...")

if not os.path.exists(RAW_FILE):
    print("❌ Raw input file not found.")
    exit()

raw_df = pd.read_csv(RAW_FILE)

required_cols = [
    "Timestamp", "User", "SessionTime",
    "HeartRate_BPM", "RespirationRate_BPM", "Range_m",
    "HeartWaveform", "BreathWaveform",
    "HeartRate_FFT", "BreathRate_FFT",
    "ConfigurationFile"
]

for col in required_cols:
    if col not in raw_df.columns:
        print(f"❌ Missing column in raw data: {col}")
        exit()

raw_df["Timestamp"] = raw_df["Timestamp"].astype(str)

# ==========================================================
# 2. LOAD EXISTING CLEANED DATA
# ==========================================================
if os.path.exists(CLEAN_FILE):
    cleaned_df = pd.read_csv(CLEAN_FILE, on_bad_lines="skip")
    cleaned_df["Timestamp"] = cleaned_df["Timestamp"].astype(str)
    existing_timestamps = set(cleaned_df["Timestamp"])
else:
    cleaned_df = pd.DataFrame()
    existing_timestamps = set()
    print("ℹ No cleaned file exists — starting fresh.")

# ==========================================================
# 3. PICK ONLY NEW ROWS
# ==========================================================
new_df = raw_df[~raw_df["Timestamp"].isin(existing_timestamps)].copy()

if len(new_df) == 0:
    print("✔ No new rows to clean. Exiting.")
    exit()

print(f"✔ New rows detected: {len(new_df)}")

# ==========================================================
# 4. TYPE CAST
# ==========================================================
num_cols = ["HeartRate_BPM","RespirationRate_BPM","Range_m"]
for col in num_cols:
    new_df[col] = pd.to_numeric(new_df[col], errors="coerce")

# ==========================================================
# 5. OUTLIER REMOVAL
# ==========================================================
filtered = new_df[
    new_df["HeartRate_BPM"].between(40,180) &
    new_df["RespirationRate_BPM"].between(5,40) &
    new_df["Range_m"].between(0.2,2.0)
].reset_index(drop=True)

if len(filtered) == 0:
    print("⚠ No valid rows after filtering.")
    exit()

# ==========================================================
# 6. FILTERING (median + low pass)
# ==========================================================
def lowpass(arr, cutoff=0.3, fs=10):
    arr = arr.ffill().bfill()
    if len(arr) < 12:
        return arr.rolling(3, min_periods=1, center=True).mean()
    b, a = butter(4, cutoff / (fs/2), btype='low')
    return filtfilt(b, a, arr)

window = min(5, len(filtered))
filtered["Heart_med"] = filtered["HeartRate_BPM"].rolling(window, center=True, min_periods=1).median()
filtered["Resp_med"]  = filtered["RespirationRate_BPM"].rolling(window, center=True, min_periods=1).median()
filtered["Range_med"] = filtered["Range_m"].rolling(window, center=True, min_periods=1).median()

filtered["Heart_clean"] = lowpass(filtered["Heart_med"])
filtered["Resp_clean"]  = lowpass(filtered["Resp_med"])
filtered["Range_clean"] = lowpass(filtered["Range_med"])

# ==========================================================
# 7. FINAL VALIDATION
# ==========================================================
filtered.loc[~filtered["Heart_clean"].between(40,180), "Heart_clean"] = np.nan
filtered.loc[~filtered["Resp_clean"].between(5,40), "Resp_clean"] = np.nan
filtered.loc[~filtered["Range_clean"].between(0.2,2.0), "Range_clean"] = np.nan

filtered = filtered.ffill().bfill()

# ==========================================================
# 8. SELECT EXACT 14 COLUMNS (YOUR FORMAT)
# ==========================================================
final_df = filtered[
    [
        "Timestamp","User","SessionTime",
        "HeartRate_BPM","RespirationRate_BPM","Range_m",
        "HeartWaveform","BreathWaveform","HeartRate_FFT","BreathRate_FFT",
        "ConfigurationFile",
        "Heart_clean","Resp_clean","Range_clean"
    ]
]

# ==========================================================
# 9. APPEND CLEANED ROWS
# ==========================================================
write_header = not os.path.exists(CLEAN_FILE)

final_df.to_csv(CLEAN_FILE, mode="a", index=False, header=write_header)

print(f"✔ Appended {len(final_df)} new cleaned rows.")
print("✔ Cleaning completed successfully.")
