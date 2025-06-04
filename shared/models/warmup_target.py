from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from shared.database.base import Base

class WarmupTarget(Base):
    __tablename__ = "warmup_targets"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    provider = Column(String)
    status = Column(String, default="active")
    reply_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    name = Column(String, nullable=False)  #eklendi
    surname = Column(String, nullable=False) #eklendi
    email_logs = relationship("EmailLog", back_populates="target")



email_logs = relationship("EmailLog", back_populates="target")