from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    chat_id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=True)

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    signal_type = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

