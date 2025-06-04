from fastapi import APIRouter, Depends, HTTPException, Response, Path
from sqlalchemy.orm import Session
from apps.api_server.core.database import get_db
from apps.api_server.models.smtp_account import SMTPAccount
from apps.api_server.schemas.smtp_account import SMTPAccountCreate, SMTPAccountOut
from apps.api_server.dependencies.auth import get_current_user
from apps.api_server.models.user import User
import smtplib
from email.mime.text import MIMEText
from apps.api_server.schemas.smtp_account import SMTPAccountUpdate
from typing import Any, List

router = APIRouter(prefix="/smtp", tags=["SMTP"],)

# ✅ SMTP bağlantı testi
def test_smtp_connection(account: SMTPAccountCreate):
    try:
        msg = MIMEText("SMTP warm-up test email.")
        msg["Subject"] = "Warm-up Test"
        msg["From"] = account.email
        msg["To"] = account.email

        if account.use_ssl:
            server = smtplib.SMTP_SSL(account.host, account.port, timeout=10)
        else:
            server = smtplib.SMTP(account.host, account.port, timeout=10)
            if account.use_tls:
                server.starttls()

        server.login(account.username, account.password)
        server.sendmail(account.email, [account.email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SMTP Test Failed: {str(e)}")


# ✅ SMTP ekle
@router.post("/", response_model=SMTPAccountOut)
def create_smtp_account(
    smtp_data: SMTPAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    smtp_account = SMTPAccount(
        **smtp_data.dict(exclude={"status", "reputation_score"}),  # Çıkar
        user_id=current_user.id,
        status="active",
        reputation_score=100
    )

    db.add(smtp_account)
    db.commit()
    db.refresh(smtp_account)
    return smtp_account


# ✅ SMTP listele
@router.get("/my", response_model=list[SMTPAccountOut], tags=["SMTP"])
def get_user_smtp_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    smtp_accounts = db.query(SMTPAccount) \
        .filter(SMTPAccount.user_id == current_user.id) \
        .order_by(SMTPAccount.id.desc()) \
        .all()
    return smtp_accounts


# ✅ SMTP güncelle
@router.patch("/{smtp_id}", response_model=SMTPAccountOut)
def update_smtp_account(
    smtp_id: int,
    updated_data: SMTPAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    smtp_account = db.query(SMTPAccount).filter_by(id=smtp_id, user_id=current_user.id).first()
    if not smtp_account:
        raise HTTPException(status_code=404, detail="SMTP account not found")

    changes = updated_data.dict(exclude_unset=True)

    # Sadece provider değiştiyse connection testi yapma
    if "provider" not in changes or len(changes) > 1:
        temp_data = smtp_account.__dict__.copy()
        temp_data.update(changes)

        try:
            test_smtp_connection(SMTPAccountCreate(**temp_data))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"SMTP connection test failed: {str(e)}")

    for key, value in changes.items():
        setattr(smtp_account, key, value)

    db.commit()
    db.refresh(smtp_account)
    return smtp_account


# ✅ SMTP sil
@router.delete("/{smtp_id}", status_code=204)
def delete_smtp_account(
    smtp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    smtp_account = db.query(SMTPAccount).filter_by(id=smtp_id, user_id=current_user.id).first()
    if not smtp_account:
        raise HTTPException(status_code=404, detail="SMTP account not found")

    db.delete(smtp_account)
    db.commit()
    return Response(status_code=204)


@router.patch("/{smtp_id}/toggle", response_model=SMTPAccountOut)
def toggle_smtp_account(
    smtp_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    smtp_account = db.query(SMTPAccount).filter_by(id=smtp_id, user_id=current_user.id).first()

    if not smtp_account:
        raise HTTPException(status_code=404, detail="SMTP account not found")

    smtp_account.status = "inactive" if smtp_account.status == "active" else "active"
    db.commit()
    db.refresh(smtp_account)
    return smtp_account

@router.post("/{smtp_id}/test")
def test_smtp_connection_by_id(
    smtp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    smtp = db.query(SMTPAccount).filter_by(id=smtp_id, user_id=current_user.id).first()
    if not smtp:
        raise HTTPException(status_code=404, detail="SMTP account not found")

    temp_account = SMTPAccountCreate(
        provider=smtp.provider,
        email=smtp.email,
        username=smtp.username,
        password=smtp.password,
        host=smtp.host,
        port=smtp.port,
        use_tls=smtp.use_tls,
        use_ssl=smtp.use_ssl,
        daily_limit=smtp.daily_limit,
        status=smtp.status,
        reputation_score=smtp.reputation_score
    )

    test_smtp_connection(temp_account)  # mevcut test fonksiyonunu kullan
    return {"success": True, "message": "SMTP connection is valid"}