import json
from abc import ABC, abstractmethod

class Mapper(ABC):
    @staticmethod
    @abstractmethod
    def get_files_mappings(prefix, exercise_name, has_hint):
        """

        """

    @staticmethod
    @abstractmethod
    def hint_exists(exercise_path):
        """

        """


    @staticmethod
    def pluck_readme(exercise_path):
        readme = f"{exercise_path}/README.md"
        with open(readme, 'r') as file:
            return file.read()

    @staticmethod
    def get_metadata(repository_path):
        config = f"{repository_path}/config.json"
        with open(config, 'r') as file:
            metadata = json.load(file)
            return metadata['exercises']
