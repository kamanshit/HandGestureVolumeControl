import subprocess
import time

def set_volume_mac(volume_percent):
    volume_level = int(volume_percent * 10)  # macOS scale: 0–10
    print(f"Setting volume to: {volume_level}/10")
    subprocess.call(["osascript", "-e", f"set volume output volume {volume_level}"])

# Try different levels
for vol in [0.0, 0.2, 0.5, 0.8, 1.0]:
    set_volume_mac(vol)
    time.sleep(2)
