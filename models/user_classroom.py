from .base import Base
from sqlalchemy import Column, String, ForeignKey, Table, Integer

user_email = Column('user_email', String, ForeignKey('users.email'),
                    primary_key=True)
class_id = Column('class_id', Integer, ForeignKey('classes.id'),
                  primary_key=True)

user_class_association = Table('users_classes_association', Base.metadata,
                               class_id, user_email)
