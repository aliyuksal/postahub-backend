from sqlalchemy.orm import Session
from apps.warming_engine.models.warmup_strategy import WarmupStrategy
from apps.api_server.schemas.warmup_strategy import WarmupPlanCreate
from datetime import datetime

def create_warmup_plan(db: Session, plan: WarmupPlanCreate):
    plan_name = f"Warmup Plan - SMTP {plan.smtp_account_id}"

    new_plan = WarmupStrategy(
        user_id=plan.user_id,
        subscription_plan_id=plan.subscription_plan_id,
        smtp_account_id=plan.smtp_account_id,
        plan_name=plan_name,
        sender_name=plan.sender_name,
        sender_surname=plan.sender_surname,
        email_language=plan.email_language,
        sending_frequency=plan.sending_frequency,
        auto_increase_volume_percent=plan.auto_increase_volume_percent,
        email_template_type=plan.email_template_type,
        esp_type=plan.esp_type,
        start_time=plan.start_time,
        end_time=plan.end_time,
        duration_days=plan.duration_days,
        active_days=plan.active_days,
        reply_timing_strategy=plan.reply_timing_strategy,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan