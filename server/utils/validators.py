import json
import logging
from functools import wraps

from flask import jsonify, make_response

from models import Class, Exercise, Language, Submission, Track, User


class ValidationError(Exception):
    def __init__(self, message, original, field):
        self.message = message
        self.original = original
        self.field = field


class AuthorizationError(Exception):
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
            return make_response(
                jsonify(error=err.message, field=err.field), 400
            )
        except AuthorizationError as err:
            logging.warn(f"Authorization Error: {err.original}")
            return make_response(
                jsonify(error=err.message, field=err.field), 403
            )

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
    return known_language


def extract_token(request):
    token = request.headers.get("authorization")
    if not token:
        message = "Authentication token header is missing"
        raise TokenError(message, message)

    return token


def extract_user(request, db_session):
    token = extract_token(request)
    user = db_session.query(User).filter_by(token=token).first()
    if not user:
        message = "Unknown indetification token"
        raise TokenError("Bad identification token", message)

    return user


def extract_teacher(db_session, token):
    user = extract_user(db_session, token)
    if not user.is_teacher:
        message = "Only teachers can use this method."
        raise AuthorizationError(message, message)
    return user


def extract_track(name, db_session, user):
    existing_track = (
        db_session.query(Track).filter_by(name=name, owner=user.email).first()
    )

    if not existing_track:
        message = "Track doesn't exist."
        raise ValidationError(message, message, "track")

    return existing_track


def extract_class(name, db_session, user):
    existing_class = (
        db_session.query(Class).filter_by(name=name, owner=user.email).first()
    )

    if not existing_class:
        message = "Class doesn't exist."
        raise ValidationError(message, message, "class")

    return existing_class


def extract_class_from_token(token, db_session):
    existing_class = (
        db_session.query(Class).filter_by(invite_token=token).first()
    )

    if not existing_class:
        message = "Your invite token is invalid."
        original = "No class associated with this token."
        raise TokenError(message, original)

    return existing_class


def extract_submission(token, db_session):
    existing_submission = (
        db_session.query(Submission).filter_by(submission_token=token).first()
    )

    if not existing_submission:
        message = "Submission token is invalid."
        raise TokenError(message, message)

    return existing_submission


def extract_files(request, expected_files):
    received_files = {file for file in request.files if file in expected_files}

    if not received_files >= expected_files:
        missing_files = ", ".join(expected_files - received_files)
        message = f"There are files missing: {missing_files}"
        raise ValidationError(message, message, "track")

    filtered_files = {
        (filename, file)
        for (filename, file) in request.files.items()
        if filename in received_files
    }
    return filtered_files


def extract_metadata(request):
    meta = request.files.get("meta")
    if meta:
        data = json.load(meta)
        return data.get("topics"), data.get("difficulty")
    return [], None


def extract_test_params(request):
    coverage = request.form.get("test_coverage")
    output = request.form.get("test_output")
    checksum = request.form.get("test_checksum")
    required = [coverage, output, checksum]
    received = [p for p in required if p]
    if len(received) < 3:
        message = f"Missing parameters"
        raise ValidationError(message, message, "test_params")
    return coverage, output, checksum


def extract_exercises(request, db_session):
    data = request.get_json(silent=True, force=True)
    exercises = data.get("exercises")
    try:
        extracted_exercises = [
            db_session(Exercise)
            .filter_by(name=ex.get("name"), language=ex.get("language"))
            .first()
            for ex in exercises
        ]
    except Exception:
        message = "Invalid exercises data"
        raise ValidationError(message, message, "exercises")
    return extracted_exercises
