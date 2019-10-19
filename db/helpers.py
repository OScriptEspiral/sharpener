from sqlalchemy import create_engine, orm
from sqlalchemy.engine import url
from models import Base


def create_schema(db_api, db_uri, echo=True):
    connection = f"{db_api}://{db_uri}"
    engine = create_engine(connection, client_encoding="utf8", echo=echo)
    return Base.metadata.create_all(engine)


def database_setup(api, username, password, name, conn_name=None, echo=False):
    unix_socket = f'/cloudsql/{conn_name}'
    engine = create_engine(
        url.URL(
            drivername=api,
            username=username,
            password=password,
            database=name,
            query={
                'host': unix_socket
            }),
        client_encoding="utf8",
        echo=echo)

    sess = orm.sessionmaker(bind=engine)
    return sess()
