# ✋ Hand Gesture Volume Controller

Control your system volume using simple hand gestures!  
Built using **Python**, **OpenCV**, and **MediaPipe**, this project tracks your hand via webcam and adjusts volume based on the distance between your thumb and index finger. It supports real-time feedback and works on macOS using AppleScript.

---

## 🎯 Features

- Live hand tracking using MediaPipe  
- Detects distance between thumb and index finger  
- Dynamically scales volume based on finger distance  
- Visual feedback: volume bar and finger highlights  
- macOS system volume control via AppleScript

---

## 🛠️ Tech Stack

- Python  
- OpenCV (`cv2`)  
- MediaPipe  
- NumPy  
- AppleScript (for macOS volume control)

---

## 🖥️ How It Works

1. Track hand landmarks using MediaPipe  
2. Measure distance between thumb tip and index finger tip  
3. Map distance range to volume scale (0% – 100%)  
4. Use AppleScript command to set macOS system volume  
5. Draw volume bar and landmarks on video feed in real time

---
