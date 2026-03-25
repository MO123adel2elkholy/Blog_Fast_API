import os
import time
from celery import Celery, shared_task
from blog.limiter import redis_path

celery_app = Celery(__name__)

celery_app.conf.broker_url = redis_path
celery_app.conf.result_backend = redis_path


@shared_task(name='create_task')
def celery_task(a, b, c):
    time.sleep(a)
    return a+b
