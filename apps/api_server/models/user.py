from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from apps.api_server.models.subscription_plan import SubscriptionPlan
from apps.warming_engine.models.warmup_strategy import WarmupStrategy
from shared.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    role = Column(String(50), default="user")
    created_at = Column(TIMESTAMP, nullable=True)

    subscription_plan_id = Column(Integer, ForeignKey("subscription_plans.id"))
    subscription_plan = relationship("SubscriptionPlan", back_populates="users")

    smtp_accounts = relationship("SMTPAccount", back_populates="user")
    warmup_plans = relationship("WarmupStrategy", back_populates="user")