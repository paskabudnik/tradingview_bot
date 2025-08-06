import asyncio
from bot import dp, bot  # Импортируй из своего bot.py Dispatcher и Bot

async def main():
    print("Запуск Telegram-бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

