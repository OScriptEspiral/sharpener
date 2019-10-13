from dynaconf import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import User, Base, Exercise

def create_db(db_uri):
    engine = create_engine(db_uri, echo=True)
    return Base.metadata.create_all(engine)

create_db(settings.DB_API+settings.DB_URI)
