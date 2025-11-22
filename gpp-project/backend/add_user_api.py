from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.csv")

# Create file if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "password"])


@app.route("/add-user", methods=["POST"])
def add_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Check duplicates
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row[0] == email:
                return jsonify({"success": False, "message": "Email already exists."})

    # Append
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([email, password])

    return jsonify({"success": True})


@app.route("/get-users", methods=["GET"])
def get_users():
    with open(CSV_FILE, "r") as f:
        return f.read()


if __name__ == "__main__":
    print("Saving CSV to:", CSV_FILE)
    app.run(port=5003, debug=True)
