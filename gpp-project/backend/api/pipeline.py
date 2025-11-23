from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import subprocess
import os
import traceback
import json

app = Flask(__name__)
CORS(app)

BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project"

RAW_FILE = os.path.join(BASE_DIR, "backend", "vital_signs_new_data.csv")
CLEAN_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "cleaning_data.py")
CALIB_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "calibration.py")
MODEL_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "predict_with_model.py")


# ------------------------------------------------------------------
# 1️⃣ UPLOAD CSV
# ------------------------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload_csv():
    try:
        file = request.files.get("file")
        if file is None:
            return jsonify({"error": "No file uploaded"}), 400

        df = pd.read_csv(file)
        df.to_csv(RAW_FILE, mode="a", header=False, index=False)

        return jsonify({"message": "File received and appended!"})

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()})


# ------------------------------------------------------------------
# 2️⃣ RUN FULL PIPELINE (clean → calibrate → model)
# ------------------------------------------------------------------
@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    try:
        # Step 1: Cleaning
        subprocess.run(["python", CLEAN_SCRIPT], check=True)

        # Step 2: Calibration & feature extraction
        subprocess.run(["python", CALIB_SCRIPT], check=True)

        # Step 3: ML model inference (returns Python dict printed as text)
        raw_output = subprocess.check_output(["python", MODEL_SCRIPT], text=True).strip()

        # Clean and parse safely
        ml_output = None

        # Try parsing clean JSON (if printed already in JSON form)
        try:
            ml_output = json.loads(raw_output)
        except:
            pass

        # Try parsing Python dict style
        if ml_output is None:
            try:
                safe = raw_output.replace("'", '"')
                ml_output = json.loads(safe)
            except:
                pass

        # Final fallback → send raw output
        if ml_output is None:
            ml_output = {"raw_output": raw_output}

        return jsonify({
            "message": "Pipeline completed",
            "ml_results": ml_output
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Pipeline error",
            "details": e.output,
            "trace": traceback.format_exc()
        })


# ------------------------------------------------------------------
# 3️⃣ HEALTH CHECK
# ------------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Radar pipeline API running"})


# ------------------------------------------------------------------
# START SERVER
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=5002, debug=True, use_reloader=False)
