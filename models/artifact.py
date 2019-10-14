from .base import Base
from sqlalchemy import Column, Integer, String


class Artifact(Base):
    __tablename__ = 'artifacts'

    id = Column(Integer, primary_key=True)
    readme = Column(String, nullable=False)
    solution = Column(String, nullable=False)
    starting_point = Column(String, nullable=False)
    test = Column(String, nullable=False)
    hint = Column(String, nullable=True)
