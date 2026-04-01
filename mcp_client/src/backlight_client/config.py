import os

from dotenv import load_dotenv

load_dotenv()

SERVER_PYTHON = os.environ.get("SERVER_PYTHON", "python")
SERVER_MODULE = os.environ.get("SERVER_MODULE", "backlight_mcp")
