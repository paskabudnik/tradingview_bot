from fastapi import FastAPI, Request
import asyncio
from bot import send_alert  # Импорт из bot.py
from pydantic import BaseModel

app = FastAPI()

class SignalData(BaseModel):
    message: str

@app.post("/webhook/tradingview")
async def tradingview_webhook(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        if not message:
            return {"error": "No message"}
        asyncio.create_task(send_alert(message))
        return {"status": "OK"}
    except Exception as e:
        return {"error": str(e)}

