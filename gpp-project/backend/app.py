from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)  # IMPORTANT

@app.get("/run-sensor")
def run_sensor():
    try:
        process = subprocess.Popen(
            [sys.executable, "vst.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return jsonify({ "success": False, "error": stderr })

        return jsonify({ "success": True, "output": stdout })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) })

if __name__ == "__main__":
    app.run(host="localhost", port=5001)
