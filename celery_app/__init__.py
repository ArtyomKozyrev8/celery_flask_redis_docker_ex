from celery import Celery

from settings import R_LOGIN, R_PSWD, R_HOST

broker_url = f"redis://{R_LOGIN}:{R_PSWD}@{R_HOST}:6379"
celery_app = Celery(
    'tasks',
    broker=broker_url,
    backend=broker_url,

)


@celery_app.task()
def add(x, y):
    return x + y


