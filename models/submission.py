from .base import Base
from sqlalchemy import (Column, String, Integer, ForeignKeyConstraint,
                        UniqueConstraint, Enum)
from sqlalchemy.orm import relationship
from .submission_state import SubmissionState
from .language import Language


class Submission(Base):
    __tablename__ = 'submissions'
    __table_args__ = (
        ForeignKeyConstraint(
            ['exercise_name', 'exercise_language'],
            ['exercises.name', 'exercises.language']
        ),
        ForeignKeyConstraint(
            ['user', 'track_class_id'],
            ['enrollments.user', 'enrollments.track_class_id']),
        UniqueConstraint('user', 'track_class_id', 'exercise_name',
                         'exercise_language')
    )

    id = Column('id', Integer, primary_key=True)
    user = Column('user', String)
    track_class_id = Column('track_class_id', Integer)
    enrollment = relationship('Enrollment', uselist=False)
    exercise_name = Column('exercise_name', String)
    exercise_language = Column('exercise_language', Enum(Language))
    exercise = relationship('Exercise')
    attempts = relationship('Attempt')
    state = Column('state', Enum(SubmissionState),
                   default=SubmissionState('pending'))

    def __repr__(self):
        return ("<Submission(user='%s', class_id='%s', \
                track='%s', class='%s', exercise='%s')>" %
                (self.user, self.class_id, self.track, self.classroom,
                 self.exercise))
