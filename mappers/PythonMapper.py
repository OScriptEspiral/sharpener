from .Mapper import Mapper


class PythonMapper(Mapper):
    repo = "https://github.com/exercism/python"
    language = "python"

    @staticmethod
    def get_files_mappings(prefix, exercise_name):
        exercise_path = f"{prefix}/{exercise_name}"
        return {
            "readme": f"{exercise_path}/README.md",
            "solution": f"{exercise_path}/example.py",
            "test": f"{exercise_path}/{exercise_name}_test.py",
            "starting_point": f"{exercise_path}/{exercise_name}.py",
            "compressed": f"{exercise_path}/{exercise_name}.tar.gz",
        }
