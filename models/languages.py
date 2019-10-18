from enum import Enum, unique


@unique
class Language(Enum):
    rust = 'rust'
    python = 'python'

    @classmethod
    def get(cls, value, default=None):
        known_values = {item.value for item in cls}
        lowercased_value = value.lower()

        if lowercased_value in known_values:
            return lowercased_value
        return default
