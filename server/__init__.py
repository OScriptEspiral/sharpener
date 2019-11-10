from flask import Flask, request

from .views import (create_classes_blueprint, create_enrollments_blueprint,
                    create_exercises_blueprint, create_health_check_blueprint,
                    create_interface_blueprint, create_submissions_blueprint,
                    create_topics_blueprint, create_tracks_blueprint,
                    create_users_blueprint)


def create_app(
    db_session,
    github_config,
    flask_secret,
    bucket_submissions,
    bucket_exercises,
    debug=True,
):
    exercises = create_exercises_blueprint(
        db_session, request, bucket_exercises
    )
    topics = create_topics_blueprint(db_session, request)
    users = create_users_blueprint(db_session, request, github_config)
    interface = create_interface_blueprint(db_session, debug)
    submissions = create_submissions_blueprint(
        db_session, request, bucket_submissions
    )
    classes = create_classes_blueprint(db_session, request)
    tracks = create_tracks_blueprint(db_session, request)
    enrollments = create_enrollments_blueprint(db_session, request)

    healthcheck = create_health_check_blueprint(db_session)

    app = Flask(__name__)
    app.secret_key = flask_secret

    app.register_blueprint(interface)
    app.register_blueprint(healthcheck, url_prefix="/api/healthcheck")
    app.register_blueprint(exercises, url_prefix="/api/exercises")
    app.register_blueprint(topics, url_prefix="/api/topics")
    app.register_blueprint(submissions, url_prefix="/api/submissions")
    app.register_blueprint(classes, url_prefix="/api/classes")
    app.register_blueprint(tracks, url_prefix="/api/tracks")
    app.register_blueprint(enrollments, url_prefix="/api/enrollments")
    app.register_blueprint(users, url_prefix="/authenticate")

    return app
