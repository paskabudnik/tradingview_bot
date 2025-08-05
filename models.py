from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Signal(Base):
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    signal_type = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
