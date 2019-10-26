from .base import Base
from sqlalchemy import (Column, String, Integer, ForeignKey,
                        ForeignKeyConstraint, Enum)
from sqlalchemy.orm import relationship
from .submission_state import SubmissionState
from .language import Language


class Submission(Base):
    __tablename__ = 'submissions'

    user = Column('user', String, primary_key=True)
    class_id = Column('class_id', Integer, primary_key=True)
    track_name = Column('track_name', String, primary_key=True)
    track_owner = Column('track_owner', String, primary_key=True)
    exercise_name = Column('exercise_name', String, primary_key=True)
    exercise_language = Column('exercise_language', Enum(Language),
                               primary_key=True)
    attempt_number = Column('attempt_number', Integer)
    attempts = relationship('Attempt')
    state = Column('state', Enum(SubmissionState),
                   default=SubmissionState('pending'))

    exercise_composite_key = ForeignKeyConstraint(
        ['exercise_name', 'exercise_language'],
        ['exercises.name', 'exercises.language']
    )

    enrollment_composite_key = ForeignKeyConstraint(
        ['user', 'class_id', 'track_name', 'track_owner'],
        [
            'enrollments.user',
            'enrollments.class_id',
            'enrollments.track_name',
            'enrollments.track_owner',
        ])

    def __repr__(self):
        return ("<Submission(user='%s', class_id='%s', \
                track='%s', class='%s', exercise='%s')>" %
                (self.user, self.class_id, self.track, self.classroom,
                 self.exercise))
    # attempt_composite_key = ForeignKeyConstraint(
    #     ['user', 'class_id', 'track_name', 'track_owner',
    #      'exercise_name', 'exercise_language', 'attempt_number'],
    #     [
    #         'attempts.user',
    #         'attempts.class_id',
    #         'attempts.track_name',
    #         'attempts.track_owner',
    #         'attempts.exercise_name',
    #         'attempts.exercise_language',
    #         'attempts.attempt_number',
    #     ])

