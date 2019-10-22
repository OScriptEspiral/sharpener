import tarfile
from uuid import uuid1
from os import listdir, walk

from git import Repo
from tqdm import tqdm

from models import User, Exercise, Artifact


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
        session.flush()
        return exercism_user
    return default_user


def upload_folder(exercise_path, starting_path, blob_destination, bucket):
    for dirpath, _dirname, filenames in walk(exercise_path):
        rel_dir = dirpath.split(starting_path)[1]
        for file in filenames:
            blob = bucket.blob(f"{blob_destination}{rel_dir}/{file}")
            blob.upload_from_filename(f"{dirpath}/{file}")


def process_exercise(name, starting_path, clone_dir,
                     blob_prefix, mapper, bucket, user):
    tqdm.write(f"Processing exercise:{name}")
    exercise_path = f"{starting_path}/{name}"
    with tarfile.open(f"{exercise_path}/{name}.tar.gz", "w:gz") as f:
        f.add(f"{exercise_path}/", arcname=name, recursive=True)

    upload_folder(exercise_path,
                  starting_path,
                  mapper.language,
                  bucket)

    has_hint = mapper.hint_exists(exercise_path)
    mappings = mapper.get_files_mappings(blob_prefix,
                                         name,
                                         has_hint=has_hint)
    metadata = mapper.get_metadata(clone_dir)
    topics, difficulty = next(iter([(ex["topics"], ex["difficulty"])
                                    for ex in metadata if ex["slug"] == name]),
                              (None, None))
    exercise = Exercise(name=name,
                        language=mapper.language,
                        description=mapper.pluck_readme(exercise_path),
                        topics=topics,
                        difficulty=difficulty,
                        creator=user.email)

    files = Artifact(readme=mappings["readme"],
                     solution=mappings["solution"],
                     starting_point=mappings["starting_point"],
                     test=mappings["test"],
                     hint=mappings["hint"],
                     compressed=mappings["compressed"],
                     exercise=exercise)

    return (exercise, files)


def populate_exercises(mapper):
    def populate_language(session, storage_client, bucket_name):
        print(f"Populating {mapper.language} language")
        clone_dir = f"/tmp/{uuid1()}"
        starting_path = f"{clone_dir}/exercises"
        blob_prefix = f"gs://{bucket_name}/{mapper.language}"

        bucket = storage_client.bucket(bucket_name)
        print(f"Cloning {mapper.repo}")
        Repo.clone_from(mapper.repo, clone_dir)
        all_exercises = listdir(f"{starting_path}")
        exercism_user = get_or_create_default_user(session)

        exercises, files = zip(*[
            process_exercise(name, starting_path, clone_dir, blob_prefix,
                             mapper, bucket, exercism_user)
            for name in tqdm(all_exercises, unit='exercise')
        ])

        session.add_all(files)
        session.commit()
        session.expire_all()
        for (exercise, file_) in zip(exercises, files):
            exercise.artifact_id = file_.id
        session.add_all(exercises)
        session.commit()

    return populate_language

