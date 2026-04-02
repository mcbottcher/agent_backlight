import os
import sys

from dotenv import load_dotenv

load_dotenv()

SERVER_PYTHON = sys.executable
SERVER_MODULE = os.environ.get("SERVER_MODULE", "backlight_mcp")
