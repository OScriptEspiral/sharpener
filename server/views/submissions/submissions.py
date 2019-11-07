from flask import Blueprint, Response
from werkzeug.utils import secure_filename
from models import Submission, Attempt
from server.utils import handle_validation_error
from server.utils import (extract_token, extract_user, extract_submission)

ALLOWED_EXTENSIONS = {'py', 'rs'}


def upload_submission_files(bucket, blob_prefix, files):
    blobs_uri = dict()
    for (filename, file) in files.items():
        blob_path = f"{blob_prefix}/{secure_filename(filename)}"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(file.read(),
                                content_type=file.content_type)
        blobs_uri[filename] = f"gs://{bucket.name}/{blob_path}"
    return blobs_uri


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_new_submission(db_session, track_class_id, language,
                          name, enrollment):
    submission = Submission(
        exercise_name=name,
        exercise_language=language
    )
    submission.enrollment = enrollment
    return submission


def create_submissions_blueprint(db_session, request, bucket):
    submissions = Blueprint('submissions', __name__)

    @submissions.route('/<submission_token>', methods=['POST'])
    @handle_validation_error
    def post_new_submission(submission_token):
        token = extract_token(request)
        user = extract_user(db_session, token)
        submission = extract_submission(submission_token, db_session)

        expected_files = {'solution_file', 'test_coverage',
                          'test_output', 'test_checksum'}

        received_files = {file for file in request.files
                          if file in expected_files}

        if not (received_files >= expected_files):
            missing_files = ", ".join(expected_files - received_files)
            return Response(f"There are files missing: {missing_files}",
                            status=400)

        attempt_number = len(submission.attempts) + 1
        blob_prefix_uri = (f"{user.email}/{submission.exercise_language.name}/"
                           f"{submission.exercise_name}"
                           f"/{attempt_number}")
        uploaded_blobs = upload_submission_files(bucket, blob_prefix_uri,
                                                 request.files)

        attempt = Attempt(
            solution_file=uploaded_blobs["solution_file"],
            test_coverage=uploaded_blobs["test_coverage"],
            test_output=uploaded_blobs["test_output"],
            test_checksum=uploaded_blobs["test_checksum"],
            attempt_number=attempt_number
        )

        submission.attempts.append(attempt)
        db_session.add(submission, attempt)
        db_session.commit()

        return Response('Exercise solution submited', status=201)
    return submissions
