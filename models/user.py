from .base import Base
from sqlalchemy import Column, String, Boolean


class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    nickname = Column(String)
    is_teacher = Column(Boolean, default=False)
    github_token = Column(String, nullable=False)

    def __repr__(self):
        return "<User(name='%s', email='%s')>" % (self.name, self.email)
