import cv2
import numpy as np
from deepface import DeepFace
import base64
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "embeddings")

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)


def base64_to_frame(base64_image):
    encoded_data = base64_image.split(",")[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return frame


def get_face_embedding(frame):
    try:
        result = DeepFace.represent(
            frame,
            model_name="Facenet",
            enforce_detection=False
        )
        return np.array(result[0]["embedding"])
    except:
        return None


def save_embedding(emp_id, embedding):
    path = os.path.join(EMBEDDINGS_DIR, f"{emp_id}.npy")
    np.save(path, embedding)


def load_embeddings():
    data = {}
    for file in os.listdir(EMBEDDINGS_DIR):
        if file.endswith(".npy"):
            emp_id = file.replace(".npy", "")
            data[emp_id] = np.load(os.path.join(EMBEDDINGS_DIR, file))
    return data


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
