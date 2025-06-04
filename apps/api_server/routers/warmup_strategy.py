from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from apps.api_server.schemas.warmup_strategy import WarmupPlanCreate, WarmupPlanOut
from apps.api_server.crud.warmup_strategy import create_warmup_plan
from apps.api_server.models import SMTPAccount, User
from apps.api_server.core.dependencies import get_db
from apps.warming_engine.models.warmup_strategy import WarmupStrategy
from apps.api_server.dependencies.auth import get_current_user
from apps.api_server.schemas.warmup_strategy import WarmupPlanUpdate
from typing import Optional, List

router = APIRouter(prefix="/warmup-strategies", tags=["Warmup Strategies"])

from apps.warming_engine.models.warmup_strategy import WarmupStrategy
from datetime import datetime

@router.post("/", response_model=WarmupPlanOut)
def create_plan(
    plan: WarmupPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ SMTP hesabı kontrolü (kullanıcıya ait mi?)
    smtp_account = db.query(SMTPAccount).filter_by(id=plan.smtp_account_id).first()
    if not smtp_account or smtp_account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="SMTP account not found or not owned by current user")

    # 2️⃣ Plan limit kontrolü
    # Tüm mevcut planların toplam günlük gönderimini al
    existing_plans = db.query(WarmupStrategy).filter_by(smtp_account_id=plan.smtp_account_id).all()
    existing_total = sum(p.sending_frequency for p in existing_plans)

    # Yeni plan ile birlikte SMTP günlük limiti aşılırsa engelle
    if existing_total + plan.sending_frequency > smtp_account.daily_limit:
        raise HTTPException(status_code=400, detail="Planned warm-up volume exceeds SMTP daily limit.")

    # 3️⃣ plan_name boşsa otomatik üret
    plan_name = plan.plan_name or f"{smtp_account.email}_Plan_{datetime.utcnow().strftime('%Y%m%d_%H%M')}"

    # 4️⃣ Plan oluştur
    new_plan = WarmupStrategy(
        **plan.dict(exclude={"plan_name"}),
        plan_name=plan_name,
        user_id=current_user.id,
        subscription_plan_id=current_user.subscription_plan_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()

    )

    # 5️⃣ Veritabanına kaydet
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan



@router.get("/", response_model=list[WarmupPlanOut])
def get_all_warmup_plans(db: Session = Depends(get_db)):
    return db.query(WarmupStrategy).all()

@router.get("/my", response_model=list[WarmupPlanOut])
def list_my_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    smtp_id: Optional[int] = Query(None),
    prompt_type: Optional[str] = Query(None)
):
    query = db.query(WarmupStrategy).filter(WarmupStrategy.user_id == current_user.id)

    if smtp_id:
        query = query.filter(WarmupStrategy.smtp_account_id == smtp_id)
    if prompt_type:
        query = query.filter(WarmupStrategy.prompt_type == prompt_type)

    return query.offset(skip).limit(limit).all()


@router.delete("/{strategy_id}")
def delete_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(WarmupStrategy).filter_by(id=strategy_id).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Strategy not found")

    smtp = db.query(SMTPAccount).filter_by(id=plan.smtp_account_id).first()
    if not smtp or smtp.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this strategy")

    db.delete(plan)
    db.commit()
    return {"message": "Warmup strategy deleted successfully"}


@router.patch("/{strategy_id}", response_model=WarmupPlanOut)
def update_strategy_partial(
    strategy_id: int,
    updates: WarmupPlanUpdate,  # sadece opsiyonel alanlar içerir
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(WarmupStrategy).filter_by(id=strategy_id, user_id=current_user.id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Warmup strategy not found.")

    update_data = updates.dict(exclude_unset=True)

    # Eğer sending_frequency ya da duration_days değiştiyse limit kontrolü yap
    if "sending_frequency" in update_data or "duration_days" in update_data:
        sending_frequency = update_data.get("sending_frequency", strategy.sending_frequency)
        duration_days = update_data.get("duration_days", strategy.duration_days)

        other_plans = db.query(WarmupStrategy).filter(
            WarmupStrategy.smtp_account_id == strategy.smtp_account_id,
            WarmupStrategy.id != strategy.id
        ).all()
        total_other = sum(p.sending_frequency * p.duration_days for p in other_plans)
        new_total = sending_frequency * duration_days
        if total_other + new_total > current_user.subscription_plan.max_daily_limit:
            raise HTTPException(status_code=400, detail="Updated volume exceeds subscription limits.")

    for field, value in update_data.items():
        setattr(strategy, field, value)

    strategy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(strategy)
    return strategy



@router.put("/{strategy_id}", response_model=WarmupPlanOut)
def update_strategy_full(
    strategy_id: int,
    updates: WarmupPlanCreate,  # aynı şema çünkü tüm alanları ister
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(WarmupStrategy).filter_by(id=strategy_id, user_id=current_user.id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Warmup strategy not found.")

    smtp_account = db.query(SMTPAccount).filter_by(id=updates.smtp_account_id).first()
    if not smtp_account or smtp_account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="SMTP account not found or not owned by current user")

    # Plan limit kontrolü
    existing_plans = db.query(WarmupStrategy).filter(
        WarmupStrategy.smtp_account_id == updates.smtp_account_id,
        WarmupStrategy.id != strategy.id
    ).all()
    planned_total = updates.sending_frequency * updates.duration_days
    existing_total = sum(p.sending_frequency * p.duration_days for p in existing_plans)
    if existing_total + planned_total > current_user.subscription_plan.max_daily_limit:
        raise HTTPException(status_code=400, detail="Planned volume exceeds subscription limits.")

    for field, value in updates.dict().items():
        setattr(strategy, field, value)

    strategy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(strategy)
    return strategy