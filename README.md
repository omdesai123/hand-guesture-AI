# hand-guesture-AI
<br> om desai<br>
This project is an AI-based Hand Gesture Recognition system that detects and classifies human hand gestures in real-time using computer vision and deep learning techniques. The system captures hand movements through a webcam and interprets them into meaningful commands or actions.


✋ AI Gesture Controller Web App

A Python-based web application that lets you control your computer using hand gestures detected through your webcam. The project combines computer vision, gesture recognition, and a Flask web dashboard to start/stop the system easily.

🚀 Features

👆 Control mouse cursor with hand movement

🖱️ Left / Right click gestures

📜 Scroll up & down gestures

🔊 Volume control gestures

🌐 Open Google / YouTube with gestures

📸 Take screenshots using gestures

🔍 Zoom in / Zoom out with two hands

🔐 Login system + dashboard control panel

🧠 How It Works

The system has two main parts:

1️⃣ Web Dashboard (Flask)

Login authentication

Start / Stop gesture controller

Status API

2️⃣ Gesture Engine (Computer Vision)

Uses webcam feed

Detects hands via MediaPipe

Maps finger positions to actions

Sends commands to system via PyAutoGUI

📂 Project Structure
project/
│
├── app.py          # Flask web server
├── final.py        # Gesture detection engine
├── templates/      # HTML pages (login, signup, dashboard)
├── users.txt       # Stored user credentials
└── README.md
🛠 Requirements

Install dependencies:

pip install flask opencv-python mediapipe numpy pyautogui

▶️ Run the Project
Step 1 — Start Flask App
python app.py
Step 2 — Open Browser
http://127.0.0.1:5000
Step 3 — Login

Default credentials:

Username: admin
Password: 1234
🎮 Gesture Controls
Gesture	Action
Index finger move	Cursor movement
Thumb + Index pinch	Left click
Thumb + Middle pinch	Right click
2 fingers up	Scroll up
3 fingers up	Scroll down
Pinky + Thumb pinch	Screenshot
Left index + thumb	Volume up
Left middle + thumb	Volume down
Left 3 finger pinch	Open Google
Left ring + thumb	Open YouTube
Both index fingers distance	Zoom in/out

Press Q to exit gesture window.

🔐 Security Note
▶️ Run the Project
Step 1 — Start Flask

