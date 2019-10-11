from dynaconf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base



def database_setup(db_uri):
    engine = create_engine(db_uri, echo=True)
    sess = sessionmaker(bind=engine)
    return sess()

session = database_setup(settings.PORT)
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
our_user = session.query(User).filter_by(name='ed').first() 

session.add(ed_user)
