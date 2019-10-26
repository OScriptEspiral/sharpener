from .base import Base
from sqlalchemy import (Column, String, Integer, ForeignKey,
                        ForeignKeyConstraint)
from sqlalchemy.orm import relationship


class Enrollment(Base):
    __tablename__ = 'enrollments'

    user = Column(String, ForeignKey('users.email'), primary_key=True)
    track_class_id = Column('track_class_id',
                            ForeignKey('tracks_classes_association.id'),
                            primary_key=True)

    track_class = relationship('TrackClassAssociation', uselist=False)
    submissions = relationship('Submission')

    def __repr__(self):
        return ("<Enrollment(user='%s', class_id='%s', \
                track='%s', class='%s')>" %
                (self.user, self.class_id, self.track, self.classroom))
