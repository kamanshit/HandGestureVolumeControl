import cv2
import numpy as np
import streamlit as st
import mediapipe as mp
import os

# -------------------- Streamlit UI Setup --------------------
st.title("🖐️ Hand Gesture Volume Controller for macOS")
st.markdown("Control your system volume using finger gestures via webcam!")
FRAME_WINDOW = st.image([])

# Slider for volume range (can be adjusted)
min_vol = st.slider("🔉 Minimum Volume", 0, 100, 0)
max_vol = st.slider("🔊 Maximum Volume", 0, 100, 100)

# -------------------- MediaPipe Initialization --------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# -------------------- Volume Scaling Function --------------------
def set_volume_mac(volume_percent):
    volume_script = f"""
    set volume output volume {volume_percent}
    """
    os.system(f"osascript -e '{volume_script}'")

# -------------------- Start Webcam --------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)

# -------------------- Streamlit Start Button --------------------
start = st.button("▶️ Start Gesture Control")

if start:
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Failed to access webcam.")
            break

        # Flip for mirror view and convert to RGB
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process hands
        result = hands.process(rgb_frame)

        # Default values
        lm_list = []
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((id, cx, cy))

                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

        if lm_list and len(lm_list) >= 9:
            x1, y1 = lm_list[4][1:]   # Thumb tip
            x2, y2 = lm_list[8][1:]   # Index finger tip

            # Draw a line and circles between thumb and index finger
            cv2.circle(frame, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

            length = np.linalg.norm(np.array([x2 - x1, y2 - y1]))

            # Map finger distance to volume
            vol = np.interp(length, [30, 200], [min_vol, max_vol])
            vol = int(np.clip(vol, min_vol, max_vol))

            set_volume_mac(vol)

            # Progress bar visualization
            bar = np.interp(length, [30, 200], [400, 150])
            cv2.rectangle(frame, (50, 150), (85, 400), (255, 255, 255), 3)
            cv2.rectangle(frame, (50, int(bar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(vol)}%', (40, 430), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        FRAME_WINDOW.image(frame, channels='BGR')

    cap.release()
