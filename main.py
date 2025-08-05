from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from bot import send_alert
import uvicorn

from models import Signal
from database import SessionLocal, init_db

app = FastAPI()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/webhook/tradingview")
async def tradingview_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    msg = "📉 Новый сигнал от TradingView:\n" + "\n".join(f"{k}: {v}" for k, v in payload.items())

    # Отправляем сообщение в Telegram
    await send_alert(msg)

    # Сохраняем сигнал в базу
    new_signal = Signal(signal_type=payload.get("type", "unknown"), description=msg)
    db.add(new_signal)
    db.commit()
    db.refresh(new_signal)

    return {"ok": True, "signal_id": new_signal.id}

@app.get("/signals")
def read_signals(db: Session = Depends(get_db)):
    signals = db.query(Signal).all()
    return signals

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

