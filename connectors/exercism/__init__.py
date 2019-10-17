from .populate import populate_exercises
from .mappings import RustMapper, PythonMapper

populate_rust = populate_exercises(RustMapper)
populate_python = populate_exercises(PythonMapper)

__all__ = ['populate_rust', 'populate_python']
