from flask import Blueprint, jsonify
from sqlalchemy.sql.expression import func
from sqlalchemy import asc
from models import Exercise, Language


def pluck_first_column(results):
    return [r for (r, *k) in results]


def create_topics_blueprint(session, request, default_limit=100):
    topics = Blueprint('topics', __name__)

    @topics.route('/', methods=['GET'])
    def get_topics():
        try:
            limit = int(request.args.get('page_size', default_limit))
            offset = int(request.args.get('page', 0))
        except ValueError:
            return(400)

        topic = func.unnest(Exercise.topics)
        results = session\
            .query(topic)\
            .group_by(topic)\
            .order_by(asc(topic))\
            .limit(limit)\
            .offset(offset)\
            .all()

        return jsonify(pluck_first_column(results))

    @topics.route('/<language>', methods=['GET'])
    def get_topics_by_language(language):
        try:
            limit = int(request.args.get('page_size', default_limit))
            offset = int(request.args.get('page', 0))
        except ValueError:
            return(400)

        known_language = Language.get(language)
        if not known_language:
            return(404)

        topic = func.unnest(Exercise.topics)
        results = session\
            .query(topic, Exercise.language)\
            .filter_by(language=known_language)\
            .group_by(topic, Exercise.language)\
            .order_by(asc(topic))\
            .limit(limit)\
            .offset(offset)\
            .all()

        return jsonify(pluck_first_column(results))

    return topics
