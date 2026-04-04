# import time

# from celery import Celery, shared_task

# from blog.Email.email import send_email

# celery_app = Celery(__name__)

# celery_app.conf.broker_url = "redis://localhost:6379/0"
# celery_app.conf.result_backend = "redis://localhost:6379/0"


# @shared_task(name="create_task")
# def celery_task(a, b, c):
#     time.sleep(a)
#     return a + b


# @shared_task(name="Welcome Email ")
# def Welcome_email(subject: str, to_email: str, body: str):
#     send_email(subject, to_email, body)


from celery import Celery

from blog.Email.email import send_email

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


# @celery_app.task(name="welcome_email")
# def welcome_email(subject: str, to_email: str, body: str):
#     send_email(subject, to_email, body)


@celery_app.task
def send_verification_email(to_email: str, token: str):
    link = f"http://localhost:8000/verify-email?token={token}"

    send_email(
        subject="Verify your email",
        to_email=to_email,
        body=f"Click here to verify: {link}",
    )


@celery_app.task
def send_reset_email(to_email: str, token: str):
    link = f"http://localhost:8002/user/rest/reset-password?token={token}"

    send_email(subject="Reset Password", to_email=to_email, body=f"Reset here: {link}")
