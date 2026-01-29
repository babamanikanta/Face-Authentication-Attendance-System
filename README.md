Face Authentication Attendance System
Overview

This project is a Face Authentication–based Attendance System developed as part of an AI/ML Internship assignment.
The system uses real-time face recognition to mark employee attendance through face authentication, supporting punch-in and punch-out actions.

The application works with live camera input and can be accessed both through a command-line interface and a browser-based frontend.

Features

Face registration using live camera

Face recognition for authentication

Punch-in and punch-out attendance marking

Real-time camera input

Browser-based camera capture

Basic spoof prevention through live camera capture

Attendance logging in CSV format

Technology Stack
Backend

Python

Flask

OpenCV

DeepFace (FaceNet model)

NumPy

Pandas

Frontend

HTML

CSS

JavaScript

Browser Camera API

Project Structure
Face-Authentication-Attendance-System/
│
├── backend/
│ ├── app.py
│ ├── main.py
│ ├── face_utils.py
│ ├── attendance.py
│ ├── attendance.csv
│ └── embeddings/
│
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
│
└── README.md

How It Works

1. Registration

Admin enters employee ID and name.

Face image is captured using the live camera.

Face embedding is generated using FaceNet.

Embedding is stored locally for future recognition.

Password for that is : admin123

2. Face Recognition

Camera captures live face input.

Face embedding is generated.

Cosine similarity is used to compare with stored embeddings.

Identity is confirmed if similarity exceeds threshold.

3. Attendance Marking

Punch-in records entry time.

Punch-out records exit time.

All records are stored in attendance.csv.

Setup Instructions
Backend Setup

Navigate to backend folder:

cd backend

Create virtual environment:

python -m venv venv

Activate virtual environment:

venv\Scripts\activate

Install dependencies:

pip install flask flask-cors opencv-python deepface tensorflow numpy pandas

Run backend server:

python app.py

Backend will start at:

http://127.0.0.1:5000

Frontend Setup

Open frontend/index.html in browser

Allow camera permissions

Use Register / Check-in / Check-out buttons

API Endpoints
Endpoint Method Description
/register POST Register face and employee
/checkin POST Mark punch-in
/checkout POST Mark punch-out
Model and Approach

FaceNet model is used via DeepFace for face embeddings.

Cosine similarity is used for face matching.

Threshold-based decision for authentication.

Accuracy Expectations

Good accuracy under normal lighting conditions

Reliable for frontal face input

Performance depends on camera quality and lighting

Known Limitations

Performance may drop in poor lighting

Extreme face angles reduce accuracy

No advanced anti-spoofing (basic live camera check only)

Single face detection at a time

Spoof Prevention

Live camera capture required

No image upload from gallery allowed

Prevents static image-based spoofing at basic level

Future Improvements

Liveness detection (blink, head movement)

Database storage instead of CSV

Multiple face detection

Improved spoof prevention

Cloud deployment

Author

Kurmala Chenchu Baba Manikanta
AI/ML Internship Assignment
Lovely Professional University
