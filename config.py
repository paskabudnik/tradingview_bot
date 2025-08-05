# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # <--- обязательно до os.getenv

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(f"DEBUG BOT_TOKEN: {BOT_TOKEN}")
print(f"DEBUG CHAT_ID: {CHAT_ID}")

