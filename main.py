from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from bot import send_alert
import uvicorn

from models import Signal
from database import SessionLocal, init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Папка с шаблонами

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

    await send_alert(msg)

    new_signal = Signal(signal_type=payload.get("type", "unknown"), description=msg)
    db.add(new_signal)
    db.commit()
    db.refresh(new_signal)

    return {"ok": True, "signal_id": new_signal.id}

@app.get("/signals")
def read_signals(db: Session = Depends(get_db)):
    return db.query(Signal).all()

# Новый маршрут для админ-панели с указанием response_class
@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, db: Session = Depends(get_db)):
    signals = db.query(Signal).order_by(Signal.created_at.desc()).all()
    return templates.TemplateResponse("admin.html", {"request": request, "signals": signals})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

