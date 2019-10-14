# Clona repo 
# os.walk em exercises 
# Pra cada folder upa no bucket e mapeia em um objeto do banco 
# Commita no banco 
from git import Repo
from google.cloud import storage
from os import listdir, walk, path
from models import User, Exercise, Artifact
from uuid import uuid1

EXERCISM_REPO ="https://github.com/exercism/rust"
CLONE_DIR = f"/tmp/{uuid1()}"
EXERCISES = f"{CLONE_DIR}/exercises/"
BUCKET_NAME = "sharpener-exercises"
LANGUAGE = "rust"
BLOB_PREFIX =f"gs://{BUCKET_NAME}/{LANGUAGE}"

def get_mappings(prefix, exercise_name, has_hint=False):
    return {
        "readme":f"{prefix}/{exercise_name}/README.md",
        "solution":f"{prefix}/{exercise_name}/example.rs",
        "test":f"{prefix}/{exercise_name}/tests/${exercise_name}.rs",
        "hint":f"{prefix}/{exercise_name}/.meta/hints.md" if has_hint else None,
        "starting_point":f"{prefix}/{exercise_name}/src/lib.rs",
    }

def hint_exists(exercise_path):
    return path.exists(f"{exercise_path}/.meta/hints.md")

def pluck_readme(exercise_path):
    readme = f"{exercise_path}/README.md"
    with open(readme, 'r') as file:
     return file.read()


def upload_folder(base_path, blob_destination, bucket):
    for dirpath, dirname, filenames in walk(base_path):
        for file in filenames:
            rel_dir = dirpath.split(EXERCISES)[1]
            blob = bucket.blob(f"{blob_destination}{rel_dir}/{file}")
            blob.upload_from_filename(f"{dirpath}/{file}")

def populate_rust(session):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    repo = Repo.clone_from(EXERCISM_REPO, CLONE_DIR)
    all_exercises = listdir(f"{EXERCISES}")
    exercism_user = User(email="hello@exercism.io",
                         name="exercism.io",
                         nickname="exercism",
                         is_teacher=True,
                         github_token="")
    session.add(exercism_user)

    for name in all_exercises:
        print(f"Fetching exercise:{name}")
        base_path = f"{EXERCISES}/{name}"
        upload_folder(base_path, LANGUAGE, bucket)
        mappings = get_mappings(BLOB_PREFIX,
                                name,
                                has_hint=hint_exists(base_path))

        files = Artifact(readme=mappings["readme"],
                         solution=mappings["solution"],
                         starting_point=mappings["starting_point"],
                         test=mappings["test"],
                         hint=mappings["hint"])

        exercise = Exercise(name=name,
                            language=LANGUAGE,
                            creator=exercism_user,
                            description=pluck_readme(base_path),
                            artifacts=files)
        session.add_all([files, exercise])
    session.commit()
