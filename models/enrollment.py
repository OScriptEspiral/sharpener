from datetime import datetime
from .base import Base
from sqlalchemy import (Column, String, ForeignKey, DateTime)
from sqlalchemy.orm import relationship


class Enrollment(Base):
    __tablename__ = 'enrollments'

    user = Column(String, ForeignKey('users.email'), primary_key=True)
    track_class_id = Column('track_class_id',
                            ForeignKey('tracks_classes_association.id'),
                            primary_key=True)

    track_class = relationship('TrackClassAssociation', uselist=False,
                               back_populates="enrollments")
    submissions = relationship('Submission')
    enrolled_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    enrolled_user = relationship('User', back_populates="enrolled_in",
                                 uselist=False)

    def __repr__(self):
        return ("<Enrollment(user='%s', track_class_id='%s'')>" %
                (self.user, self.track_class_id))
