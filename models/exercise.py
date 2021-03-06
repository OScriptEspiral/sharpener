from .base import Base
from .languages import Language
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Integer, String, Text, ARRAY, Enum


class Exercise(Base):
    __tablename__ = 'exercises'

    name = Column(String, primary_key=True)
    language = Column(Enum(Language), primary_key=True)
    creator = Column(ForeignKey('users.email'), nullable=False)
    description = Column(Text, nullable=False)
    topics = Column(ARRAY(String))
    difficulty = Column(Integer)
    artifact_id = Column(ForeignKey('artifacts.id'))
    artifact = relationship("Artifact",
                            back_populates="exercise",
                            uselist=False)
