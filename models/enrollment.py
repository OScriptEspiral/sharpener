from .base import Base
from sqlalchemy import (Column, String, Integer, ForeignKey,
                        ForeignKeyConstraint)


class Enrollment(Base):
    __tablename__ = 'enrollments'

    user = Column(String, ForeignKey('users.email'), primary_key=True)
    class_id = Column('class_id', Integer, primary_key=True)
    track_name = Column('track_name', String, primary_key=True)
    track_owner = Column('track_owner', String, primary_key=True)

    track_class_composite_key = ForeignKeyConstraint(
        ['class_id', 'track_name', 'track_owner'],
        [
            'tracks_classes_association.class_id',
            'tracks_classes_association.name',
            'tracks_classes_association.owner',
        ])

    def __repr__(self):
        return ("<Enrollment(user='%s', class_id='%s', \
                track='%s', class='%s')>" %
                (self.user, self.class_id, self.track, self.classroom))
