# capture.py
import mss
from PIL import Image
from datetime import datetime
import os


def take_screenshot(filename):
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Full primary screen
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # Save screenshot to 'screenshots/' directory
        os.makedirs("screenshots", exist_ok=True)
        filepath = os.path.join("screenshots", filename)
        img.save(filepath)
        return filepath
