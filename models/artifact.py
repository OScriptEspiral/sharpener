from .base import Base
from sqlalchemy import ForeignKey, Column, Integer, String, Text, ARRAY
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship


class Artifact(Base):
    __tablename__ = 'artifacts'

    id = Column(Integer, primary_key=True)
    readme = Column(String, nullable=False)
    solution = Column(String, nullable=False)
    starting_point = Column(String, nullable=False)
    tests = Column(String, nullable=False)
    hints = Column(String, nullable=True)
