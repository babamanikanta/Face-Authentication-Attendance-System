import cv2
import pandas as pd
from face_utils import *
from attendance import mark_attendance
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTENDANCE_CSV = os.path.join(BASE_DIR, "attendance.csv")


def recognize_face(action):
    embeddings = load_embeddings()
    cam = cv2.VideoCapture(0)

    print("Looking at camera... Press ESC to cancel")

    while True:
        ret, frame = cam.read()
        emb = get_face_embedding(frame)

        if emb is not None:
            for emp_id, saved_emb in embeddings.items():
                sim = cosine_similarity(emb, saved_emb)

                if sim > 0.65:  # slightly stricter
                    df = pd.read_csv(ATTENDANCE_CSV)

                    match = df[df["employee_id"].astype(str) == str(emp_id)]
                    name = match.iloc[0]["name"] if not match.empty else "Unknown"

                    cam.release()
                    cv2.destroyAllWindows()
                    return mark_attendance(emp_id, name, action)

        cv2.imshow("Recognizing", frame)
        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return "Cancelled"
