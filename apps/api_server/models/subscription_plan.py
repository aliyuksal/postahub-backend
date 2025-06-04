from sqlalchemy import Column, Integer, String, Numeric, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from shared.database.base import Base

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(50), unique=True, nullable=False)
    max_daily_limit = Column(Integer, nullable=False)
    max_days = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔧 Eksik olan ilişki tanımı (User modeliyle bağlantı kurar)
    users = relationship("User", back_populates="subscription_plan")
    warmup_plans = relationship("WarmupStrategy", back_populates="subscription_plan")