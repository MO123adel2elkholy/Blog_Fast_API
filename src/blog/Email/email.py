import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

# Path صحيح لملف .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

print(f" your cridintials is {EMAIL_USER} - {EMAIL_PASS}")

MAIL_USERNAME = "adel333mahmoud@gmail.com"
MAIL_PASSWORD = "cklpvjzlkrzvqjyi"


def send_email(subject: str, to_email: str, body: str):
    email = EmailMessage()
    email["From"] = MAIL_USERNAME
    email["To"] = MAIL_USERNAME
    email["Subject"] = subject
    email.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(email)
