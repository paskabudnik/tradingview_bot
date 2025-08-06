import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

from database import SessionLocal
from models import User

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Кнопки
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start")],
        [KeyboardButton(text="FAQ")]
    ],
    resize_keyboard=True
)

# /start
@dp.message(Command("start"))
async def handle_command_start(message: Message):
    db = SessionLocal()
    chat_id = str(message.chat.id)
    first_name = message.from_user.first_name
    username = message.from_user.username
    try:
        user = db.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            new_user = User(chat_id=chat_id, first_name=first_name, username=username)
            db.add(new_user)
            db.commit()
            await message.answer("✅ Вы подписаны на сигналы.", reply_markup=keyboard)
        else:
            await message.answer("Вы уже подписаны.", reply_markup=keyboard)
    finally:
        db.close()

# FAQ
@dp.message(F.text.lower() == "faq")
async def faq_handler(message: Message):
    await message.answer(
        "❓ FAQ:\n1. Нажмите Start чтобы подписаться.\n2. Сигналы будут приходить автоматически.",
        reply_markup=keyboard
    )
# Команда /testalert для теста рассылки
@dp.message(Command("testalert"))
async def test_alert_handler(message: Message):
    await send_alert("⚠️ Это тестовое сообщение рассылки всем подписчикам!")
    await message.answer("Рассылка отправлена.")
# Рассылка
async def send_alert(message: str):
    db = SessionLocal()
    users = db.query(User).all()
    for user in users:
        try:
            await bot.send_message(chat_id=int(user.chat_id), text=message)
        except Exception as e:
            print(f"❌ Не удалось отправить сообщение {user.chat_id}: {e}")
    db.close()

# Запуск бота
async def main():
    await dp.start_polling(bot)



