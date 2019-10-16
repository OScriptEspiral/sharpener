import json
from .Mapper import Mapper
from os import path


class RustMapper(Mapper):
    repo = "https://github.com/exercism/rust"
    language = "rust"

    @staticmethod
    def get_files_mappings(prefix, exercise_name, has_hint=False):
        exercise_path = f"{prefix}/{exercise_name}"
        return {
            "readme": f"{exercise_path}/README.md",
            "solution": f"{exercise_path}/example.rs",
            "test": f"{exercise_path}/tests/{exercise_name}.rs",
            "hint": f"{exercise_path}/.meta/hints.md" if has_hint else None,
            "starting_point": f"{exercise_path}/src/lib.rs",
        }

    @staticmethod
    def hint_exists(exercise_path):
        return path.exists(f"{exercise_path}/.meta/hints.md")
