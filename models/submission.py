from uuid import uuid4

from sqlalchemy import (Column, Enum, ForeignKeyConstraint, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from .base import Base
from .language import Language
from .submission_state import SubmissionStatus


class Submission(Base):
    __tablename__ = "submissions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["exercise_name", "exercise_language"],
            ["exercises.name", "exercises.language"],
        ),
        ForeignKeyConstraint(
            ["user", "track_class_id"],
            ["enrollments.user", "enrollments.track_class_id"],
        ),
        UniqueConstraint(
            "user", "track_class_id", "exercise_name", "exercise_language"
        ),
    )

    id = Column("id", Integer, primary_key=True)
    user = Column("user", String)
    track_class_id = Column("track_class_id", Integer)
    enrollment = relationship("Enrollment", uselist=False)
    exercise_name = Column("exercise_name", String)
    exercise_language = Column("exercise_language", Enum(Language))
    exercise = relationship("Exercise")
    attempts = relationship("Attempt")
    submission_token = Column(
        "submission_token", String, nullable=False, default=uuid4()
    )
    status = Column(
        "status", Enum(SubmissionStatus), default=SubmissionStatus("pending")
    )

    def __repr__(self):
        return (
            "<Submission(user='%s', class_id='%s', \
                track_class_id='%s', exercise='%s, language:'%s')>"
            % (
                self.user,
                self.id,
                self.track_class_id,
                self.exercise_name,
                self.exercise_language,
            )
        )
