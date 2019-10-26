from .base import Base
from sqlalchemy import (Column, String, ForeignKey, Integer,
                        ForeignKeyConstraint, UniqueConstraint,
                        )
from sqlalchemy.orm import relationship


class TrackClassAssociation(Base):
    __tablename__ = 'tracks_classes_association'
    __table_args__ = (
        ForeignKeyConstraint(['track_name', 'track_owner'],
                             ['tracks.name', 'tracks.owner']),
        UniqueConstraint('class_id', 'track_name', 'track_owner')
    )

    id = Column('id', Integer, primary_key=True)
    class_id = Column('class_id', Integer, ForeignKey('classes.id'))
    track_name = Column('track_name', String)
    track_owner = Column('track_owner', String)

    track = relationship('Track', uselist=False)
    class_ref = relationship('Class', uselist=False)
