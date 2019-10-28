from .base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Class(Base):
    __tablename__ = 'classes'
    __table_args__ = (UniqueConstraint('name', 'owner'),)

    id = Column(Integer, primary_key=True)
    owner = Column(String, ForeignKey('users.email'))
    name = Column(String, nullable=False)
    invite_token = Column(String, nullable=False)
    students = relationship("User", secondary='users_classes_association',
                            back_populates="classes")
    tracks = relationship("Track", secondary='tracks_classes_association',
                          back_populates="classes")

    tracks_classes = relationship("TrackClassAssociation",
                                  back_populates="class_ref")

    def __repr__(self):
        return ("<Class(id='%s', name='%s', owner='%s')>"
                % (self.id, self.name, self.owner))
