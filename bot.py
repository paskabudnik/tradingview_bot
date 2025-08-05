# bot.py
import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()  # Загружаем переменные из .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("DEBUG BOT_TOKEN:", BOT_TOKEN)
print("DEBUG CHAT_ID:", CHAT_ID)

if CHAT_ID is not None:
    CHAT_ID = int(CHAT_ID)  # Преобразуем к int

bot = Bot(token=BOT_TOKEN)

async def send_alert(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message)
