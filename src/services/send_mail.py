import smtplib
import ssl
from email.message import EmailMessage
from src.core.config import CLIENT_EMAIL_APP_PASSWORD, CLIENT_EMAIL, TEST_EMAIL


async def send_email_message(
    subject: str, content: str, send_to: str, test: bool = True
) -> dict:
    sender_email = CLIENT_EMAIL
    app_password = CLIENT_EMAIL_APP_PASSWORD
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = TEST_EMAIL if test else send_to
    message["Subject"] = subject
    message.set_content(content)
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        return {"status": "success", "message": f"Email envoyé à {send_to}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
