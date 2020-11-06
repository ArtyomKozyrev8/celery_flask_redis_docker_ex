from celery import Celery
import time

from settings import R_LOGIN, R_PSWD, R_HOST

broker_url = f"redis://{R_LOGIN}:{R_PSWD}@{R_HOST}:6379"


def create_celery_app():
    _celery_app = Celery(
        'tasks',
        broker=broker_url,
        backend=broker_url,
    )

    _celery_app.conf.update(
        task_acks_late=True, # good for long tasks
        worker_prefetch_multiplier=1  # good for long tasks
    )
    return _celery_app


celery_app = create_celery_app()


@celery_app.task()
def add(x, y):
    time.sleep(10)
    r = {"x": x, "y": y, "res": x+y}
    return r


