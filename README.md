# celery_flask_redis_docker_ex
Very simple dockerized application to illustrate how to use Celery with Flask and Redis in Docker containers

**HOW TO RUN:**

_Flask app:_

docker run -d -p 5555:80 --name serv --network test_net -e GUNICORN_CONF="/usr/src/app/gunicorn_conf.py" serv

_Celery app:_

docker run -d --name c_app --network test_net  c_app

**HOW TO Build Images:**

_Flask app:_

docker build -t serv .

_Celery app:_

docker build -f Dockerfile.Celery -t c_app .