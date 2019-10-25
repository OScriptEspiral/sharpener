from .base import Base
from .language import Language
from sqlalchemy import (Column, String, Table,
                        Integer, ForeignKeyConstraint, Enum)

track_name = Column('track_name', String, primary_key=True)

track_owner = Column('track_owner', String, primary_key=True)

exercise_name = Column('exercise_name', String, primary_key=True)

exercise_language = Column('exercise_language',
                           Enum(Language), primary_key=True)

step = Column('step', Integer)

exercise_composite_key = ForeignKeyConstraint(
    ['exercise_name', 'exercise_language'],
    ['exercises.name', 'exercises.language']
)

track_composite_key = ForeignKeyConstraint(['track_name', 'track_owner'],
                                           ['tracks.name', 'tracks.owner'])


track_exercise_association = Table('tracks_exercises_association',
                                   Base.metadata,
                                   exercise_name, exercise_language,
                                   track_name, track_owner, step,
                                   track_composite_key, exercise_composite_key)
