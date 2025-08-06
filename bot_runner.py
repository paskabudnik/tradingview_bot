import asyncio
from bot import dp, bot  # импортируем и dp, и bot

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

