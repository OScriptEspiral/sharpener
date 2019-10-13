from dynaconf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Exercise, Base



def database_setup(db_uri):
    engine = create_engine(db_uri, echo=True)
    sess = sessionmaker(bind=engine)
    return sess()

session = database_setup(f"{settings.DB_API}{settings.DB_URI}")
ed = session.query(User).filter_by(name='ed').first()
our_user = Exercise(name="Hello World",
                    creator='Ed Jones',
                    language='Rust',
                    description="First program",
                    files="uri://")

session.add(our_user)
session.commit()
