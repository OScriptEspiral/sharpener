import logging
from functools import wraps

from flask import Blueprint, jsonify
from sqlalchemy import text


def check_successful(service_name=""):
    def outer_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            status = True
            try:
                func(*args, **kwargs)
            except Exception:
                logging.exception(
                    "Error while checking {} health.".format(service_name)
                )
                status = False

            return {service_name: status}

        return wrapper

    return outer_wrapper


@check_successful("database")
def database_is_alive(session):
    session.execute(text("SELECT 1;"))


def create_health_check_blueprint(session):
    healthcheck = Blueprint("healthcheck", __name__)

    @healthcheck.route("/", methods=["GET"])
    def check_health():
        services = {**database_is_alive(session)}

        healthy = all(services.values())
        status = 200 if healthy else 500

        return jsonify({"healthy": healthy, "services": services}), status

    return healthcheck
