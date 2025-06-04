from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from shared.database.base import Base
from typing import TYPE_CHECKING
from apps.warming_engine.models.warmup_strategy import WarmupStrategy



class SMTPAccount(Base):
    __tablename__ = "smtp_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(100), nullable=True)
    email = Column(String(255), nullable=False)
    username = Column(String(255), nullable=True)
    password = Column(String, nullable=True)
    host = Column(String(255), nullable=True)
    port = Column(Integer, nullable=True)
    use_tls = Column(Boolean, default=True)
    use_ssl = Column(Boolean, default=False)
    daily_limit = Column(Integer, default=100)
    status = Column(String(50), default="active")
    reputation_score = Column(Integer, default=100)


    # Kullanıcı ilişkisi
    user = relationship("User", back_populates="smtp_accounts")

    # WarmupStrategy ilişkisi
    warmup_plans = relationship(
        "WarmupStrategy",  # ❗ String olmalı
        back_populates="smtp_account",
        cascade="all, delete"
    )

    email_logs = relationship("EmailLog", back_populates="smtp_account")

