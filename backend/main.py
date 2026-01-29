import os
import cv2
import pandas as pd
from face_utils import *
from attendance import mark_attendance

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTENDANCE_CSV = os.path.join(BASE_DIR, "attendance.csv")

ADMIN_PASSWORD = "admin123"


def ensure_csv():
    if not os.path.exists(ATTENDANCE_CSV):
        df = pd.DataFrame(columns=["employee_id", "name", "date", "time", "action"])
        df.to_csv(ATTENDANCE_CSV, index=False)


def register():
    emp_id = input("Employee ID: ").strip()
    name = input("Name: ").strip()

    if os.path.exists(f"embeddings/{emp_id}.npy"):
        print("Already Registered")
        return

    pwd = input("Admin Password: ")
    if pwd != ADMIN_PASSWORD:
        print("Unauthorized")
        return

    cam = cv2.VideoCapture(0)
    print("Press SPACE to capture face")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Register", frame)

        if cv2.waitKey(1) == 32:
            emb = get_face_embedding(frame)
            if emb is not None:
                save_embedding(emp_id, emb)
                print("Registration Successful")
                break
            else:
                print("Face not detected, try again")

    cam.release()
    cv2.destroyAllWindows()


def recognize(action):
    ensure_csv()
    embeddings = load_embeddings()
    cam = cv2.VideoCapture(0)

    prev_emb = None
    motion_frames = 0

    print("Looking at camera... Press ESC to cancel")

    while True:
        ret, frame = cam.read()
        emb = get_face_embedding(frame)

        if emb is not None:
            if prev_emb is not None:
                diff = cosine_similarity(emb, prev_emb)
                if diff < 0.98:
                    motion_frames += 1
            prev_emb = emb

            if motion_frames < 3:
                cv2.putText(frame, "Move head slightly",
                            (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (0, 0, 255), 2)
                cv2.imshow("Recognizing", frame)
                continue

            for emp_id, saved_emb in embeddings.items():
                sim = cosine_similarity(emb, saved_emb)

                if sim > 0.6:
                    df = pd.read_csv(ATTENDANCE_CSV)
                    match = df[df["employee_id"].astype(str) == str(emp_id)]

                    name = match.iloc[0]["name"] if not match.empty else "Unknown"
                    msg = mark_attendance(emp_id, name, action)

                    print(msg)
                    print(f"Matched {emp_id} | Similarity: {sim:.2f}")

                    cam.release()
                    cv2.destroyAllWindows()
                    return

        cv2.imshow("Recognizing", frame)
        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


while True:
    print("\n1.Register\n2.Check In\n3.Check Out\n4.Exit")
    ch = input("Choose: ").strip()

    if ch == "1":
        register()
    elif ch == "2":
        recognize("in")
    elif ch == "3":
        recognize("out")
    elif ch == "4":
        break
