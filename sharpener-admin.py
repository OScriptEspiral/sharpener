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
from connectors import exercism
from models import Base
from api import create_app


def create_db(db_uri):
    engine = create_engine(db_uri, client_encoding="utf8", echo=True)
    return Base.metadata.create_all(engine)


def database_setup(db_uri):
    engine = create_engine(db_uri, client_encoding="utf8", echo=True)
    sess = orm.sessionmaker(bind=engine)
    return sess()


session = database_setup(f"{settings.DB_API}{settings.DB_URI}")
app = create_app(session)

if __name__ == "__main__":
    args = docopt(__doc__)
    if args["create_schema"]:
        create_db(f"{settings.DB_API}{settings.DB_URI}")

    if args["populate"]:
        STORAGE_CLIENT = storage.Client()
        exercism.populate_python(session,
                                 STORAGE_CLIENT,
                                 settings.BUCKET_EXERCISES)

        exercism.populate_rust(session,
                               STORAGE_CLIENT,
                               settings.BUCKET_EXERCISES)

    if args["start_server"]:
        app.run()
