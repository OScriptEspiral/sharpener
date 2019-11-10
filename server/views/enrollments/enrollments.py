from flask import Blueprint, Response
from models import UserClassAssociation
from flasgger import swag_from
from server.utils import (extract_user, extract_class_from_token, handle_validation_error)


def create_enrollments_blueprint(db_session, request):
    enrollments = Blueprint('enrollments', __name__)

    @enrollments.route('/<invite_token>', methods=['POST'])
    @handle_validation_error
    @swag_from('enroll_user_in_class.yaml')
    def enroll_user_in_class(invite_token):
        user = extract_user(request, db_session)
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
