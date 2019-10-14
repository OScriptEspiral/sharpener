from git import Repo
from os import listdir, walk
from models import User, Exercise, Artifact
from uuid import uuid1


def get_or_create_default_user(session):
    default_user = session.query(User).filter(
        User.email == 'hello@exercism.io').first()
    if not default_user:
        exercism_user = User(email="hello@exercism.io",
                             name="exercism.io",
                             nickname="exercism",
                             is_teacher=True,
                             github_token="")
        session.add(exercism_user)
        return exercism_user
    return default_user


def upload_folder(exercise_path, starting_path, blob_destination, bucket):
    for dirpath, dirname, filenames in walk(exercise_path):
        rel_dir = dirpath.split(starting_path)[1]
        for file in filenames:
            blob = bucket.blob(f"{blob_destination}/{rel_dir}/{file}")
            blob.upload_from_filename(f"{dirpath}/{file}")


def populate_exercises(mapper):
    def populate_language(session, storage_client, bucket_name):
        clone_dir = f"/tmp/{uuid1()}"
        starting_path = f"{clone_dir}/exercises"
        blob_prefix = f"gs://{bucket_name}/{mapper.language}"

        bucket = storage_client.bucket(bucket_name)
        Repo.clone_from(mapper.repo, clone_dir)
        all_exercises = listdir(f"{starting_path}")
        exercism_user = get_or_create_default_user(session)

        for name in all_exercises[0:3]:
            print(f"Fetching exercise:{name}")
            exercise_path = f"{starting_path}/{name}"
            upload_folder(exercise_path,
                          starting_path,
                          mapper.language,
                          bucket)

            has_hint = mapper.hint_exists(exercise_path)
            mappings = mapper.get_files_mappings(blob_prefix,
                                                 name,
                                                 has_hint=has_hint)
            exercise = Exercise(name=name,
                                language=mapper.language,
                                description=mapper.pluck_readme(exercise_path))

            files = Artifact(readme=mappings["readme"],
                             solution=mappings["solution"],
                             starting_point=mappings["starting_point"],
                             test=mappings["test"],
                             hint=mappings["hint"])

            session.add(files)
            session.add(exercise)
            exercise.artifact_id = files.id
            exercise.creator = exercism_user.email

        session.commit()

    return populate_language
