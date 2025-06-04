from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from apps.api_server.schemas.email_log import EmailLogOut
from shared.models.email_logs import EmailLog
from apps.api_server.models.smtp_account import SMTPAccount
from apps.api_server.models.user import User
from apps.api_server.dependencies.auth import get_current_user, get_db

router = APIRouter(
    prefix="/email-logs",
    tags=["Email Logs"],
)

@router.get("/", response_model=List[EmailLogOut])
def get_user_email_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    smtp_ids = db.query(SMTPAccount.id)\
        .filter(SMTPAccount.user_id == current_user.id)\
        .all()

    smtp_ids = [smtp_id for (smtp_id,) in smtp_ids]

    logs = db.query(EmailLog)\
        .filter(EmailLog.smtp_account_id.in_(smtp_ids))\
        .order_by(EmailLog.sent_at.desc())\
        .all()

    return logs
