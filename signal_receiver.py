from fastapi import FastAPI, Request
import asyncio
from bot import send_alert  # Импортируй send_alert из bot.py

app = FastAPI()

@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    message = data.get("message", "📢 Новый сигнал от TradingView")
    
    # Запуск отправки уведомлений
    asyncio.create_task(send_alert(message))
    
    return {"status": "ok"}

