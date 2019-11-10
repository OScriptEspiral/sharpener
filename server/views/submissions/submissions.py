from flasgger import swag_from
from flask import Blueprint, Response, jsonify
from models import Attempt, Submission, SubmissionStatus
from server.utils import (extract_files, extract_submission,
                          extract_test_params, extract_user,
                          handle_validation_error, upload_files)


def submission_to_dict(submission):
    return {
        "exercise_name": submission.exercise_name,
        "exercise_language": submission.exercise_language.value,
        "submission_token": submission.submission_token,
        "attempts": len(submission.attempts),
    }


def create_new_submission(
    db_session, track_class_id, language, name, enrollment
):
    submission = Submission(exercise_name=name, exercise_language=language)
    submission.enrollment = enrollment
    return submission


def create_submissions_blueprint(db_session, request, bucket):
    submissions = Blueprint("submissions", __name__)

    @submissions.route("/", methods=["GET"])
    @handle_validation_error
    @swag_from("get_pending_submissions.yaml")
    def get_pending_submissions():
        user = extract_user(request, db_session)
        submissions = (
            db_session.query(Submission)
            .filter_by(user=user.email, status=SubmissionStatus("pending"))
            .all()
        )
        print(submissions)
        data = [submission_to_dict(submission) for submission in submissions]
        return jsonify(data)

    @submissions.route("/<submission_token>", methods=["GET"])
    @handle_validation_error
    @swag_from("get_submission.yaml")
    def get_submission(submission_token):
        extract_user(request, db_session)
        submission = extract_submission(submission_token, db_session)
        artifact = submission.exercise.artifact

        return {
            "exercise_name": submission.exercise_name,
            "exercise_language": submission.exercise_language.value,
            "submission_token": submission_token,
            "attempts": len(submission.attempts),
            "submission_status": submission.status.value,
            "download_uri": artifact.compressed,
        }

    @submissions.route("/<submission_token>", methods=["POST"])
    @handle_validation_error
    @swag_from("post_new_submission.yaml")
    def post_new_submission(submission_token):
        user = extract_user(request, db_session)
        submission = extract_submission(submission_token, db_session)
        expected_files = {"solution"}
        files = extract_files(request, expected_files)
        coverage, output, checksum = extract_test_params(request)
        print(coverage, output, checksum)

        attempt_number = len(submission.attempts)
        blob_prefix_uri = (
            f"{user.email}/{submission.exercise_language.name}/"
            f"{submission.exercise_name}"
            f"/{attempt_number}"
        )

        mapper = submission.exercise_language.get_mapper()
        files_map = mapper(blob_prefix_uri, submission.exercise_name)

        uploaded_blobs = upload_files(bucket, files, files_map)

        attempt = Attempt(
            solution_file=uploaded_blobs["solution"],
            test_coverage=coverage,
            test_output=output,
            test_checksum=checksum,
            attempt_number=attempt_number + 1,
        )

        submission.attempts.append(attempt)
        db_session.add(submission, attempt)
        db_session.commit()

        return Response("Exercise solution submited", status=201)

    return submissions
