from datetime import datetime
from .base import Base
from sqlalchemy import (Column, String, Integer,
                        ForeignKeyConstraint, DateTime, Enum)
from .language import Language


class Attempt(Base):
    __tablename__ = 'attempts'

    user = Column('user', String, primary_key=True)
    class_id = Column('class_id', Integer,
                      primary_key=True)
    track_name = Column('track_name', String, primary_key=True)
    track_owner = Column('track_owner', String, primary_key=True)
    exercise_name = Column('exercise_name', String, primary_key=True)
    exercise_language = Column('exercise_language', Enum(Language),
                               primary_key=True)
    attempt_number = Column('attempt_number', Integer, primary_key=True)

    solution_file = Column(String, nullable=False)
    test_coverage = Column(String, nullable=False)
    test_ouput = Column(String, nullable=False)
    tests_checksum = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow,
                          nullable=False)

    submission_composite_key = ForeignKeyConstraint(
        ['user', 'class_id', 'track_name', 'track_owner',
         'exercise_name', 'exercise_language'],
        [
            'submissions.user',
            'submissions.class_id',
            'submissions.track_name',
            'submissions.track_owner',
            'submissions.exercise_name',
            'submissions.exercise_language',
        ])

    def __repr__(self):
        return ("<Attempt(user='%s', class_id='%s', \
                track='%s', class='%s', exercise='%s', attempt_number='%s')>" %
                (self.user, self.class_id, self.track, self.classroom,
                 self.exercise, self.attempt_number))
