from celery import Celery
import time
from datetime import datetime

from settings import REDIS_LOGIN, REDIS_HOST, REDIS_PSWD, RABBIT_HOST

backend_storage_url = f"redis://{REDIS_LOGIN}:{REDIS_PSWD}@{REDIS_HOST}:6379"
broker_url = f"amqp://guest@{RABBIT_HOST}:5672/"



def create_celery_app():
    _celery_app = Celery(
        'tasks',
        broker=broker_url,
        backend=backend_storage_url,
    )

    _celery_app.conf.update(
        task_acks_late=True,  # good for long tasks
        worker_prefetch_multiplier=1,  # good for long tasks
        result_expires=60  # 1 minutes
    )
    return _celery_app


celery_app = create_celery_app()


# celery_app is the module name in the case is used to prevent  duplicated if several modules
# though you can use anu or none value for name argument
@celery_app.task(name="celery_app.add")
def add(x, y):
    time.sleep(10)
    r = {"x": x, "y": y, "res": x+y}
    return r


@celery_app.task(name="celery_app.run_my_task")
def run_my_task(x):
    time.sleep(10)
    r = {"result": f"RESULT: {x}", "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    return r

