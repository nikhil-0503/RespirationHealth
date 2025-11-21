import csv
import firebase_admin
from firebase_admin import credentials, firestore

# ----------------------------
# 1. Initialize Firebase Admin
# ----------------------------
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ----------------------------
# 2. CSV FILE PATH
# ----------------------------
CSV_FILE = "vital_signs_data2.csv"   # <-- change if needed

# ----------------------------
# 3. Upload Function
# ----------------------------
def upload_csv_to_firestore():
    print("\nUploading CSV data to Firestore...\n")

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)

        count = 0
        for row in reader:
            # Convert string fields into correct numeric types
            try:
                doc = {
                    "Timestamp": row["Timestamp"],
                    "User": row["User"],
                    "SessionTime": float(row["SessionTime"]),
                    "HeartRate_BPM": float(row["HeartRate_BPM"]),
                    "RespirationRate_BPM": float(row["RespirationRate_BPM"]),
                    "Range_m": float(row["Range_m"]),
                    "HeartWaveform": float(row["HeartWaveform"]),
                    "BreathWaveform": float(row["BreathWaveform"]),
                    "HeartRate_FFT": float(row["HeartRate_FFT"]),
                    "BreathRate_FFT": float(row["BreathRate_FFT"]),
                    "ConfigurationFile": int(row["ConfigurationFile"])
                }

                db.collection("VitalSignsData").add(doc)
                count += 1

                if count % 50 == 0:
                    print(f"Uploaded {count} records...")

            except Exception as e:
                print("ERROR uploading row:", row)
                print("Reason:", e)

        print(f"\n✔ Upload completed. Total rows uploaded: {count}")

# ----------------------------
# Run the upload
# ----------------------------
if __name__ == "__main__":
    upload_csv_to_firestore()
