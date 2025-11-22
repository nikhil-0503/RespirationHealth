from flask import Flask, request, jsonify
import pandas as pd
import subprocess
import os
import traceback

app = Flask(__name__)

BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project"

RAW_FILE = os.path.join(BASE_DIR, "backend", "vital_signs_new_data.csv")
CLEAN_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "cleaning_data.py")
CALIB_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "calibration.py")
MODEL_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "predict_with_model.py")


# -----------------------------------------------------------
# 1️⃣ UPLOAD CSV & APPEND TO vital_signs_new_data.csv
# -----------------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload_csv():
    try:
        file = request.files.get("file")
        if file is None:
            return jsonify({"error": "No file uploaded"}), 400

        df = pd.read_csv(file)

        # Append to raw file
        df.to_csv(RAW_FILE, mode="a", header=False, index=False)

        return jsonify({"message": "File received and appended!"})

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()})


# -----------------------------------------------------------
# 2️⃣ RUN CLEANING → CALIBRATION → ML MODEL
# -----------------------------------------------------------
@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    try:
        # Run cleaning_data.py
        subprocess.run(["python", CLEAN_SCRIPT], check=True)

        # Run calibration pipeline (feature extraction)
        subprocess.run(["python", CALIB_SCRIPT], check=True)

        # Run ML inference script
        output = subprocess.check_output(["python", MODEL_SCRIPT], text=True)

        return jsonify({
            "message": "Pipeline completed",
            "model_output": output
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Pipeline error",
            "details": e.output,
            "trace": traceback.format_exc()
        })


# -----------------------------------------------------------
# Simple health check
# -----------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Radar pipeline API running"})


if __name__ == "__main__":
    app.run(port=5002, debug=True)
