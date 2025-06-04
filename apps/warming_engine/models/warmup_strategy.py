from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from datetime import datetime
from shared.database.base import Base  # veya kullandığın base class
from sqlalchemy.orm import relationship
from sqlalchemy import Time


class WarmupStrategy(Base):
    __tablename__ = "warmup_strategies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    smtp_account_id = Column(Integer, ForeignKey("smtp_accounts.id"))
    subscription_plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=True)

    plan_name = Column(String, nullable=False)
    sender_name = Column(String, nullable=False)
    sender_surname = Column(String, nullable=True)
    email_language = Column(String, default="en")
    sending_frequency = Column(Integer, nullable=False)
    auto_increase_volume_percent = Column(Integer, default=0)
    email_template_type = Column(String, nullable=False)
    esp_type = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_days = Column(Integer, nullable=False)
    active_days = Column(ARRAY(String), nullable=False)  # JSON stringified list gibi tutulabilir
    reply_timing_strategy = Column(String, nullable=False)
    prompt_type = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="warmup_plans")
    smtp_account = relationship("SMTPAccount", back_populates="warmup_plans")
    subscription_plan = relationship("SubscriptionPlan", back_populates="warmup_plans")

# ✅ Sınıf tanımından sonra log
print("✅ WarmupStrategy modeli yüklendi:", WarmupStrategy.__tablename__)

