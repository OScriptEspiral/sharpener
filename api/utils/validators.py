import logging
from flask import make_response, jsonify
from functools import wraps


class ValidationError(Exception):
    def __init__(self, message, original, field):
        self.message = message
        self.original = original
        self.field = field


def handle_validation_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as err:
            logging.warn(f"Validation Error: {err.original}")
            return make_response(jsonify(error=err.message,
                                         field=err.field), status=400)
    return wrapper


def extract_int_arg(request, key, default=0):
    try:
        return int(request.args.get(key, default))
    except ValueError as err:
        raise ValidationError("Not an integer", err, key)
