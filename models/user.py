from datetime import datetime
from .base import Base
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    is_teacher = Column(Boolean, default=False)
    token = Column(String, nullable=False)
    github_token = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    github_repositories = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow,
                        nullable=False)
    creator = relationship('Track')

    class_owner = relationship('Class', uselist=False)
    created_exercises = relationship('Exercise', back_populates="created_by")
    enrolled_in = relationship('Enrollment')

    classes = relationship('Class', secondary="users_classes_association",
                           back_populates="users")

    def __repr__(self):
        return "<User(name='%s', email='%s')>" % (self.name, self.email)
