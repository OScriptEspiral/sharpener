from .base import Base
from sqlalchemy import ForeignKey, Column, Integer, String, Text, ARRAY
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship


languages = ENUM('Rust', name='languages')

class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    creator = Column(String, ForeignKey('users.email'), nullable=False)
    description = Column(Text, nullable=False)
    topics = Column(ARRAY(String))
    difficulty = Column(Integer)
    language = Column(languages, nullable=False)
    artifacts = Column(ForeignKey('artifact.id'), nullable=False)
