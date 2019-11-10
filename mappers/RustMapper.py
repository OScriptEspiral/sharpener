from .Mapper import Mapper
from os import path


class RustMapper(Mapper):
    repo = "https://github.com/exercism/rust"
    language = "rust"

    @staticmethod
    def get_files_mappings(prefix, exercise_name):
        exercise_path = f"{prefix}/{exercise_name}"
        return {
            "readme": f"{exercise_path}/README.md",
            "solution": f"{exercise_path}/example.rs",
            "test": f"{exercise_path}/tests/{exercise_name}.rs",
            "starting_point": f"{exercise_path}/src/lib.rs",
            "compressed": f"{exercise_path}/{exercise_name}.tar.gz",
        }
