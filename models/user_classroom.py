from .base import Base
from sqlalchemy import Column, String, ForeignKey, Integer


class UserClassAssociation(Base):
    __tablename__ = 'users_classes_association'
    user_email = Column('user_email', String, ForeignKey('users.email'),
                        primary_key=True)
    class_id = Column('class_id', Integer, ForeignKey('classes.id'),
                      primary_key=True)
