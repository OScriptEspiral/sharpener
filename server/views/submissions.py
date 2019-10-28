from flask import Blueprint, Response
from werkzeug.utils import secure_filename
from models import Submission, Language, Attempt, User, Enrollment
from server.utils import handle_validation_error

ALLOWED_EXTENSIONS = {'py', 'rs'}


def upload_submission_files(bucket, blob_prefix, files):
    blobs_uri = dict()
    for file in files:
        blob_path = f"{blob_prefix}/{secure_filename(file.filename)}"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        blobs_uri[file.filename] = blob_path
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

    @submissions.route('<language>/<name>', methods=['GET'])
    @handle_validation_error
    def post_new_submission(language, name):
        # better if on authorization
        print(request.header)
        token = request.headers.get('authorization')
        track_class_id = request.headers.get('track_class_id')
        if not token:
            return Response(response="AuthToken required in header",
                            status=401)

        known_language = Language.get(language)
        if not known_language:
            return Response(response="Unknown language",
                            status=404)

        expected_files = {'solution_file', 'test_coverage',
                          'test_output', 'test_checksum'}

        received_files = {file for file in expected_files
                          if file in expected_files}

        if not (received_files >= expected_files):
            return Response("There are files missing",
                            status=400)

        user = db_session.query(User)\
            .filter_by(token=token)\
            .first()

        if not user:
            return Response(response="Invalid token supplied",
                            status=403)

        enrollment = db_session.query(Enrollment)\
            .filter_by(user=user,
                       track_class_id=track_class_id)

        if not enrollment:
            return Response(response="You are not enrolled in this track",
                            status=400)

        submission = db_session.query(Submission)\
            .filter_by(exercise_name=name,
                       exercise_language=known_language,
                       user=user)\
            .first()

        if not submission:
            submission = create_new_submission(db_session, track_class_id,
                                               known_language, name,
                                               enrollment)

        # Upload to bucket
        # Bucket_Uri to each attempt
        # bucket-submission/<user>/<submission-id>/<attempt-number>
        attempt_number = len(submission.attempts) + 1
        blob_prefix_uri = (f"{bucket.name}/{user.email}/{submission.id}\
                           /{attempt_number}")
        uploaded_blobs = upload_submission_files(bucket, blob_prefix_uri,
                                                 request.files)

        attempt = Attempt(
            solution_file=uploaded_blobs["solution_file"],
            test_coverage=uploaded_blobs["test_coverage"],
            test_output=uploaded_blobs["test_output"],
            test_checksum=uploaded_blobs["test_checksum"]
        )

        submission.attempts.append(attempt)
        db_session.add(submission, attempt)
        db_session.commit()

        return Response('Exercise solution submited', status=201)
    return submissions
