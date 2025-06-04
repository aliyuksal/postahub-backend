from celery import shared_task
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from shared.database.session import SessionLocal
from apps.api_server.models.smtp_account import SMTPAccount
from shared.models.warmup_target import WarmupTarget
from shared.models.email_logs import EmailLog
from shared.utils.email_content import get_random_prompt, generate_email_body
from shared.utils.email_sender import send_email
import uuid
from apps.warming_engine.models.warmup_strategy import WarmupStrategy
from apps.warming_engine.scheduler.celery_app import celery_app


@shared_task
def test_task():
    print("✅ test_task çalıştı")
    return "ok"


@shared_task
def warmup_test_task(smtp_account_id: int):
    print(f"🔥 Running warm-up test task for SMTP Account ID: {smtp_account_id}")
    return {"status": "ok", "smtp_account_id": smtp_account_id}


@shared_task
def run_warmup_for_smtp(smtp_id: int):
    print(f"🚀 Starting warm-up for SMTP ID: {smtp_id}")
    db = SessionLocal()

    try:
        smtp = db.query(SMTPAccount).filter_by(id=smtp_id).first()
        if not smtp:
            print(f"❌ SMTPAccount not found for ID: {smtp_id}")
            return {"status": "error", "reason": "smtp_not_found"}

        # ⬇️ Strategy entegrasyonu
        strategy = db.query(WarmupStrategy).filter_by(smtp_account_id=smtp_id).first()
        if not strategy:
            print(f"⚠️ No strategy defined for SMTP ID {smtp_id}, skipping...")
            return {"status": "skipped", "reason": "no_strategy"}

        for i in range(strategy.sending_frequency):
            # Hedef mail adresi seç
            target = db.query(WarmupTarget)\
                       .filter_by(status="active", reply_enabled=True)\
                       .order_by(func.random())\
                       .first()

            if not target:
                print("⚠️ No available warmup target.")
                continue

            to_email = target.email

            # AI içerik üretimi
            prompt = get_random_prompt(db, user_id=smtp.user_id, language=strategy.email_language)
            body = generate_email_body(prompt, name=target.name, surname=target.surname)

            # Konu ve UUID
            subject = f"Hey {target.name}, quick note 👋"
            tracking_code = uuid.uuid4()
            body += f"\n\n[uuid:{tracking_code}]"

            # Gönderim
            try:
                message_id = send_email(
                    smtp_account=smtp,
                    to=to_email,
                    subject=subject,
                    body=body
                )
                status = "sent"
                error_message = None
            except Exception as send_error:
                status = "failed"
                error_message = str(send_error)
                message_id = None

            # Email log kaydı
            log = EmailLog(
                smtp_account_id=smtp.id,
                recipient_email=to_email,
                subject=subject,
                body=body,
                tracking_code=tracking_code,
                status=status,
                error_message=error_message,
                prompt_id=prompt.id if prompt else None,
                target_id=target.id
            )
            db.add(log)

        db.commit()
        print(f"✅ Warm-up complete for SMTP {smtp.email}")
        return {"status": "completed"}

    except SQLAlchemyError as db_error:
        print(f"❌ DB Error: {str(db_error)}")
        return {"status": "db_error", "error": str(db_error)}

    except Exception as e:
        print(f"❌ General Error: {str(e)}")
        return {"status": "error", "error": str(e)}

    finally:
        db.close()


@shared_task
def run_daily_warmups():
    print("📅 Starting daily warm-up routine...")
    db = SessionLocal()

    try:
        active_smtps = db.query(SMTPAccount).filter_by(status="active").all()
        for smtp in active_smtps:
            run_warmup_for_smtp.delay(smtp.id)
            print(f"🟢 Scheduled warm-up for SMTP ID: {smtp.id}")

        return {"total": len(active_smtps)}

    except Exception as e:
        print(f"❌ Error in daily warm-up: {str(e)}")
        return {"status": "error", "reason": str(e)}

    finally:
        db.close()