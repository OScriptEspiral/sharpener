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


def create_db(db_uri):
    engine = create_engine(db_uri, echo=True)
    return Base.metadata.create_all(engine)


def database_setup(db_uri):
    engine = create_engine(db_uri, echo=True)
    sess = orm.sessionmaker(bind=engine)
    return sess()


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["create_schema"]:
        create_db(settings.DB_API+settings.DB_URI)

    if args["populate"]:
        session = database_setup(f"{settings.DB_API}{settings.DB_URI}")
        storage_client = storage.Client()
        exercism.populate_rust(session,
                               storage_client,
                               settings.BUCKET_EXERCISES)
    if args["start_server"]:
        app = Flask(__name__)
        app.run()
