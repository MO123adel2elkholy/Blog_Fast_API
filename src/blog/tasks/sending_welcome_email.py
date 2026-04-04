from celery import shared_task

from blog.Email.email import send_email


@shared_task
def welcome_email(subject: str, to_email: str, body: str):
    send_email(subject, to_email, body)
