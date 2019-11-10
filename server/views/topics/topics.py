from flasgger import swag_from
from flask import Blueprint, jsonify
from models import Exercise
from server.utils import (extract_int_arg, extract_language,
                          handle_validation_error)
from sqlalchemy import asc
from sqlalchemy.sql.expression import func


def pluck_first_column(results):
    return [r for (r, *k) in results]


def create_topics_blueprint(session, request, default_limit=100):
    topics = Blueprint("topics", __name__)

    @topics.route("/", methods=["GET"])
    @handle_validation_error
    @swag_from('get_topics.yaml')
    def get_topics():
        limit = extract_int_arg(request, "page_size", default=default_limit)
        offset = extract_int_arg(request, "page", default=0)

        topic = func.unnest(Exercise.topics)
        results = (
            session.query(topic)
            .group_by(topic)
            .order_by(asc(topic))
            .limit(limit)
            .offset(offset)
            .all()
        )

        return jsonify(pluck_first_column(results))

    @topics.route("/<language>", methods=["GET"])
    @handle_validation_error
    @swag_from('get_topics_by_language.yaml')
    def get_topics_by_language(language):
        limit = extract_int_arg(request, "page_size", default=default_limit)
        offset = extract_int_arg(request, "page", default=0)
        known_language = extract_language(language)

        topic = func.unnest(Exercise.topics)
        results = (
            session.query(topic, Exercise.language)
            .filter_by(language=known_language)
            .group_by(topic, Exercise.language)
            .order_by(asc(topic))
            .limit(limit)
            .offset(offset)
            .all()
        )

        return jsonify(pluck_first_column(results))

    return topics
