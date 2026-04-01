import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

# Path صحيح لملف .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

print(f" your cridintials is {EMAIL_USER} - {EMAIL_PASS}")


def send_email(subject: str, to_email: str, body: str):
    email = EmailMessage()
    email["From"] = EMAIL_USER
    email["To"] = EMAIL_USER
    email["Subject"] = subject
    email.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(email)
