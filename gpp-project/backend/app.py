from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import io

import firebase_admin
from firebase_admin import credentials, firestore

# -----------------------------
# Initialize Firebase Admin SDK
# -----------------------------
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Ensure proper UTF-8 output handling
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)   # Allow React frontend to communicate with Flask


# ================================
# POST /run-sensor endpoint
# ================================
@app.post("/run-sensor")
def run_sensor():

    try:
        # Read JSON body from React
        data = request.get_json()

        user_email = data.get("userEmail")
        config_number = data.get("configuration")

        if not user_email or config_number is None:
            return jsonify({
                "success": False,
                "error": "Missing userEmail or configuration in request."
            })

        print("\n--- Received Request from React ---")
        print("User Email:", user_email)
        print("Configuration File:", config_number)
        print("-----------------------------------\n")

        # Run vst.py and pass arguments
        process = subprocess.Popen(
            [sys.executable, "vst.py", user_email, str(config_number)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        # On error
        if process.returncode != 0:
            print("Error running vst.py:", stderr)
            return jsonify({
                "success": False,
                "error": stderr
            })

        # On success
        return jsonify({
            "success": True,
            "output": stdout
        })

    except Exception as e:
        print("Backend Error:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        })


# -----------------------------
# Start Flask Server
# -----------------------------
if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
