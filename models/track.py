from .base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .track_classroom import track_class_association
from .track_exercise import track_exercise_association


class Track(Base):
    __tablename__ = 'tracks'

    name = Column(String, primary_key=True)
    owner = Column(String, ForeignKey('users.email'), primary_key=True)

    classes = relationship("Class", secondary=track_class_association,
                           back_populates="tracks")

    exercises = relationship("Exercise",
                             secondary=track_exercise_association,
                             back_populates="tracks")

    def __repr__(self):
        return "<Track(name='%s', creator='%s')>" % (self.name, self.creator)
