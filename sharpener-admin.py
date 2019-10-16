"""
sharpener-admin.

Usage:
  sharpener-admin create_schema
  sharpener-admin populate
  sharpener-admin start_server
"""

from flask import Flask
from docopt import docopt
from dynaconf import settings
from google.cloud import storage
from sqlalchemy import create_engine, orm
from connectors import exercism
from models import Base
from api import create_app


def create_db(db_uri):
    engine = create_engine(db_uri, client_encoding="utf8",echo=True)
    return Base.metadata.create_all(engine)


def database_setup(db_uri):
    engine = create_engine(db_uri, client_encoding="utf8", echo=True)
    sess = orm.sessionmaker(bind=engine)
    return sess()


if __name__ == "__main__":
    ARGS = docopt(__doc__)
    if ARGS["create_schema"]:
        create_db(settings.DB_API+settings.DB_URI)

    if ARGS["populate"]:
        SESSION = database_setup(f"{settings.DB_API}{settings.DB_URI}")
        STORAGE_CLIENT = storage.Client()
        exercism.populate_python(SESSION,
                                 STORAGE_CLIENT,
                                 settings.BUCKET_EXERCISES)

        exercism.populate_rust(SESSION,
                               STORAGE_CLIENT,
                               settings.BUCKET_EXERCISES)

    if ARGS["start_server"]:
        SESSION = database_setup(f"{settings.DB_API}{settings.DB_URI}")
        APP = create_app(SESSION)
        APP.run()
