from enum import Enum, unique

from mappers import PythonMapper, RustMapper


@unique
class Language(Enum):
    rust = "rust"
    python = "python"

    @classmethod
    def get(cls, value, default=None):
        known_values = {item.value for item in cls}
        lowercased_value = value.lower()

        if lowercased_value in known_values:
            return lowercased_value
        return default

    def get_mapper(self):
        return {
            "rust": RustMapper.get_files_mappings,
            "python": PythonMapper.get_files_mappings,
        }[self.value]
