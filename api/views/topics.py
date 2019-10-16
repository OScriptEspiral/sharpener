from flask import Blueprint, jsonify
from sqlalchemy.sql.expression import func
from sqlalchemy import asc
from models import Exercise, Language

DEFAULT_LIMIT = 1100

def pluck_first_column(results):
    return [r for (r, *k ) in results]

def create_topics_blueprint(session, request):
    topics = Blueprint('topics', __name__)

    @topics.route('/', methods=['GET'])
    def get_topics(default_limit=DEFAULT_LIMIT):
        limit = request.args.get('page_size', default_limit)
        offset = request.args.get('page', 0)

        topic = func.unnest(Exercise.topics)
        results = session.query(topic)\
                           .group_by(topic)\
                           .order_by(asc(topic))\
                           .limit(limit)\
                           .offset(offset)\
                           .all()


        return jsonify(pluck_first_column(results))

    @topics.route('/<language>', methods=['GET'])
    def get_topics_by_language(language, default_limit=DEFAULT_LIMIT):
        limit = request.args.get('page_size', default_limit)
        offset = request.args.get('page', 0)

        known_language = Language.get(language)
        if known_language:
            topic = func.unnest(Exercise.topics)
            results = session.query(topic, Exercise.language)\
                              .filter_by(language=known_language)\
                              .group_by(topic, Exercise.language)\
                              .order_by(asc(topic))\
                              .limit(limit)\
                              .offset(offset)\
                              .all()
        else:
            results = []

        return jsonify(pluck_first_column(results))


    return topics
