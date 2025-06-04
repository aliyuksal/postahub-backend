from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from datetime import datetime
from shared.database.base import Base

class EngagementLog(Base):
    __tablename__ = "engagement_logs"

    id = Column(Integer, primary_key=True)
    email_log_id = Column(Integer, ForeignKey("email_logs.id"))
    event_type = Column(String(50))  # örn: reply_sent, read, click
    event_time = Column(DateTime, default=datetime.utcnow)
    ai_generated_response = Column(Text, nullable=True)