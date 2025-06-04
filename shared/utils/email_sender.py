import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from apps.api_server.models.smtp_account import SMTPAccount

def send_email(
    smtp_account: SMTPAccount,
    to: str,
    subject: str,
    body: str,
    html: Optional[str] = None
) -> None:
    """
    SMTPAccount modelindeki bilgilere göre mail gönderir.

    :param smtp_account: SMTPAccount SQLAlchemy modeli
    :param to: Alıcı adresi
    :param subject: E-posta konusu
    :param body: Temel düz metin içeriği
    :param html: İsteğe bağlı HTML içeriği
    """
    # Mesajı hazırla
    if html:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(body, "plain"))
        msg.attach(MIMEText(html, "html"))
    else:
        msg = MIMEText(body, "plain")

    msg["Subject"] = subject
    msg["From"] = smtp_account.email
    msg["To"] = to

    # Bağlantı kur
    if smtp_account.use_ssl:
        server = smtplib.SMTP_SSL(smtp_account.host, smtp_account.port, timeout=30)
    else:
        server = smtplib.SMTP(smtp_account.host, smtp_account.port, timeout=30)
        if smtp_account.use_tls:
            server.starttls()

    try:
        # Giriş yap
        server.login(smtp_account.username, smtp_account.password)
        # Gönder
        server.sendmail(smtp_account.email, [to], msg.as_string())
    finally:
        # Bağlantıyı kapat
        server.quit()