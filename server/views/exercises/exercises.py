from flasgger import swag_from
from flask import Blueprint, Response, jsonify
from models import Artifact, Exercise, Language
from server.utils import (extract_files, extract_int_arg, extract_language,
                          extract_metadata, extract_teacher,
                          handle_validation_error, upload_files)
from sqlalchemy import asc


def exercise_to_dict(exercise):
    return {
        "name": exercise.name,
        "language": exercise.language.value,
        "creator": exercise.creator,
        "topics": exercise.topics,
        "difficulty": exercise.difficulty,
    }


def complete_exercise_to_dict(exercise, artifact):
    return {
        "name": exercise.name,
        "language": exercise.language.value,
        "creator": exercise.creator,
        "topics": exercise.topics,
        "difficulty": exercise.difficulty,
        "description": exercise.description,
        "readme": artifact.readme,
        "solution": artifact.solution,
        "starting_point": artifact.starting_point,
        "compressed": artifact.compressed,
        "test": artifact.test,
    }


def create_exercises_blueprint(db_session, request, bucket, default_limit=25):
    exercises = Blueprint("exercises", __name__)

    @exercises.route("/", methods=["GET"])
    @handle_validation_error
    @swag_from("get_exercises.yaml")
    def get_exercises():
        limit = extract_int_arg(request, "page_size", default=default_limit)
        offset = extract_int_arg(request, "page", default=0)

        exercises = (
            db_session.query(Exercise)
            .order_by(asc(Exercise.difficulty))
            .limit(limit)
            .offset(offset)
            .all()
        )

        results = [exercise_to_dict(ex) for ex in exercises]
        return jsonify(results)

    @exercises.route("/<language>", methods=["GET"])
    @handle_validation_error
    @swag_from("get_exercises_by_language.yaml")
    def get_exercises_by_language(language):
        limit = extract_int_arg(request, "page_size", default=default_limit)
        offset = extract_int_arg(request, "page", default=0)
        known_language = extract_language(language)

        exercises = (
            db_session.query(Exercise)
            .filter_by(language=known_language)
            .order_by(asc(Exercise.difficulty))
            .limit(limit)
            .offset(offset)
            .all()
        )

        results = [exercise_to_dict(ex) for ex in exercises]

        return jsonify(results)

    @exercises.route("/<language>/<name>", methods=["GET"])
    @handle_validation_error
    @swag_from("get_specific_exercise.yaml")
    def get_specific_exercise(language, name):
        extract_teacher(request, db_session)
        known_language = extract_language(language)

        exercise, artifact = (
            db_session.query(Exercise, Artifact)
            .filter(Exercise.artifact_id == Artifact.id)
            .filter_by(language=known_language, name=name)
            .order_by(asc(Exercise.difficulty))
            .first()
        ) or (None, None)

        if not exercise:
            return Response("Exercise doesn't exist", status=404)

        results = complete_exercise_to_dict(exercise, artifact)

        return jsonify(results)

    @exercises.route("/<language>/<name>", methods=["PUT"])
    @handle_validation_error
    @swag_from("upsert_exercise.yaml")
    def upsert_exercise(language, name):
        teacher = extract_teacher(request, db_session)
        known_language = extract_language(language)

        expected_files = {
            "readme",
            "solution",
            "test",
            "starting_point",
            "compressed",
        }

        filterd_files = extract_files(request, expected_files)

        topics, difficulty = extract_metadata(request)

        prefix = f"{known_language}"
        mapper = Language(known_language).get_mapper()
        files_map = mapper(prefix, name)
        blobs_uri = upload_files(bucket, filterd_files, files_map)

        exercise, artifact = db_session.query(Exercise, Artifact).filter(
            Exercise.artifact_id == Artifact.id
        ).filter_by(language=language, name=name).order_by(
            asc(Exercise.difficulty)
        ).first() or (
            None,
            None,
        )

        if not exercise:
            exercise = Exercise()
            artifact = Artifact()

        exercise.language = known_language
        exercise.name = name
        exercise.creator = teacher.email
        exercise.description = request.files["readme"].read()
        exercise.topics = topics
        exercise.difficulty = difficulty

        artifact.readme = blobs_uri["readme"]
        artifact.solution = blobs_uri["solution"]
        artifact.starting_point = blobs_uri["starting_point"]
        artifact.test = blobs_uri["test"]
        artifact.compressed = blobs_uri["compressed"]

        exercise.artifact = artifact
        db_session.add_all([exercise, artifact])
        db_session.commit()
        return Response("Created", status=201)

    return exercises
