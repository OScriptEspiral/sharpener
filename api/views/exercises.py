from flask import Blueprint, jsonify
from sqlalchemy import asc
from models import Exercise, Artifact, Language

DEFAULT_LIMIT = 25

def exercise_to_dict(exercise):
    return {
        'name': exercise.name,
        'language': exercise.language.value,
        'creator': exercise.creator,
        'topics': exercise.topics,
        'difficulty': exercise.difficulty,
    }

def complete_exercise_to_dict(exercise, artifact):
    return {
        'name': exercise.name,
        'language': exercise.language.value,
        'creator': exercise.creator,
        'topics': exercise.topics,
        'difficulty': exercise.difficulty,
        'description': exercise.description,
        'readme': artifact.readme,
        'solution': artifact.solution,
        'starting_point': artifact.starting_point,
        'test': artifact.test,
        'hint': artifact.hint,
    }


def create_exercises_blueprint(session, request):
    exercises = Blueprint('exercises', __name__)

    @exercises.route('/', methods=['GET'])
    def get_exercises(default_limit=DEFAULT_LIMIT):
        limit = request.args.get('page_size', default_limit)
        offset = request.args.get('page', 0)
        exercises = session.query(Exercise)\
                           .order_by(asc(Exercise.difficulty))\
                           .limit(limit)\
                           .offset(offset)\
                           .all()

        results = [exercise_to_dict(ex) for ex in exercises]
        return jsonify(results)

    @exercises.route('/<language>', methods=['GET'])
    def get_exercises_by_language(language, default_limit=DEFAULT_LIMIT):
        limit = request.args.get('page_size', default_limit)
        offset = request.args.get('page', 0)
        known_language = Language.get(language)

        if known_language:
            exercises = session.query(Exercise)\
                                .filter_by(language=known_language)\
                                .order_by(asc(Exercise.difficulty))\
                                .limit(limit)\
                                .offset(offset)\
                                .all()

            results = [exercise_to_dict(ex) for ex in exercises]
        else:
            results = []

        return jsonify(results)


    @exercises.route('/<language>/<name>', methods=['GET'])
    def get_specific_exercise(language, name, default_limit=DEFAULT_LIMIT):
        limit = request.args.get('page_size', default_limit)
        offset = request.args.get('page', 0)

        known_language = Language.get(language)

        if known_language:
            exercise, artifact = session.query(Exercise, Artifact)\
                .filter_by(language=language, name=name)\
                .order_by(asc(Exercise.difficulty))\
                .limit(limit)\
                .offset(offset)\
                .first()

            results= complete_exercise_to_dict(exercise, artifact)

        else:
            results = []


        return jsonify(results)


    return exercises
