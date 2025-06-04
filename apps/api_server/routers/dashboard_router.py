from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from apps.api_server.dependencies.auth import get_current_user, get_db
from apps.api_server.models.user import User
from apps.api_server.models.smtp_account import SMTPAccount
from shared.models.email_logs import EmailLog
from shared.models.engagement_logs import EngagementLog

router = APIRouter(prefix="/dashboard/summary", tags=["Dashboard Summary"])

# 🟩 1. Toplam Gönderilen Mail Sayısı
@router.get("/total-sent")
def get_total_sent(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = db.query(func.count()).select_from(EmailLog).join(SMTPAccount).filter(
        SMTPAccount.user_id == current_user.id,
        EmailLog.status == "sent"
    ).scalar()
    return {"value": count}


# 🟩 2. Toplam Açılan Mail Sayısı
@router.get("/opened-count")
def get_opened_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = db.query(func.count(EngagementLog.id))\
        .join(EmailLog, EngagementLog.email_log_id == EmailLog.id)\
        .join(SMTPAccount, EmailLog.smtp_account_id == SMTPAccount.id)\
        .filter(
            SMTPAccount.user_id == current_user.id,
            EngagementLog.event_type.in_(["opened", "reply_sent"])
        )\
        .scalar()

    return {"value": count}


# 🟩 3. Açılma Oranı (%)
@router.get("/open-rate")
def get_open_rate(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sent = db.query(func.count(EmailLog.id))\
        .join(SMTPAccount, EmailLog.smtp_account_id == SMTPAccount.id)\
        .filter(
            SMTPAccount.user_id == current_user.id,
            EmailLog.status == "sent"
        ).scalar()

    opened = db.query(func.count(EngagementLog.id))\
        .join(EmailLog, EngagementLog.email_log_id == EmailLog.id)\
        .join(SMTPAccount, EmailLog.smtp_account_id == SMTPAccount.id)\
        .filter(
            SMTPAccount.user_id == current_user.id,
            EngagementLog.event_type.in_(["opened", "reply_sent"])
        ).scalar()

    rate = (opened / sent * 100) if sent else 0
    return {"value": round(rate, 2)}


from sqlalchemy import cast, Date

@router.get("/activity/daily")
def get_daily_email_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        cast(EmailLog.sent_at, Date).label("date"),
        func.count(EmailLog.id).label("sent_count")
    )\
    .join(SMTPAccount, EmailLog.smtp_account_id == SMTPAccount.id)\
    .filter(SMTPAccount.user_id == current_user.id)\
    .group_by(cast(EmailLog.sent_at, Date))\
    .order_by(cast(EmailLog.sent_at, Date))\
    .all()

    return [{"date": str(row.date), "count": row.sent_count} for row in results]