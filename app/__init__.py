from flask import Flask, current_app
from redis import Redis
from settings import R_LOGIN, R_HOST, R_PSWD
from random import randint
from celery_app import add


def create_app():
    app = Flask(__name__)

    r_pool = Redis.from_url(f"redis://{R_LOGIN}:{R_PSWD}@{R_HOST}:6379")

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
        result = add.delay(23, 42)
        c = result.wait()
        return f"{c}"

    return app
