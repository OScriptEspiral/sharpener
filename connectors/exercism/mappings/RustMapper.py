import json
from os import path


class RustMapper(object):
    repo = "https://github.com/exercism/rust"
    language = "rust"

    def get_files_mappings(prefix, exercise_name, has_hint=False):
        return {
            "readme": f"{prefix}/{exercise_name}/README.md",
            "solution": f"{prefix}/{exercise_name}/example.rs",
            "test": f"{prefix}/{exercise_name}/tests/${exercise_name}.rs",
            "hint": f"{prefix}/{exercise_name}/.meta/hints.md" if has_hint
            else None,
            "starting_point": f"{prefix}/{exercise_name}/src/lib.rs",
        }

    def hint_exists(exercise_path):
        return path.exists(f"{exercise_path}/.meta/hints.md")

    def pluck_readme(exercise_path):
        readme = f"{exercise_path}/README.md"
        with open(readme, 'r') as file:
            return file.read()

    def get_metadata(exercise_path):
        config = f"{exercise_path}/config.json"
        with json.load(config) as metadata:
            return metadata['exercises']
