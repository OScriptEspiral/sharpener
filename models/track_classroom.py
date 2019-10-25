from .base import Base
from sqlalchemy import (Column, String, ForeignKey, Table,
                        Integer, ForeignKeyConstraint)

class_id = Column('class_id', Integer, ForeignKey('classes.id'),
                  primary_key=True)

track_name = Column('track_name', String, primary_key=True)

track_owner = Column('track_owner', String, primary_key=True)

track_composite_key = ForeignKeyConstraint(['track_name', 'track_owner'],
                                           ['tracks.name', 'tracks.owner'])

track_class_association = Table('tracks_classes_association', Base.metadata,
                                class_id, track_name, track_owner,
                                track_composite_key)
