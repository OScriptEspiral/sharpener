from .exercises import create_exercises_blueprint
from .topics import create_topics_blueprint
from .health_check import create_health_check_blueprint


__all__ = ['create_exercises_blueprint',
           'create_topics_blueprint',
           'create_health_check_blueprint']
