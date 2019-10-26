from .base import Base
from .language import Language
from sqlalchemy import (Column, String, Table,
                        Integer, ForeignKeyConstraint, Enum)


class TrackExerciseAssociation(Base):
    __tablename__ = 'tracks_exercises_association'
    __table_args__ = (
        ForeignKeyConstraint(
            ['exercise_name', 'exercise_language'],
            ['exercises.name', 'exercises.language']
        ),
        ForeignKeyConstraint(['track_name', 'track_owner'],
                             ['tracks.name', 'tracks.owner'])
    )

    id = Column('id', Integer, primary_key=True)
    track_name = Column('track_name', String)
    track_owner = Column('track_owner', String)
    exercise_name = Column('exercise_name', String)
    exercise_language = Column('exercise_language', Enum(Language))
    step = Column('step', Integer)
