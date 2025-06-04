from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from shared.database.base import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)