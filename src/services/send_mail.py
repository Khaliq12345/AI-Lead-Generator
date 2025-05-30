import smtplib
import ssl
from email.message import EmailMessage
from src.core.config import CLIENT_EMAIL_APP_PASSWORD, CLIENT_EMAIL, TEST_EMAIL
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

async def send_email_draft(subject: str, content: str, send_to: str, test: bool = True) -> dict:
    sender_email = CLIENT_EMAIL
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(content, 'plain')
        message['to'] =  TEST_EMAIL if test else send_to
        message['from'] = sender_email
        message['subject'] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}
        draft = service.users().drafts().create(userId='me', body=create_message).execute()
        return {"status": "success", "draft_id": draft['id']}
    except Exception as e:
        return {"status": "error", "message": str(e)}

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
