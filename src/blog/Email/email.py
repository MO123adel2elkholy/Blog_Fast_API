import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

MAIL_USERNAME = "adel333mahmoud@gmail.com"
MAIL_PASSWORD = "iagm jlya neou htea"


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
