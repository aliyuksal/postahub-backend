from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from apps.api_server.dependencies.auth import get_db, get_current_user
from apps.api_server.models.smtp_account import SMTPAccount
from shared.models.email_logs import EmailLog
from shared.models.engagement_logs import EngagementLog
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/smtp-summary",
    tags=["SMTP Summary"]
)

class SMTPSummaryOut(BaseModel):
    smtp_id: int
    smtp_email: str
    open_rate: float
    failed_count: int
    total_sent: int

    class Config:
        orm_mode = True

@router.get("/overview", response_model=List[SMTPSummaryOut])
def get_smtp_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    smtp_accounts = db.query(SMTPAccount).filter(SMTPAccount.user_id == current_user.id).all()
    summaries = []

    for smtp in smtp_accounts:
        total_sent = db.query(func.count()).select_from(EmailLog).filter(
            EmailLog.smtp_account_id == smtp.id,
            EmailLog.status == "sent"
        ).scalar()

        open_count = db.query(func.count()).select_from(EngagementLog).join(EmailLog).filter(
            EmailLog.smtp_account_id == smtp.id,
            EngagementLog.event_type == "open"
        ).scalar()

        failed_count = db.query(func.count()).select_from(EmailLog).filter(
            EmailLog.smtp_account_id == smtp.id,
            EmailLog.status.in_(["failed", "bounced"])
        ).scalar()

        open_rate = round((open_count / total_sent) * 100, 2) if total_sent > 0 else 0.0

        summaries.append(SMTPSummaryOut(
            smtp_id=smtp.id,
            smtp_email=smtp.email,
            open_rate=open_rate,
            failed_count=failed_count,
            total_sent=total_sent
        ))

    return summaries