from flask import Blueprint, jsonify, Response
from sqlalchemy import asc
from models import Exercise, Artifact, Language
from server.utils import (extract_int_arg, handle_validation_error,
                          extract_language, extract_token, extract_user)
from flasgger import swag_from


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
        'compressed': artifact.compressed,
        'test': artifact.test,
        'hint': artifact.hint,
    }


def create_exercises_blueprint(db_session, request, default_limit=25):
    exercises = Blueprint('exercises', __name__)

    @exercises.route('/', methods=['GET'])
    @handle_validation_error
    @swag_from('get_exercises.yaml')
    def get_exercises():
        limit = extract_int_arg(request, 'page_size', default=default_limit)
        offset = extract_int_arg(request, 'page', default=0)

        exercises = db_session.query(Exercise)\
                           .order_by(asc(Exercise.difficulty))\
                           .limit(limit)\
                           .offset(offset)\
                           .all()

        results = [exercise_to_dict(ex) for ex in exercises]
        return jsonify(results)

    @exercises.route('/<language>', methods=['GET'])
    @handle_validation_error
    @swag_from('get_exercises_by_language.yaml')
    def get_exercises_by_language(language):
        limit = extract_int_arg(request, 'page_size', default=default_limit)
        offset = extract_int_arg(request, 'page', default=0)
        known_language = extract_language(language)

        exercises = db_session.query(Exercise)\
            .filter_by(language=known_language)\
            .order_by(asc(Exercise.difficulty))\
            .limit(limit)\
            .offset(offset)\
            .all()

        results = [exercise_to_dict(ex) for ex in exercises]

        return jsonify(results)

    @exercises.route('/<language>/<name>', methods=['GET'])
    @handle_validation_error
    @swag_from('get_specific_exercise.yaml')
    def get_specific_exercise(language, name):
        known_language = Language.get(language)
        if not known_language:
            return Response("Unknown language",
                            status=404)

        exercise, artifact = db_session.query(Exercise, Artifact)\
            .filter(Exercise.artifact_id == Artifact.id)\
            .filter_by(language=language, name=name)\
            .order_by(asc(Exercise.difficulty))\
            .first()

        if not exercise:
            return Response("Exercise doesn't exist",
                            status=404)

        results = complete_exercise_to_dict(exercise, artifact)

        return jsonify(results)

    return exercises

    # @exercises.route('/<language>/<name>', methods=['PUT'])
    # @handle_validation_error
    # @swag_from('get_specific_exercise.yaml')
    # def upsert_exercise(language, name):
    #     token = extract_token(request)
    #     user = extract_user(db_session, token)

    #     if not user.is_teacher:
    #         return Response(response="Only teachers can upload exercises.",
    #                         status=403)

    #     known_language = Language.get(language)
    #     if not known_language:
    #         return Response("Unknown language",
    #                         status=404)

    #     exercise, artifact = db_session.query(Exercise, Artifact)\
    #         .filter(Exercise.artifact_id == Artifact.id)\
    #         .filter_by(language=language, name=name)\
    #         .order_by(asc(Exercise.difficulty))\
    #         .first()

    #     if not exercise:
    #         new_exercise = Exercise(
    #             language=known_language,
    #             name=name,
    #             creator=user.email,
    #         )
    #         new_artifact = Artifact(
    #             readme="",
    #             solution="",
    #             starting_point="",
    #             test="",
    #             compressed="",
    #         )
    #         new_exercise.artifact = new_artifact
    #         db_session.add_all(new_exercise, new_artifact)
    #         db_session.commit()
    #         return Response("Created", status=201)
