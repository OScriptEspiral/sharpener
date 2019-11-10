from .classes import create_classes_blueprint
from .enrollments import create_enrollments_blueprint
from .exercises import create_exercises_blueprint
from .health_check import create_health_check_blueprint
from .interface import create_interface_blueprint
from .submissions import create_submissions_blueprint
from .topics import create_topics_blueprint
from .tracks import create_tracks_blueprint
from .users import create_users_blueprint

__all__ = [
    "create_exercises_blueprint",
    "create_topics_blueprint",
    "create_health_check_blueprint",
    "create_users_blueprint",
    "create_interface_blueprint",
    "create_submissions_blueprint",
    "create_classes_blueprint",
    "create_tracks_blueprint",
    "create_enrollments_blueprint",
]
