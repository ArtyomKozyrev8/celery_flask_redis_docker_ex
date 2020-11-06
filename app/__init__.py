from flask import Flask, current_app, jsonify
from redis import Redis
from settings import REDIS_LOGIN, REDIS_HOST, REDIS_PSWD, RABBIT_HOST
from celery_app import add
from random import randint
from celery.result import AsyncResult


def create_app():
    app = Flask(__name__)

    r_pool = Redis.from_url(f"redis://{REDIS_LOGIN}:{REDIS_PSWD}@{REDIS_HOST}:6379")

    app.config.from_mapping(
        SECRET_KEY="dsfewfwerfgfrgra",
        SESSION_COOKIE_NAME="celery_test",
        R_POOL=r_pool
    )

    @app.route("/", methods=["GET"])
    def index():
        return "index"

    @app.route("/set/<name>", methods=["GET"])
    def set_var_redis(name):
        x = randint(100, 999)
        current_app.config["R_POOL"].set(name, x, ex=120)
        return f"SET: {name} - {x}"

    @app.route("/get/<name>", methods=["GET"])
    def get_var_redis(name):
        x = current_app.config["R_POOL"].get(name)
        return f"GET: {name} ======> {x}"

    @app.route("/cel", methods=["GET"])
    def cel():
        temp1 = randint(1, 100)
        temp2 = randint(1, 100)
        result = add.delay(temp1, temp2)
        return jsonify({"taskid": result.task_id, "args": [temp1, temp2]})

    @app.route("/celres/<task_id>", methods=["GET"])
    def celresult(task_id):
        task = AsyncResult(task_id)
        if task.ready():
            if task.successful():
                result = task.get()
                return jsonify({"result": result, "error": False, "pending": False})
            else:
                return jsonify({"result": None, "error": True, "pending": False})
        return jsonify({"result": None, "error": False, "pending": True})

    return app
