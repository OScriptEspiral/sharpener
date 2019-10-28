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

    track = relationship('Track', uselist=False,
                         back_populates="tracks_classes")
    class_ref = relationship('Class', uselist=False)
    enrollments = relationship('Enrollment', back_populates="track_class")

    def __repr__(self):
        return ("<TrackClassAssociation(class_id='%s', track_name='%s',"
                "track_owner='%s')>" %
                (self.class_id, self.track_name, self.track_owner))
