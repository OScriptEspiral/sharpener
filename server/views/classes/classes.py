from uuid import uuid4

from flasgger import swag_from
from flask import Blueprint, Response, jsonify

from models import Class, Track
from server.utils import extract_teacher, handle_validation_error


def extract_class_data(classroom):
    return {
        "name": classroom.name,
        "created_at": classroom.created_at.isoformat(),
        "members": len(classroom.students),
        "tracks": len(classroom.tracks_classes),
        "invite_token": classroom.invite_token,
    }


def create_classes_blueprint(db_session, request):
    classes = Blueprint("classes", __name__)

    @classes.route("/", methods=["GET"])
    @handle_validation_error
    @swag_from("get_all_classes.yaml")
    def get_all_classes():
        teacher = extract_teacher(request, db_session)

        existing_classes = (
            db_session.query(Class).filter_by(owner=teacher.email).all()
        )

        classes_data = [
            extract_class_data(classroom) for classroom in existing_classes
        ]

        return jsonify(classes_data)

    @classes.route("/<name>", methods=["PUT"])
    @handle_validation_error
    @swag_from("create_class.yaml")
    def create_class(name):
        teacher = extract_teacher(request, db_session)

        existing_class = (
            db_session.query(Class)
            .filter_by(owner=teacher.email, name=name)
            .first()
        )
        if existing_class:
            return Response(
                response="You already have a class with that name.", status=409
            )

        new_class = Class(name=name, invite_token=uuid4())

        teacher.classes_owned.append(new_class)
        db_session.add(teacher)
        db_session.flush()
        db_session.add(new_class)

        db_session.commit()

        return Response(status=201)

    @classes.route("/<name>/<track>", methods=["PUT"])
    @handle_validation_error
    @swag_from("register_track.yaml")
    def register_track(name, track):
        teacher = extract_teacher(request, db_session)

        existing_class = (
            db_session.query(Class)
            .filter_by(owner=teacher.email, name=name)
            .first()
        )

        if not existing_class:
            return Response(
                response="You don't own a class with this name.", status=404
            )

        existing_track = (
            db_session.query(Track)
            .filter_by(owner=teacher.email, name=track)
            .first()
        )

        if not existing_track:
            return Response(
                response="You don't own a track with this name.", status=404
            )

        existing_class.tracks.append(existing_track)

        return Response(status=201)

    return classes
