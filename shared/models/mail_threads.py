from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from shared.database.base import Base

class MailThread(Base):
    __tablename__ = "mail_threads"

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)