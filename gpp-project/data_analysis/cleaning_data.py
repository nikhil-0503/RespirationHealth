import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
from datetime import datetime

# ----------------------------------------------------
# 1. LOAD DATA FROM CSV
# ----------------------------------------------------
print("Loading data from CSV...")

df = pd.DataFrame(pd.read_csv(r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project\backend\vital_signs_new_data.csv"))
print(f"✔ Loaded {len(df)} raw rows.")

# Ensure numeric
numeric_cols = [
    "SessionTime","HeartRate_BPM","RespirationRate_BPM",
    "Range_m","HeartWaveform","BreathWaveform",
    "HeartRate_FFT","BreathRate_FFT"
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ----------------------------------------------------
# 2. OUTLIER REMOVAL
# ----------------------------------------------------
df = df[
    (df["HeartRate_BPM"].between(40, 180)) &
    (df["RespirationRate_BPM"].between(5, 40)) &
    (df["Range_m"].between(0.2, 2.0))
].reset_index(drop=True)

print(f"✔ Rows after outlier removal: {len(df)}")

# ----------------------------------------------------
# 3. MEDIAN FILTER
# ----------------------------------------------------
window = 5
df["Heart_med"] = df["HeartRate_BPM"].rolling(window, center=True).median().fillna(df["HeartRate_BPM"])
df["Resp_med"]  = df["RespirationRate_BPM"].rolling(window, center=True).median().fillna(df["RespirationRate_BPM"])
df["Range_med"] = df["Range_m"].rolling(window, center=True).median().fillna(df["Range_m"])

# ----------------------------------------------------
# 4. LOW-PASS FILTER
# ----------------------------------------------------
def lowpass(data, cutoff=0.3, fs=10):
    b, a = butter(4, cutoff / (fs / 2), btype='low')
    return filtfilt(b, a, data)

df["Heart_clean"] = lowpass(df["Heart_med"].interpolate())
df["Resp_clean"]  = lowpass(df["Resp_med"].interpolate())
df["Range_clean"] = lowpass(df["Range_med"].interpolate())

print("✔ Applied median + low-pass filtering.")

# ----------------------------------------------------
# 5. SECOND-PASS VALIDATION
# ----------------------------------------------------
df.loc[(df["Heart_clean"] < 40) | (df["Heart_clean"] > 180), "Heart_clean"] = np.nan
df.loc[(df["Resp_clean"] < 5) | (df["Resp_clean"] > 40), "Resp_clean"] = np.nan
df.loc[(df["Range_clean"] < 0.2) | (df["Range_clean"] > 2.0), "Range_clean"] = np.nan

df["Heart_clean"].interpolate(inplace=True)
df["Resp_clean"].interpolate(inplace=True)
df["Range_clean"].interpolate(inplace=True)

print("✔ Applied final smoothing and validation.")

# ----------------------------------------------------
# 6. SAVE CLEANED DATA AS CSV
# ----------------------------------------------------
# Create a clean dataframe for CSV export
csv_df = pd.DataFrame({
    "Timestamp": df["Timestamp"],
    "User": df["User"],
    "SessionTime": df["SessionTime"],
    "HeartRate_raw": df["HeartRate_BPM"],
    "RespirationRate_raw": df["RespirationRate_BPM"],
    "Range_raw": df["Range_m"],
    "HeartWaveform": df["HeartWaveform"],
    "BreathWaveform": df["BreathWaveform"],
    "HeartRate_FFT": df["HeartRate_FFT"],
    "BreathRate_FFT": df["BreathRate_FFT"],
    "ConfigurationFile": df["ConfigurationFile"],
    "Heart_clean": df["Heart_clean"],
    "Resp_clean": df["Resp_clean"],
    "Range_clean": df["Range_clean"],
})

# Generate filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"cleaned_vital_signs_{timestamp}.csv"

csv_df.to_csv(csv_filename, index=False)
print(f"\n✔ Cleaning complete. Saved {len(csv_df)} rows.")
print(f"✔ CSV export saved as: {csv_filename}")