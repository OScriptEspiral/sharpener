from .exercises import create_exercises_blueprint
from .topics import create_topics_blueprint
from .users import create_users_blueprint
from .health_check import create_health_check_blueprint
from .interface import create_interface_blueprint


__all__ = ['create_exercises_blueprint',
           'create_topics_blueprint',
           'create_health_check_blueprint',
           'create_users_blueprint',
           'create_interface_blueprint']
