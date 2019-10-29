import logging
from models import User, Language, Track, Class, Submission
from flask import make_response, jsonify
from functools import wraps


class ValidationError(Exception):
    def __init__(self, message, original, field):
        self.message = message
        self.original = original
        self.field = field


class TokenError(Exception):
    def __init__(self, original, message):
        self.original = original
        self.message = message


def handle_validation_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            logging.warn(f"Validation Error: {err.original}")
            return make_response(jsonify(error=err.message,
                                         field=err.field), 400)
        except TokenError as err:
            logging.warn(f"Token error: {err.original}")
            return make_response(jsonify(error=err.message), 401)
    return wrapper


def extract_int_arg(request, key, default=0):
    try:
        return int(request.args.get(key, default))
    except ValueError as err:
        raise ValidationError("Not an integer", err, key)


def extract_language(language):
    known_language = Language.get(language)
    if not known_language:
        message = f"Unknown language {language}"
        return ValidationError(message, message, "language")


def extract_token(request):
    bearer_token = request.headers.get('authorization')
    if not bearer_token:
        message = 'Authentication token header is missing'
        raise TokenError(message, message)
    token = bearer_token.rsplit('Bearer ')[1]
    return token


def extract_user(db_session, token):
    user = db_session.query(User)\
        .filter_by(token=token)\
        .first()
    if not user:
        message = 'Unknown indetification token'
        raise TokenError('Bad identification token', message)

    return user


def extract_track(name, db_session, user):
    existing_track = db_session.query(Track)\
        .filter_by(name=name, owner=user.email)\
        .first()

    if not existing_track:
        message = "Track doesn't exist."
        raise ValidationError(message, message, 'track')

    return existing_track


def extract_class(name, db_session, user):
    existing_class = db_session.query(Class)\
        .filter_by(name=name, owner=user.email)\
        .first()

    if not existing_class:
        message = "Class doesn't exist."
        raise ValidationError(message, message, 'class')

    return existing_class


def extract_class_from_token(token, db_session):
    existing_class = db_session.query(Class)\
        .filter_by(invite_token=token)\
        .first()

    if not existing_class:
        message = "Your invite token is invalid."
        original = "No class associated with this token."
        raise TokenError(message, original)

    return existing_class


def extract_submission(token, db_session):
    existing_submission = db_session.query(Submission)\
        .filter_by(submission_token=token)\
        .first()

    if not existing_submission:
        message = "Submission token is invalid."
        raise TokenError(message, message)

    return existing_submission
