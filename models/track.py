from datetime import datetime
from .base import Base
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Track(Base):
    __tablename__ = 'tracks'

    name = Column(String, primary_key=True)
    owner = Column(String, ForeignKey('users.email'), primary_key=True)

    classes = relationship("Class", secondary="tracks_classes_association",
                           back_populates="tracks")

    exercises = relationship("Exercise",
                             secondary="tracks_exercises_association",
                             back_populates="tracks")
    created_at = Column(DateTime, default=datetime.utcnow,
                        nullable=False)

    tracks_classes = relationship("TrackClassAssociation")

    def __repr__(self):
        return "<Track(name='%s', creator='%s')>" % (self.name, self.creator)
