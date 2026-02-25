import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import math
import webbrowser
import time
from datetime import datetime

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


# ================== HAND DETECTION FIX (IMPORTANT!) ==================

def get_hands(results, w, h):
    left = None
    right = None

    if results.multi_hand_landmarks:
        for idx, hand in enumerate(results.multi_hand_landmarks):

            handed = results.multi_handedness[idx].classification[0].label  # Left/Right

            # Convert normalized coords to pixel (x,y)
            lm = []
            for p in hand.landmark:
                lm.append((int(p.x * w), int(p.y * h)))

            if handed == "Left":
                left = lm
            else:
                right = lm

    return left, right


def fingers_up(pts):
    if pts is None:
        return [0,0,0,0,0]

    fingers = []

    # Thumb (horizontal)
    fingers.append(1 if pts[4][0] < pts[3][0] else 0)

    # Other 4 fingers (vertical)
    tips = [8,12,16,20]
    pips = [6,10,14,18]

    for t,p in zip(tips,pips):
        fingers.append(1 if pts[t][1] < pts[p][1] else 0)

    return fingers


def distance(a, b):
    return math.dist(a, b)


# ================== CAMERA & GESTURE LOOP ==================

cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()
zoom_prev = None

with mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Hand detection FIXED
        left_hand, right_hand = get_hands(results, w, h)

        # Draw landmarks
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        # ======================================================
        # RIGHT HAND → MOUSE, CLICK, SCROLL, SCREENSHOT
        # ======================================================
        if right_hand:

            fingersR = fingers_up(right_hand)
            idx = right_hand[8]
            thumb = right_hand[4]
            mid = right_hand[12]
            pinky = right_hand[20]

            # Cursor movement
            mouse_x = int((idx[0] / w) * screen_w)
            mouse_y = int((idx[1] / h) * screen_h)
            pyautogui.moveTo(mouse_x, mouse_y, duration=0.05)

            # Left Click
            if distance(idx, thumb) < 40:
                pyautogui.click()
                time.sleep(0.15)

            # Right Click
            if distance(mid, thumb) < 40:
                pyautogui.rightClick()
                time.sleep(0.15)

            # Scroll Up (2 fingers)
            if fingersR == [0,1,1,0,0]:
                pyautogui.scroll(60)

            # Scroll Down (3 fingers)
            if fingersR == [0,1,1,1,0]:
                pyautogui.scroll(-60)

            # Screenshot → Pinky + Thumb pinch
            if distance(pinky, thumb) < 40:
                filename = f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
                pyautogui.screenshot(filename)
                print("[SCREENSHOT]:", filename)
                time.sleep(1)

        # ======================================================
        # LEFT HAND → VOLUME, GOOGLE, YOUTUBE
        # ======================================================
        if left_hand:

            fingersL = fingers_up(left_hand)
            idx = left_hand[8]
            thumb = left_hand[4]
            mid = left_hand[12]
            ring = left_hand[16]

            # Volume Up (index + thumb pinch)
            if distance(idx, thumb) < 40:
                pyautogui.press("volumeup")
                time.sleep(0.2)

            # Volume Down (middle + thumb pinch)
            if distance(mid, thumb) < 40:
                pyautogui.press("volumedown")
                time.sleep(0.2)

            # Google (index + middle + thumb close)
            if distance(idx, thumb) < 40 and distance(idx, mid) < 40:
                webbrowser.open("https://google.com")
                time.sleep(1)

            # YouTube (thumb + ring finger close)
            if distance(ring, thumb) < 40:
                webbrowser.open("https://youtube.com")
                time.sleep(1)

        # ======================================================
        # BOTH HANDS → ZOOM IN / ZOOM OUT
        # ======================================================
        if left_hand and right_hand:

            L = left_hand[8]
            R = right_hand[8]

            d = distance(L, R)

            if zoom_prev is not None:
                if d - zoom_prev > 20:
                    pyautogui.hotkey("ctrl", "+")  # zoom in
                elif zoom_prev - d > 20:
                    pyautogui.hotkey("ctrl", "-")  # zoom out

            zoom_prev = d

        # ======================================================
        # SHOW WINDOW
        # ======================================================

        cv2.imshow("AI Gesture Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()