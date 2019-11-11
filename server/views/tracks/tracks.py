from flasgger import swag_from
from flask import Blueprint, Response, jsonify

from models import (Enrollment, Track, TrackClassAssociation,
                    TrackExerciseAssociation)
from server.utils import (extract_class, extract_exercises, extract_teacher,
                          extract_track, handle_validation_error)


def pluck_first_column(results):
    return [r for (r, *k) in results]


def create_track_class(existing_class, existing_track):
    track_class = TrackClassAssociation()
    track_class.class_ref = existing_class
    track_class.track = existing_track
    return track_class


def get_new_enrollments(track_class, db_session):
    existing_class = track_class.class_ref
    students = existing_class.students
    already_enrolled = pluck_first_column(
        db_session.query(Enrollment)
        .filter_by(track_class_id=track_class.id)
        .with_entities(Enrollment.user)
        .all()
    )

    enrollments = [
        Enrollment(user=student.email, track_class_id=track_class.id)
        for student in students
        if student.email not in already_enrolled
    ]
    return enrollments


def exercise_to_dict(exercise):
    return {"name": exercise.name, "language": exercise.language.value}


def track_to_dict(track):
    return {
        "name": track.name,
        "exercises": [
            exercise_to_dict(exercise) for exercise in track.exercises
        ],
        "created_at": track.created_at,
    }


def create_tracks_blueprint(db_session, request):
    tracks = Blueprint("tracks", __name__)

    @tracks.route("/", methods=["GET"])
    @handle_validation_error
    @swag_from("get_tracks.yaml")
    def get_tracks():
        teacher = extract_teacher(request, db_session)
        existing_tracks = (
            db_session.query(Track).filter_by(owner=teacher.email).all()
        )
        data = [track_to_dict(track) for track in existing_tracks]

        return jsonify(data)

    @tracks.route("/<track_name>", methods=["PUT"])
    @handle_validation_error
    @swag_from("create_track.yaml")
    def create_track(track_name):
        teacher = extract_teacher(request, db_session)

        existing_track = (
            db_session.query(Track)
            .filter_by(owner=teacher.email, name=track_name)
            .first()
        )

        if existing_track:
            message = "You already have a track with that track_name."
            return Response(response=message, status=409)

        new_track = Track(name=track_name)

        teacher.tracks_owned.append(new_track)
        db_session.add(teacher)
        db_session.flush()
        db_session.add(new_track)

        db_session.commit()

        return Response(status=201)

    @tracks.route("/<track_name>/classes/<class_name>", methods=["POST"])
    @handle_validation_error
    @swag_from("enroll_class_track.yaml")
    def enroll_class_track(track_name, class_name):
        teacher = extract_teacher(request, db_session)
        existing_class = extract_class(class_name, db_session, teacher)
        existing_track = extract_track(track_name, db_session, teacher)

        existing_track_class = (
            db_session.query(TrackClassAssociation)
            .filter_by(class_ref=existing_class, track=existing_track)
            .first()
        )

        if not existing_track_class:
            existing_track_class = create_track_class(
                existing_class, existing_track
            )
            db_session.add(existing_track_class)
            db_session.flush()

        enrollments = get_new_enrollments(existing_track_class, db_session)
        db_session.add_all(enrollments)
        db_session.flush()
        existing_track_class.enrollments.extend(enrollments)
        db_session.merge(existing_track_class)
        db_session.commit()
        return Response(status=201)

    @tracks.route("/<track_name>/exercises", methods=["POST"])
    @handle_validation_error
    @swag_from("register_track_exercises.yaml")
    def register_track_exercise(track_name):
        teacher = extract_teacher(request, db_session)
        track = extract_track(track_name, db_session, teacher)
        exercises = extract_exercises(request, db_session)
        new_track_exercises = []
        for (ex, step) in exercises:
            existing_track_exercise = (
                db_session.query(TrackExerciseAssociation)
                .filter_by(
                    track_name=track.name,
                    track_owner=track.owner,
                    exercise_name=ex.name,
                    exercise_language=ex.language,
                )
                .first()
            )
            if not existing_track_exercise:
                new_association = TrackExerciseAssociation(
                    track_name=track.name,
                    track_owner=track.owner,
                    exercise_name=ex.name,
                    exercise_language=ex.language,
                    step=step,
                )
                new_track_exercises.append(new_association)

        db_session.add_all(new_track_exercises)
        db_session.commit()

        return Response(status=201)

    return tracks
