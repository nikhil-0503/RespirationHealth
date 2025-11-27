from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import subprocess
import sys
import io
import csv
import os
import traceback
import json

# Fix UTF-8 for printing
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE_DIR = r"C:\Users\Nikhil\Downloads\SSN\College Files\Grand Project\RespirationHealth\gpp-project"

MASTER_FILE = os.path.join(BASE_DIR, "backend", "vital_signs_new_data.csv")
USERS_FILE = os.path.join(BASE_DIR, "backend", "users.csv")

CLEAN_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "cleaning_data.py")
CALIB_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "calibration.py")
MODEL_SCRIPT = os.path.join(BASE_DIR, "data_analysis", "predict_with_model.py")


# ------------------------------------------------------------
# USER CHECK
# ------------------------------------------------------------
def user_exists(email):
    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row and row[0].strip().lower() == email.lower():
                return True
    return False


# ------------------------------------------------------------
# 1️⃣ UPLOAD CSV
# ------------------------------------------------------------
@app.post("/upload")
def upload_csv():
    try:
        file = request.files.get("file")
        if file is None:
            return jsonify({"error": "No file uploaded"}), 400

        df = pd.read_csv(file)
        df.to_csv(MASTER_FILE, mode="a", header=False, index=False)

        return jsonify({"message": "File received and appended!"})

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()})


# ------------------------------------------------------------
# 2️⃣ RUN SENSOR → SAVE DATA → RUN PIPELINE
# ------------------------------------------------------------
@app.post("/run-sensor")
def run_sensor():
    try:
        data = request.get_json()
        user_email = data.get("userEmail")
        config_number = data.get("configuration")

        if not user_email or config_number is None:
            return jsonify({"success": False, "error": "Missing userEmail or configuration"})

        if not user_exists(user_email):
            return jsonify({"success": False, "error": "User does not exist. Please sign up first."})

        VITALSIGNS_SCRIPT = os.path.join(BASE_DIR, "backend", "vitalsigns.py")

        # RUN SENSOR
        process = subprocess.Popen(
            [sys.executable, VITALSIGNS_SCRIPT, user_email, str(config_number)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return jsonify({"success": False, "error": stderr or stdout})

        # Extract stats block
        stats_text = "No stats returned."
        collecting = False
        json_buffer = ""

        for line in stdout.splitlines():
            if "STATS_BEGIN" in line:
                collecting = True
                continue
            if "STATS_END" in line:
                break
            if collecting:
                json_buffer += line

        try:
            stats_text = json.loads(json_buffer).get("stats_text", "No stats found.")
        except:
            pass

        # RUN PIPELINE: CLEAN → CALIBRATE → ML
        subprocess.run([sys.executable, CLEAN_SCRIPT], check=True)
        subprocess.run([sys.executable, CALIB_SCRIPT], check=True)

        raw_output = subprocess.check_output([sys.executable, MODEL_SCRIPT], text=True).strip()

        try:
            ml_results = json.loads(raw_output)
        except:
            ml_results = {"raw_output": raw_output}

        # FINAL OUTPUT (same as upload pipeline)
        return jsonify({
            "success": True,
            "stats_text": stats_text,
            "ml_results": ml_results
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# ------------------------------------------------------------
# 3️⃣ MANUAL PIPELINE RUN (upload flow)
# ------------------------------------------------------------
@app.post("/run_pipeline")
def run_pipeline():
    try:
        subprocess.run(["python", CLEAN_SCRIPT], check=True)
        subprocess.run(["python", CALIB_SCRIPT], check=True)

        raw_output = subprocess.check_output(["python", MODEL_SCRIPT], text=True).strip()

        try:
            ml_output = json.loads(raw_output)
        except:
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


# ------------------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------------------
@app.get("/")
def home():
    return jsonify({"status": "Radar pipeline API running"})


# ------------------------------------------------------------
# START SERVER
# ------------------------------------------------------------
if __name__ == "__main__":
    print("📌 Using master file:", MASTER_FILE)
    print("📌 Users file:", USERS_FILE)
    app.run(port=5002, debug=True, use_reloader=False)
