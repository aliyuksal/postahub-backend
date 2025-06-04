from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from shared.database.base import Base


class AIPrompt(Base):
    __tablename__ = "ai_prompts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String)
    template = Column(Text)
    category = Column(String)  # örn: promosyon, hediye teklifi, bilgilendirme
    language = Column(String)
    tone = Column(String)
    prompt_type = Column(String, nullable=True)  # örn: 'marketing', 'followup'
    created_at = Column(DateTime, server_default=func.now())

    # İlişkiyi burada tanımlıyoruz (tek sefer yeterli)
    email_logs = relationship("EmailLog", back_populates="prompt")

