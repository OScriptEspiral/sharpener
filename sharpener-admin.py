"""
sharpener-admin.

Usage:
  sharpener-admin create_schema
  sharpener-admin populate
  sharpener-admin start_server
"""

from docopt import docopt
from dynaconf import settings
from google.cloud import storage
from sqlalchemy import create_engine, orm
from sqlalchemy.engine import url
from connectors import exercism
from models import Base
from api import create_app


def create_db(db_uri):
    engine = create_engine(db_uri, client_encoding="utf8", echo=True)
    return Base.metadata.create_all(engine)


def database_setup(api, username, password, name, conn_name=None):
    unix_socket = f'/cloudsql/{conn_name}'
    print(url.URL(
            drivername=api,
            username=username,
            password=password,
            database=name,
            query={
                'host': unix_socket
            }))
    engine = create_engine(
        url.URL(
            drivername=api,
            username=username,
            password=password,
            database=name,
            query={
                'host': unix_socket
            }),
        client_encoding="utf8")

    sess = orm.sessionmaker(bind=engine)
    return sess()


try:
    import googleclouddebugger
    googleclouddebugger.enable()
except ImportError:
    pass

session = database_setup(settings.DB_API,
                         settings.DB_USERNAME,
                         settings.DB_PASSWORD,
                         settings.DB_NAME,
                         settings.DB_CONN_NAME)

app = create_app(session)

if __name__ == "__main__":
    args = docopt(__doc__)
    if args["create_schema"]:
        create_db(f"{settings.DB_API}{settings.DB_URI}")

    if args["populate"]:
        storage_client = storage.Client()
        exercism.populate_python(session,
                                 storage_client,
                                 settings.BUCKET_EXERCISES)

        exercism.populate_rust(session,
                               storage_client,
                               settings.BUCKET_EXERCISES)

    if args["start_server"]:
        app.run()
