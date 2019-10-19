from flask import Flask, request
from .views import (create_exercises_blueprint, create_topics_blueprint,
                    create_health_check_blueprint)


def create_app(session):
    exercises = create_exercises_blueprint(session, request)
    topics = create_topics_blueprint(session, request)
    healthcheck = create_health_check_blueprint(session)

    app = Flask(__name__)
    app.register_blueprint(healthcheck, url_prefix='/api/healthcheck')
    app.register_blueprint(exercises, url_prefix='/api/exercises')
    app.register_blueprint(topics, url_prefix='/api/topics')
    return app
