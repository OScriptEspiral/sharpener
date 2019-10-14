from .base import Base
from sqlalchemy import ForeignKey, Column, Integer, String, Text, ARRAY
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship


languages = ENUM('Rust', name='languages')

class Exercise(Base):
    __tablename__ = 'exercises'

    name = Column(String, primary_key=True)
    language = Column(languages,primary_key=True)
    creator = Column(ForeignKey('users.email'), nullable=False)
    description = Column(Text, nullable=False)
    topics = Column(ARRAY(String))
    difficulty = Column(Integer)
    artifacts = Column(ForeignKey('artifacts.id'), nullable=False)
