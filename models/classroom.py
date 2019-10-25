from .base import Base
from .language import Language
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .user_classroom import user_class_association
from .track_classroom import track_class_association


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    owner = Column(String, ForeignKey('users.email'))
    name = Column(String, nullable=False)
    invite_token = Column(String, nullable=False)
    language = Column(Enum(Language))
    users = relationship("User", secondary=user_class_association,
                         back_populates="classes")
    tracks = relationship("Track", secondary=track_class_association,
                          back_populates="classes")

    def __repr__(self):
        return ("<Class(id='%s', name='%s', owner='%s')>"
                % (self.id, self.name, self.owner))
