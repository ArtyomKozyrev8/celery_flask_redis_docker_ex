from celery import Celery
import time

from settings import REDIS_LOGIN, REDIS_HOST, REDIS_PSWD, RABBIT_HOST

backend_storage_url = f"redis://{REDIS_LOGIN}:{REDIS_PSWD}@{REDIS_HOST}:6379"
broker_url = f"pyamqp://guest@{RABBIT_HOST}//"


def create_celery_app():
    _celery_app = Celery(
        'tasks',
        broker=broker_url,
        backend=backend_storage_url,
    )

    _celery_app.conf.update(
        task_acks_late=True,  # good for long tasks
        worker_prefetch_multiplier=1  # good for long tasks
    )
    return _celery_app


celery_app = create_celery_app()


@celery_app.task()
def add(x, y):
    time.sleep(10)
    r = {"x": x, "y": y, "res": x+y}
    return r


# docker run -d --name=test_rabbit --network=test_net rabbitmq
