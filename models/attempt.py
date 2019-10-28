from datetime import datetime
from .base import Base
from sqlalchemy import (Column, String, Integer, UniqueConstraint,
                        ForeignKey, DateTime, Enum)
from sqlalchemy.orm import relationship
from .language import Language


class Attempt(Base):
    __tablename__ = 'attempts'
    submission_id = Column(ForeignKey('submissions.id'), primary_key=True)
    submission = relationship('Submission')
    attempt_number = Column('attempt_number', Integer, primary_key=True)

    solution_file = Column(String, nullable=False)
    test_coverage = Column(String, nullable=False)
    test_ouput = Column(String, nullable=False)
    test_checksum = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow,
                          nullable=False)

    def __repr__(self):
        return ("<Attempt(user='%s', class_id='%s', \
                track='%s', class='%s', exercise='%s', attempt_number='%s')>" %
                (self.user, self.class_id, self.track, self.classroom,
                 self.exercise, self.attempt_number))
