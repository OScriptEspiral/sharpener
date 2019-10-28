from flask import Blueprint, Response
from models import Class, Track
from server.utils import extract_token, extract_user, handle_validation_error
from uuid import uuid4


def create_classes_blueprint(db_session, request):
    classes = Blueprint('classes', __name__)

    @classes.route('/<name>', methods=['POST'])
    @handle_validation_error
    def create_class(name):
        token = extract_token(request)
        user = extract_user(db_session, token)

        if not user.is_teacher:
            return Response(response="Only teachers can create classes.",
                            status=403)

        existing_class = db_session.query(Class).filter_by(owner=user.email,
                                                           name=name).first()
        if existing_class:
            return Response(
                response="You already have a class with that name.",
                status=409
            )

        new_class = Class(name=name,
                          invite_token=uuid4())

        user.classes_owned.append(new_class)
        db_session.add(user)
        db_session.flush()
        db_session.add(new_class)

        db_session.commit()

        return Response(status=201)

    @classes.route('/<name>/<track>', methods=['POST'])
    @handle_validation_error
    def register_track(name, track):
        token = extract_token(request)
        user = extract_user(db_session, token)

        if not user.is_teacher:
            return Response(response="Only teachers can register tracks.",
                            status=403)

        existing_class = db_session.query(Class)\
            .filter_by(owner=user.email, name=name)\
            .first()

        if not existing_class:
            return Response(response="You don't own a class with this name.",
                            status=404)

        existing_track = db_session.query(Track)\
            .filter_by(owner=user.email, name=track)\
            .first()

        print(existing_track)
        if not existing_track:
            return Response(response="You don't own a track with this name.",
                            status=404)

        existing_class.tracks.append(existing_track)

        return Response(status=201)

    return classes
