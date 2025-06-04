from apps.api_server.models.smtp_account import SMTPAccount
from shared.utils.email_sender import send_email
from shared.utils.email_content import get_random_prompt, generate_email_body
from shared.database.session import SessionLocal

def test_warmup_email():
    db = SessionLocal()

    smtp = SMTPAccount(
        email="admin@app.postahub.com",
        username="admin@app.postahub.com",
        password="AoDaB7JeItqKHoG9",
        host="host.postahub.com",
        port=587,
        use_tls=True,
        use_ssl=False
    )

    try:
        prompt = get_random_prompt(db, user_id=1, category="promosyon")
        body = generate_email_body(prompt, recipient_name="Kerem")

        send_email(
            smtp_account=smtp,
            to="aliyuksal1@gmail.com",
            subject="🔥 AI Warm-up Test",
            body=body
        )

        print("✅ Dinamik AI içerik ile mail gönderildi!")

    except Exception as e:
        print(f"❌ Hata: {str(e)}")

    finally:
        db.close()

if __name__ == "__main__":
    test_warmup_email()