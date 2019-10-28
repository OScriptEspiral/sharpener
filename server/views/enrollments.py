from flask import Blueprint, Response
from models import UserClassAssociation
from server.utils import (extract_token, extract_user,
                          extract_class_from_token, handle_validation_error)


def create_enrollments_blueprint(db_session, request):
    enrollments = Blueprint('enrollments', __name__)

    @enrollments.route('/<invite_token>', methods=['POST'])
    @handle_validation_error
    def enroll_user_in_class(invite_token):
        token = extract_token(request)
        user = extract_user(db_session, token)
        existing_class = extract_class_from_token(invite_token, db_session)

        existing_class_user = db_session.query(UserClassAssociation)\
            .filter_by(class_id=existing_class.id, user_email=user.email)\
            .first()

        if existing_class_user:
            return Response(status=200)

        user.classes.append(existing_class)
        db_session.add(user)
        db_session.commit()

        return Response(status=201)

    return enrollments
