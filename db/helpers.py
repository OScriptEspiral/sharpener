from sqlalchemy import create_engine, orm
from sqlalchemy.engine import url
from models import Base


def create_db_uri(api, username, password, name, conn_name,
                  production):
    if production:
        unix_socket = f'/cloudsql/{conn_name}'
        db_uri = url.URL(drivername=api, username=username, password=password,
                         database=name, query={'host': unix_socket})

    else:
        db_uri = url.URL(drivername=api, username=username, host="localhost",
                         password=password, database=name)

    return db_uri


def create_schema(api, username, password, name,
                  conn_name=None, echo=False, production=False):
    db_uri = create_db_uri(api, username, password,
                           name, conn_name, production)

    engine = create_engine(db_uri, client_encoding="utf8", echo=echo)
    return Base.metadata.create_all(engine)


def database_setup(api, username, password, name, conn_name=None,
                   echo=False, production=False):

    db_uri = create_db_uri(api, username, password,
                           name, conn_name, production)
    engine = create_engine(db_uri, client_encoding="utf8", echo=echo)
    sess = orm.sessionmaker(bind=engine)
    return sess()
