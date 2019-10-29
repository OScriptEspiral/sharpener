from flask import Blueprint, Response
from models import Track, TrackClassAssociation, Enrollment
from server.utils import (extract_token, extract_user, extract_class,
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
    already_enrolled,  = pluck_first_column(
        db_session.query(Enrollment)
        .filter_by(track_class_id=track_class.id)
        .with_entities(Enrollment.user)
        .all()
    )

    enrollments = [Enrollment(user=student.email,
                              track_class_id=track_class.id)
                   for student in students
                   if student.email not in already_enrolled]
    return enrollments


def create_tracks_blueprint(db_session, request):
    tracks = Blueprint('tracks', __name__)

    @tracks.route('/<track_name>', methods=['POST'])
    @handle_validation_error
    def create_track(track_name):
        token = extract_token(request)
        user = extract_user(db_session, token)

        if not user.is_teacher:
            return Response(response="Only teachers can create tracks.",
                            status=403)

        existing_track = db_session.query(Track)\
            .filter_by(owner=user.email, name=track_name)\
            .first()

        if existing_track:
            return Response(
                response="You already have a track with that track_name.",
                status=409
            )

        new_track = Track(name=track_name)

        user.tracks_owned.append(new_track)
        db_session.add(user)
        db_session.flush()
        db_session.add(new_track)

        db_session.commit()

        return Response(status=201)

    @tracks.route('/<track_name>/classes/<class_name>', methods=['POST'])
    @handle_validation_error
    def enroll_class_track(track_name, class_name):
        token = extract_token(request)
        user = extract_user(db_session, token)
        if not user.is_teacher:
            return Response(response="Only teachers can enroll classes in tracks.",
                            status=403)

        existing_class = extract_class(class_name, db_session, user)
        existing_track = extract_track(track_name, db_session, user)
        existing_track_class = db_session.query(TrackClassAssociation)\
            .filter_by(class_ref=existing_class, track=existing_track)\
            .first()
        if not existing_track_class:
            existing_track_class = create_track_class(existing_class,
                                                      existing_track)
            db_session.add(existing_track_class)
            db_session.flush()

        enrollments = get_new_enrollments(existing_track_class, db_session)
        db_session.add_all(enrollments)
        db_session.flush()
        existing_track_class.enrollments.extend(enrollments)
        db_session.merge(existing_track_class)
        db_session.commit()
        return Response(status=201)

    return tracks
