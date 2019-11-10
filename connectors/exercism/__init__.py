from mappers import PythonMapper, RustMapper

from .populate import populate_exercises

populate_rust = populate_exercises(RustMapper)
populate_python = populate_exercises(PythonMapper)

__all__ = ["populate_rust", "populate_python"]
