from .Mapper import Mapper
from os import path


class PythonMapper(Mapper):
    repo = "https://github.com/exercism/python"
    language = "python"

    @staticmethod
    def get_files_mappings(prefix, exercise_name, has_hint=False):
        exercise_path = f"{prefix}/{exercise_name}"
        return {
            "readme": f"{exercise_path}/README.md",
            "solution": f"{exercise_path}/example.py",
            "test": f"{exercise_path}/{exercise_name}_test.py",
            "hint": f"{exercise_path}/.meta/hints.md" if has_hint else None,
            "starting_point": f"{exercise_path}/{exercise_name}.py",
        }

    @staticmethod
    def hint_exists(exercise_path):
        return False
