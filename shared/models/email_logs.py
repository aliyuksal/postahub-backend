from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from shared.database.base import Base


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True)
    smtp_account_id = Column(Integer, ForeignKey("smtp_accounts.id"), nullable=False)
    prompt_id = Column(Integer, ForeignKey("ai_prompts.id"), nullable=True)
    target_id = Column(Integer, ForeignKey("warmup_targets.id"), nullable=True)

    recipient_email = Column(String, nullable=False)
    subject = Column(Text)
    body = Column(Text)
    tracking_code = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    message_id = Column(String)
    status = Column(String)
    error_message = Column(Text)
    sent_at = Column(DateTime, server_default=func.now())

    # İlişkiler
    smtp_account = relationship("SMTPAccount", back_populates="email_logs")
    prompt = relationship("AIPrompt", back_populates="email_logs")
    target = relationship("WarmupTarget", back_populates="email_logs")