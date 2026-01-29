from flask import Flask, request, jsonify
from flask_cors import CORS
from face_utils import *
from attendance import mark_attendance
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMPLOYEE_CSV = os.path.join(BASE_DIR, "employees.csv")
ATTENDANCE_CSV = os.path.join(BASE_DIR, "attendance.csv")


# =========================
# FACE RECOGNITION FUNCTION
# =========================
def recognize_from_browser(image, action):
    frame = base64_to_frame(image)
    emb = get_face_embedding(frame)

    if emb is None:
        return "Face not detected"

    embeddings = load_embeddings()

    for emp_id, saved_emb in embeddings.items():
        similarity = cosine_similarity(emb, saved_emb)

        if similarity > 0.65:
            df = pd.read_csv(EMPLOYEE_CSV)
            row = df[df["employee_id"].astype(str) == emp_id]
            name = row.iloc[0]["name"] if not row.empty else "Unknown"
            return mark_attendance(emp_id, name, action)

    return "Face not recognized"


# =========================
# REGISTER (POST)
# =========================
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    emp_id = str(data["emp_id"])
    name = data["name"]
    image = data["image"]

    frame = base64_to_frame(image)
    emb = get_face_embedding(frame)

    if emb is None:
        return jsonify({"message": "Face not detected"}), 400

    embeddings = load_embeddings()

    if emp_id in embeddings:
        return jsonify({"message": "Employee already registered"}), 400

    # Save face embedding
    embeddings[emp_id] = emb
    save_embedding(emp_id, emb)


    # Save employee details
    if not os.path.exists(EMPLOYEE_CSV):
        df = pd.DataFrame(columns=["employee_id", "name"])
        df.to_csv(EMPLOYEE_CSV, index=False)

    df = pd.read_csv(EMPLOYEE_CSV)
    df = df._append(
        {"employee_id": emp_id, "name": name},
        ignore_index=True
    )
    df.to_csv(EMPLOYEE_CSV, index=False)

    return jsonify({"message": "Registration successful"})


# =========================
# CHECK IN (POST)
# =========================
@app.route("/checkin", methods=["POST"])
def checkin():
    image = request.json["image"]
    msg = recognize_from_browser(image, "in")
    return jsonify({"message": msg})


# =========================
# CHECK OUT (POST)
# =========================
@app.route("/checkout", methods=["POST"])
def checkout():
    image = request.json["image"]
    msg = recognize_from_browser(image, "out")
    return jsonify({"message": msg})


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)
