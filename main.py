# main.py

from fastapi import FastAPI, Request
import asyncio
from bot import send_alert
import uvicorn

app = FastAPI()

@app.post("/webhook/tradingview")
async def tradingview_webhook(request: Request):
    payload = await request.json()
    # Формируем текст для Telegram
    msg = "📉 Новый сигнал от TradingView:\n"
    msg += "\n".join(f"{k}: {v}" for k, v in payload.items())
    await send_alert(msg)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

