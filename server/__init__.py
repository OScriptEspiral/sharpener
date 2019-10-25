from flask import Flask, request
from .views import (create_exercises_blueprint, create_topics_blueprint,
                    create_health_check_blueprint, create_users_blueprint,
                    create_interface_blueprint)


def create_app(db_session, github_config, flask_secret, debug=True):
    exercises = create_exercises_blueprint(db_session, request)
    topics = create_topics_blueprint(db_session, request)
    users = create_users_blueprint(db_session, request, github_config)
    interface = create_interface_blueprint(db_session, debug)

    healthcheck = create_health_check_blueprint(db_session)

    app = Flask(__name__)
    app.secret_key = flask_secret

    app.register_blueprint(interface)
    app.register_blueprint(healthcheck, url_prefix='/api/healthcheck')
    app.register_blueprint(exercises, url_prefix='/api/exercises')
    app.register_blueprint(topics, url_prefix='/api/topics')
    app.register_blueprint(users,  url_prefix='/authenticate')

    return app
