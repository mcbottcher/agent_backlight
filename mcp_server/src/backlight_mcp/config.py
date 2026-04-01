import os

from dotenv import load_dotenv

load_dotenv()

LED_NAME = os.environ.get("LED_NAME")
if not LED_NAME:
    raise RuntimeError("LED_NAME must be set in .env or environment")

BRIGHTNESS_PATH = f"/sys/class/leds/{LED_NAME}/brightness"
MAX_BRIGHTNESS_PATH = f"/sys/class/leds/{LED_NAME}/max_brightness"
