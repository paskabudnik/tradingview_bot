# bot.py

from aiogram import Bot
from config import BOT_TOKEN, CHAT_ID

bot = Bot(token=BOT_TOKEN)

async def send_alert(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message)

