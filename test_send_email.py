from apps.api_server.models.smtp_account import SMTPAccount
from shared.utils.email_sender import send_email

# SMTP bilgileri (test hesabı ya da kendi sunucun)
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
    send_email(
        smtp_account=smtp,
        to="aliyuuksel13@gmail.com",
        subject="Warm-up Test ✅",
        body="This is a test email from the warm-up system."
    )
    print("✅ Mail gönderildi!")
except Exception as e:
    print(f"❌ Hata oluştu: {str(e)}")

